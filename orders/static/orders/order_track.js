document.addEventListener('DOMContentLoaded', () => {
	setInterval(updateOrderStatus, 1000)
	});

function updateOrderStatus() {
	const order_status = document.querySelector("#order-status");
	const delivery_estimate = document.querySelector("#delivery-estimate")
	const order_id = order_status.dataset.order;
	fetch(`/api/orders/${order_id}`).then(response => {
		if (!response.ok)
			throw 'Failed to update order status.'
		response.json().then(data => {
			order_status.innerHTML = data.status;
			const delivery_datetime = new Date(data.delivery_estimate);
			delivery_estimate.innerHTML = delivery_datetime;
		});
	});
}