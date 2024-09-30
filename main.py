from tkinter import ttk
import tkinter as tk
from tkinter import filedialog, messagebox
# import sv_ttk
import asyncio
import edge_tts

# Variable global para almacenar las voces
voice_list = []

# Función asíncrona para obtener la lista de voces y almacenarla en la variable global
async def get_voice_list():
    global voice_list
    voices = await edge_tts.list_voices()
    voice_list = voices
    # Actualiza el combobox con la lista de voces después de obtenerlas
    update_combobox()

def update_combobox():
    # Extraer los FriendlyName de cada voz y ponerlos en el combobox
    friendly_names = [voice['FriendlyName'] for voice in voice_list]
    combobox['values'] = friendly_names
    combobox.current(0)  # Selecciona la primera voz por defecto

async def convert_text_to_speech(text, voice):
    """Convierte el texto a voz y guarda el audio en un archivo."""
    output_file = "output.mp3"
    communicate = edge_tts.Communicate(text, voice)
    with open(output_file, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")
    messagebox.showinfo("Conversión completada", f"El audio ha sido guardado como {output_file}.")

def on_convert_button_click():
    """Función que se ejecuta al hacer clic en el botón de conversión."""
    text = text_widget.get("1.0", tk.END).strip()  # Obtiene el texto del widget de texto
    selected_voice = combobox.get()  # Obtiene la voz seleccionada del combobox
    voice = next((v for v in voice_list if v['FriendlyName'] == selected_voice), None)
    
    if not text:
        messagebox.showwarning("Advertencia", "Por favor, ingrese algún texto para convertir.")
        return
    if voice is None:
        messagebox.showwarning("Advertencia", "Por favor, seleccione una voz válida.")
        return

    # Ejecutar la conversión de texto a voz
    asyncio.run(convert_text_to_speech(text, voice['ShortName']))

def open_file():
    # Abrir un diálogo para seleccionar un archivo de texto
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:  # Verifica si se seleccionó un archivo
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # Lee el contenido del archivo
            text_widget.delete(1.0, tk.END)  # Limpia el widget de texto
            text_widget.insert(tk.END, content)  # Inserta el contenido del archivo en el widget

def main():
    global combobox, text_widget

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Interfaz Básica en Tkinter")
    root.geometry("500x500")  # Ajustar el tamaño de la ventana

    # Crear un combobox más ancho
    combobox = ttk.Combobox(root, state="readonly", width=50)  # Ajustar el ancho a 50 caracteres
    combobox.pack(pady=20)

    # Crear un botón para abrir el archivo
    open_button = ttk.Button(root, text="Abrir archivo de texto", command=open_file)
    open_button.pack(pady=10)

    # Crear un widget de texto para mostrar el contenido del archivo
    text_widget = tk.Text(root, wrap=tk.WORD, width=60, height=15)
    text_widget.pack(pady=10)

    # Crear un botón para convertir texto a voz
    convert_button = ttk.Button(root, text="Convertir a voz", command=on_convert_button_click)
    convert_button.pack(pady=10)

    # Aplicar el tema oscuro usando sv_ttk
    # sv_ttk.set_theme("dark")

    # Ejecutar la función asíncrona al inicio usando asyncio
    root.after(100, lambda: asyncio.run(get_voice_list()))

    # Iniciar el bucle principal de la interfaz
    root.mainloop()

# Llamar a la función main
if __name__ == "__main__":
    main()
