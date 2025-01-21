"""
Script di esecuzione e upload per GitHub Actions
"""
import asyncio
import os
from ftplib import FTP
from main import main

# Configurazione FTP dalle variabili d'ambiente
FTP_CONFIG = {
    'host': os.getenv('FTP_HOST', 'notizia.info'),
    'user': os.getenv('FTP_USER', 'scriptok@notizia.info'),
    'password': os.getenv('FTP_PASS', 'scriptok2025##'),
    'path': '/public_html',
    'remote_filename': 'tiktok_trending.html'
}

def upload_to_ftp(local_file):
    """
    Carica un file nella directory specificata del server FTP
    """
    print("\nTentativo di connessione FTP...")
    try:
        with FTP(FTP_CONFIG['host']) as ftp:
            # Connessione e login
            ftp.login(user=FTP_CONFIG['user'], passwd=FTP_CONFIG['password'])
            print("Connessione FTP stabilita e login effettuato!")
            
            # Cambia directory
            ftp.cwd(FTP_CONFIG['path'])
            print(f"Directory cambiata in: {FTP_CONFIG['path']}")
            
            # Prova a eliminare il file esistente se presente
            try:
                ftp.delete(FTP_CONFIG['remote_filename'])
                print("File esistente eliminato con successo!")
            except:
                print("Nessun file esistente da eliminare o errore durante l'eliminazione")
            
            # Carica il nuovo file
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {FTP_CONFIG["remote_filename"]}', f)
            
            print(f"File caricato con successo: {FTP_CONFIG['remote_filename']}")
                
    except Exception as e:
        print(f"Errore durante il caricamento FTP: {str(e)}")
        raise

async def run():
    try:
        # Esegui lo script principale
        print("Avvio dello script principale...")
        await main()
        
        # Carica il file su FTP
        local_file = 'tiktok_trending.html'
        print("\nInizio caricamento FTP...")
        upload_to_ftp(local_file)
        
        print("\nOperazione completata con successo!")
        
    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")
        raise  # Importante: rilancia l'errore per far fallire l'action

if __name__ == "__main__":
    asyncio.run(run())
