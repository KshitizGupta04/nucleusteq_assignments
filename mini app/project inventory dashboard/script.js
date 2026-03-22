document.addEventListener("DOMContentLoaded", () => {
  
  // ==========================================
  // 1. STATE & DEFAULT DATA
  // ==========================================
  let products = [];
  const defaultProducts = [
    { 
      id: 1, name: "Atomic Habits", price: 499, stock: 15, category: "books", 
      image: "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400&q=80" 
    },
    { 
      id: 2, name: "The Hidden Hindu", price: 299, stock: 2, category: "books", 
      image: "https://images.unsplash.com/photo-1604537466158-719b1972fed8?w=400&q=80" 
    },
    { 
      id: 3, name: "Rich Dad Poor Dad", price: 399, stock: 8, category: "books", 
      image: "https://images.unsplash.com/photo-1554774853-719586f82d77?w=400&q=80" 
    },
    { 
      id: 4, name: "Redmi Watch", price: 3999, stock: 20, category: "accessories", 
      image: "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=400&q=80" 
    },
    { 
      id: 5, name: "Nike Shoes", price: 7499, stock: 4, category: "clothing", 
      image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80" 
    },
    { 
      id: 6, name: "Roadster Jeans", price: 1299, stock: 12, category: "clothing", 
      image: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&q=80" 
    },
    { 
      id: 7, name: "Allen Solly Shirt", price: 1599, stock: 18, category: "clothing", 
      image: "https://images.unsplash.com/photo-1596755094514-f87e32f85e23?w=400&q=80" 
    },
    { 
      id: 8, name: "HP Laptop", price: 65000, stock: 3, category: "electronics", 
      image: "https://images.unsplash.com/photo-1531297172867-46406b724ccb?w=400&q=80" 
    },
    { 
      id: 9, name: "Realme Tablet", price: 19999, stock: 0, category: "electronics", 
      image: "https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?w=400&q=80" 
    }
  ];

  const productGrid = document.getElementById("productGrid");
  const loaderContainer = document.getElementById("loader-container");
  const analyticsSection = document.getElementById("analytics");
  const form = document.getElementById("productForm");

  const searchInput = document.getElementById("search");
  const categoryFilter = document.getElementById("categoryFilter");
  const sortSelect = document.getElementById("sort");
  const lowStockFilter = document.getElementById("lowStockFilter");
  const submitBtn = document.getElementById("submitBtn");

  // ==========================================
  // 2. IMAGE COMPRESSION
  // ==========================================
  function compressImage(file) {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = (e) => {
        const img = new Image();
        img.src = e.target.result;
        img.onload = () => {
          const canvas = document.createElement("canvas");
          const ctx = canvas.getContext("2d");
          const maxWidth = 400; 
          const scale = maxWidth / img.width;
          canvas.width = maxWidth;
          canvas.height = img.height * scale;
          ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
          resolve(canvas.toDataURL("image/jpeg", 0.7));
        };
      };
    });
  }

  // 3. ASYNC LOADING
  function fetchProducts() {
    return new Promise((resolve) => {
      setTimeout(() => {
        try {
          const storedData = localStorage.getItem("cyber_inventory");
          resolve(storedData ? JSON.parse(storedData) : [...defaultProducts]);
        } catch (error) {
          console.error("Local storage error:", error);
          resolve([...defaultProducts]);
        }
      }, 1500);
    });
  }

  function saveData() {
    localStorage.setItem("cyber_inventory", JSON.stringify(products));
  }


  // 4. UI RENDERING
  function updateAnalytics() {
    const totalProducts = products.length;
    const totalValue = products.reduce((sum, p) => sum + (p.price * p.stock), 0);
    const outOfStock = products.filter(p => p.stock === 0).length;

    analyticsSection.innerHTML = `
      <div class="glass-panel text-center">
        <div class="metric-title">Active Assets</div>
        <div class="metric-value">${totalProducts}</div>
      </div>
      <div class="glass-panel text-center">
        <div class="metric-title">Network Value</div>
        <div class="metric-value" style="color: var(--neon-cyan)">₹${totalValue.toLocaleString('en-IN')}</div>
      </div>
      <div class="glass-panel text-center">
        <div class="metric-title">Critical (0 Stock)</div>
        <div class="metric-value ${outOfStock > 0 ? 'danger-text' : ''}">${outOfStock}</div>
      </div>
    `;
  }

  function renderProducts(list) {
    productGrid.innerHTML = "";

    if (list.length === 0) {
      productGrid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted); padding: 40px;">No assets match current filters.</div>`;
      return;
    }

    list.forEach(product => {
      let stockStatus = product.stock > 4 ? `${product.stock} Units` :
                        product.stock > 0 ? `Low: ${product.stock}` : "DEPLETED";
     
      let colorStyle = product.stock === 0 ? "color: var(--neon-magenta);" : "";
      let imgSrc = product.image || "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&q=80";

      const card = document.createElement("div");
      card.className = "product-card";
      card.innerHTML = `
        <div class="card-content">
          <span class="badge">${product.category}</span>
          <img src="${imgSrc}" class="product-image" alt="${product.name}">
          <h3 class="product-name">${product.name}</h3>
          <p style="color: var(--text-muted); font-size: 0.9rem; margin-top: 5px; ${colorStyle}">Status: ${stockStatus}</p>
          <p class="product-price">₹${product.price.toLocaleString('en-IN')}</p>
        </div>
        <button class="btn-delete" onclick="deleteProduct(${product.id})">Purge Asset</button>
      `;
      productGrid.appendChild(card);
    });
  }

  // Mouse Spotlight
  productGrid.addEventListener("mousemove", (e) => {
    for(const card of document.getElementsByClassName("product-card")) {
      const rect = card.getBoundingClientRect(),
            x = e.clientX - rect.left,
            y = e.clientY - rect.top;
      card.style.setProperty("--mouse-x", `${x}px`);
      card.style.setProperty("--mouse-y", `${y}px`);
    }
  });

 
  // 5. FILTERS
  function applyFilters() {
    let filtered = [...products];
    const searchStr = searchInput.value.toLowerCase().trim();
    if (searchStr) filtered = filtered.filter(p => p.name.toLowerCase().includes(searchStr));

    const catVal = categoryFilter.value;
    if (catVal !== "all") filtered = filtered.filter(p => p.category === catVal);

    if (lowStockFilter.checked) filtered = filtered.filter(p => p.stock < 5);

    const sortVal = sortSelect.value;
    if (sortVal === "low") filtered.sort((a, b) => a.price - b.price);
    if (sortVal === "high") filtered.sort((a, b) => b.price - a.price);
    if (sortVal === "az") filtered.sort((a, b) => a.name.localeCompare(b.name));
    if (sortVal === "za") filtered.sort((a, b) => b.name.localeCompare(a.name));

    renderProducts(filtered);
  }

  searchInput.addEventListener("input", applyFilters);
  categoryFilter.addEventListener("change", applyFilters);
  sortSelect.addEventListener("change", applyFilters);
  lowStockFilter.addEventListener("change", applyFilters);

 
  // 6. CRUD: ADD & DELETE
  window.deleteProduct = function(id) {
    products = products.filter(p => p.id !== id);
    saveData();
    applyFilters();
    updateAnalytics();
    showToast("Asset purged from database.", "error");
  }

  form.addEventListener("submit", async function(e) {
    e.preventDefault();
    submitBtn.disabled = true;

    const name = document.getElementById("assetName").value.trim();
    const price = Number(document.getElementById("assetPrice").value);
    const stock = Number(document.getElementById("assetStock").value);
    const category = document.getElementById("assetCategory").value;
    const imageFile = document.getElementById("assetImage").files[0];

    if (!name || price <= 0 || stock < 0 || !category || !imageFile) {
      showToast("Invalid data. Ensure image is uploaded.", "error");
      submitBtn.disabled = false;
      return;
    }

    const compressedImageBase64 = await compressImage(imageFile);

    products.push({
      id: Date.now(),
      name,
      price,
      stock,
      category,
      image: compressedImageBase64
    });
   
    saveData();
    form.reset();
    applyFilters();
    updateAnalytics();
   
    submitBtn.disabled = false;
    showToast("Asset successfully injected.", "success");
  });

  function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    if (!container) return;
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.innerText = message;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
  }

  async function initApp() {
    products = await fetchProducts();
    if (loaderContainer) loaderContainer.style.display = "none";
   
    [searchInput, categoryFilter, sortSelect, lowStockFilter, submitBtn].forEach(el => {
      if (el) el.disabled = false;
    });

    updateAnalytics();
    renderProducts(products);
  }

  initApp();
});

  
  