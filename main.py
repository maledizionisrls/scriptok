async def main(pages: int = None, num_videos: int = None):
    """
    Funzione principale che coordina il processo di scraping
    """
    # [tutto il codice esistente rimane uguale fino alla generazione HTML]

        # Genera il file HTML con il nome specificato in LOCAL_FILENAME
        HTMLGenerator.generate_html_file(videos_data, CONFIG['LOCAL_FILENAME'])
        
        # Genera i file necessari per l'analisi dei trend
        output_dir = os.path.dirname(CONFIG['LOCAL_FILENAME'])
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 1. trend_data.js - Processore dati
        trend_data = '''// trend_data.js
class TrendAnalyzer {
    constructor() {
        if (typeof window === 'undefined' || !window.videos) {
            throw new Error('Dati non disponibili');
        }
        this.videos = window.videos;
        this.processedData = this.processData();
    }
    // ... [resto del codice trend_data.js]
}
window.TrendAnalyzer = TrendAnalyzer;'''

        # 2. trend.html - Interfaccia analisi
        trend_html = '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Analisi Trend</title>
    <!-- ... [resto del codice trend.html] -->
</head>
<body>
    <!-- ... -->
</body>
</html>'''

        # Scrivi i file nella stessa directory del file principale
        base_path = os.path.dirname(CONFIG['LOCAL_FILENAME'])
        with open(os.path.join(base_path, 'trend_data.js'), 'w', encoding='utf-8') as f:
            f.write(trend_data)
        with open(os.path.join(base_path, 'trend.html'), 'w', encoding='utf-8') as f:
            f.write(trend_html)

        if os.path.exists(CONFIG['LOCAL_FILENAME']):
            print(f"\nFile HTML generato con successo: {CONFIG['LOCAL_FILENAME']}")
            print("File di analisi trend generati con successo")
            print(f"Dimensione file: {os.path.getsize(CONFIG['LOCAL_FILENAME'])} bytes")
        else:
            print(f"\nERRORE: Il file {CONFIG['LOCAL_FILENAME']} non è stato creato!")
