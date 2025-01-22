async def main(pages: int = None, num_videos: int = None):
    """
    Funzione principale che coordina il processo di scraping
    """
    # Inizializza lo scraper
    scraper = TikTokScraper()
    
    # Usa i valori passati o quelli di default da CONFIG
    pages_to_analyze = min(27, pages if pages is not None else CONFIG['PAGES_TO_ANALYZE'])
    output_videos = num_videos if num_videos is not None else CONFIG['OUTPUT_VIDEOS']
    
    # [... tutto il codice dello scraping rimane uguale fino alla generazione dei file ...]

    if all_videos:
        # [... tutto il codice dell'analisi dei video rimane uguale ...]
        
        # Assicurati che la directory esista
        output_dir = os.path.dirname(CONFIG['LOCAL_FILENAME'])
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Genera tutti i file necessari
        HTMLGenerator.generate_all_files(videos_data, output_dir or '.')
        
        if os.path.exists(CONFIG['LOCAL_FILENAME']):
            print(f"\nFile HTML generato con successo: {CONFIG['LOCAL_FILENAME']}")
            print("File di analisi trend generati con successo")
            print(f"Dimensione file: {os.path.getsize(CONFIG['LOCAL_FILENAME'])} bytes")
        else:
            print(f"\nERRORE: Il file {CONFIG['LOCAL_FILENAME']} non è stato creato!")
        
        print(f"Analizzate {pages_to_analyze} pagine, trovati {total_videos} video totali, generato output con i {output_videos} più recenti.")
