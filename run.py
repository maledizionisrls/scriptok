"""
Script di esecuzione e upload per Python Anywhere
"""
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

def check_file_status():
    """Verifica lo stato del file locale"""
    local_file = CONFIG['LOCAL_FILENAME']
    print(f"\nVerifica del file locale:")
    print(f"- Directory corrente: {os.getcwd()}")
    print(f"- Nome file cercato: {local_file}")
    
    files_in_dir = os.listdir()
    print("\nFile presenti nella directory:")
    for file in files_in_dir:
        print(f"- {file}")
    
    if os.path.exists(local_file):
        size = os.path.getsize(local_file)
        print(f"\nFile trovato! Dimensione: {size} bytes")
        return True
    else:
        print(f"\nFile non trovato!")
        return False

def upload_to_ftp(local_file):
    """
    Carica un file nella directory specificata del server FTP
    """
    print("\nTentativo di connessione FTP...")
    print(f"File da caricare: {local_file}")
    
    # Verifica prima se il file esiste
    if not os.path.exists(local_file):
        raise FileNotFoundError(f"File locale non trovato: {local_file}")
    
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
            print(f"Tentativo di caricamento di '{local_file}' come '{FTP_CONFIG['remote_filename']}'")
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {FTP_CONFIG["remote_filename"]}', f)
            
            # Verifica che il file sia stato caricato
            file_list = ftp.nlst()
            if FTP_CONFIG['remote_filename'] in file_list:
                print(f"File caricato con successo e verificato: {FTP_CONFIG['remote_filename']}")
                
                # Verifica dimensione del file
                file_size = ftp.size(FTP_CONFIG['remote_filename'])
                print(f"Dimensione file sul server: {file_size} bytes")
            else:
                print("ERRORE: Il file non risulta presente dopo il caricamento!")
                
    except Exception as e:
        print(f"Errore durante il caricamento FTP: {str(e)}")
        raise

async def run():
    try:
        # Esegui lo script principale
        print("Avvio dello script principale...")
        print(f"File configurati:")
        print(f"- File locale: {CONFIG['LOCAL_FILENAME']}")
        print(f"- File remoto: {CONFIG['REMOTE_FILENAME']}")
        
        await main()
        
        # Verifica lo stato del file
        if not check_file_status():
            raise FileNotFoundError(f"File non trovato dopo l'esecuzione dello script")
        
        # Carica il file su FTP
        print("\nInizio caricamento FTP...")
        upload_to_ftp(CONFIG['LOCAL_FILENAME'])
        
        print("\nOperazione completata con successo!")
        
    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")
        import traceback
        print("\nDettaglio dell'errore:")
        print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(run())
