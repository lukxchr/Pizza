document.addEventListener('DOMContentLoaded', () => {
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
	document.querySelectorAll('.add-to-cart-form')
		.forEach(form => form.onsubmit = 
			e => submit(e.target) );
});



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
			fetch('/addToCart', {method: 'post', body: form_data})
			.then(response => response.json())
			.then(data => instance.setContent(data.message))
			return false; 
		}
}



const add_to_cart_form_template = Handlebars.compile(`
<form class="add-to-cart-form">
<input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
<input type="hidden" name="item_id" value={{ item_id }}>
{{#each addons}}
	<label>{{ this.name }}{{ formatAddonPrice this.price }}</label>
	<input type="checkbox" name="addon" value="{{ this.id }}">
	<br>
{{/each}}
<input type=submit value="Add to Cart">
</form>`);

//returns empty string if price==0.00 otherwise adds $ symbol in the front
Handlebars.registerHelper('formatAddonPrice', price => price == 0.00 ? '' : `(+\$${price})`);






function submit(form) {
	console.log("submit called");
	const form_data = new FormData(form);
	fetch('/addToCart', {method: 'post', body: form_data})
		.then(response => {
			if (!response.ok)
				throw 'Failed to add to cart. Please try again.'
			response.json().then(data => {
				const submit_btn = form.querySelector('input[type=image]');
				tippy(submit_btn, 
					{content: data['message'], 
					showOnCreate: true, 
					placement: 'right',
					onHidden(instance) {
						instance.reference._tippy.destroy();
					}});
			});
		})
		.catch(err => console.log(err));
		
	return false;
}