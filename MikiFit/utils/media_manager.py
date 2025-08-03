"""
--------------------------------------
    Media_manager (MediaManager)
-------------------------------------- 
De `MediaManager` class biedt een centrale database voor het opslaan, laden en cachen van chatberichten en foto's.

Functionaliteiten:
- Slaat berichten lokaal op in een centrale SQLite-database, standaard in: `data/save_files/database/`.
- Werkt onafhankelijk van de gespreksgeschiedenis van externe bronnen (zoals OpenAI's API).
- Zorgt ervoor dat gebruikers hun gegevens op elk moment veilig en lokaal kunnen opslaan of herstellen.
"""
import sqlite3
import re
import unicodedata
import logging
from pathlib import Path

# Configureer logger
logger = logging.getLogger(__name__)                                            
logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")   

class MediaManager:
    
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.DB_PATH = Path(self.BASE_DIR / "data" / "save_files" / "database")                # Standaard opslagmap voor database
        
    def database(self) -> None:
        """
        Initieert de centrale database voor het opslaan van chatsessies.
        
        Onderdelen database:
            - chat_sessions: Opslag voor chat sessies (session_id, session_name, created_at)
            - chat_messages: Opslag voor chat berichten (session_id, role, content)
        """
        try:
            self.DB_PATH.mkdir(parents=True, exist_ok=True)                                    # Maakt database directory indien nodig
            db_path = self.DB_PATH / "chat.db"                                                 # Stelt path in naar database
            
            # Manager voor het connecten, openen, sluiten en voeren van queries voor database
            with sqlite3.connect(db_path) as db_connect:
                cursor = db_connect.cursor()
            
            CREATE_SESSIONS_TABLE = """
                CREATE TABLE IF NOT EXISTS chat_sessions(
                    session_id      INTEGER PRIMARY KEY,
                    session_name    TEXT    UNIQUE NOT NULL,
                    created_at      TEXT    DEFAULT (current_timestamp) NOT NULL
                );
            """
            
            CREATE_MESSAGES_TABLE = """
                CREATE TABLE IF NOT EXISTS chat_messages(
                        session_id  INTEGER REFERENCES chat_sessions (session_id) 
                                    ON DELETE CASCADE NOT DEFERRABLE INITIALLY IMMEDIATE NOT NULL,
                        role        TEXT    NOT NULL,
                        content     TEXT    NOT NULL
                );
            """
            
            tables = [
                CREATE_SESSIONS_TABLE,
                CREATE_MESSAGES_TABLE
            ]
            
            for table in tables:
                cursor.execute(table)
            
            db_connect.commit()         # Slaat alle wijzigingen op in de database
            
        except sqlite3.Error as e:
            logger.error(f"❌: Database initialisatie fout: {e}")
            raise
    
    def naam_generator(self, berichten_historie: str, subject_text: str, max_words: int=3, max_length: int=30) -> str:
        """
        Maakt een korte bestandsnaam op basis van het onderwerp van de gebruiker
        """
        # Lijst met veel voorkomende stopwoorden in het Nederlands en Engels
        STOPWORDS = [                                                               
            "de","het","een","en","van","in",
            "to","the","and","a","of","for","is"
        ]
        
        # Zorgt ervoor dat speciale leestekens worden omgezet naar normale leestekens in lowercase
        normalized = (
            unicodedata.normalize("NFKD", subject_text or berichten_historie)
            .encode("ascii", "ignore")
            .decode("ascii")
            .lower()
        )
        
        words = re.findall(r"\b\w+\b",normalized)                                           # Splits de tekst in “echte” woorden
        
        # Voegt alle woorden die geen stopwoord zijn toe aan de lijst
        filtered = []
        
        for word in words:
            if word not in STOPWORDS:
                filtered.append(word)
            
        kernwoorden = filtered[:max_words] or words[:max_words]                             # Ga langs drie kernwoorden (of val terug op een woord als er geen kernwoord is gevonden)

        onderwerp = "-".join(kernwoorden)                                                   # Plakt woorden met koppeltekens
        onderwerp = onderwerp[:max_length].rstrip("-")                                      # Knipt af op de ingestelde maximumlengte en verwijdert eventuele overgebleven streepjes
        return onderwerp       
    
    