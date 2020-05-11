document.addEventListener('DOMContentLoaded', () => {
	document.addEventListener('click', (e) => {
		if (e.target.matches('.rm-from-cart-btn')) {
			console.log('removing');
			const dataset = e.target.dataset;
			deleteOrderItem(dataset.item, dataset.csrf_token);
		}
	})

	calculateTotalOrderPrice()
		
});


function calculateTotalOrderPrice() {
	let total = 0;
	document.querySelectorAll('.item-total-price')
	.forEach(price_elem => total += parseFloat(price_elem.dataset.price) )
	document.querySelector("#total-order-price").innerHTML = `
		Total: ${total.toFixed(2)}`;
	
}

function deleteOrderItem(id, csrf_token) {
	const form_data = new FormData();
    form_data.append('csrfmiddlewaretoken', Cookies.get('csrftoken'));


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
		//recalculate order total
		calculateTotalOrderPrice();
	});
}