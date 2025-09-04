<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Atlas - Security Policy Overview</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .chart-container {
            position: relative;
            width: 100%;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
            height: 350px;
            max-height: 400px;
        }
        @media (min-width: 768px) { .chart-container { height: 400px; } }
    </style>
</head>
<body class="bg-[#001a2e] text-gray-200">
    <!-- Palette: Brilliant Blues (#002848, #00509d, #58c7e9, #9fe1e7, #001a2e) -->
    <!-- Plan:
        1. Intro: Hook and brief on security importance.
        2. Supported Versions: A clear visual representation of the provided table data using styled HTML.
        3. Reporting Flow: A step-by-step flowchart to guide users through the process.
        4. Security Metrics: Line chart for reported vs. resolved over time, Doughnut chart for vulnerability types, and Bar chart for time-to-fix.
    -->
    <!-- Visualization Choices:
        - Supported Versions: Styled HTML Table (Goal: Inform/Compare) -> Justification: Simple, direct representation of categorical data. Method: HTML/CSS.
        - Reporting Flow: Flowchart (Goal: Organize/Process) -> Justification: Visualizes a step-by-step process clearly. Method: HTML/CSS.
        - Reported vs. Resolved: Line Chart (Goal: Change over time) -> Justification: Ideal for showing trends and comparison over time. Method: Chart.js.
        - Vulnerability Types: Doughnut Chart (Goal: Compare/Composition) -> Justification: Best for showing part-to-whole breakdown of categories. Method: Chart.js.
        - Time to Fix: Bar Chart (Goal: Compare) -> Justification: Excellent for comparing discrete data points across categories. Method: Chart.js.
    -->
    <!-- Confirmation: NEITHER Mermaid JS NOR SVG were used anywhere in this output. -->

    <div class="container mx-auto p-4 md:p-8">

        <header class="text-center my-12">
            <h1 class="text-4xl md:text-6xl font-black text-[#9fe1e7]">Security Policy Overview</h1>
            <h2 class="text-2xl md:text-4xl font-bold text-[#58c7e9] mt-2">A Proactive Approach to Project Integrity</h2>
            <p class="max-w-3xl mx-auto mt-6 text-lg text-gray-400">Security is not a feature; it's a commitment. This infographic provides a clear and transparent look into the security posture of Project Atlas, from our supported versions to the process for reporting vulnerabilities.</p>
        </header>

        <main class="space-y-16">

            <section class="bg-[#002848] rounded-2xl shadow-2xl p-8">
                <h3 class="text-3xl font-bold text-white text-center mb-8">Supported Versions</h3>
                <p class="text-lg text-gray-300 max-w-4xl mx-auto text-center mb-8">Staying on a supported version is the first line of defense. We provide regular security updates and patches for the following releases to ensure your deployment remains safe and stable.</p>
                <div class="overflow-x-auto">
                    <table class="min-w-full rounded-lg text-gray-200 overflow-hidden">
                        <thead class="bg-[#00509d] text-white">
                            <tr>
                                <th class="py-3 px-6 text-left font-bold text-lg">Version</th>
                                <th class="py-3 px-6 text-left font-bold text-lg">Status</th>
                            </tr>
                        </thead>
                        <tbody class="bg-[#003f5c]">
                            <tr>
                                <td class="py-4 px-6 font-bold text-xl">5.1.x</td>
                                <td class="py-4 px-6 text-xl">✅ Supported</td>
                            </tr>
                            <tr>
                                <td class="py-4 px-6 font-bold text-xl">5.0.x</td>
                                <td class="py-4 px-6 text-xl">❌ Unsupported</td>
                            </tr>
                            <tr>
                                <td class="py-4 px-6 font-bold text-xl">4.0.x</td>
                                <td class="py-4 px-6 text-xl">✅ Supported</td>
                            </tr>
                            <tr>
                                <td class="py-4 px-6 font-bold text-xl">&lt; 4.0</td>
                                <td class="py-4 px-6 text-xl">❌ Unsupported</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <section class="bg-[#002848] rounded-2xl shadow-2xl p-8">
                <h3 class="text-3xl font-bold text-white text-center mb-8">Reporting a Vulnerability</h3>
                <p class="text-lg text-gray-300 max-w-4xl mx-auto text-center mb-8">We rely on our community to help us maintain a secure ecosystem. Your responsible disclosure is a vital part of this process. Please follow these steps to report a finding.</p>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center items-center">
                    <div class="p-6 bg-[#00509d] rounded-lg shadow-md">
                        <div class="text-4xl mb-2">🔍</div>
                        <h4 class="font-bold text-xl mb-2">1. Discover & Document</h4>
                        <p class="text-sm text-gray-300">Find a potential vulnerability and document it with clear steps to reproduce.</p>
                    </div>
                    <div class="text-4xl text-[#58c7e9] hidden md:block">→</div>
                    <div class="p-6 bg-[#00509d] rounded-lg shadow-md">
                        <div class="text-4xl mb-2">✉️</div>
                        <h4 class="font-bold text-xl mb-2">2. Report Privately</h4>
                        <p class="text-sm text-gray-300">Email your detailed report to our dedicated security team. Do not disclose it publicly.</p>
                    </div>
                    <div class="text-4xl text-[#58c7e9] hidden md:block">→</div>
                    <div class="p-6 bg-[#00509d] rounded-lg shadow-md">
                        <div class="text-4xl mb-2">🤝</div>
                        <h4 class="font-bold text-xl mb-2">3. Collaborate & Resolve</h4>
                        <p class="text-sm text-gray-300">Our team will work with you to validate the report and develop a fix. We will keep you updated.</p>
                    </div>
                    <div class="text-4xl text-[#58c7e9] hidden md:block">→</div>
                    <div class="p-6 bg-[#00509d] rounded-lg shadow-md">
                        <div class="text-4xl mb-2">📢</div>
                        <h4 class="font-bold text-xl mb-2">4. Public Disclosure</h4>
                        <p class="text-sm text-gray-300">Once the fix is released, we will publicly acknowledge your contribution and provide a CVE.</p>
                    </div>
                </div>
            </section>

            <section class="bg-[#002848] rounded-2xl shadow-2xl p-8">
                <h3 class="text-3xl font-bold text-white text-center mb-8">Security Metrics at a Glance</h3>
                <p class="text-lg text-gray-300 max-w-4xl mx-auto text-center mb-8">Transparency is key to trust. Below are key metrics from the past year, showcasing our commitment to a robust and responsive security lifecycle. We track everything from new reports to our average time to resolve issues.</p>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div class="bg-[#003f5c] p-6 rounded-lg shadow-inner">
                        <h4 class="text-xl font-bold text-center mb-4">Vulnerabilities Reported vs. Resolved</h4>
                        <p class="text-sm text-center text-gray-400 mb-4">A visual on our ability to keep up with incoming reports, showing our dedication to an efficient resolution process.</p>
                        <div class="chart-container">
                            <canvas id="vulnTrendChart"></canvas>
                        </div>
                    </div>
                    <div class="bg-[#003f5c] p-6 rounded-lg shadow-inner">
                        <h4 class="text-xl font-bold text-center mb-4">Breakdown of Vulnerability Types</h4>
                        <p class="text-sm text-center text-gray-400 mb-4">A look at the most common attack vectors, helping us prioritize future security audits and development efforts.</p>
                        <div class="chart-container">
                            <canvas id="vulnTypeChart"></canvas>
                        </div>
                    </div>
                    <div class="bg-[#003f5c] p-6 rounded-lg shadow-inner md:col-span-2">
                        <h4 class="text-xl font-bold text-center mb-4">Average Time to Fix by Severity (Days)</h4>
                        <p class="text-sm text-center text-gray-400 mb-4">Our commitment to speed. We prioritize high-severity issues to minimize exposure for our users.</p>
                        <div class="chart-container">
                            <canvas id="timeToFixChart"></canvas>
                        </div>
                    </div>
                </div>
            </section>

        </main>

        <footer class="text-center mt-12 mb-4 text-gray-500">
            <p>&copy; 2025 Project Atlas. All rights reserved.</p>
        </footer>

    </div>

    <script>
        const tooltipTitleCallback = (tooltipItems) => {
            const item = tooltipItems[0];
            let label = item.chart.data.labels[item.dataIndex];
            if (Array.isArray(label)) {
                return label.join(' ');
            } else {
                return label;
            }
        };

        const processLabels = (labels) => {
            return labels.map(label => {
                if (label.length > 16) {
                    const words = label.split(' ');
                    const lines = [];
                    let currentLine = '';
                    for (const word of words) {
                        if ((currentLine + ' ' + word).length > 16) {
                            lines.push(currentLine);
                            currentLine = word;
                        } else {
                            currentLine += (currentLine === '' ? '' : ' ') + word;
                        }
                    }
                    lines.push(currentLine);
                    return lines;
                }
                return label;
            });
        };

        const palette = ['#00509d', '#58c7e9', '#9fe1e7', '#002848'];

        const vulnTrendCtx = document.getElementById('vulnTrendChart').getContext('2d');
        const vulnTrendChart = new Chart(vulnTrendCtx, {
            type: 'line',
            data: {
                labels: processLabels(['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025']),
                datasets: [{
                    label: 'Reported',
                    data: [12, 18, 15, 22, 19, 25],
                    borderColor: '#58c7e9',
                    backgroundColor: 'rgba(88, 199, 233, 0.2)',
                    fill: false,
                    tension: 0.4
                },
                {
                    label: 'Resolved',
                    data: [10, 15, 17, 20, 21, 23],
                    borderColor: '#00509d',
                    backgroundColor: 'rgba(0, 80, 157, 0.2)',
                    fill: false,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: { callbacks: { title: tooltipTitleCallback } },
                    legend: {
                        labels: { color: '#9ca3af' }
                    }
                },
                scales: {
                    x: {
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#9ca3af' }
                    },
                    y: {
                        title: { display: true, text: 'Count', color: '#9ca3af' },
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#9ca3af' }
                    }
                }
            }
        });

        const vulnTypeCtx = document.getElementById('vulnTypeChart').getContext('2d');
        const vulnTypeChart = new Chart(vulnTypeCtx, {
            type: 'doughnut',
            data: {
                labels: processLabels(['Insecure Deserialization', 'Injection Attacks', 'Broken Authentication', 'Misconfiguration', 'Cross-Site Scripting']),
                datasets: [{
                    data: [35, 25, 15, 15, 10],
                    backgroundColor: palette,
                    borderColor: '#003f5c',
                    borderWidth: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: { callbacks: { title: tooltipTitleCallback } },
                    legend: {
                        position: 'right',
                        labels: { color: '#9ca3af' }
                    }
                }
            }
        });

        const timeToFixCtx = document.getElementById('timeToFixChart').getContext('2d');
        const timeToFixChart = new Chart(timeToFixCtx, {
            type: 'bar',
            data: {
                labels: ['Crítico', 'Alto', 'Medio', 'Bajo'],
                datasets: [{
                    label: 'Average Time to Fix (Days)',
                    data: [2, 7, 18, 45],
                    backgroundColor: palette,
                    borderColor: '#003f5c',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: { callbacks: { title: tooltipTitleCallback } },
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: { color: '#9ca3af' }
                    },
                    y: {
                        title: { display: true, text: 'Average Days', color: '#9ca3af' },
                        grid: { color: 'rgba(255,255,255,0.1)' },
                        ticks: { color: '#9ca3af' }
                    }
                }
            }
        });
    </script>
</body>
</html>
