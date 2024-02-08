import flet as ft
from pytube import YouTube
import os 
import string

def main(page):
    # Configuración de la página
    page.window_resizable = False
    page.bgcolor = "#F6F3F7"
    page.window_height = 160
    page.window_width = 500
    page.title = "Pydownload"

    # Campo de entrada de la URL
    url = ft.TextField(label="URL", autofocus=True, color="#34495E", text_size=16)

    # Botones de descarga
    submitmp4 = ft.ElevatedButton("Descargar MP4", bgcolor="#84CCDD")
    submitmp3 = ft.ElevatedButton("Descargar MP3", bgcolor="#BB8FCE")

    # Función para mostrar el cuadro de diálogo de descarga en proceso
    def open_dlg(e):
        page.dialog = dlg_in_process
        dlg_in_process.open = True
        page.update()
    
    # Función para mostrar el cuadro de diálogo de descarga completada
    def open_completion_dlg(title):
        dlg_completion.title.spans[0].text = "Descarga completa: {}".format(title)
        page.dialog = dlg_completion
        dlg_completion.open = True
        page.update()

    # Función para crear una carpeta si no existe
    def create_folder_if_not_exists(folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Función para descargar un video MP4
    def download_mp4(e):
        try:
            current_folder = os.getcwd()
            videos_folder = os.path.join(current_folder, "Videos")
            create_folder_if_not_exists(videos_folder)
            yt = YouTube(url.value)
            open_dlg(e)
            video = yt.streams.get_highest_resolution()
            cleaned_title = clean_filename(video.title)
            video.download(output_path=videos_folder, filename=cleaned_title + ".mp4")
            print("Descarga completa: {}".format(cleaned_title))
            url.value = ""
            dlg_in_process.open = False  # Cerrar cuadro de diálogo de descarga en proceso
            open_completion_dlg(cleaned_title)  # Mostrar cuadro de diálogo de descarga completada
        except Exception as error:
            print("Error en la descarga: {}".format(str(error)))

    # Función para descargar un audio MP3
    def download_mp3(e):
        try:
            current_folder = os.getcwd()
            audio_folder = os.path.join(current_folder, "Audio")
            create_folder_if_not_exists(audio_folder)
            yt = YouTube(url.value)
            open_dlg(e)
            audio_stream = yt.streams.filter(only_audio=True).first()
            cleaned_title = clean_filename(audio_stream.title)
            audio_stream.download(output_path=audio_folder, filename=cleaned_title + ".mp3")
            print("Descarga completa del MP3: {}".format(cleaned_title))
            url.value = ""
            dlg_in_process.open = False  # Cerrar cuadro de diálogo de descarga en proceso
            open_completion_dlg(cleaned_title)  # Mostrar cuadro de diálogo de descarga completada
        except Exception as error:
            print("Error en la descarga del MP3: {}".format(str(error)))

    # Asignación de funciones a los botones
    submitmp4.on_click = download_mp4
    submitmp3.on_click = download_mp3

    # Diálogo de descarga en proceso
    dlg_in_process = ft.AlertDialog(
        title=ft.Text(spans=[
            ft.TextSpan(
                "Descarga en proceso...",
                ft.TextStyle(
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK54,
                ),
            ),
        ]),
        on_dismiss=lambda e: print("Dialogo cerrado")
    )

    # Diálogo de descarga completada
    dlg_completion = ft.AlertDialog(
        title=ft.Text(spans=[
            ft.TextSpan(
                "Descarga completa:",
                ft.TextStyle(
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.BLACK54,
                ),
            ),
        ]),
        on_dismiss=lambda e: print("Dialogo cerrado")
    )

    # Diseño de la interfaz de usuario
    page.add(
        url,
        ft.Row(controls=[submitmp4, submitmp3], alignment="center")
    )

# Limpiar el título del archivo para obtener un nombre de archivo válido
def clean_filename(title):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    cleaned_title = ''.join(c for c in title if c in valid_chars)
    return cleaned_title

# Iniciar la aplicación
ft.app(target=main)
