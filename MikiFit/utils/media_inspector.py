"""
--------------------------------------
    Media_inspector (MediaInspector)
-------------------------------------- 
De `MediaInspector` class biedt een centrale interface voor het beheren van invoerapparaten zoals microfoons en camera’s.

Functionaliteiten:
- Scant automatisch naar beschikbare audio- en video-invoerapparaten.
- Toont een overzichtslijst van aangesloten invoerapparaten.
- Ondersteunt handmatige selectie van voorkeurapparaten door de gebruiker.
- Prioriteert handmatig geselecteerde invoer boven automatisch gedetecteerde apparaten.
- Houdt interne status bij van geselecteerde audio- en video-invoer, voor eenvoudig hergebruik binnen applicaties.   
"""
import sounddevice as sd
import cv2
import logging

# Configureer logger
logger = logging.getLogger(__name__)                                            
logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")                                         

class MediaInspector:
    
        def __init__(self):
            self.audio_index = sd.query_devices()           # Methode die audioapparaten ophaalt 
            self.default_input = None                       # Standaard geselecteerd inputapparaat
            self.select_input = None                        # Door gebruiker gekozen inputapparaat
            
            
            logger.info("🕵️: Zoekt naar beschikbare audio-invoerapparaten...")  
            
        def scan_sound_input(self, max_src: int = 5):
            """
            Detecteert automatisch de eerste beschikbare input-audiobron (microfoon).
            """
            self.max_input = self.audio_index()[:max_src]    # Beperk de lijst tot max_src apparaten
            logger.info("🎙️: Beschikbare audio-inputbronnen:")
            
            if self.default_input is None:
                for i, device in enumerate(self.max_input):
                    if device['max_input_channels'] > 0:
                        logger.info(f"{i}: {device['name']} \n")
                        self.default_input = i
                        logger.info(f"✅: Automatisch geselecteerd inputapparaat: {device['name']}")
                        return self.default_input
                if self.default_input is None: 
                        logger.error(" ❌: Geen geschikt inputapparaat gevonden.")
                        return []
            
        def select_sound_input(self, max_src: int = 3):
            """
            Laat de gebruiker een inputapparaat selecteren. Bij geen selectie wordt automatisch gescand. 
            """
            self.max_input = self.audio_index()[:max_src]
            
            if self.select_input is not None:
                self.default_input = self.select_input
            else:
                self.scan_sound_input()
            
            return self.default_input
        
        def scan_video_input(self, max_src: int = 3):
            """
            Detecteert beschikbare videobronnen (bijv. webcams) en test of ze beeld leveren.
    
            Returns:
                Een lijst met werkende videobronnen in de vorm van dictionaries met 'index' en 'label'.
            """
            video_source = []                                                       # Lijst met werkende videobronnen
            
            try:
                for i in range(max_src):
                    cap = cv2.VideoCapture(i)                                       # Probeer videobron op index i te openen   
                    ret, _ = cap.read()                                             # Test of er succesvol een frame gelezen kan worden
                    if ret:
                        # Voeg werkende bron toe aan de lijst met een herkenbaar label                                                            
                        video_source.append({'index': i, 'label': f"camera{i}"})    
                    cap.release()                                                   # Vrijgeven van de systeembron voor deze videobron
                return video_source
            except Exception:
                logger.exception("❌: Fout bij het detecteren van videobronnen")
                return []