"""
Generatore dei template HTML e dei file correlati
"""
import json
import os
from typing import List, Dict
from config import CONFIG

class HTMLGenerator:
    @staticmethod
    def get_trend_data_content():
        """Contenuto del file trend_data.js"""
        return '''// trend_data.js
class TrendAnalyzer {
    constructor() {
        // Verifica che i dati siano disponibili
        if (!window.videos || !Array.isArray(window.videos))
                .enter()
                .append('g');

            arcs.append('path')
                .attr('d', arc)
                .attr('fill', d => color(d.data.keyword))
                .attr('stroke', '#121212')
                .style('stroke-width', '2px')
                .style('opacity', 0.8)
                .transition()
                .duration(1000)
                .attrTween('d', function(d) {
                    const i = d3.interpolate(d.startAngle, d.endAngle);
                    return function(t) {
                        d.endAngle = i(t);
                        return arc(d);
                    }
                });

            const legend = d3.select(container)
                .append('div')
                .attr('class', 'legend');

            data.forEach((d, i) => {
                const legendItem = legend.append('div')
                    .attr('class', 'legend-item');

                legendItem.append('div')
                    .attr('class', 'legend-color')
                    .style('background-color', color(d.keyword));

                legendItem.append('span')
                    .text(`${d.keyword} (${d.percentage}%)`);
            });
        }

        function renderBarChart(data) {
            const container = document.getElementById('categoryChart');
            const width = container.clientWidth;
            const height = container.clientHeight;
            const margin = {top: 20, right: 20, bottom: 60, left: 60};

            container.innerHTML = '';

            const svg = d3.select(container)
                .append('svg')
                .attr('width', width)
                .attr('height', height);

            const x = d3.scaleBand()
                .domain(data.map(d => d.category))
                .range([margin.left, width - margin.right])
                .padding(0.1);

            const y = d3.scaleLinear()
                .domain([0, d3.max(data, d => d.avgViews)])
                .range([height - margin.bottom, margin.top]);

            svg.append('g')
                .attr('transform', `translate(0,${height - margin.bottom})`)
                .call(d3.axisBottom(x))
                .selectAll('text')
                .style('text-anchor', 'end')
                .attr('dx', '-.8em')
                .attr('dy', '.15em')
                .attr('transform', 'rotate(-45)')
                .style('fill', '#a0a0a0');

            svg.append('g')
                .attr('transform', `translate(${margin.left},0)`)
                .call(d3.axisLeft(y).ticks(5).tickFormat(d3.format('.2s')))
                .selectAll('text')
                .style('fill', '#a0a0a0');

            svg.selectAll('rect')
                .data(data)
                .enter()
                .append('rect')
                .attr('x', d => x(d.category))
                .attr('y', height - margin.bottom)
                .attr('width', x.bandwidth())
                .attr('height', 0)
                .attr('fill', (d, i) => i % 2 === 0 ? '#00f2ea' : '#ff0050')
                .transition()
                .duration(1000)
                .attr('y', d => y(d.avgViews))
                .attr('height', d => height - margin.bottom - y(d.avgViews));
        }

        function safeInitialize() {
            if (!checkD3() || !checkData()) {
                setTimeout(safeInitialize, 100);
                return;
            }

            try {
                window.videos = window.parent.videos;
                const analyzer = new window.TrendAnalyzer();
                const data = analyzer.getData();
                
                if (data.wordCloud && data.wordCloud.length > 0) {
                    renderWordCloud(data.wordCloud);
                } else {
                    document.getElementById('wordCloudError').style.display = 'block';
                }

                if (data.keywords && data.keywords.length > 0) {
                    renderPieChart(data.keywords);
                } else {
                    document.getElementById('keywordsError').style.display = 'block';
                }

                if (data.categories && data.categories.length > 0) {
                    renderBarChart(data.categories);
                } else {
                    document.getElementById('categoryError').style.display = 'block';
                }
            } catch (e) {
                console.error('Errore nell\'inizializzazione:', e);
            }
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', safeInitialize);
        } else {
            safeInitialize();
        }
    </script>
</body>
</html>'''

    @staticmethod
    def get_html_template(videos_data: List[Dict]) -> str:
        """Genera il template HTML principale"""
        # [Il resto del codice del template principale rimane uguale]
        
    @staticmethod
    def generate_all_files(videos_data: List[Dict], base_path: str):
        """Genera tutti i file necessari per il sistema"""
        # 1. Assicurati che la directory esista
        os.makedirs(base_path, exist_ok=True)
        
        # 2. Genera il file HTML principale
        main_file = os.path.join(base_path, CONFIG['LOCAL_FILENAME'])
        html_content = HTMLGenerator.get_html_template(videos_data)
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        # 3. Genera trend_data.js
        trend_data_file = os.path.join(base_path, 'trend_data.js')
        with open(trend_data_file, 'w', encoding='utf-8') as f:
            f.write(HTMLGenerator.get_trend_data_content())
            
        # 4. Genera trend.html
        trend_html_file = os.path.join(base_path, 'trend.html')
        with open(trend_html_file, 'w', encoding='utf-8') as f:
            f.write(HTMLGenerator.get_trend_html_content()) {
            console.error('Dati video non disponibili');
            this.videos = [];
            return;
        }
        this.videos = window.videos;
        this.processedData = this.processData();
    }

    processData() {
        if (!this.videos.length) {
            return {
                wordCloud: [],
                keywords: [],
                categories: []
            };
        }

        const wordWeights = {};
        const keywordCounts = {};
        const categoryStats = {};

        this.videos.forEach(video => {
            try {
                // Gestione sicura delle visualizzazioni
                const views = parseInt((video.views || '0').replace(/\\./g, '')) || 0;
                
                // Gestione keywords
                if (Array.isArray(video.keywords)) {
                    video.keywords.forEach(keyword => {
                        if (keyword && keyword !== 'N/A') {
                            if (!wordWeights[keyword]) wordWeights[keyword] = 0;
                            wordWeights[keyword] += views;
                            
                            if (!keywordCounts[keyword]) keywordCounts[keyword] = 0;
                            keywordCounts[keyword]++;
                        }
                    });
                }

                // Gestione categorie
                if (Array.isArray(video.categories)) {
                    video.categories.forEach(category => {
                        if (category && category !== 'N/A') {
                            if (!categoryStats[category]) {
                                categoryStats[category] = {
                                    totalViews: 0,
                                    count: 0
                                };
                            }
                            categoryStats[category].totalViews += views;
                            categoryStats[category].count++;
                        }
                    });
                }
            } catch (e) {
                console.error('Errore nel processamento del video:', e);
            }
        });

        return {
            wordCloud: this.prepareWordCloudData(wordWeights),
            keywords: this.prepareKeywordsData(keywordCounts),
            categories: this.prepareCategoriesData(categoryStats)
        };
    }

    prepareWordCloudData(weights) {
        try {
            return Object.entries(weights)
                .map(([text, value]) => ({
                    text,
                    size: this.calculateFontSize(value, Object.values(weights)),
                    weight: value
                }))
                .sort((a, b) => b.weight - a.weight)
                .slice(0, 40);
        } catch (e) {
            console.error('Errore nella preparazione word cloud:', e);
            return [];
        }
    }

    calculateFontSize(value, allValues) {
        try {
            const max = Math.max(...allValues);
            const min = Math.min(...allValues);
            const range = max - min;
            if (range === 0) return 24;
            const normalized = (value - min) / range;
            return Math.floor(12 + normalized * 36);
        } catch (e) {
            return 24;
        }
    }

    prepareKeywordsData(counts) {
        try {
            const total = Object.values(counts).reduce((sum, count) => sum + count, 0);
            if (total === 0) return [];

            return Object.entries(counts)
                .map(([keyword, count]) => ({
                    keyword,
                    count,
                    percentage: ((count / total) * 100).toFixed(1)
                }))
                .sort((a, b) => b.count - a.count)
                .slice(0, 10);
        } catch (e) {
            console.error('Errore nella preparazione keywords:', e);
            return [];
        }
    }

    prepareCategoriesData(stats) {
        try {
            return Object.entries(stats)
                .map(([category, data]) => ({
                    category,
                    avgViews: Math.round(data.totalViews / data.count),
                    totalVideos: data.count
                }))
                .sort((a, b) => b.avgViews - a.avgViews)
                .slice(0, 8);
        } catch (e) {
            console.error('Errore nella preparazione categorie:', e);
            return [];
        }
    }

    getData() {
        return this.processedData;
    }

    static formatNumber(num) {
        try {
            return new Intl.NumberFormat('it-IT').format(num);
        } catch (e) {
            return num.toString();
        }
    }
}

window.TrendAnalyzer = TrendAnalyzer;'''

    @staticmethod
    def get_trend_html_content():
        """Contenuto del file trend.html"""
        return '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analisi Trend</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script defer src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
    <script defer src="trend_data.js"></script>
    <style>
        :root {
            --primary: #00f2ea;
            --secondary: #ff0050;
            --bg-dark: #121212;
            --card-bg: #1e1e1e;
            --text: #ffffff;
            --text-secondary: #a0a0a0;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body {
            background: rgba(0, 0, 0, 0.8);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .modal-content {
            background: var(--bg-dark);
            width: 100%;
            max-width: 1200px;
            border-radius: 20px;
            padding: 30px;
            position: relative;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }

        .close-button {
            position: absolute;
            top: 20px;
            right: 20px;
            background: none;
            border: none;
            color: var(--text);
            font-size: 28px;
            cursor: pointer;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
        }

        .close-button:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: rotate(90deg);
        }

        .title {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 30px;
            text-align: center;
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .charts-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 24px;
            margin-bottom: 24px;
        }

        .chart-card {
            background: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .chart-title {
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 20px;
            text-align: center;
            color: var(--text-secondary);
        }

        .word-cloud {
            height: 300px;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 20px;
            overflow: hidden;
        }

        .word-cloud span {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            transition: all 0.3s ease;
            cursor: default;
        }

        .word-cloud span:hover {
            transform: scale(1.1);
            filter: brightness(1.2);
        }

        .pie-chart, .bar-chart {
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .legend {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 15px;
            justify-content: center;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 12px;
            color: var(--text-secondary);
            background: rgba(255, 255, 255, 0.05);
            padding: 4px 8px;
            border-radius: 4px;
        }

        .legend-color {
            width: 12px;
            height: 12px;
            border-radius: 3px;
        }

        .error-message {
            text-align: center;
            color: var(--text-secondary);
            padding: 20px;
            font-size: 14px;
            background: rgba(255, 0, 0, 0.1);
            border-radius: 8px;
            margin-top: 10px;
        }

        @media (max-width: 768px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }

            .modal-content {
                padding: 20px;
                margin: 10px;
            }

            .chart-card {
                padding: 15px;
            }

            .title {
                font-size: 20px;
            }

            .chart-title {
                font-size: 16px;
            }
        }
    </style>
</head>
<body>
    <div class="modal-content">
        <button class="close-button" onclick="closeModal()">&times;</button>
        <h1 class="title">Analisi dei Trend</h1>
        
        <div class="charts-grid">
            <div class="chart-card">
                <h2 class="chart-title">Parole più utilizzate per visualizzazioni</h2>
                <div id="wordCloud" class="word-cloud"></div>
                <div id="wordCloudError" class="error-message" style="display: none;">
                    Dati insufficienti per la nuvola di parole
                </div>
            </div>
            
            <div class="chart-card">
                <h2 class="chart-title">Distribuzione Parole Chiave</h2>
                <div id="keywordsPie" class="pie-chart"></div>
                <div id="keywordsError" class="error-message" style="display: none;">
                    Dati insufficienti per il grafico a torta
                </div>
            </div>

            <div class="chart-card" style="grid-column: span 2;">
                <h2 class="chart-title">Media Visualizzazioni per Categoria</h2>
                <div id="categoryChart" class="bar-chart"></div>
                <div id="categoryError" class="error-message" style="display: none;">
                    Dati insufficienti per il grafico a barre
                </div>
            </div>
        </div>
    </div>

    <script>
        function checkD3() {
            if (typeof d3 === 'undefined') {
                console.error('D3.js non caricato');
                return false;
            }
            return true;
        }

        function checkData() {
            if (typeof window.TrendAnalyzer === 'undefined') {
                console.error('TrendAnalyzer non caricato');
                return false;
            }
            if (!window.parent.videos || !Array.isArray(window.parent.videos)) {
                console.error('Dati video non disponibili');
                return false;
            }
            return true;
        }

        function closeModal() {
            try {
                window.parent.postMessage('closeModal', '*');
            } catch (e) {
                console.error('Errore nella chiusura della modale:', e);
                window.close();
            }
        }

        function renderWordCloud(data) {
            const container = document.getElementById('wordCloud');
            container.innerHTML = '';

            data.forEach(word => {
                const span = document.createElement('span');
                span.textContent = word.text;
                span.style.fontSize = `${word.size}px`;
                const hue = Math.random() < 0.5 ? '183' : '341';
                const saturation = 70 + Math.random() * 20;
                const lightness = 50 + Math.random() * 20;
                span.style.color = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
                container.appendChild(span);
            });
        }

        function renderPieChart(data) {
            const container = document.getElementById('keywordsPie');
            const width = container.clientWidth;
            const height = container.clientHeight;
            const radius = Math.min(width, height) / 2.5;

            container.innerHTML = '';

            const svg = d3.select(container)
                .append('svg')
                .attr('width', width)
                .attr('height', height)
                .append('g')
                .attr('transform', `translate(${width/2},${height/2})`);

            const color = d3.scaleOrdinal()
                .domain(data.map(d => d.keyword))
                .range(['#00f2ea', '#ff0050', '#00b4d8', '#f72585', '#7209b7', '#3a0ca3', '#4361ee', '#4cc9f0']);

            const pie = d3.pie()
                .value(d => d.count)
                .sort(null);

            const arc = d3.arc()
                .innerRadius(radius * 0.5)
                .outerRadius(radius * 0.8);

            const arcs = svg.selectAll('arc')
                .data(pie(data
