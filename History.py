# Importación de librerías
import os # Importa la librería os para trabajar con el sistema operativo
import random # Importa la librería random para generar números aleatorios
import colorama # Importa la librería colorama para darle color al texto
import json # Importa la librería json para trabajar con archivos JSON
import logging # Importa la librería logging para guardar logs en un archivo de texto
import datetime # Importa la librería datetime para trabajar con fechas y horas
from Traslate import translate_text # Importa la función translate_text del archivo Translate.py


import requests # Importa la librería requests para hacer solicitudes HTTP
import argparse # Importa la librería argparse para crear un objeto ArgumentParser


# Crear el directorio de logs si no existe
log_directory = 'logs'
os.makedirs(log_directory, exist_ok=True)
# Generar un nombre de archivo único basado en la fecha y hora actuales
log_filename = os.path.join(log_directory, datetime.datetime.now().strftime("History_%Y%m%d_%H%M%S.log"))

# Configuración de los logs para guardar la información en un archivo de texto
logging.basicConfig(
    filename=log_filename,
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    encoding='utf-8'
)

logging.info("Inicio de la ejecución del programa History.py")
logging.info("Programa escrito por Williams Chan Pescador")


colorama.init() # Inicializa colorama para darle color al texto

# Define la clase del personaje
class Character:
    # Constructor de la clase Character que recibe un diccionario con los atributos del personaje 
    def __init__(self, DictionaryCharacter):
        self.Name = DictionaryCharacter['Name']
        self.Location = DictionaryCharacter['Location']
        self.Gender = DictionaryCharacter['Gender']
        self.Personality = DictionaryCharacter['Personality']
        self.EmotionTowardsOtherCharacter = DictionaryCharacter['EmotionTowardsOtherCharacter']
        self.MapFound = DictionaryCharacter['MapFound']
        self.ObjectMastered = DictionaryCharacter['ObjectMastered']
        self.CaptivityStatus = DictionaryCharacter['CaptivityStatus']
        self.Dangers = DictionaryCharacter['Dangers']
        self.Success = DictionaryCharacter['Success']
        self.ObjectOfEmotion = DictionaryCharacter['ObjectOfEmotion']

    # Método que imprime los atributos del personaje
    def printCharacter(self):
        print(f"Name: {self.Name}")
        print(f"Location: {self.Location}")
        print(f"Gender: {self.Gender}")
        print(f"Personality: {self.Personality}")
        print(f"EmotionTowardsOtherCharacter: {self.EmotionTowardsOtherCharacter}")
        print(f"MapFound: {self.MapFound}")
        print(f"ObjectMastered: {self.ObjectMastered}")
        print(f"CaptivityStatus: {self.CaptivityStatus}")
        print(f"Dangers: {self.Dangers}")
        print(f"Success: {self.Success}")
        print(f"ObjectOfEmotion: {self.ObjectOfEmotion}")
        print("\n")
        
# Limpiar el contenido de un archivo
def clear_file(file_path):
    # Abre el archivo en modo de escritura para vaciar su contenido
    with open(file_path, 'w') as file:
        pass  # No se necesita hacer nada aquí, solo abrir el archivo en modo de escritura lo vacía

# Guardar el historial de texto en un archivo
def saveFileHistory(Text):
    with open("History.txt", "a") as file:
        file.write(f"{Text} \n")

# Imprimir un diccionario en formato JSON
def printJSON(data):
    print(json.dumps(data, indent=4, ensure_ascii=False))

# Cargar los personajes desde un archivo JSON
def loadSettigs():
    try:
        with open("Characters.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

Seeker = None # Variable para almacenar el personaje buscador
Crush = None # Variable para almacenar el personaje Crush



# Función imprimir los detalles de los personajes 
def printCharacters():
    for Character_ in Characters:
        Character(Character_).printCharacter()

# Función para obtener los detalles de los personajes en lugar de imprimirlos
def getCharactersDetails():
    details = []
    for Character_ in Characters:
        char = Character(Character_)
        details.append(f"\nName: {char.Name}\n"
                        f"Location: {char.Location}\n"
                        f"Gender: {char.Gender}\n"
                        f"Personality: {char.Personality}\n"
                        f"EmotionTowardsOtherCharacter: {char.EmotionTowardsOtherCharacter}\n"
                        f"MapFound: {char.MapFound}\n"
                        f"ObjectMastered: {char.ObjectMastered}\n"
                        f"CaptivityStatus: {char.CaptivityStatus}\n"
                        f"Dangers: {char.Dangers}\n"
                        f"Success: {char.Success}\n"
                        f"ObjectOfEmotion: {char.ObjectOfEmotion}\n")
    return "\n".join(details)

                       


    
Characters = loadSettigs() # Carga los personajes desde el archivo JSON
logging.info("Personajes instanciados correctamente")
logging.info("Personajes: ")
logging.info(getCharactersDetails())
clear_file("History.txt") # Limpia el contenido del archivo History.txt

#printCharacters() # Imprime los detalles de los personajes


# Función para definir un personaje según un atributo y un valor
def defineCharacter(Characters, Attribute, Value):
    SelectedCharacter = list(filter(lambda Character_: Character_[Attribute] == Value, Characters))
    return random.choice(SelectedCharacter) if SelectedCharacter else None

def storyActionReconciliation(Charactertolove: Character, Lovedcharacter: Character):

    def Precondition():
        logging.info("Sin precondiciones para la acción de reconciliación")
        pass

    def Postcondition():
        logging.info("Postcondiciones para la acción de reconciliación")
        Charactertolove.EmotionTowardsOtherCharacter = "Loved"
        Lovedcharacter.EmotionTowardsOtherCharacter = "Loved"
        logging.info("Emoción de los personajes actualizada a Loved")
        logging.info("Emocion por otro personaje de " + Charactertolove.Name + ": " + Charactertolove.EmotionTowardsOtherCharacter)
        logging.info("Emocion por otro personaje de " + Lovedcharacter.Name + ": " + Lovedcharacter.EmotionTowardsOtherCharacter)

    def Template():
        lista = []
        lista.append(f"The {Charactertolove.Name} would do whatever was necessary for the love of The {Lovedcharacter.Name}, facing any obstacle in their path")
        lista.append(f"For the love of The {Lovedcharacter.Name}, the {Charactertolove.Name} was willing to overcome any challenge, no matter how impossible it seemed.")
        lista.append(f"Motivated by the love of The {Lovedcharacter.Name}, the {Charactertolove.Name} would stop at nothing, willing to do the impossible for her.")

        #Escoge un elemento aleatorio de la lista
        Text = random.choice(lista)
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)

        

    Precondition()
    Template()
    Postcondition()

# Meta conductora Un buscador decide ir en busca de un tesoro
def GoalASeekerDecidesToGoInSearchOfATreasure():

    logging.info("Meta Conductora: Un buscador decide ir en busca de un tesoro")
    def inittext():
        global Seeker
        global Crush
        print(colorama.Fore.LIGHTCYAN_EX + "Un buscador decide ir en busca de un tesoro" + colorama.Style.RESET_ALL)
        print(colorama.Fore.LIGHTCYAN_EX + "=========================================" + colorama.Style.RESET_ALL)
        print("\n")
        TextSeeker = f"The {Seeker.Name} was in the {Seeker.Location} with one main motive which was, {Seeker.ObjectOfEmotion}."
        saveFileHistory(TextSeeker)
        logging.info("Texto de la historia: " + TextSeeker)
        TextCrush = f"The {Crush.Name} was a {Crush.Personality} person thanks to the motivation of the {Seeker.Name} in search of going for the treasure she would be his girlfriend."
        saveFileHistory(TextCrush)
        logging.info("Texto de la historia: " + TextCrush)

    def preconditions():
        global Seeker
        global Crush

        logging.info("Validando las precondiciones de la meta: Un buscador decide ir en busca de un tesoro")

        if Seeker != None and Crush != None:
            logging.info("Precondiciones validadas los personajes Seeker y Crush existen")
            return 
        
        Speeker = defineCharacter(Characters, "Personality", "Daring")
        Seeker = Character(Speeker)

        Crush = defineCharacter(Characters, "Personality", "Sentimental")
        Crush = Character(Crush)

        logging.info("Personajes instanciados correctamente")
        logging.info("Seeker: " + Seeker.Name)
        logging.info("Crush: " + Crush.Name)

        #Eliminar el Buscador de los personajes
        Characters.remove(Speeker)

        inittext() # Inicializa el texto de la historia

        logging.info("Acción de reconciliación entre el buscador y Crush")
        storyActionReconciliation(Seeker, Crush)

    
    def plan():
        pass
    
    preconditions() # Verifica las precondiciones
    plan() # Planifica la meta

GoalASeekerDecidesToGoInSearchOfATreasure() # Ejecuta la meta conductora



# Función para leer el contenido de un archivo de texto 
def read_file(file_path):
    # Abre el archivo en modo de lectura
    with open(file_path, 'r') as file:
        # Lee todo el contenido del archivo
        content = file.read()
    return content

file_content = read_file("History.txt") # Lee el contenido del archivo History.txt
print(colorama.Fore.MAGENTA + "\n Historia en Ingles: ")
print(file_content ) # Imprime el contenido del archivo History.txt
logging.info("Texto de la historia en Ingles " + file_content)

Text_Translate = translate_text(file_content) # Traduce el contenido del archivo History.txt al español
print(colorama.Fore.GREEN + "\n Historia en Español:")
print(Text_Translate) # Imprime la traducción de la historia
logging.info("Texto de la historia en Español " + Text_Translate)
