const status = document.querySelector('#status');
const money = cents => new Intl.NumberFormat('en-IE', { style: 'currency', currency: 'EUR' }).format(cents / 100);

async function request(method, path, body) {
  const response = await fetch(path, {
    method,
    headers: { 'Content-Type': 'application/json' },
    ...(body === undefined ? {} : { body: JSON.stringify(body) })
  });
  if (!response.ok) throw new Error(`HTTP ${response.status} from ${method} ${path}`);
  return response.json();
}

function renderCart(cart) {
  document.querySelector('#cart-count').textContent = cart.itemCount;
  document.querySelector('#line-count').textContent =
    `${cart.items.length} ${cart.items.length === 1 ? 'product' : 'products'}`;
  document.querySelector('#total').textContent = money(cart.totalCents);
  const rows = cart.items.map(item => {
    const row = document.createElement('div');
    row.className = 'cart-line';
    const name = document.createElement('strong');
    name.textContent = item.name;
    const total = document.createElement('span');
    total.className = 'line-total';
    total.textContent = money(item.lineTotalCents);
    const quantity = document.createElement('p');
    quantity.textContent = `Quantity ${item.quantity} × ${money(item.priceCents)}`;
    const actions = document.createElement('div');
    actions.className = 'actions';
    row.append(name, total, quantity, actions);
    return row;
  });
  if (rows.length === 0) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = 'Your cart is empty. Choose something from the collection.';
    rows.push(empty);
  }
  document.querySelector('#cart-lines').replaceChildren(...rows);
}

async function changeCart(method, path, body) {
  document.querySelectorAll('button').forEach(button => { button.disabled = true; });
  status.removeAttribute('data-error');
  status.textContent = 'Updating your cart…';
  try {
    await request(method, path, body);
    const cart = await request('GET', '/api/cart');
    renderCart(cart);
    status.textContent = `Server cart: ${cart.itemCount} item(s), ${money(cart.totalCents)}.`;
  } catch (error) {
    status.dataset.error = 'true';
    status.textContent = `Could not update your cart: ${error.message}. Check the running app and retry.`;
    console.warn('Cart update failed:', error);
  } finally {
    document.querySelectorAll('button').forEach(button => { button.disabled = false; });
  }
}

document.querySelector('#reset').addEventListener('click', () =>
  changeCart('POST', '/api/workshop/reset?items=0'));
document.querySelector('#sample').addEventListener('click', () =>
  changeCart('POST', '/api/workshop/reset?items=8'));

async function initialize() {
  try {
    const products = await request('GET', '/api/products');
    document.querySelector('#products').replaceChildren(...products.map(product => {
      const row = document.createElement('li');
      const name = document.createElement('span');
      name.className = 'product-name';
      name.textContent = product.name;
      const price = document.createElement('span');
      price.className = 'price';
      price.textContent = money(product.priceCents);
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'add-button';
      button.textContent = 'Add to cart';
      button.setAttribute('aria-label', `Add ${product.name} to cart`);
      button.addEventListener('click', () =>
        changeCart('POST', '/api/cart/items', { productId: product.id, quantity: 1 }));
      row.append(name, price, button);
      return row;
    }));
    renderCart(await request('GET', '/api/cart'));
    const identity = await request('GET', '/api/workshop');
    document.querySelector('#identity').textContent =
      `Revision: ${identity.revision} · Process: ${identity.processId}`;
    status.textContent = 'Ready. Try adding the same notebook twice.';
  } catch (error) {
    status.dataset.error = 'true';
    status.textContent = `Cannot load the shop: ${error.message}. Start the workshop app and reload.`;
    console.warn('Shop initialization failed:', error);
  }
}
initialize();
