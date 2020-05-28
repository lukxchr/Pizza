document.addEventListener('DOMContentLoaded', () => {
	//static tippy instances(set inside html template)
	//e.g. info toolptip for special menu items
	tippy('[data-tippy-content]', {
		placement: 'right',
	});

	//add to cart for items with addons
	//1)init tippy with placeholder 
	//2)get available addons via ajax and show form inside tippy
	//3)add to cart item with selected addons when form submitted
	tippy('.add-to-cart-addons-btn', {
	  content: 'Loading...',
	  trigger: 'click',
	  placement: 'right',
	  arrow: true,
	  interactive: true,
	  allowHTML: true,
	  onShow(instance) {
	  	renderAddToCart(instance)
	  	.catch(err => instance.setContent(err));	
	  }
	});

	//add to cart for items without addons
	//add to cart via ajax and show confrimation inside tippy
	document.querySelectorAll('.add-to-cart-form')
		.forEach(form => form.onsubmit = 
			e => submit(e.target) 
	);

	//render DOM elements
	renderCart();
});


//templates

const add_to_cart_form_template = Handlebars.compile(`
<form class="add-to-cart-form">
<input type="hidden" name="item_id" value={{ item_id }}>
{{#each addons}}
	<label>{{ this.name }}{{ formatAddonPrice this.price }}</label>
	<input type="checkbox" name="addon" value="{{ this.id }}">
	<br>
{{/each}}
<input type=submit value="Add to Cart">
</form>`);



const cart_template = Handlebars.compile(`
	{{#each items}}
		<b>{{this.size}} {{this.category}}</b>
		</br>
		{{this.name}}
		</br>
		\${{this.base_price}}
		</br>
		{{#each this.addons}}
			+{{this.name}}
			{{ formatAddonPrice this.price }}
			<br/>
		{{/each}}
		<br/>
	{{/each}}
	<div id="total-price"><h3>Total: \${{total_price}}</h3></div>`);

//returns empty string if price==0.00 otherwise adds $ symbol in the front
Handlebars.registerHelper('formatAddonPrice', price => price == 0.00 ? '' : `(+\$${price})`);

function test() {
	console.log("test");
}

async function renderCart() {
	//fetch existing pending order
	let response = await fetch('/getCart');
	if (!response.ok)
		throw 'Failed to fetch pending order.';
	const cart_data = await response.json();
	if (cart_data.items.length == 0)
		return; //nothing to render

	const cart = cart_template({
		items: cart_data.items, total_price: cart_data.total_price});
	const cart_body = document.querySelector('#cart-body');
	cart_body.innerHTML = cart;
	//enable checkout button if at least one item added to cart
	if (cart_data.items.length > 0)
		document.querySelector('#checkout-btn').disabled = false;
}

async function renderAddToCart(instance) {
	const item_id = instance.reference.dataset.item;
	const csrf_token = instance.reference.dataset.csrfToken;
	
	//fetch list of available addons
	const response = await fetch(`/api/menu_item_addons/?allowed_for=${item_id}`);
	if (!response.ok) 
		throw('Failed to fetch addons. Please try again.');
	const addons = await response.json();
	
	//build add_to_cart_form with the addons and display inside tippy instance 
	const form = add_to_cart_form_template({
		item_id: item_id, csrf_token: csrf_token, addons: addons});
	instance.setContent(form);
	instance.popper.childNodes[0].onsubmit =
		e => {
			const form_data = new FormData(e.target);
			const headers = {'X-CSRFToken' : Cookies.get('csrftoken'),};
			fetch('/addToCart', {method: 'post', body: form_data, headers: headers})
			.then(response => response.json())
			.then(data => instance.setContent(data.message));
			test();
			renderCart();
			test();
			return false; 
		}
}

function submit(form) {
	const form_data = new FormData(form);
	fetch('/addToCart', {method: 'post', body: form_data})
		.then(response => {
			if (!response.ok) {
				throw 'Failed to add to cart.';
			}
			response.json().then(data => {
				const submit_btn = form.querySelector('input[type=submit]');
				tippy(submit_btn, 
					{content: data['message'], 
					showOnCreate: true, 
					placement: 'right',
					onHidden(instance) {
						instance.reference._tippy.destroy();
					}});
				renderCart();
			});
		})
		.catch(err => console.log(err));	
	return false;
}