from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from orders.models import Address, Order

class SignUpForm(UserCreationForm):
	email = forms.EmailField(required=True, label='Email')

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')


class CreateAddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ['id', 'name', 'address1', 'address2', 'zip_code', 'city', 'user']
		widgets= {'user': forms.HiddenInput()}


	# def clean(self):
	# 	data = self.cleaned_data
	# 	data['User'] = self.


class PlaceOrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['id', 'notes', 'payment_method', 'delivery_address']
		widgets = {}

# class MenuItemOrderForm(forms.Form):
# 	pass

# class PizzaOrderForm(forms.Form):
	
# 	def __init__(self, pizzas, toppings, *args, **kwargs):
# 		super(PizzaOrderForm, self).__init__(*args, **kwargs)

# 		toppings_choices = [(topping.id, topping.name) for topping in toppings]
		
# 		pizza_choices = []
# 		for pizza in pizzas:
# 			if pizza.is_special:
# 				choice_name = f'{pizza.size} – Unlimited toppings – ${pizza.price}'
# 			elif pizza.n_addons == 0:
# 				choice_name = f'{pizza.size} – Cheese – ${pizza.price}'
# 			elif pizza.n_addons == 1:
# 				choice_name = f'{pizza.size} – 1 topping – ${pizza.price}'
# 			else:
# 				choice_name = f'{pizza.size} – {pizza.n_addons} toppings – ${pizza.price}'
# 			pizza_choices.append((pizza.id, choice_name))

# 		self.fields['pizza'] = forms.ChoiceField(
# 			choices=pizza_choices, widget=forms.RadioSelect, 
# 			label='Choose size')
# 		# self.fields['pizza'] = forms.ChoiceField(
# 		# 	choices=pizza_choices, label='Choose size')
# 		self.fields['toppings'] = forms.MultipleChoiceField(
# 			widget=forms.CheckboxSelectMultiple, 
# 			choices = toppings_choices, 
# 			label='Add toppings')

		

	# def clean_toppings(self):
	# 	print('clean_toppings')
	# 	chosen_toppings = self.cleaned_data['toppings']
	# 	if len(toppings) != self.pizza.n_toppings:
	# 		raise forms.ValidationError(
	# 			f'Please choose exactly {self.pizza.n_toppings} or choose different pizza')
	# 	return self.cleaned_data

	# 

	