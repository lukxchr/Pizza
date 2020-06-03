from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
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
from django.contrib.auth.forms import AuthenticationForm

from .utils import save_cart, serialize_cart

from collections import OrderedDict
import datetime


import stripe 

stripe.api_key = settings.STRIPE_SECRET_KEY

# @login_required
def index(request):
	return HttpResponseRedirect(
		reverse('menu', kwargs={'slug' : Category.objects.first().slug}))
 


def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user:
			#copy pending order to new session 
			#(keep cart items that user added before logging in)
			pending_order = request.session.get('pending_order')
			login(request, user)
			request.session['pending_order'] = pending_order
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, 'login.html', {'message': 'Invalid credentials.'})
	elif request.method == 'GET':
		if request.user.is_authenticated:
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, 'login.html')


class SignUpView(CreateView):
	form_class = SignUpForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'

class AddressCreateView(CreateView):
	form_class = CreateAddressForm
	success_url = reverse_lazy('place_order')
	template_name = 'create_address.html'

	def get_initial(self, *args, **kwargs):
		initial = super(AddressCreateView, self).get_initial(**kwargs)
		initial['user'] = self.request.user
		return initial




class PlaceOrderView(View):
	def get(self, request):
		context = {'form' : CreateOrderForm(user=self.request.user)}
		return render(request, 'place_order.html', context)

	def post(self, request):
		form = CreateOrderForm(request.POST, user=self.request.user)
		if form.is_valid():
			order = form.save(commit=False)
			order.customer = request.user
			order.delivery_estimate = datetime.datetime.now() + datetime.timedelta(minutes=40)
			order.save()
			save_cart(request.session.get('pending_order'), order)
			request.session['pending_order'] = [] #clear cart
			redirect_view = 'order_payment' if order.payment_method == 'CardOnline' else 'track_order'
			return HttpResponseRedirect(reverse(redirect_view, kwargs={'pk' : order.pk}))
		context = {'form' : CreateOrderForm(user=self.request.user)}
		return render(request, 'place_order.html', context)

	# def get_form_kwargs(self):
	# 	kwargs = super(PlaceOrderView, self).get_form_kwargs()
	# 	kwargs.update({'user': self.request.user})
	# 	return kwargs

	
class OrderListView(ListView):
	model = Order
	template_name = 'orders.html'




def track_order(request, pk):
	try:
		order = Order.objects.get(pk=pk)
		if order.customer != request.user:
			raise PermissionDenied
	except Order.DoesNotExist:
		raise Http404('Order does not exisit')


	context = {'order' : order}
	return render(request, 'order_track.html', context)




def logout_view(request):
      logout(request)
      return render(request, 'login.html', {'message': 'Logged out.'})
	

def menu(request, slug):
	category = Category.objects.filter(slug=slug).first()
	if not category:
		raise Http404("Category does not exist")

	menu_items = MenuItem.objects.filter(category=category) 
	#build list with distinct sizes/item names while keeping order 
	distinct_sizes = list(OrderedDict.fromkeys(menu_item.size for menu_item in menu_items))
	distinct_item_names = list(OrderedDict.fromkeys(menu_item.name for menu_item in menu_items))


	header = [None] + [size.name if size else '' for size in distinct_sizes]
	rows = []
	for name in distinct_item_names:
		row = [name]
		for size in distinct_sizes:
			item = menu_items.filter(name=name, size=size).first()
			row.append(item if item else None)
		rows.append(row)

	context = {'header' : header, 'rows': rows, 'categories' : Category.objects.all()}
	return render(request, 'menu.html', context=context)



def add_to_cart(request):
	if request.method != 'POST':
		raise Http404('Method not allowed')

	item_id = request.POST.get('item_id')
	addon_ids = request.POST.getlist('addon')
	try:
		menu_item = MenuItem.objects.get(pk=item_id)
		addons = [MenuItemAddon.objects.get(pk=id_) for id_ in addon_ids]
	except MenuItem.DoesNotExist:
		raise Http404('MenuItem does not exist')
	except MenuItemAddon.DoesNotExist:
		raise Http404('MenuItemAddon does not exist')

	#validate n addons 
	if len([addon for addon in addons if addon.price == 0]) != menu_item.n_addons:
		return JsonResponse({
			'message' : f'Please choose exactly {menu_item.n_addons} toppings'}, status=400)

	#validate if addons allowed for menu item
	for id_ in addon_ids:
		if not menu_item.allowed_addons.filter(pk=id_).exists():
			return JsonResponse({
				'message' : 'Please choose valid addons'}, status=400) 
	
	#store items/addons inside session 
	if not request.session.get('pending_order'):
		request.session['pending_order'] = [{'id': 1, 'item_id' : item_id, 'addon_ids' : addon_ids}]
	else:
		pending_order = request.session['pending_order']
		next_id = pending_order[-1]['id'] + 1
		pending_order.append({'id': next_id, 'item_id' : item_id, 'addon_ids' : addon_ids})
		request.session['pending_order'] = pending_order


	return JsonResponse({'message' : 'Item added to cart.'})


@require_POST
def remove_from_cart(request):
	item_id = int(request.POST.get('item_id'))
	pending_order = [item for item in request.session['pending_order'] if item['id'] != item_id]
	request.session['pending_order'] = pending_order
	return JsonResponse({'message' : 'Item removed from cart.'})
	
def cart(request):
	return JsonResponse(serialize_cart(request.session.get('pending_order')), safe=False)
	
@login_required
def order_payment(request, pk):
	order = get_object_or_404(Order, pk=pk)
	if order.customer != request.user:
		raise PermissionDenied
	if order.is_paid:
		return HttpResponseRedirect(reverse('track_order', kwargs={'pk' : pk}))

	#create stripe session
	#redirect back to this view when payment completed or cancelled
	success_redirect_url = request.build_absolute_uri(reverse('track_order', args=[order.pk]))
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
		# Fulfill the purchase...
		payment = get_object_or_404(Payment, stripe_id=session.payment_intent)
		payment.status = 'Completed'
		payment.save()

	return HttpResponse(status=200)
	