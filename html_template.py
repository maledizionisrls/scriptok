import json
from typing import List, Dict
from config import CONFIG  # Importa la configurazione dal file config.py

class HTMLGenerator:
    @staticmethod
    def get_html_template(videos_data: List[Dict]) -> str:
        html_start = '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScripTok</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; }
        body { 
            font-family: 'Inter', sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: #121212; 
            color: white;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px; 
            padding: 20px;
        }
        .video-card { 
            background: #1e1e1e; 
            border-radius: 12px; 
            padding: 20px; 
            margin-bottom: 20px; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s ease;
        }
        .video-card:hover {
            transform: translateY(-5px);
        }
        .video-title { 
            font-size: 16px; 
            font-weight: 600; 
            margin-bottom: 10px;
            color: #ffffff;
        }
        .video-stats { 
            margin-bottom: 15px; 
            font-size: 14px;
            color: #a0a0a0;
        }
        .video-url {
            font-size: 13px;
            word-break: break-all;
            margin-bottom: 10px;
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }
        .video-url a {
            color: #00f2ea;
            text-decoration: none;
        }
        .video-url a:hover {
            text-decoration: underline;
            color: #ff0050;
        }
        .video-container {
            width: 100%;
            position: relative;
            margin-bottom: 15px;
        }
        .video-embed {
            position: relative;
            padding-bottom: 177.77%;
            height: 0;
            overflow: hidden;
            border-radius: 8px;
            background: #000;
        }
        .video-embed iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
        .tag { 
            display: inline-block; 
            background: rgba(0,242,234,0.1); 
            padding: 4px 8px; 
            border-radius: 12px; 
            margin: 2px; 
            font-size: 12px;
            color: #00f2ea;
            transition: all 0.2s ease;
        }
        .tag:hover {
            background: rgba(0,242,234,0.2);
            transform: scale(1.05);
        }
        .header { 
            text-align: center; 
            padding: 40px 20px; 
            margin-bottom: 20px;
            background: #1e1e1e;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            position: relative;
        }
        .header h1 {
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 12px;
            background: linear-gradient(45deg, #00f2ea, #ff0050);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header p {
            color: #a0a0a0;
            font-size: 18px;
        }
        .trend-button {
            margin-top: 20px;
            padding: 12px 24px;
            background: linear-gradient(45deg, #00f2ea, #ff0050);
            border: none;
            border-radius: 25px;
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 16px;
        }
        .trend-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,242,234,0.2);
        }
        .pagination {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin: 20px 0;
        }
        .pagination button {
            padding: 12px 24px;
            border: none;
            background: #1e1e1e;
            color: white;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s ease;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .pagination button:not(:disabled):hover {
            background: #2d2d2d;
            transform: translateY(-2px);
        }
        .pagination button:disabled {
            background: rgba(255,255,255,0.1);
            cursor: not-allowed;
            opacity: 0.5;
        }
        .pagination-info {
            text-align: center;
            margin: 10px 0;
            color: #a0a0a0;
        }
        .modal-frame {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
            z-index: 1000;
        }
        @media (max-width: 768px) {
            .grid { grid-template-columns: 1fr; }
            body { padding: 10px; }
            .header h1 { font-size: 36px; }
            .header p { font-size: 16px; }
        }
        @media (min-width: 769px) and (max-width: 1200px) {
            .grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (min-width: 1201px) {
            .grid { grid-template-columns: repeat(3, 1fr); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>ScripTok</h1>
            <p>I video più popolari in Italia</p>
            <button id="trendButton" class="trend-button">Analisi dei Trend</button>
        </div>
        <div class="pagination"></div>
        <div class="pagination-info"></div>
        <div class="grid" id="videos-container"></div>
        <div class="pagination"></div>
    </div>

    <!-- Frame per la modale -->
    <iframe id="trendFrame" class="modal-frame" src="about:blank"></iframe>

    <script>'''

        videos_json = json.dumps([{
            'id': video['url'].split('/')[-1],
            'title': video['titolo'],
            'creator': video['creator'],
            'views': video['views'],
            'url': video['url'],
            'categories': [cat for cat in video['categorie'].split(', ') if cat != 'N/A'],
            'keywords': [kw for kw in video['keywords'].split(', ') if kw != 'N/A']
        } for video in videos_data])

        html_middle = f'''
        // Configurazione
        const VIDEOS_PER_PAGE = {CONFIG['VIDEOS_PER_PAGE']};
        const videos = {videos_json};

        // Stato corrente
        let currentPage = 1;
        const totalPages = Math.ceil(videos.length / VIDEOS_PER_PAGE);

        // Gestione modale trend
        const trendButton = document.getElementById('trendButton');
        const trendFrame = document.getElementById('trendFrame');

        trendButton.addEventListener('click', () => {
            trendFrame.src = 'trend.html';
            trendFrame.style.display = 'block';
            document.body.style.overflow = 'hidden';
        });

        // Gestione chiusura modale
        window.addEventListener('message', (event) => {
            if (event.data === 'closeModal') {
                trendFrame.style.display = 'none';
                trendFrame.src = 'about:blank';
                document.body.style.overflow = 'auto';
            }
        });

        // Gestione Intersection Observer per lazy loading
        const videoObserver = new IntersectionObserver((entries, observer) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    const container = entry.target;
                    const iframe = container.querySelector('iframe');
                    if (iframe.dataset.src) {{
                        iframe.src = iframe.dataset.src;
                        iframe.removeAttribute('data-src');
                        observer.unobserve(container);
                    }}
                }}
            }});
        }}, {{
            rootMargin: '50px 0px',
            threshold: 0.1
        }});

        function createVideoCard(video) {{
            const categories = video.categories.map(cat => 
                `<span class="tag">${{cat}}</span>`).join(' ') || 'Nessuna categoria';
            const keywords = video.keywords.map(kw => 
                `<span class="tag">${{kw}}</span>`).join(' ') || 'Nessuna parola chiave';
            
            const card = document.createElement('div');
            card.className = 'video-card';
            card.innerHTML = `
                <div class="video-title">${{video.title}}</div>
                <div class="video-stats">
                    <strong>Creator:</strong> ${{video.creator}}<br>
                    <strong>Views:</strong> ${{video.views}}
                </div>
                <div class="video-url">
                    <strong>URL:</strong> <a href="${{video.url}}" target="_blank">${{video.url}}</a>
                </div>
                <div class="video-container">
                    <div class="video-embed">
                        <iframe data-src="https://www.tiktok.com/embed/${{video.id}}" 
                                allowfullscreen scrolling="no" 
                                allow="encrypted-media;">
                        </iframe>
                    </div>
                </div>
                <div class="metadata">
                    <strong>Categorie:</strong><br>
                    ${{categories}}
                </div>
                <div class="metadata" style="margin-top: 10px;">
                    <strong>Keywords:</strong><br>
                    ${{keywords}}
                </div>
            `;
            return card;
        }}

        function updatePagination() {{
            const paginationElements = document.querySelectorAll('.pagination');
            const paginationHTML = `
                <button onclick="changePage(1)" ${{currentPage === 1 ? 'disabled' : ''}}">Prima</button>
                <button onclick="changePage(${{currentPage - 1}})" ${{currentPage === 1 ? 'disabled' : ''}}">Precedente</button>
                <button onclick="changePage(${{currentPage + 1}})" ${{currentPage === totalPages ? 'disabled' : ''}}">Successiva</button>
                <button onclick="changePage(${{totalPages}})" ${{currentPage === totalPages ? 'disabled' : ''}}">Ultima</button>
            `;
            paginationElements.forEach(el => el.innerHTML = paginationHTML);
            
            document.querySelector('.pagination-info').textContent = 
                `Pagina ${{currentPage}} di ${{totalPages}} (${{videos.length}} video totali)`;
        }}

        function changePage(newPage) {{
            if (newPage < 1 || newPage > totalPages) return;
            currentPage = newPage;
            displayCurrentPage();
            updatePagination();
            window.scrollTo({{
                top: 0,
                behavior: 'smooth'
            }});
        }}

        function displayCurrentPage() {{
            const container = document.getElementById('videos-container');
            container.innerHTML = '';
            
            const start = (currentPage - 1) * VIDEOS_PER_PAGE;
            const end = start + VIDEOS_PER_PAGE;
            const pageVideos = videos.slice(start, end);
            
            pageVideos.forEach(video => {{
                const card = createVideoCard(video);
                container.appendChild(card);
                videoObserver.observe(card.querySelector('.video-container'));
            }});
        }}

        // Inizializzazione
        displayCurrentPage();
        updatePagination();
    </script>
</body>
</html>'''

        return html_start + html_middle

    @staticmethod
    def generate_html_file(videos_data: List[Dict], output_filename: str):
        """Genera il file HTML con i video"""
        html_content = HTMLGenerator.get_html_template(videos_data)
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
