document.addEventListener('DOMContentLoaded', () => {
	setInterval(updateOrderStatus, 1000)
});

function updateOrderStatus() {
	const payment_status = document.querySelector('#payment-status');
	const order_status = document.querySelector("#order-status");
	const delivery_estimate = document.querySelector("#delivery-estimate");
	const order_id = order_status.dataset.order;
	fetch(`/api/orders/${order_id}`).then(response => {
		if (!response.ok)
			throw 'Failed to update order status.'
		response.json().then(data => {
			payment_status.innerHTML = (data.is_paid) ? 'Completed' : 'Pending';
			order_status.innerHTML = data.status;
			const delivery_datetime = new Date(data.delivery_estimate);
			const now = new Date()
			delivery_estimate.innerHTML = `${delivery_datetime.getHours()}:${delivery_datetime.getMinutes()} (${parseInt((delivery_datetime - now)/1000/60)} minutes)`;
		});
	});
}