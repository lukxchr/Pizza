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
		fields = '__all__'
		widgets= {'user': forms.HiddenInput()}

class CreateOrderForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')  
		super(CreateOrderForm, self).__init__(*args, **kwargs)
		self.fields['delivery_address'].queryset = Address.objects.filter(user=user)
	class Meta:
		model = Order
		fields = ['delivery_address', 'payment_method', 'notes']
		widgets = {'notes' : forms.Textarea(
			attrs={'cols': 60, 'rows': 3, 'style': 'font-size: 1.5rem;',}),
			'payment_method' : forms.Select(choices=Address.objects.all()),
		}
		labels = {
			'delivery_address' : 'Choose delivery address',
			'payment_method' : 'Choose payment method',
		}

