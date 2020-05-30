from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View


from .models import Category, Size, MenuItem, MenuItemAddon, User, Address, Order, OrderItem, OrderItemAddon
from .models import PAYMENT_METHOD_CHOICES

from .forms import CreateAddressForm, CreateOrderForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm

from collections import OrderedDict
import datetime



# @login_required
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
			return HttpResponseRedirect(reverse('track_order', kwargs={'pk' : order.pk}))
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



def remove_from_cart(request):
	if request.method != 'POST':
		raise Http404('Method not allowed')
	item_id = int(request.POST.get('item_id'))
	pending_order = [item for item in request.session['pending_order'] if item['id'] != item_id]
	request.session['pending_order'] = pending_order
	return JsonResponse({'message' : 'Item removed from cart.'})
	
def cart(request):
	return JsonResponse(serialize_cart(request.session.get('pending_order')), safe=False)
	
#given cart representation stored inside session returns JSON serializable object 
def serialize_cart(pending_order):
	serialized = {'items' : []}
	total_price = 0
	for item in pending_order:
		menu_item = MenuItem.objects.get(pk=item['item_id'])
		addons = [MenuItemAddon.objects.get(pk=id_) for id_ in item['addon_ids']]
		total_price += menu_item.price + sum(addon.price for addon in addons)
		serialized_item =  {
			'id' : item['id'],
			'name' : menu_item.name,
			'category' : menu_item.category.name,
			'size' : menu_item.size.name if menu_item.size else None,
			'base_price' : menu_item.price,
			'total_price' : menu_item.price + sum(addon.price for addon in addons),
			'addons' : [{'name': addon.name, 'price': addon.price} for addon in addons],
		}	
		serialized['items'].append(serialized_item)
	serialized['total_price'] = total_price
	print(serialized)
	return serialized

#adds all items from cart(pending_order stored in session)
#to db and links them with order instance
def save_cart(pending_order, order):
	for item in pending_order:
		menu_item = MenuItem.objects.get(pk=item['item_id'])
		order_item = OrderItem(menu_item=menu_item, order=order)
		order_item.save()
		for addon_id in item['addon_ids']:
			menu_item_addon = MenuItemAddon.objects.get(pk=addon_id)
			order_item_addon = OrderItemAddon(
				menu_item_addon=menu_item_addon, order_item=order_item)
			order_item_addon.save()



	