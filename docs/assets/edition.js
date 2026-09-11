(() => {
  'use strict';
  const rows = JSON.parse(document.getElementById('country-data').textContent);
  const select = document.getElementById('country');
  function describe() {
    const row = rows.find(r => r.country === select.value);
    document.getElementById('country-name').textContent = row.country;
    document.getElementById('cup-price').textContent = '£' + row.price.toFixed(2);
    document.getElementById('work-time').textContent = row.minutes.toFixed(1) + ' min';
    document.getElementById('price-rank').textContent = `Price rank ${row.price_rank} of ${rows.length}`;
    document.getElementById('time-rank').textContent = `Time rank ${row.minutes_rank} of ${rows.length}`;
    document.getElementById('country-note').textContent = `${row.n} cafés · Mean hourly pay £${row.wage.toFixed(2)}, excluding tips. Ranks run from cheapest / shortest (1) to most expensive / longest (${rows.length}).`;
  }
  select.addEventListener('change', describe);
  const search = document.getElementById('country-search'), sort = document.getElementById('sort');
  function table() {
    const matching = rows.filter(row => row.country.toLowerCase().includes(search.value.trim().toLowerCase()));
    matching.sort((a,b) => sort.value === 'country' ? a.country.localeCompare(b.country) : sort.value === 'n' ? b.n-a.n : a[sort.value]-b[sort.value]);
    const body = document.getElementById('countries');
    body.replaceChildren();
    for (const row of matching) {
      const tr = document.createElement('tr');
      for (const value of [row.country,'£'+row.price.toFixed(2),'£'+row.wage.toFixed(2),row.minutes.toFixed(1),row.n]) {
        const cell = document.createElement('td');cell.textContent=value;tr.append(cell);
      }
      body.append(tr);
    }
    document.getElementById('table-status').textContent = matching.length ? `${matching.length} of ${rows.length} countries` : 'No countries match. Try another name.';
  }
  search.addEventListener('input',table);sort.addEventListener('change',table);
  describe();table();
})();
