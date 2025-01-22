import asyncio
import os
from ftplib import FTP
from main import main
from config import CONFIG

# Configurazione FTP
FTP_CONFIG = {
    'host': 'notizia.info',
    'user': 'scriptok@notizia.info',
    'password': 'scriptok2025##',
    'path': '/public_html',
    'remote_filename': CONFIG['REMOTE_FILENAME'],
}

def check_local_file(filename):
    """
    Verifica l'esistenza e lo stato del file locale
    """
    print(f"\nVerifica del file locale '{filename}':")
    print(f"Directory corrente: {os.getcwd()}")
    
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        print(f"File trovato! Dimensione: {size} bytes")
        return True
    else:
        print(f"File non trovato in {os.getcwd()}")
        # Lista i file nella directory corrente
        print("File presenti nella directory:")
        for file in os.listdir():
            print(f"- {file}")
        return False

async def run():
    try:
        # Esegui lo script principale
        print("Avvio dello script principale...")
        await main()
        
        # Verifica che il file sia stato creato
        local_file = CONFIG['LOCAL_FILENAME']
        print("\nControllo il file creato...")
        
        if not check_local_file(local_file):
            raise FileNotFoundError(f"File non trovato: {local_file}")
        
        print("\nInizio caricamento FTP...")
        upload_to_ftp(local_file)
        
        print("\nOperazione completata con successo!")
        
    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")
        # Stampa ulteriori informazioni sull'errore
        import traceback
        print("\nDettaglio dell'errore:")
        print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(run())
