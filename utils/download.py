from googleapiclient.http import MediaIoBaseDownload
import io

def download_file(file_id, service):
    """Télécharge un fichier depuis Google Drive."""
    
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO('downloaded_file.pdf', 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
