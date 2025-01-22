import json
from typing import List, Dict
from config import CONFIG

class HTMLGenerator:
    @staticmethod
    def get_html_template(videos_data: List[Dict]) -> str:
        html_start = '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScripTok</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/react@17/umd/react.production.min.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@17/umd/react-dom.production.min.js" crossorigin></script>
    <script src="https://unpkg.com/recharts/umd/Recharts.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/lodash@4.17.21/lodash.min.js"></script>
    <script src="analytics-component.js"></script>
    <style>
        * { 
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        :root {
            --primary: #00f2ea;
            --secondary: #ff0050;
            --bg-dark: #121212;
            --card-bg: #1e1e1e;
            --text: #ffffff;
            --text-secondary: #a0a0a0;
            --card-hover: #2d2d2d;
        }

        body { 
            font-family: 'Inter', sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }

        .container { 
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .grid { 
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 24px;
            padding: 20px 0;
        }

        .video-card { 
            background: var(--card-bg);
            border-radius: 16px;
            padding: 20px;
            transition: transform 0.2s ease, background-color 0.2s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .video-card:hover {
            transform: translateY(-5px);
            background: var(--card-hover);
        }

        .video-title { 
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            line-height: 1.4;
            color: var(--text);
        }

        .video-stats {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            color: var(--text-secondary);
            font-size: 14px;
        }

        .video-url {
            font-size: 14px;
            word-break: break-all;
            margin-bottom: 16px;
            padding: 12px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }

        .video-url a {
            color: var(--primary);
            text-decoration: none;
            transition: color 0.2s ease;
        }

        .video-url a:hover {
            color: var(--secondary);
        }

        .video-container {
            margin-bottom: 20px;
            border-radius: 12px;
            overflow: hidden;
            background: var(--bg-dark);
        }

        .video-embed {
            position: relative;
            padding-bottom: 177.77%;
            height: 0;
            overflow: hidden;
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
            background: rgba(0, 242, 234, 0.1);
            color: var(--primary);
            padding: 6px 12px;
            border-radius: 20px;
            margin: 4px;
            font-size: 12px;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        .tag:hover {
            background: rgba(0, 242, 234, 0.2);
            transform: scale(1.05);
        }

        .header { 
            text-align: center;
            padding: 40px 20px;
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, var(--card-bg) 0%, var(--bg-dark) 100%);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .header h1 {
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 12px;
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header p {
            color: var(--text-secondary);
            font-size: 18px;
        }

        .analytics-button {
            display: block;
            margin: 20px auto 0;
            padding: 12px 24px;
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            border: none;
            border-radius: 25px;
            color: var(--text);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 16px;
        }

        .analytics-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 242, 234, 0.2);
        }

        .pagination {
            display: flex;
            justify-content: center;
            gap: 12px;
            margin: 32px 0;
        }

        .pagination button {
            padding: 12px 24px;
            border: none;
            background: var(--card-bg);
            color: var(--text);
            border-radius: 12px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 16px;
        }

        .pagination button:not(:disabled):hover {
            background: var(--card-hover);
            transform: translateY(-2px);
        }

        .pagination button:disabled {
            background: rgba(255, 255, 255, 0.1);
            cursor: not-allowed;
            opacity: 0.5;
        }

        .pagination-info {
            text-align: center;
            margin: 20px 0;
            color: var(--text-secondary);
            font-size: 14px;
        }

        .metadata {
            margin-top: 16px;
            padding: 16px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
        }

        .metadata strong {
            display: block;
            margin-bottom: 8px;
            color: var(--text-secondary);
        }

        .hidden {
            display: none !important;
        }

        /* Stili per la modale */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.75);
            z-index: 999;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .modal-content {
            background-color: var(--card-bg);
            padding: 30px;
            border-radius: 16px;
            width: 90%;
            max-width: 1200px;
            max-height: 90vh;
            overflow-y: auto;
            position: relative;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }

        .modal-close {
            position: absolute;
            top: 20px;
            right: 20px;
            background: none;
            border: none;
            color: var(--text);
            font-size: 24px;
            cursor: pointer;
            padding: 5px;
            z-index: 1001;
        }

        .analytics-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1000;
            display: none;
        }

        .analytics-container.visible {
            display: block;
        }

        @media (max-width: 768px) {
            .grid { 
                grid-template-columns: 1fr;
                padding: 10px;
            }
            .header h1 {
                font-size: 36px;
            }
            .header p {
                font-size: 16px;
            }
            .container {
                padding: 10px;
            }
            .modal-content {
                padding: 15px;
                width: 95%;
            }
        }
        
        @media (min-width: 769px) and (max-width: 1200px) {
            .grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>ScripTok</h1>
            <p>I video più popolari in Italia</p>
            <button onclick="toggleAnalytics()" class="analytics-button">
                Analisi dei Trend
            </button>
        </div>
        <div id="analytics-container" class="analytics-container">
            <div class="modal-overlay" onclick="closeAnalytics(event)">
                <div class="modal-content" onclick="event.stopPropagation()">
                    <button class="modal-close" onclick="closeAnalytics(event)">×</button>
                    <div id="analytics-root"></div>
                </div>
            </div>
        </div>
        <div class="pagination"></div>
        <div class="pagination-info"></div>
        <div class="grid" id="videos-container">
        </div>
        <div class="pagination"></div>
    </div>
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
        const VIDEOS_PER_PAGE = {CONFIG['VIDEOS_PER_PAGE']};
        const videos = {videos_json};

        let currentPage = 1;
        const totalPages = Math.ceil(videos.length / VIDEOS_PER_PAGE);

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
                `Pagina ${currentPage} di ${totalPages} (${videos.length} video totali)`;
        }

        function toggleAnalytics() {
            try {
                console.log("Apertura analytics");
                const analyticsContainer = document.getElementById('analytics-container');
                const analyticsRoot = document.getElementById('analytics-root');
                
                if (!analyticsRoot.hasChildNodes()) {
                    if (typeof TrendAnalytics === 'undefined') {
                        console.error('Componente TrendAnalytics non trovato');
                        alert('Errore nel caricamento del componente di analisi');
                        return;
                    }
                    
                    ReactDOM.render(
                        React.createElement(TrendAnalytics, { 
                            videos: videos 
                        }),
                        analyticsRoot
                    );
                }
                analyticsContainer.classList.add('visible');
                document.body.style.overflow = 'hidden';
            } catch (error) {
                console.error("Errore nell'apertura degli analytics:", error);
                alert('Si è verificato un errore. Controlla la console per i dettagli.');
            }
        }

        function closeAnalytics(event) {
            event.preventDefault();
            const analyticsContainer = document.getElementById('analytics-container');
            analyticsContainer.classList.remove('visible');
            document.body.style.overflow = 'auto';
        }

        function changePage(newPage) {
            if (newPage < 1 || newPage > totalPages) return;
            currentPage = newPage;
            displayCurrentPage();
            updatePagination();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }

        function displayCurrentPage() {
            const container = document.getElementById('videos-container');
            container.innerHTML = '';
            
            const start = (currentPage - 1) * VIDEOS_PER_PAGE;
            const end = start + VIDEOS_PER_PAGE;
            const pageVideos = videos.slice(start, end);
            
            pageVideos.forEach(video => {
                const card = createVideoCard(video);
                container.appendChild(card);
                videoObserver.observe(card.querySelector('.video-container'));
            });
        }

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
            f.write(html_content)<span class="tag">${{cat}}</span>`).join(' ') || 'Nessuna categoria';
            const keywords = video.keywords.map(kw => 
                `<span class="tag">${{kw}}</span>`).join(' ') || 'Nessuna parola chiave';
            
            const card = document.createElement('div');
            card.className = 'video-card';
            card.innerHTML = `
                <div class="video-title">${{video.title}}</div>
                <div class="video-stats">
                    <span><strong>Creator:</strong> ${{video.creator}}</span>
                    <span><strong>Views:</strong> ${{video.views}}</span>
                </div>
                <div class="video-url">
                    <a href="${{video.url}}" target="_blank">${{video.url}}</a>
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
                    <strong>Categorie:</strong>
                    ${{categories}}
                </div>
                <div class="metadata" style="margin-top: 16px;">
                    <strong>Keywords:</strong>
                    ${{keywords}}
                </div>
            `;
            return card;
        }}

        function updatePagination() {{
            const paginationElements = document.querySelectorAll('.pagination');
            const paginationHTML = `
                <button onclick="changePage(1)" ${{currentPage === 1 ? 'disabled' : ''}}>⏮️</button>
                <button onclick="changePage(${{currentPage - 1}})" ${{currentPage === 1 ? 'disabled' : ''}}>⬅️</button>
                <button onclick="changePage(${{currentPage + 1}})" ${{currentPage === totalPages ? 'disabled' : ''}}>➡️</button>
                <button onclick="changePage(${{totalPages}})" ${{currentPage === totalPages ? 'disabled' : ''}}>⏭️</button>
            `;
            paginationElements.forEach(el => el.innerHTML = paginationHTML);
            
            document.querySelector('.pagination-info').textContent = 
                `Pagina ${{currentPage}} di ${{totalPages}} (${{videos.length}} video totali)`;
        }}

        function toggleAnalytics() {
    try {
        console.log("Apertura analytics con i dati:", videos);
        const analyticsRoot = document.getElementById('analytics-root');
        
        if (!analyticsRoot.hasChildNodes()) {
            if (typeof TrendAnalytics === 'undefined') {
                console.error('Componente TrendAnalytics non trovato');
                alert('Errore nel caricamento del componente di analisi');
                return;
            }
            
            ReactDOM.render(
                React.createElement(TrendAnalytics, { 
                    videos: videos,
                    onClose: () => {
                        analyticsRoot.classList.add('hidden');
                    }
                }),
                analyticsRoot
            );
        }
        analyticsRoot.classList.remove('hidden');
    } catch (error) {
        console.error("Errore nell'apertura degli analytics:", error);
        alert('Si è verificato un errore. Controlla la console per i dettagli.');
    }
}

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
