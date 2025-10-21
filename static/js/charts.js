document.addEventListener('DOMContentLoaded', () => {
  const chartEl = document.getElementById('nutrientChart');
  if (!chartEl) return;
  const targets = JSON.parse(sessionStorage.getItem('targets') || '{}');
  const recs = JSON.parse(sessionStorage.getItem('recommendations') || '[]');

  // Populate targets text
  const targetsEl = document.getElementById('targets');
  targetsEl.innerHTML = `
    <div class="card card-body">
      <div><strong>Calories:</strong> ${targets.calories || '-'} kcal</div>
      <div><strong>Protein:</strong> ${targets.protein_g || '-'} g</div>
      <div><strong>Carbs:</strong> ${targets.carbs_g || '-'} g</div>
      <div><strong>Fat:</strong> ${targets.fat_g || '-'} g</div>
    </div>`;

  // Populate recommendations list
  const list = document.getElementById('recommendations');
  list.innerHTML = '';
  recs.forEach(item => {
    const li = document.createElement('li');
    li.className = 'list-group-item d-flex justify-content-between align-items-start';
    li.innerHTML = `
      <div class="ms-2 me-auto">
        <div class="fw-bold">${item.name}</div>
        <small>${item.category} · cluster ${item.cluster} · sim ${item.similarity}</small>
      </div>
      <span class="badge bg-primary rounded-pill">${Math.round(item.calories)} kcal</span>
    `;
    list.appendChild(li);
  });

  const data = {
    labels: ['Protein (g)', 'Carbs (g)', 'Fat (g)'],
    datasets: [{
      label: 'Daily Targets',
      data: [targets.protein_g || 0, targets.carbs_g || 0, targets.fat_g || 0],
      backgroundColor: ['rgba(54, 162, 235, 0.5)','rgba(255, 206, 86, 0.5)','rgba(255, 99, 132, 0.5)'],
      borderColor: ['rgb(54, 162, 235)','rgb(255, 206, 86)','rgb(255, 99, 132)'],
      borderWidth: 1
    }]
  };

  new Chart(chartEl, {
    type: 'bar',
    data,
    options: {
      responsive: true,
      plugins: { legend: { display: true } },
      scales: { y: { beginAtZero: true } }
    }
  });
});


