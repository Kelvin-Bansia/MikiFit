"""
--------------------------------------
    env_manager (variabelen manager)
--------------------------------------  
De env_manager is een simpel programma die variabelen, die niet geopenbaard mogen worden,
managed. Het programma zoekt de .env file in de mappenstructuur en laadt vanuit daar de
juiste variabelen. 
"""
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()                                         # Zoekt path naar .env-file
    
if not dotenv_path:                                                 # Controleert of path naar .env-file is gevonden
    raise FileNotFoundError("❌: .env bestand niet gevonden - controleer PATH.") 

load_dotenv(dotenv_path)                                            # Laad omgevingsvariabelen uit .env-file

def var_ip_setup():
    """
    Controleert of de opgegeven ip adres van de server geldig is.
    """
    ip_adres = os.getenv("ip_adres_server", "").strip()         # Laad ip adres uit bestand zonder witregels
    
    if not ip_adres or not ip_adres.startswith("192.168"):      # Valideert of de ip adres niet leeg is en het juiste formaat heeft
        raise ValueError("❌: ip_adres_server is leeg of ongeldig – controleer je .env-bestand.")
    else:
        print("✅: ip adres is geladen en ingesteld")
        return ip_adres

def django_secret_key():
    """
    Controleert of secret_key van Django geldig is.
    """
    secret_key = os.getenv("SECRET_KEY ", "").strip()         
    
    if not secret_key or not secret_key.startswith("django"):      
        raise ValueError("❌: Django secret_key is leeg of ongeldig – controleer je .env-bestand.")
    else:
        print("✅: secret_key Django is geladen en ingesteld")
        return secret_key