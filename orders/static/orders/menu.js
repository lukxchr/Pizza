import {get, post, getJSON, postJSON} from './requests_utils.js'


document.addEventListener('DOMContentLoaded', () => {
	// tippy('[data-tippy-content]');

	tippy('.add-to-cart-addons-btn', {
	  content: 'Loading...',
	  trigger: 'click',
	  placement: 'right',
	  arrow: true,
	  interactive: true,
	  allowHTML: true,
	  onShow(instance) {
	  	const form = buildAddToCartForm(
	  		instance.reference.dataset.item, 
	  		instance.reference.dataset.csrfToken);
	  	form.then((f) => {instance.setContent(f);});
	  	

	  	}
	  
	  	
	  });
	});



const add_to_cart_form_template = Handlebars.compile(`
<form method="POST" action="/">
<input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
{{#each addons}}
	<label>{{ this.name }}</label>
	<input type="checkbox" name="{{ this.name }}" value="{{ this.id }}">
	<br>
  {{/each}}
  <input type=submit value="Add to Cart">
</form>`);

// console.log(add_to_cart_form_template({addons: ['a','b','c']}))

function buildAddToCartForm(item_id, csrf_token) {
	
	return getJSON(`/api/menu_item_addons/`, {allowed_for: item_id}).then(data => {
		
		//console.log(add_to_cart_form_template({addons: data, csrf_token: csrf_token}));
		const form = add_to_cart_form_template({addons: data, csrf_token: csrf_token});
		return form
	});
}