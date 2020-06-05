document.addEventListener('DOMContentLoaded', () => {


	document.addEventListener('click', (e) => {
		if (e.target.matches('.rm-from-cart-btn')) {
			const dataset = e.target.dataset;
			deleteCartItem(dataset.item);
		}
	});
	renderCart();
});



async function renderCart() {
	//fetch existing pending order
	let response = await fetch('/get-cart');
	if (!response.ok)
		throw 'Failed to fetch pending order.';
	const cart_data = await response.json();
	if (cart_data.items.length == 0)
		return; //nothing to render

	const cart = cart_template({items: cart_data.items, total_price: cart_data.total_price});
	document.querySelector('#cart-items-container').innerHTML = cart;
	document.querySelector('#total-order-price').innerHTML = `Total: \$${cart_data.total_price}`;

	//init tippy tooltips
	tippy('[data-tippy-content]', {
		placement: 'right',
	});

}


const cart_template = Handlebars.compile(`
<table id="order-items-table">
	<tr>
		<td>#</td>
		<td>Item</td>
		<td>
			Base Price
			<i 
				class="fa fa-info-circle" 
				data-tippy-content="Price without addons.">
			</i>
		</td>
		<td>
		Total Price
		<i 
			class="fa fa-info-circle" 
			data-tippy-content="Price with addons.">
		</i>
		</td>
		<td></td>
	</tr>
{{#each items}}
	<tr>
		<td>{{counter @index}}</td>
		<td class="item-name-col-td">{{this.size}} {{this.category}} {{this.name}}</td>
		<td>\${{this.base_price}}</td>
		<td>\${{this.total_price}}</td>
		<td>
			<i class="fa fa-trash-o rm-from-cart-btn" data-item="{{ this.id }}"></i>
		</td>
	</tr>

	{{#if this.addons}}
	<tr>
		<td></td>
		<td colspan=4 class="item-name-col-td">
			<ul>
			{{#each this.addons}}
			<li>{{this.name}} {{ formatAddonPrice this.price }}</li>
			</ou>
		{{/each}}
	</td>
	</tr>
	{{/if}}

{{/each}}
</table>
`);

//returns empty string if price==0.00 otherwise adds $ symbol in the front
Handlebars.registerHelper('formatAddonPrice', price => 
	price == 0.00 ? '' : `(+\$${price})`);

//1-indexed counter. Usage: {{counter @index}}
Handlebars.registerHelper("counter", index => index + 1);



// **************************************************************



//calculate total price and row numbers and update DOM
//called when page loads or item deleted
// function recalculateCart() {
// 	//update total price
// 	let total = 0;
// 	document.querySelectorAll('.item-total-price')
// 	.forEach(price_elem => total += parseFloat(price_elem.dataset.price) );
// 	document.querySelector("#total-order-price").innerHTML = `
// 		Total: \$${total.toFixed(2)}`;

// 	//update row nums (changes when item item delated from the middle)
// 	let counter = 1;
// 	document.querySelectorAll('.row-n').forEach(row_n => {
// 		row_n.innerHTML = counter;
// 		counter += 1;
// 	});
	
// }

function deleteCartItem(id) {
	const form_data = new FormData();
	form_data.append('item_id', id)
	fetch(`/remove-cart-item`, {
		method: 'post',
		body: form_data,
		headers: {
			'X-CSRFToken' : Cookies.get('csrftoken'),
		}
	}).then(response => {
		if (!response.ok)
			throw 'Failed to delete order item.'
		//remove tr(s) from DOM (2 rows if item with addons)
		// document.querySelectorAll(`tr[data-item="${id}"]`)
		// .forEach(element => element.remove() );
		// recalculateCart();

		renderCart();
	});
}