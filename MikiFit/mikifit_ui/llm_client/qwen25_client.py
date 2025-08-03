"""
--------------------------------------
 Qwen2.5_client (locale llm)
--------------------------------------
De class 'Qwen25LocalClient' beheert communicatie met lokale Qwen2.5 server
via OpenAI-compatibele API endpoints.
Functionaliteiten:
- OpenAI client initialisatie met lokale server configuratie
- Instructieprompt configuratie voor model gedrag
- Chat message handling (ontvangen/versturen)
- Error handling voor server communicatie
- Request/response formatting volgens OpenAI standaard
"""
import logging
import openai
from pathlib import Path
from env_manager import var_ip_setup

# Configureer logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class Qwen25LocalClient:
    def __init__(self):
        """
        Initialiseert OpenAI client voor lokale LLM server
        """
        self.client = openai.OpenAI(
            base_url= var_ip_setup(),
            api_key='dummy_key'
        )
        # Initialiseer chat_history als instance variabele
        self.chat_history = []

    def prompt_loader(self):
        """
        Laadt de instructieprompt voor de config van model gedrag
        """
        BASE_DIR = Path(__file__).resolve().parent.parent
        prompt_path = BASE_DIR / "data" / "prompt" / "kledingadviseur.txt"
        
        try:
            with prompt_path.open("r", encoding="utf-8") as file:
                self.prompt_kledingadvies = file.read()
        except FileNotFoundError:
            logger.exception(f"❌: Promptbestand niet gevonden – {prompt_path}")
            raise
        
        instructions = [{"role": "system", "content": self.prompt_kledingadvies}]
        return instructions

    def message_handler(self, user_message: str) -> str:
        """
        Handelt de ontvangst van de prompt en berichten tussen user en system af
        """
        # Laadt de systemprompt
        system_messages = self.prompt_loader()
        
        # Voegt gebruikersbericht toe aan chatgeschiedenis
        self.chat_history.append({"role": "user", "content": user_message})
        
        # Combineer system prompt + chat history voor de API call
        system_messages = self.prompt_loader()
        messages = system_messages + self.chat_history
        
        # DEBUG: Print wat er wordt verstuurd
        print("DEBUG - Messages being sent to API:")
        for i, msg in enumerate(messages):
            print(f"  {i}: {msg}")
        print(f"DEBUG - Type of messages: {type(messages)}")
        
        try:
            response = self.client.chat.completions.create(
                model="qwen2.5-14b",
                messages=messages,
                temperature=0.7  # Bepaalt hoe creatief/random berichten zijn
            )
            
            # Verwerkt antwoorden assistent en voegt deze toe aan chatgeschiedenis
            assistant_berichten = response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": assistant_berichten})
            
            logger.info("✅: Verbinding succesvol tot stand gekomen")
            return assistant_berichten
            
        except Exception as e:
            logger.error(f"❌: Verbinding mislukt: {e}")
            return f"Er is een fout opgetreden: {str(e)}"

if __name__ == "__main__":
    client = Qwen25LocalClient()
    # Test message toevoegen
    result = client.message_handler("Hallo, kun je jezelf voorstellen?")
    print(result)