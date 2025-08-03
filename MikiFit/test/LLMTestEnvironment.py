"""
--------------------------------------
                Test ENV
-------------------------------------- 
"""
import logging
import openai
import time

# Configureer logger
logger = logging.getLogger(__name__)                                            
logging.basicConfig(level=logging.INFO,format="%(asctime)s [%(levelname)s] %(message)s") 

class LLMTestEnvironment:
    def __init__(self):
        self.client = openai.OpenAI(                    
            base_url="http://192.168.2.17:8080",
            api_key= 'dummy_key'
        )
        
    def test_connection(self):
        try:
            response = self.client.chat.completions.create(
                model="Qwen2.5-14B",
                messages=[{"role": "user", "content": "Hello"}],
                temperature=0.7
            )
            
            logger.info("✅: Verbinding werkt!")
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"❌: Verbinding mislukt: {e}")
            return None
            
    def test_model_capabilities(self):
        """Test verschillende aspecten van het model"""
        tests = [
            {
                "name": "Basis chat",
                "messages": [{"role": "user", "content": "Wat is 2+2?"}]
            },
            {
                "name": "Context behoud",
                "messages": [
                    {"role": "user", "content": "Mijn naam is Jan"},
                    {"role": "assistant", "content": "Hallo Jan!"},
                    {"role": "user", "content": "Wat is mijn naam?"}
                ]
            }
        ]
        
        results = {}
        for test in tests:
            try:
                response = self.client.chat.completions.create(
                    model="qwen2.5-14b",
                    messages=test["messages"]
                )
                results[test["name"]] = {
                    "success": True,
                    "response": response.choices[0].message.content
                }
                logger.info(f"✅ Test '{test['name']}' succesvol")
            except Exception as e:
                results[test["name"]] = {
                    "success": False,
                    "error": str(e)
                }
                logger.error(f"❌ Test '{test['name']}' mislukt: {e}")
                
        return results

    def test_performance(self):
        """Test response tijden en model prestaties"""
        start_time = time.time()
        result = self.test_connection()
        response_time = time.time() - start_time
        
        logger.info(f"Response tijd: {response_time:.2f} seconden")
        return {
            "response_time": response_time,
            "success": result is not None
        }

# Run de test
client = LLMTestEnvironment()
connection_test = client.test_connection()
capabilities = client.test_model_capabilities()
performance = client.test_performance()

# Print resultaten
print("Test resultaten:")
print(f"Verbinding: {'✅' if connection_test else '❌'}")
print(f"Capabilities: {capabilities}")
print(f"Performance: {performance}")