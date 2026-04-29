const COLORS = [
  '#4e73df','#1cc88a','#36b9cc','#f6c23e','#e74a3b',
  '#858796','#5a5c69','#2e59d9','#17a673','#2c9faf',
];

function makeChart(id, type, labels, datasets, opts = {}) {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  new Chart(ctx, {
    type,
    data: { labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: type !== 'bar' || datasets.length > 1 } },
      ...opts,
    },
  });
}

async function fetchData(name) {
  const r = await fetch(`/analytics/data/${name}`);
  return r.json();
}

async function buildCharts() {
  const [month, cat, ship, prod, country] = await Promise.all([
    fetchData('sales_by_month'),
    fetchData('sales_by_category'),
    fetchData('ship_status'),
    fetchData('top_products'),
    fetchData('orders_by_country'),
  ]);

  if (month.error) console.warn('sales_by_month:', month.error);
  makeChart('chartMonth', 'line', month.labels || [], [{
    label: 'Revenue (€)',
    data: month.values || [],
    borderColor: COLORS[0],
    backgroundColor: COLORS[0] + '33',
    tension: 0.3,
    fill: true,
  }]);

  makeChart('chartCategory', 'bar', cat.labels || [], [{
    label: 'Revenue',
    data: cat.values || [],
    backgroundColor: COLORS,
  }], { plugins: { legend: { display: false } } });

  makeChart('chartShip', 'doughnut', ship.labels || [], [{
    data: ship.values || [],
    backgroundColor: [COLORS[1], COLORS[4]],
  }]);

  makeChart('chartProducts', 'bar', prod.labels || [], [{
    label: 'Revenue',
    data: prod.revenue || [],
    backgroundColor: COLORS[0],
  }], {
    indexAxis: 'y',
    plugins: { legend: { display: false } },
  });

  makeChart('chartCountry', 'bar', country.labels || [], [{
    label: 'Orders',
    data: country.counts || [],
    backgroundColor: COLORS[2],
  }], {
    indexAxis: 'y',
    plugins: { legend: { display: false } },
  });
}

buildCharts();
