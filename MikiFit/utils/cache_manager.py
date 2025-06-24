"""
--------------------------------------
    Cache_manager (CacheManager)
--------------------------------------
De `CacheManager` is een modulaire database voor tijdelijke opslag van mediabestanden.

Functionaliteiten:
- Slaat mediabestanden zoals foto's en video's lokaal op in een centrale SQLite-database (`data/cache/cache.db`).
- Automatische opschoning: standaard worden cache-items maximaal 30 dagen bewaard, daarna automatisch verwijderd. 
"""
import sqlite3
import logging
from pathlib import Path

# Configureer logger
logger = logging.getLogger(__name__)                                            
logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s")  

class CacheManager:
    
    def __init__(self):
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.CACHE_DB_PATH = Path(self.BASE_DIR / "data" / "cache")                            # standaard opslagmap voor cache 
        
    def cache_database(self) -> None:
        """
        Initieert de cache database voor tijdelijke opslag van media (30 dagen).
        
        Onderdelen database:
            - media_cache: Tijdelijke opslag voor media bestanden:
                * content: Pad/data van mediabestand (UNIQUE voorkomt duplicaten)
                * created_at: Voor automatische cleanup na 30 dagen
        """
        try:
            self.CACHE_DB_PATH.mkdir(parents=True, exist_ok=True)
            cache_db_path = self.CACHE_DB_PATH / "cache.db"
            
            with sqlite3.connect(cache_db_path) as db_connect:
                cursor = db_connect.cursor()
            
            CREATE_MEDIA_CACHE = """
                CREATE TABLE IF NOT EXISTS media_cache(
                        content     TEXT    UNIQUE NOT NULL,
                        created_at  TEXT    DEFAULT (current_timestamp) NOT NULL,
                );
            """
            
            # leegt cache automatisch na 30 dagen
            CLEANUP_OLD_MEDIA = """
                DELETE FROM media_cache 
                WHERE datetime(created_at) < datetime('now', '-30 days');
            """
            
            cursor.execute(CREATE_MEDIA_CACHE)
            cursor.execute(CLEANUP_OLD_MEDIA)
            db_connect.commit()
            
        except sqlite3.Error as e:
            logger.error(f"❌: Cache-Database initialisatie fout: {e}")
            raise
    
    def write_to_cache(self):
        """
        - Schrijft media naar cache, slaat alleen unieke content op.
        - Als content al bestaat (door UNIQUE constraint) wordt deze genegeerd.
        """
        try:
            cache_db_path = self.CACHE_DB_PATH / "cache.db"
            
            with sqlite3.connect(cache_db_path) as db_connect:
                cursor = db_connect.cursor()
            
            INSERT_MEDIA = """
                INSERT OR IGNORE INTO media_cache (content)  
                VALUES (?);
            """
            
            cursor.execute(INSERT_MEDIA, (content,))
            db_connect.commit()
            
            
        except sqlite3.Error as e:
            logger.error(f"❌: Fout bij het wegschrijven van cache: {e}")
            raise 