import subprocess

subprocess.call(['pip', 'install', 'pandas', 'gradio', 'nltk', '--user'])

# Importar las librerías necesarias
import pandas as pd
import nltk

nltk.download('stopwords')
nltk.download('punkt')  # Descargar el recurso 'punkt'

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import gradio as gr

# Leer el archivo CSV con la información de los productos
df = pd.read_csv('https://daphtech.com/products.csv', error_bad_lines=False)

# Definir las stopwords para el procesamiento del texto
stop_words = set(stopwords.words('spanish'))

# Función para procesar el texto de la pregunta del usuario
def process_question(question):
    # Tokenizar la pregunta
    tokens = word_tokenize(question.lower())

    # Eliminar las stopwords de la pregunta
    filtered_tokens = [token for token in tokens if not token in stop_words]

    # Unir los tokens filtrados para obtener la pregunta procesada
    processed_question = " ".join(filtered_tokens)

    return processed_question

# Función para buscar una respuesta en el archivo CSV
def search_csv(question):
    try:
        # Procesar la pregunta del usuario
        processed_question = process_question(question)

        # Buscar la respuesta en el archivo CSV
        for index, row in df.iterrows():
            if processed_question in row['prompt'].lower():
                return row['prompt']
    except Exception as e:
        # Mostrar el mensaje de error al usuario
        return f"Ha ocurrido un error: {e}"

    # Si no se encuentra una respuesta, devolver None
    return None

# Función para crear una interfaz de chat utilizando Gradio
def chatbot_search_csv(question):
    # Buscar una respuesta en el archivo CSV
    answer = search_csv(question)

    # Si se encuentra una respuesta, mostrarla al usuario
    if answer is not None:
        return answer
    else:
        return "Lo siento, no puedo ayudarte con eso."

# Crear la interfaz de chat utilizando Gradio
iface = gr.Interface(fn=chatbot_search_csv, 
                     inputs=gr.inputs.Textbox(lines=2, placeholder="Escribe tu pregunta aquí..."), 
                     outputs="text", 
                     layout="vertical", 
                     title="Chatbot de productos")

# Ejecutar la interfaz de chat
iface.launch()
