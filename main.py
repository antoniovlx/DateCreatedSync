import subprocess
import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from video import get_creation_time
import magic
from pytz import timezone


def change_file(f):
        # printing the human readable type of the file 
        print(magic.from_file(f)) 
  
        # printing the mime type of the file 
        print(magic.from_file(f, mime = True))

        fecha_de_captura = None

        if magic.from_file(f, mime = True) in ['video/mp4', 'application/octet-stream'] :
            fecha_de_captura = get_creation_time(f)
            if fecha_de_captura:
                print(f"Fecha de Captura: {fecha_de_captura}")
                fecha_de_captura = datetime.strptime(fecha_de_captura[:-8], "%Y-%m-%dT%H:%M:%S")
                fecha_de_captura = fecha_de_captura.replace(tzinfo=timezone('UTC'))

                fecha_de_captura = fecha_de_captura.astimezone(timezone('Europe/Madrid'))
            else:
                print("La fecha de captura no está disponible en los metadatos EXIF.")
            
        if magic.from_file(f, mime = True) in ['image/jpeg', 'image/png']:
            # Abrir la imagen
            imagen = Image.open(f)

            # Obtener los metadatos EXIF
            exif_data = imagen._getexif()

            # Buscar el valor EXIF correspondiente a la fecha de captura
            for tag, valor in exif_data.items():
                if TAGS.get(tag) == 'DateTimeOriginal':
                    fecha_de_captura = valor
                    if fecha_de_captura:
                        print(f"Fecha de Captura: {fecha_de_captura}")
                        fecha_de_captura = datetime.strptime(fecha_de_captura, "%Y:%m:%d %H:%M:%S")
                    else:
                        print("La fecha de captura no está disponible en los metadatos EXIF.")
                    break

        if fecha_de_captura:
            # Ejecutar el comando de PowerShell y capturar la salida
            fecha_de_captura = fecha_de_captura.strftime('%d %B %Y %H:%M:%S')
            comando_powershell = f'(Get-Item {f}).CreationTime=("{fecha_de_captura}")'
            creation_time = subprocess.check_output(['powershell', comando_powershell], shell=True, text=True)

            comando_powershell = f'(Get-Item {f}).LastWriteTime=("{fecha_de_captura}")'
            creation_time = subprocess.check_output(['powershell', comando_powershell], shell=True, text=True)

            # Imprimir la salida
            print(creation_time)

        else:
            print("La fecha de captura no está disponible en los metadatos EXIF.")

# Comando de PowerShell que obtiene información básica sobre un archivo
comando_powershell = '(Get-Item "file.jpg").CreationTime=("3 August 2012 17:00:00")'


if __name__ == "__main__":
    try:
        try:
            path_of_the_directory= os.getcwd() + '\\fotos'
            print("Files and directories in a specified path:")
            for filename in os.listdir(path_of_the_directory):
                f = os.path.join(path_of_the_directory,filename)
                if os.path.isfile(f):
                    change_file(f)
                    
        except Exception as e:
            print(f"Error al leer los metadatos de la imagen: {e}")

        
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando de PowerShell: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")