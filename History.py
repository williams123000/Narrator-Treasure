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

# Crear un objeto ArgumentParser para manejar los argumentos de la línea de comandos
parser = argparse.ArgumentParser(description="Descripción de tu programa")

# Agregar los argumentos que se pueden pasar al programa
parser.add_argument('-Voice', type=int, help='Funcionamiento de voz', required=True)
parser.add_argument('-IA', type=int, help='Funcionamiento con IA', required=True)

args = parser.parse_args() # Parsear los argumentos
ModeVoice = args.Voice # Obtener el valor del argumento Voice (Para activar o desactivar la voz del narrador)
ModeIA = args.IA # Obtener el valor del argumento IA (Para activar o desactivar la mejora de la historia con IA)


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
        self.Map = DictionaryCharacter['Map']
        self.Found = DictionaryCharacter['Found']
        self.ObjectMastered = DictionaryCharacter['ObjectMastered']
        self.CapacityStatus = DictionaryCharacter['CapacityStatus']
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
        print(f"Map: {self.Map}")
        print(f"Found: {self.Found}")
        print(f"ObjectMastered: {self.ObjectMastered}")
        print(f"CapacityStatus: {self.CapacityStatus}")
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

StatusGoalDecipheringTheMap = False # Variable para almacenar el estado de la meta Decifrar el mapa
StatusGoalFormAnExpeditionTeam = False # Variable para almacenar el estado de la meta Formar un equipo de expedición
StatusGoalTheSeekerRealizesThatHeNeedsToPrepareTheExpedition = False # Variable para almacenar el estado de la meta El buscador se percata que necesita preparas la expedición
StatusGoalReachTheLocationWhereTheTreasureIsBelievedToBeHidden = False # Variable para almacenar el estado de la meta Alcanzar la ubicación donde se cree que está escondido el tesoro
StatusGoalASeekerDecidesToGoInSearchOfATreasure = False # Variable para almacenar el estado de la meta conductora Un buscador decide ir en busca de un tesoro

Seeker = None # Variable para almacenar el personaje Buscador
Crush = None # Variable para almacenar el personaje Crush
Treasure = None # Variable para almacenar el personaje Tesoro
Candidate = None # Variable para almacenar el personaje Candidato


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
                        f"Map: {char.Map}\n"
                        f"Found: {char.Found}\n"
                        f"ObjectMastered: {char.ObjectMastered}\n"
                        f"CapacityStatus: {char.CapacityStatus}\n"
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


def storyActionUseAncientKnowledge(Seeker: Character):
    def preconditions():
        logging.info("Validando las precondiciones para la acción de usar conocimientos antiguos")
        if Seeker.Map != "Ancient symbols":
            logging.info("Precondiciones validadas el personaje Buscador ha encontrado símbolos antiguos")
            return
        

    def postconditions():
        logging.info("Postcondiciones para la acción de usar conocimientos antiguos")
        Seeker.Map = "Ancient symbols"
        logging.info("Mapa actualizado a símbolos antiguos")
        logging.info("Mapa: " + Seeker.Map)



    def template():
        Text = f"Studying the map he possessed, the {Seeker.Name} noticed that it was covered in {Seeker.Map}. Thanks to his vast knowledge and experience, he not only recognized the symbols, but also began to decipher them. Each symbol revealed a clue, and with each revelation, the path to the treasure became clearer."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)
    
    preconditions()
    postconditions()
    template()

def storyActionUseDecodingTechniques(Seeker: Character):
    def preconditions():
        logging.info("Validando las precondiciones para la acción de usar técnicas de decodificación")
        if Seeker.Map != "Coordinates encrypted":
            logging.info("Precondiciones validadas el personaje Buscador ha encontrado un mapa con criptografía")
            return

    def postconditions():
        logging.info("Postcondiciones para la acción de usar técnicas de decodificación")
        Seeker.Map = "Coordinates encrypted"
        logging.info("Mapa actualizado a coordenadas encriptadas")
        logging.info("Mapa: " + Seeker.Map)

    def template():
        Text = f"Analyzing the map in his hands, the {Seeker.Name} realized that it contained {Seeker.Map}. Using his decoding skills and knowledge of cryptography, he began to unravel the code. Each number and letter lined up to reveal the exact location of the treasure."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)
    
    preconditions()
    postconditions()
    template()

def storyActionUseExhaustiveInvestigation(Seeker: Character):
    def preconditions():
        logging.info("Validando las precondiciones para la acción de usar investigación exhaustiva")
        if Seeker.Map != "Hidden marks":
            logging.info("Precondiciones validadas el personaje Buscador ha encontrado marcas ocultas")
            return

    def postconditions():
        logging.info("Postcondiciones para la acción de usar investigación exhaustiva")
        Seeker.Map = "Hidden marks"
        logging.info("Mapa actualizado a marcas ocultas")
        logging.info("Mapa: " + Seeker.Map)

    def template():
        Text = f"Upon examining the map, the {Seeker.Name} noticed that it contained {Seeker.Map}. Using his keen perception and his experience from previous explorations, he began to reveal the marks hidden beneath the surface of the paper. Each mark indicated a secret path that brought him closer to the treasure."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)
    
    preconditions()
    postconditions()
    template()

def storyActionUseOtherTracks(Seeker: Character):
    def preconditions():
        logging.info("Validando las precondiciones para la acción de usar otras pistas")
        if Seeker.Map != "Other type of track":
            logging.info("Precondiciones validadas el personaje Buscador ha encontrado otras pistas")
            return

    def postconditions():
        logging.info("Postcondiciones para la acción de usar otras pistas")
        Seeker.Map = "Other type of track"
        logging.info("Mapa actualizado a otro tipo de pista")
        logging.info("Mapa: " + Seeker.Map)

    def template():
        Text = f"Studying the map, the {Seeker.Name} noticed that it was full of {Seeker.Map} subtle and details that went unnoticed at first glance. With his keen ability for observation and analysis, he began to decipher the hidden clues. Every detail, every little clue, led him to the whereabouts of the treasure."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)
    
    preconditions()
    postconditions()
    template()

# Acción Saber la ubicación del tesoro
def storyActionKnowTheLocationOfTheTreasure():
    global Treasure
    def preconditions():
        global Treasure
        logging.info("Validando las precondiciones para la acción de saber la ubicación del tesoro")
        Treasure = defineCharacter(Characters, "Name", "Treasure")
        Treasure = Character(Treasure)
        ListUbicaction= []
        ListUbicaction.append("Desert")
        ListUbicaction.append("Abandoned house")
        ListUbicaction.append("Building in ruins")

        #Escoge un elemento aleatorio de la lista
        UbicactionTreasure = random.choice(ListUbicaction)
        Treasure.Location = UbicactionTreasure
        logging.info("Ubicación del tesoro: " + Treasure.Location)
        
        if Treasure != None:
            logging.info("Precondiciones validadas el personaje Tesoro existe")
            return
        
    def postconditions():
        global Seeker
        logging.info("Postcondiciones para la acción de saber la ubicación del tesoro")
        Seeker.Found = "Yes"
        logging.info("El buscador ha encontrado el tesoro")
        logging.info("Encontrado: " + Seeker.Found)

    def template():
        global Seeker
        global Treasure
        Text = f"The {Seeker.Name} with what he discovered on the map knows that it is in the {Treasure.Location}."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)


    preconditions()
    postconditions()
    template()

# Meta Descifrar el mapa
def GoalDecipheringTheMap():
    def preconditions():
        global Seeker
        logging.info("Validando las precondiciones de la meta: Descifrar el mapa")
        if Seeker.Name == "Historian":
            logging.info("Precondiciones validadas el personaje Buscador es un Hisotriador")
            logging.info("Acción: Usa conocimentos antiguos")
            storyActionUseAncientKnowledge(Seeker)

        elif Seeker.Name == "Hacker":
            logging.info("Precondiciones validadas el personaje Buscador es un Hacker")
            logging.info("Acción: Usa tecnicas de decodificación")
            storyActionUseDecodingTechniques(Seeker)

        elif Seeker.Name == "Expert Explorer":
            logging.info("Precondiciones validadas el personaje Buscador es un Experto Explorador")
            logging.info("Acción: Usa investigación exhaustiva")
            storyActionUseExhaustiveInvestigation(Seeker)

        elif Seeker.Name == "Detective":
            logging.info("Precondiciones validadas el personaje Buscador es un Detective")
            logging.info("Acción: Usa otras pistas")
            storyActionUseOtherTracks(Seeker)

    def plan():
        global StatusGoalDecipheringTheMap
        logging.info("Planificación de la meta: Descifrar el mapa")
        logging.info("Acción: Saber la ubicación del tesoro")
        storyActionKnowTheLocationOfTheTreasure()
        StatusGoalDecipheringTheMap = True
        logging.info("Meta: Descifrar el mapa completada")
    preconditions()
    plan()

# Acción Va en busca de
def storyActionGoInSearchOf(Candidate: Character):
    def preconditions():
        logging.info("La acción de Va en busca de no tiene precondiciones")
        pass
    def postconditions():
        logging.info("Postcondiciones para la acción de Va en busca de")
        Candidate.Found = "Yes"
        logging.info("Encontrado: " + Candidate.Found + " " + Candidate.Name)
    def template():
        global Seeker
        global Candidate
        global Treasure
        Text = f"The {Seeker.Name} was determined to press on, knowing that he would need more than just his knowledge and skills to overcome the challenges that the {Treasure.Location} would pose to him. With this realization in mind, he decided that it was time to seek out a helper, someone with combat experience and capable of handling any dangerous situation that might arise. Thus, he set out in search of a {Candidate.Name} expert in {Candidate.ObjectMastered}, an old acquaintance who had served on multiple dangerous missions and who possessed deep knowledge of survival and defense tactics. Together, they formed a formidable duo, ready to face any obstacle in their path to the treasure."
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)
    preconditions()
    postconditions()
    template()

# Meta Formar un equipo de expedición
def GoalFormAnExpeditionTeam():
    def preconditions():
        global Candidate
        logging.info("Validando las precondiciones de la meta: Formar un equipo de expedición")
        Candidate = defineCharacter(Characters, "Personality", "Helper")
        Candidate = Character(Candidate)
        logging.info("Precondiciones validadas el personaje Candidato existe")
        logging.info("Candidato: " + Candidate.Name)

    def plan():
        global StatusGoalFormAnExpeditionTeam
        logging.info("Planificación de la meta: Formar un equipo de expedición")
        if Candidate.ObjectMastered == "Weapons":
            logging.info("El candidato domina las armas")
            logging.info("El candidato se une al equipo de expedición")
            logging.info("Acción: Va en busca de")
            storyActionGoInSearchOf(Candidate)
        elif Candidate.ObjectMastered == "Swords":
            logging.info("El candidato domina las espadas")
            logging.info("El candidato se une al equipo de expedición")
            logging.info("Acción: Va en busca de")
            storyActionGoInSearchOf(Candidate)

        StatusGoalFormAnExpeditionTeam = True
        logging.info("Meta: Formar un equipo de expedición completada")

    preconditions()
    plan()

# Acción Enfrentar y resolver ingeniosos desafíos físicos e intelectuales diseñados para proteger el tesoro
def storyActionFaceAndSolveIngeniousPhysicalChallenges():
    def preconditions():
        global Treasure
        logging.info("Validando las precondiciones para la acción de enfrentar y resolver ingeniosos desafíos físicos e intelectuales diseñados para proteger el tesoro")
        if Treasure.Dangers == "None":
            logging.info("Precondiciones validadas el tesoro no tiene peligros")
            return
    def postconditions():
        global Seeker
        global Candidate
        global Treasure
        logging.info("Postcondiciones para la acción de enfrentar y resolver ingeniosos desafíos físicos e intelectuales diseñados para proteger el tesoro")
        Seeker.CapacityStatus = "Leader"
        Candidate.CapacityStatus = "Helper"
        Treasure.Dangers = "Maze"
        logging.info(f"Estado de capacidad del buscador: {Seeker.CapacityStatus}")
        logging.info("Estado de capacidad del candidato actualizado")
        logging.info(f"Estado de capacidad del candidato: {Candidate.CapacityStatus}")
        logging.info("Peligros del tesoro actualizados")
        logging.info(f"Peligros del tesoro: {Treasure.Dangers}")

    def template():
        global Seeker
        global Candidate
        global Treasure
        Text = f"The {Seeker.Name} became the {Seeker.CapacityStatus} along with the {Candidate.Name} were aware that in that inhospitable terrain, the dangers would not only come from the weather and harsh conditions, but also from possible threats that could arise on their journey. As they moved forward, they encountered ingenious challenges, clearly designed to protect the treasure. The first was a {Treasure.Dangers} of shifting dunes, where every misstep could trap them forever."
        Text2 = f"Using their knowledge of the terrain and observation skills, the {Seeker.Name} accurately guided every move, while the {Seeker.Name} stayed alert for any unexpected dangers. But they were finally able to find the whereabouts of the treasure."
        saveFileHistory(Text)
        saveFileHistory(Text2)
        logging.info("Texto de la historia: " + Text)
        logging.info("Texto de la historia: " + Text2)

    preconditions()
    postconditions()
    template()


# Meta El buscador se percata que necesita preparas la expedición
def GoalTheSeekerRealizesThatHeNeedsToPrepareTheExpedition():
    def preconditions():
        logging.info("Validando las precondiciones de la meta: El buscador se percata que necesita preparas la expedición")
        logging.info("La meta El buscador se percata que necesita preparas la expedición se pone en pausa")
        logging.info("Meta: Formar un equipo de expedición")
        GoalFormAnExpeditionTeam()
        logging.info("Precondiciones validadas para la meta El buscador se percata que necesita preparas la expedición")
    def plan():
        global StatusGoalTheSeekerRealizesThatHeNeedsToPrepareTheExpedition
        logging.info("Planificación de la meta: El buscador se percata que necesita preparas la expedición")
        logging.info("Acción: : Enfrentar y resolver ingeniosos desafíos físicos e intelectuales diseñados para proteger el tesoro.")
        storyActionFaceAndSolveIngeniousPhysicalChallenges()
        StatusGoalTheSeekerRealizesThatHeNeedsToPrepareTheExpedition = True
        logging.info("Meta: El buscador se percata que necesita preparas la expedición completada")


    preconditions()
    plan()

# Acción El buscador asegura el tesoro exitosamente
def storyActionTheSeekerSuccessfullySecuresTheTreasure():
    def preconditions():
        global Seeker
        global Candidate
        global Crush
        logging.info("La acción de El buscador asegura el tesoro exitosamente no tiene precondiciones")
        pass
    def postconditions():
        global Seeker
        logging.info("Postcondiciones para la acción de El buscador asegura el tesoro exitosamente")
        Seeker.Success = "Yes"
        logging.info("Éxito: " + Seeker.Success + " " + Seeker.Name)


    def template():
        global Seeker
        global Candidate
        global Crush
        Text = f"The {Seeker.Name} and the {Candidate.Name} finally guard the treasure. And the {Crush.Name} after a long time decided to be a partner of the {Seeker.Name}, together they enjoyed the reward of the treasure." 
        saveFileHistory(Text)
        logging.info("Texto de la historia: " + Text)

    preconditions()
    postconditions()
    template()




# Meta Alcanzar la ubicación donde se cree que está escondido el tesoro
def GoalReachTheLocationWhereTheTreasureIsBelievedToBeHidden():
    def preconditions():
        logging.info("Validando las precondiciones de la meta: Alcanzar la ubicación donde se cree que está escondido el tesoro")
        logging.info("La meta Alcanzar la ubicación donde se cree que está escondido el tesoro se pone en pausa")
        logging.info("Meta: El buscador se percata que necesita preparas la expedición")
        GoalTheSeekerRealizesThatHeNeedsToPrepareTheExpedition()
        logging.info("Precondiciones validadas para la meta Alcanzar la ubicación donde se cree que está escondido el tesoro")
    def plan():
        global StatusGoalReachTheLocationWhereTheTreasureIsBelievedToBeHidden
        logging.info("Planificación de la meta: Alcanzar la ubicación donde se cree que está escondido el tesoro")
        storyActionTheSeekerSuccessfullySecuresTheTreasure()
        StatusGoalReachTheLocationWhereTheTreasureIsBelievedToBeHidden = True
        logging.info("Meta: Alcanzar la ubicación donde se cree que está escondido el tesoro completada")

    preconditions()
    plan()


# Meta conductora Un buscador decide ir en busca de un tesoro
def GoalASeekerDecidesToGoInSearchOfATreasure():

    logging.info("Meta Conductora: Un buscador decide ir en busca de un tesoro")
    def inittext():
        global Seeker
        global Crush
        print(colorama.Fore.LIGHTCYAN_EX + "Un buscador decide ir en busca de un tesoro" + colorama.Style.RESET_ALL)
        
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

        logging.info("La meta Un bucador decide ir en busca de un tesoro se pone en pausa")
        logging.info("Meta: Descifrar el mapa ")
        GoalDecipheringTheMap()
        logging.info("Precondiciones validadas para la meta Descifrar el mapa")

    
    def plan():
        global StatusGoalASeekerDecidesToGoInSearchOfATreasure
        logging.info("Planificación de la meta: Un buscador decide ir en busca de un tesoro")
        logging.info("Meta: Alcanzar la ubicación donde se cree que está escondido el tesoro")
        GoalReachTheLocationWhereTheTreasureIsBelievedToBeHidden()
        StatusGoalASeekerDecidesToGoInSearchOfATreasure = True
        logging.info("Meta: Un buscador decide ir en busca de un tesoro completada")
    
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
#print(colorama.Fore.MAGENTA + "\n Historia en Ingles: ")
#print(file_content ) # Imprime el contenido del archivo History.txt
logging.info("Texto de la historia en Ingles " + file_content)

Text_Translate = translate_text(file_content) # Traduce el contenido del archivo History.txt al español
#print(colorama.Fore.GREEN + "\n Historia en Español:")
#print(Text_Translate) # Imprime la traducción de la historia
logging.info("Texto de la historia en Español " + Text_Translate)



# Función para mejorar la historia con IA usando la API de Llama3
def UpgradeIA(Text):

        # URL del servidor de LM Studio
    url = "http://localhost:1234/v1/chat/completions"

    # Encabezados de la solicitud
    headers = {
        "Content-Type": "application/json"
    }

    Text_History = "Mejora el siguiente texto manteniendo la historia intacta, pero optimizando la fluidez para evitar la repetición innecesaria de personajes. Reemplaza o reformula oraciones para que los personajes no se mencionen tantas veces seguidas, sin agregar nuevos elementos ni alterar el contenido original es decir no alterar la historia, tampoco pierdas el contexto y su idea IMPORTANTE: SOLO DAME LA NUEVA HISTORIA, NO AGREGUES NADA MÁS: " + Text 

    # Cuerpo de la solicitud
    data = {
        "model": "lmstudio-community/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf",
        "messages": [
            {"role": "system", "content": "Eres un mejorador de historias."},
            {"role": "user", "content": Text_History},
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, json=data)

    # Mostrar el resultado
    if response.status_code == 200:
        completion = response.json()
        return completion['choices'][0]['message']['content']
    else:
        print(f"Error: {response.status_code}")
        return "Error"


##print(response.json())


NewHistory = Text_Translate # Guarda la historia traducida al español en una nueva variable NewHistory


#print(statusGoalHeroDecideRescueHostage) # Imprime el estado de la meta conductora

# Imprime los modos de funcionamiento de la IA y la voz del narrador
if ModeIA == 1: # Si el modo de IA está activado
    
    logging.info("Modo de IA encendida")
    NewHistory = UpgradeIA(NewHistory)
    #print(colorama.Fore.CYAN + "\n Historia Mejorada: ")
    #print(colorama.Fore.CYAN + "\n Historia Mejorada: " + NewHistory) # Imprime la historia mejorada
    #print(NewHistory)
    logging.info("Texto de la historia mejorada " + NewHistory)

else:
    #print("\nModo de IA apagada")
    logging.info("Modo de IA apagada")
    #print("\nTexto de la historia: ")
    #print(NewHistory)
    #logging.info("Texto de la historia " + NewHistory)

if ModeVoice == 1: # Si el modo de voz está activado
    logging.info("Modo de voz encendida")
    #print("\nModo de voz encendida")
    #VoiceText(NewHistory)
    #print(colorama.Fore.CYAN + "\nTexto de la historia: ")
    print(NewHistory)
    logging.info("Texto de la historia " + NewHistory)

else:
    #print("\nModo de voz apagada")
    logging.info("Modo de voz apagada")
    #print("\nTexto de la historia: ")
    print(NewHistory)



