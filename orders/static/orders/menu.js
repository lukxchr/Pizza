import {add_to_cart_form_template, cart_template} from './templates.js'

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

async function renderCart() {
  //fetch existing pending order
  let response = await fetch('/get-cart');
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

  //fetch list of available addons
  const response = await fetch(`/api/menu_item_addons/?allowed_for=${item_id}`);
  if (!response.ok)
    throw('Failed to fetch addons. Please try again.');
  const addons = await response.json();

  //build add_to_cart_form with the addons and display inside tippy instance
  const form = add_to_cart_form_template({
    item_id: item_id, addons: addons});
  instance.setContent(form);
  instance.popper.childNodes[0].onsubmit =
    e => {
      const form_data = new FormData(e.target);
      const headers = {'X-CSRFToken' : Cookies.get('csrftoken'),};
      fetch('/add-to-cart', {method: 'post', body: form_data, headers: headers})
      .then(response => response.json())
      .then(data => {
        instance.setContent(data.message);
        renderCart();
      });
      return false; //prevent page reload on submit
    }
}

function submit(form) {
  const form_data = new FormData(form);
  fetch('/add-to-cart', {method: 'post', body: form_data})
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
  return false; //prevent page reload on submit
}
