document.addEventListener('DOMContentLoaded', () => {
	//init tippy tooltips
	tippy('[data-tippy-content]', {
		placement: 'right',
	});

	document.addEventListener('click', (e) => {
		if (e.target.matches('.rm-from-cart-btn')) {
			const dataset = e.target.dataset;
			deleteOrderItem(dataset.item);
		}
	});
	recalculateCart();
});

//calculate total price and row numbers and update DOM
//called when page loads or item deleted
function recalculateCart() {
	//update total price
	let total = 0;
	document.querySelectorAll('.item-total-price')
	.forEach(price_elem => total += parseFloat(price_elem.dataset.price) );
	document.querySelector("#total-order-price").innerHTML = `
		Total: \$${total.toFixed(2)}`;

	//update row nums (changes when item item delated from the middle)
	let counter = 1;
	document.querySelectorAll('.row-n').forEach(row_n => {
		row_n.innerHTML = counter;
		counter += 1;
	});
	
}

function deleteOrderItem(id) {
	const form_data = new FormData();
	fetch(`/api/order_items/${id}`, {
		method: 'delete',
		headers: {
			'X-CSRFToken' : Cookies.get('csrftoken'),
		}
	}).then(response => {
		if (!response.ok)
			throw 'Failed to delete order item.'
		//remove tr(s) from DOM (2 rows if item with addons)
		document.querySelectorAll(`tr[data-item="${id}"]`)
		.forEach(element => element.remove() );
		recalculateCart();
	});
}