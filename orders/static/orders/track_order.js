var timerID;
document.addEventListener('DOMContentLoaded', () => {
  updateOrderStatus();
  timerID = setInterval(updateOrderStatus, 30_000);
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
      delivery_estimate.innerHTML = `${parseInt((delivery_datetime - now)/1000/60)} minutes`;
       //if delivered stop updating order status and hide delivery time
      if (data.status === 'Delivered') {
        clearInterval(timerID);
        document.querySelector('#delivery-estimate-wrapper').hidden = true;
      }
    });
  });
}