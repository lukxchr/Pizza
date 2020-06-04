from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Category, Size, MenuItem, MenuItemAddon, User, Address, Order, OrderItem, OrderItemAddon, Payment
from .models import PAYMENT_METHOD_CHOICES
from .forms import CreateAddressForm, CreateOrderForm, SignUpForm
from .utils import build_menu_table, save_cart, serialize_cart

from datetime import datetime, timedelta

import stripe 
stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
	return HttpResponseRedirect(
		reverse('menu', args=[Category.objects.first().slug]))

class LoginView(View):
	def get(self, request):
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, 'login.html')
	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user:
			#keep cart items that user added before logging in
			pending_order = request.session.get('pending_order')
			login(request, user)
			request.session['pending_order'] = pending_order
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, 'login.html', {'message': 'Invalid credentials.'})

class SignUpView(CreateView):
	form_class = SignUpForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'

class AddressCreateView(LoginRequiredMixin, CreateView):
	form_class = CreateAddressForm
	success_url = reverse_lazy('place_order')
	template_name = 'create_address.html'
	def get_initial(self, *args, **kwargs):
		initial = super(AddressCreateView, self).get_initial(**kwargs)
		initial['user'] = self.request.user
		return initial

class PlaceOrderView(LoginRequiredMixin, View):
	def get(self, request):
		context = {'form' : CreateOrderForm(user=self.request.user)}
		return render(request, 'place_order.html', context)
	def post(self, request):
		form = CreateOrderForm(request.POST, user=self.request.user)
		if form.is_valid():
			order = form.save(commit=False)
			order.customer = request.user
			order.delivery_estimate = datetime.now() + timedelta(minutes=40)
			order.save()
			save_cart(request.session.get('pending_order'), order)
			request.session['pending_order'] = [] #clear cart
			redirect_view = 'order_payment' if order.payment_method == 'CardOnline' else 'track_order'
			return HttpResponseRedirect(reverse(redirect_view, args=[order.pk]))
		return render(request, 'place_order.html', 
			{'form' : CreateOrderForm(user=self.request.user)})
	
class OrderListView(LoginRequiredMixin, ListView):
	model = Order
	template_name = 'orders.html'

@login_required
def track_order(request, pk):
	order = get_object_or_404(Order, pk=pk)
	return render(request, 'order_track.html', {'order' : order})

def logout_view(request):
      logout(request)
      return render(request, 'login.html', {'message': 'Logged out.'})
	
def menu(request, slug):
	category = get_object_or_404(Category, slug=slug)
	context = build_menu_table(category)
	context['categories'] = Category.objects.all()
	return render(request, 'menu.html', context=context)

@require_POST
def add_to_cart(request):
	item_id = request.POST.get('item_id')
	addon_ids = request.POST.getlist('addon')
	menu_item = get_object_or_404(MenuItem, pk=item_id)
	addons = [get_object_or_404(MenuItemAddon, pk=id_) for id_ in addon_ids]

	#validate n addons 
	if len([addon for addon in addons if addon.price == 0]) != menu_item.n_addons:
		return JsonResponse({
			'message' : f'Please choose exactly {menu_item.n_addons} toppings'}, 
			status=400)

	#validate if addons allowed for menu item
	for id_ in addon_ids:
		if not menu_item.allowed_addons.filter(pk=id_).exists():
			return JsonResponse({
				'message' : 'Please choose valid addons'}, status=400) 
	
	#store items/addons inside session 
	if not request.session.get('pending_order'):
		request.session['pending_order'] = [
			{'id': 1, 'item_id' : item_id, 'addon_ids' : addon_ids}
		]
	else:
		pending_order = request.session['pending_order']
		next_id = pending_order[-1]['id'] + 1
		pending_order.append({
			'id': next_id, 
			'item_id' : item_id, 
			'addon_ids' : addon_ids,
		})
		request.session['pending_order'] = pending_order
	return JsonResponse({'message' : 'Item added to cart.'})

@login_required
@require_POST
def remove_from_cart(request):
	item_id = int(request.POST.get('item_id'))
	pending_order = [
		item for item in request.session['pending_order'] 
		if item['id'] != item_id
	]
	request.session['pending_order'] = pending_order
	return JsonResponse({'message' : 'Item removed from cart.'})

def cart(request):
	return JsonResponse(
		serialize_cart(
			request.session.get('pending_order')), safe=False)
	
@login_required
def order_payment(request, pk):
	order = get_object_or_404(Order, pk=pk)
	if order.customer != request.user:
		raise PermissionDenied
	if order.is_paid:
		return HttpResponseRedirect(reverse('track_order', kwargs={'pk' : pk}))

	#create stripe session
	#redirect to track_order if payment succeeds or back to this view if payment fails 
	success_redirect_url = request.build_absolute_uri(
		reverse('track_order', args=[order.pk]))
	cancel_redirect_url = request.build_absolute_uri() 
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price_data': {
				'currency': 'usd',
				'product': 'prod_HNt51ckSz46ZmG',
				'unit_amount': int(float(order.total_price)/0.01),
			},
			'quantity': 1,
		}],
		mode='payment',
		success_url=success_redirect_url,
		cancel_url=cancel_redirect_url,
		)
	#create payment object
	payment = Payment(
		amount=order.total_price,
		stripe_id=session.payment_intent,
		order=order,
		)
	payment.save()
	context = {
		'order': order,
		'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
		'CHECKOUT_SESSION_ID': session.id
	}
	return render(request, 'order_payment.html', context)

@csrf_exempt
@require_POST
def stripe_webhook(request):
	payload = request.body
	sig_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
		)
	except ValueError as e:
		# Invalid payload
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		# Invalid signature
		return HttpResponse(status=400)
	# Handle the checkout.session.completed event
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		#update payment in db
		payment = get_object_or_404(Payment, stripe_id=session.payment_intent)
		payment.status = 'Completed'
		payment.save()
	return HttpResponse(status=200)
	