let products = [
  { id: 1, name: "Laptop", price: 55000, stock: 5, category: "electronics" },
  { id: 2, name: "Shirt", price: 1200, stock: 10, category: "clothing" },
  { id: 3, name: "Book", price: 500, stock: 2, category: "books" },
  { id: 4, name: "Headphones", price: 2000, stock: 0, category: "electronics" },
  { id: 5, name: "Shoes", price: 3000, stock: 3, category: "clothing" },
  { id: 6, name: "Watch", price: 2500, stock: 8, category: "accessories" },
  { id: 7, name: "Bag", price: 1500, stock: 6, category: "accessories" },
  { id: 8, name: "Notebook", price: 100, stock: 20, category: "books" }]

  function renderProducts(productList) {
  const container = document.getElementById("productGrid");
  container.innerHTML = "";

  if (productList.length === 0) {
    container.innerHTML = "<p>No products found</p>";
    return;
  }

  productList.forEach(product => {
    const card = document.createElement("div");

    card.innerHTML = `
      <h3>${product.name}</h3>
      <p>Category: ${product.category}</p>
      <p>Price: ₹${product.price}</p>
      <p>Stock: ${product.stock}</p>
      <button onclick="deleteProduct(${product.id})">Delete</button>
    `;

    container.appendChild(card);
  });
}

// Initial render
renderProducts(products);

function deleteProduct(id) {
  products = products.filter(product => product.id !== id);
  renderProducts(products);
}
