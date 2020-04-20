from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView


from .models import Category, Size, MenuItem, MenuItemAddon, User

from .forms import PizzaOrderForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm



@login_required
def index(request):
	context = {
		'categories' : Category.objects.all()
	} 
	return render(request, 'index.html', context=context)
    # return HttpResponse("Project 3: TODO")


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



def logout_view(request):
      logout(request)
      return render(request, 'login.html', {'message': 'Logged out.'})
	

@login_required
def menu(request, category_id):
	category = Category.objects.filter(id=category_id).first()
	if not category:
		raise Http404("Category does not exist")

	menu_items = MenuItem.objects.filter(category=category) 
	distinct_sizes = set([menu_item.size for menu_item in menu_items])
	distinct_names = menu_items.order_by('name').values_list('name', flat=True).distinct()

	menu_data = []
	for name in distinct_names:
		row = [name]
		for size in distinct_sizes:
			item = menu_items.filter(name=name, size=size).first()
			row.append(item if item else None)
		menu_data.append(row)


	context = {
		'menu_data' : menu_data,
		'menu_header' : [None] + list(distinct_sizes),
		'categories' : Category.objects.all(),
		'category' : category,
	}

	if category.is_pizza_category:
		context['form'] = PizzaOrderForm(menu_items, menu_items.first().allowed_addons.all())
		return render(request, 'pizza_menu.html', context=context)
	else:
		distinct_item_names = menu_items.values_list('name', flat=True).distinct()
		return render(request, 'menu.html', context=context)

def add_to_cart(request):
	print(request.POST.getlist('toppings'))
	return HttpResponse(request.POST.getlist('toppings'))
	
	
	
	

	