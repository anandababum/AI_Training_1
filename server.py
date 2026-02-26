from http.server import HTTPServer, BaseHTTPRequestHandler
import os

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>This is dashboard designed by Pavi</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #0f172a;
      color: #e2e8f0;
      min-height: 100vh;
      padding: 24px;
    }
    header {
      text-align: center;
      margin-bottom: 32px;
    }
    header h1 {
      font-size: 2rem;
      font-weight: 700;
      color: #f8fafc;
      letter-spacing: 0.5px;
    }
    header p {
      color: #94a3b8;
      margin-top: 6px;
      font-size: 0.95rem;
    }
    .kpi-row {
      display: flex;
      gap: 16px;
      justify-content: center;
      flex-wrap: wrap;
      margin-bottom: 32px;
    }
    .kpi {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 20px 28px;
      text-align: center;
      min-width: 180px;
    }
    .kpi .value {
      font-size: 1.8rem;
      font-weight: 700;
      color: #38bdf8;
    }
    .kpi .label {
      font-size: 0.8rem;
      color: #94a3b8;
      margin-top: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .charts-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      max-width: 1300px;
      margin: 0 auto 32px;
    }
    @media (max-width: 900px) {
      .charts-grid { grid-template-columns: 1fr; }
    }
    .card {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 16px;
      padding: 24px;
    }
    .card h2 {
      font-size: 1rem;
      font-weight: 600;
      color: #cbd5e1;
      margin-bottom: 20px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }
    .chart-container {
      position: relative;
      height: 320px;
    }
    .trend-card {
      max-width: 1300px;
      margin: 0 auto 32px;
    }
    .trend-card .chart-container {
      height: 360px;
    }
    .legend-inline {
      display: flex;
      gap: 20px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.82rem;
      color: #94a3b8;
    }
    .legend-line {
      width: 28px;
      height: 3px;
      border-radius: 2px;
    }
    .legend-line.dashed {
      background: repeating-linear-gradient(90deg, #f472b6 0, #f472b6 6px, transparent 6px, transparent 10px);
    }
    .table-card {
      max-width: 1300px;
      margin: 0 auto;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.9rem;
    }
    th {
      background: #0f172a;
      color: #94a3b8;
      padding: 12px 16px;
      text-align: left;
      font-weight: 600;
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.5px;
      border-bottom: 1px solid #334155;
    }
    td {
      padding: 12px 16px;
      border-bottom: 1px solid #1e293b;
      color: #e2e8f0;
    }
    tr:hover td { background: #1e293b; }
    .rank { font-weight: 700; color: #94a3b8; }
    .bar-cell { width: 200px; }
    .bar-bg {
      background: #0f172a;
      border-radius: 4px;
      height: 10px;
      overflow: hidden;
    }
    .bar-fill {
      height: 100%;
      border-radius: 4px;
      background: linear-gradient(90deg, #38bdf8, #818cf8);
    }
    .share-pct { font-weight: 700; color: #38bdf8; }
    .badge {
      display: inline-block;
      padding: 2px 10px;
      border-radius: 99px;
      font-size: 0.75rem;
      font-weight: 600;
    }
    .badge-up   { background: #14532d; color: #4ade80; }
    .badge-mid  { background: #1e3a5f; color: #60a5fa; }
    .badge-down { background: #450a0a; color: #f87171; }
    footer {
      text-align: center;
      margin-top: 32px;
      color: #475569;
      font-size: 0.8rem;
    }
    footer a { color: #38bdf8; text-decoration: none; }
  </style>
</head>
<body>

<header>
  <h1>This is dashboard designed by Pavi</h1>
  <p>Top 10 CRM Platforms &mdash; Global market data &bull; Total market size: $112.91B</p>
</header>

<div class="kpi-row">
  <div class="kpi"><div class="value">$112.91B</div><div class="label">Market Size 2025</div></div>
  <div class="kpi"><div class="value">$262.74B</div><div class="label">Projected Size 2032</div></div>
  <div class="kpi"><div class="value">21.7%</div><div class="label">Salesforce Share</div></div>
  <div class="kpi"><div class="value">54.2%</div><div class="label">Top 10 Combined Share</div></div>
  <div class="kpi"><div class="value">18.6%</div><div class="label">CAGR 2025-2032</div></div>
</div>

<div class="charts-grid">
  <div class="card">
    <h2>Market Share by Vendor (%)</h2>
    <div class="chart-container">
      <canvas id="barChart"></canvas>
    </div>
  </div>
  <div class="card">
    <h2>Market Share Distribution</h2>
    <div class="chart-container">
      <canvas id="doughnutChart"></canvas>
    </div>
  </div>
</div>

<div class="card trend-card">
  <h2>CRM Market Growth 2020 &ndash; 2032 (USD Billions)</h2>
  <div class="legend-inline">
    <div class="legend-item">
      <div class="legend-line" style="background:#38bdf8"></div>Historical (Actual)
    </div>
    <div class="legend-item">
      <div class="legend-line dashed"></div>Forecast (Projected &bull; CAGR ~11.9%)
    </div>
  </div>
  <div class="chart-container">
    <canvas id="trendChart"></canvas>
  </div>
</div>

<div class="card table-card">
  <h2>Top 10 CRM Vendors &mdash; Detailed Breakdown</h2>
  <table>
    <thead>
      <tr>
        <th>#</th>
        <th>Vendor</th>
        <th>Market Share</th>
        <th>Share Bar</th>
        <th>Revenue (2024)</th>
        <th>Customers</th>
        <th>YoY Growth</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="rank">1</td><td>Salesforce</td>
        <td class="share-pct">21.7%</td>
        <td class="bar-cell"><div class="bar-bg"><div class="bar-fill" style="width:100%"></div></div></td>
        <td>$37.9B</td><td>327,000+</td>
        <td><span class="badge badge-up">+11%</span></td>
      </tr>
      <tr>
        <td class="rank">2</td><td>Microsoft Dynamics 365</td>
        <td class="share-pct">5.2%</td>
        <td class="bar-cell"><div class="bar-bg"><div class="bar-fill" style="width:24%"></div></div></td>
        <td>$10.1B</td><td>500,000+</td>
        <td><span class="badge badge-up">+23%</span></td>
      </tr>
      <tr>
        <td class="rank">3</td><td>Oracle</td>
        <td class="share-pct">4.1%</td>
        <td class="bar-cell"><div class="bar-bg"><div class="bar-fill" style="width:19%"></div></div></td>
        <td>$5.8B</td><td>430,000+</td>
        <td><span class="badge badge-mid">+7%</span></td>
      </tr>
      <tr>
        <td class="rank">4</td><td>HubSpot</td>
        <td class="share-pct">3.4%</td>
        <td class="bar-cell"><div class="bar-bg"><div class="bar-fill" style="width:16%"></div></div></td>
        <td>$2.63B</td><td>248,000+</td>
        <td><span class="badge badge-up">+21%</span></td>
      </tr>
      <tr>
        <td class="rank">5</td><td>Adobe</td>
        <td class="share-pct">3.4%</td>
        <td class="bar-cell"><div class="bar-bg"><div class="bar-fill" style="width:16%"></div></div></td>
        <td>$5.4B</td><td>28,000+</td>
        <td><span class="badge badge-up">+14%</span></td>
      </tr>
      <tr>
        <td class="rank">6</td><td>SAP</td>
        <td class="share-pct">3.1%</td>
        <td class="bar-cell"><div class="bar-bg"><div class="bar-fill" style="width:14%"></div></div></td>
        <td>$4.9B</td><td>440,000+</td>
        <td><span class="badge badge-mid">+8%</span></td>
      </tr>
      <tr>
        <td class="rank">7</td><td>Zoho</td>
        <td class="share-pct">2.8%</td>
        <td class="bar-cell"><div class="bar-bg"><div class="bar-fill" style="width:13%"></div></div></td>
        <td>$1.5B</td><td>185,000+</td>
        <td><span class="badge badge-up">+19%</span></td>
      </tr>
      <tr>
        <td class="rank">8</td><td>Zendesk</td>
        <td class="share-pct">2.5%</td>
        <td class="bar-cell"><div class="bar-bg"><div class="bar-fill" style="width:12%"></div></div></td>
        <td>$2.1B</td><td>170,000+</td>
        <td><span class="badge badge-mid">+9%</span></td>
      </tr>
      <tr>
        <td class="rank">9</td><td>Freshworks</td>
        <td class="share-pct">1.5%</td>
        <td class="bar-cell"><div class="bar-bg"><div class="bar-fill" style="width:7%"></div></div></td>
        <td>$0.7B</td><td>68,000+</td>
        <td><span class="badge badge-up">+20%</span></td>
      </tr>
      <tr>
        <td class="rank">10</td><td>ServiceNow</td>
        <td class="share-pct">1.3%</td>
        <td class="bar-cell"><div class="bar-bg"><div class="bar-fill" style="width:6%"></div></div></td>
        <td>$2.0B</td><td>8,100+</td>
        <td><span class="badge badge-up">+22%</span></td>
      </tr>
    </tbody>
  </table>
</div>

<footer>
  <p>Data sources:
    <a href="https://www.salesforce.com/news/stories/idc-crm-market-share-ranking-2025/" target="_blank">IDC / Salesforce</a> &bull;
    <a href="https://www.webbycrown.com/crm-market-share/" target="_blank">WebbyCrown</a> &bull;
    <a href="https://www.cirrusinsight.com/blog/crm-statistics-trends-and-predictions" target="_blank">Cirrus Insight</a>
    &bull; Dashboard served by Python &bull; 2026
  </p>
</footer>

<script>
  const vendors = ['Salesforce','Microsoft','Oracle','HubSpot','Adobe','SAP','Zoho','Zendesk','Freshworks','ServiceNow'];
  const shares  = [21.7, 5.2, 4.1, 3.4, 3.4, 3.1, 2.8, 2.5, 1.5, 1.3];
  const others  = 100 - shares.reduce((a,b)=>a+b,0);

  const palette = [
    '#38bdf8','#818cf8','#34d399','#f472b6','#fb923c',
    '#a78bfa','#facc15','#4ade80','#f87171','#2dd4bf'
  ];

  // Bar chart
  new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
      labels: vendors,
      datasets: [{
        label: 'Market Share (%)',
        data: shares,
        backgroundColor: palette,
        borderRadius: 6,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { color: '#94a3b8', font: { size: 11 } }, grid: { color: '#1e293b' } },
        y: { ticks: { color: '#94a3b8', callback: v => v + '%' }, grid: { color: '#334155' } }
      }
    }
  });

  // Trend line chart
  const years = ['2020','2021','2022','2023','2024','2025','2026','2027','2028','2029','2030','2031','2032'];
  // Historical actuals (2020-2025), null for forecast years
  const historical = [40.2, 47.3, 57.8, 80.0, 91.3, 112.9, null, null, null, null, null, null, null];
  // Forecast (2025-2032), null for purely historical years
  const forecast   = [null, null, null, null, null, 112.9, 126.4, 141.5, 158.4, 177.3, 198.4, 222.0, 248.5];

  new Chart(document.getElementById('trendChart'), {
    type: 'line',
    data: {
      labels: years,
      datasets: [
        {
          label: 'Historical',
          data: historical,
          borderColor: '#38bdf8',
          backgroundColor: 'rgba(56,189,248,0.12)',
          pointBackgroundColor: '#38bdf8',
          pointRadius: 5,
          pointHoverRadius: 7,
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          spanGaps: false,
        },
        {
          label: 'Forecast',
          data: forecast,
          borderColor: '#f472b6',
          backgroundColor: 'rgba(244,114,182,0.08)',
          pointBackgroundColor: '#f472b6',
          pointRadius: 5,
          pointHoverRadius: 7,
          borderWidth: 3,
          borderDash: [8, 4],
          fill: true,
          tension: 0.4,
          spanGaps: false,
        }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => ' ' + ctx.dataset.label + ': $' + ctx.parsed.y + 'B'
          }
        },
        annotation: {}
      },
      scales: {
        x: {
          ticks: { color: '#94a3b8', font: { size: 11 } },
          grid: { color: '#334155' }
        },
        y: {
          ticks: {
            color: '#94a3b8',
            callback: v => '$' + v + 'B'
          },
          grid: { color: '#334155' },
          title: {
            display: true,
            text: 'Market Size (USD Billions)',
            color: '#64748b',
            font: { size: 11 }
          }
        }
      }
    }
  });

  // Doughnut chart
  new Chart(document.getElementById('doughnutChart'), {
    type: 'doughnut',
    data: {
      labels: [...vendors, 'Others'],
      datasets: [{
        data: [...shares, parseFloat(others.toFixed(1))],
        backgroundColor: [...palette, '#334155'],
        borderColor: '#0f172a',
        borderWidth: 2,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'right',
          labels: { color: '#94a3b8', font: { size: 11 }, padding: 12, boxWidth: 14 }
        },
        tooltip: {
          callbacks: { label: ctx => ' ' + ctx.label + ': ' + ctx.parsed + '%' }
        }
      }
    }
  });
</script>

</body>
</html>
"""

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/achievements':
            import os
            here = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(here, 'achievements.html'), 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6543))
    server = HTTPServer(('0.0.0.0', port), DashboardHandler)
    print(f'Dashboard running on http://0.0.0.0:{port}')
    server.serve_forever()
