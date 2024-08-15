import tkinter as tk
from tkinter import filedialog, messagebox
from googletrans import Translator
import speech_recognition as sr
from PIL import Image, UnidentifiedImageError
import pytesseract
import io

# Initialize the translator
translator = Translator()

# Specify path to Tesseract executable (if necessary)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function for translating text
def translate_text(text, target_language='en'):
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Function for translating speech directly from the microphone
def translate_speech_from_mic(target_language='en'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        root.update()
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            status_label.config(text=f"Recognized Speech: {text}")
            translated_text = translate_text(text, target_language)
            return translated_text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Sorry, there was an error with the request."

# Function for translating text in an image from a byte stream
def translate_image_from_bytes(image_bytes, target_language='en'):
    try:
        image = Image.open(io.BytesIO(image_bytes))
    except UnidentifiedImageError:
        return "Sorry, the image could not be opened. Please check the format."
    except Exception as e:
        return f"An error occurred: {e}"

    try:
        text = pytesseract.image_to_string(image)
    except Exception as e:
        return f"An error occurred during OCR: {e}"

    if not text.strip():
        return "No readable text found in the image."

    return translate_text(text, target_language)

# Function to handle text translation
def handle_text_translation():
    text_input = text_entry.get("1.0", tk.END).strip()
    target_language = language_entry.get().strip()
    if text_input and target_language:
        translated_text = translate_text(text_input, target_language)
        result_label.config(text=translated_text)
    else:
        messagebox.showwarning("Input Error", "Please enter text and target language.")

# Function to handle speech translation
def handle_speech_translation():
    target_language = language_entry.get().strip()
    if target_language:
        translated_speech = translate_speech_from_mic(target_language)
        result_label.config(text=translated_speech)
    else:
        messagebox.showwarning("Input Error", "Please enter the target language.")

# Function to handle image translation
def handle_image_translation():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    try:
        with open(file_path, 'rb') as image_file:
            image_bytes = image_file.read()
        target_language = language_entry.get().strip()
        if target_language:
            translated_text = translate_image_from_bytes(image_bytes, target_language)
            result_label.config(text=translated_text)
        else:
            messagebox.showwarning("Input Error", "Please enter the target language.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the main application window
root = tk.Tk()
root.title("Translation App")

# Set up the UI components
tk.Label(root, text="Enter text to translate:").pack()
text_entry = tk.Text(root, height=5, width=50)
text_entry.pack()

tk.Label(root, text="Target Language (e.g., 'en' for English):").pack()
language_entry = tk.Entry(root, width=20)
language_entry.pack()

tk.Button(root, text="Translate Text", command=handle_text_translation).pack(pady=5)
tk.Button(root, text="Translate Speech", command=handle_speech_translation).pack(pady=5)
tk.Button(root, text="Translate Image", command=handle_image_translation).pack(pady=5)

status_label = tk.Label(root, text="")
status_label.pack(pady=5)

result_label = tk.Label(root, text="", wraplength=400)
result_label.pack(pady=5)

# Run the application
root.mainloop()