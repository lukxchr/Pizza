from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, View


from .models import Category, Size, MenuItem, MenuItemAddon, User, Address, Order, OrderItem, OrderItemAddon
from .models import PAYMENT_METHOD_CHOICES

from .forms import CreateAddressForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm

from collections import OrderedDict
import datetime



@login_required
def index(request):
	first_category = Category.objects.first()
	return HttpResponseRedirect(
		reverse('menu', kwargs={'category_id' : first_category.id}))
 


def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
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
		try:
			order = Order.objects.get(customer=request.user, status='Pending')
		except Order.DoesNotExist:
			order = Order(customer=request.user)
			order.save()
		addresses = Address.objects.filter(user=request.user)
		context = {
			'order': order,
			'order_items' : order.order_items.all(),
			'addresses' : addresses,
			'payment_methods': PAYMENT_METHOD_CHOICES,
			}
		return render(request, 'order_update.html', context)

	def post(self, request):
		try: 
			order = Order.objects.get(pk=request.POST['order'])
			address = Address.objects.get(pk=request.POST['address'])
			payment_method = request.POST['payment-method']
			notes = request.POST['order-comments']
		except Order.DoesNotExist:
			raise Http404('Order does not exisit.')
		except Address.DoesNotExist:
			raise Http404('Address does not exisit')
		#TO DO: validate order notes lenght 

	
		order.delivery_address = address
		order.payment_method = payment_method
		order.notes = notes
		order.delivery_estimate = datetime.datetime.now() + datetime.timedelta(minutes=30)
		order.status = 'Placed'
		order.save()



		return HttpResponseRedirect(reverse('track_order', kwargs={'pk' : order.pk}))





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
	

@login_required
def menu(request, category_id):
	category = Category.objects.filter(id=category_id).first()
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

	context = {'header' : header, 'rows': rows, 
	'categories' : Category.objects.all()}
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

	if len([addon for addon in addons if addon.price == 0]) != menu_item.n_addons:
		return JsonResponse({
			'message' : f'Please choose exactly {menu_item.n_addons} toppings'}, status=400)
		
	#try to retrieve Pending order (for any user there is at most one Pending order at any time)
	#if it failes create a new pending order
	try:
		order = Order.objects.get(customer=request.user, status='Pending')
	except Order.DoesNotExist:
		order = Order(customer=request.user)
		order.save()
	finally:
		#create OrderItem and related OrderItemAddons. Commit changes 
		order_item = OrderItem(menu_item=menu_item, order=order)
		order_item.save()
		for addon in addons:
			order_addon = OrderItemAddon(menu_item_addon=addon, order_item=order_item)
			order_addon.save()
		
	return JsonResponse({'message' : 'Item added to cart.'})

	
	
	
	

	