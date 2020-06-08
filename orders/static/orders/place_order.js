import {cart_table_template} from './templates.js'

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

	const cart = cart_table_template({items: cart_data.items, total_price: cart_data.total_price});
	document.querySelector('#cart-items-container').innerHTML = cart;
	document.querySelector('#total-order-price').innerHTML = `Total: \$${cart_data.total_price}`;

	//init tippy tooltips
	tippy('[data-tippy-content]', {
		placement: 'right',
	});
}

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
		renderCart();
	});
}