import os, requests, json
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path)

def list_available_models():
    """List all available models from OpenRouter"""
    
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        return "API key not found"
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    try:
        logging.info("Requesting available models from OpenRouter")
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=15
        )
        
        if response.status_code == 200:
            try:
                models_data = response.json()
                
                # Pretty print the first model to see its structure
                if models_data and len(models_data) > 0:
                    logging.info(f"First model structure: {json.dumps(models_data[0], indent=2)}")
                
                # Extract model IDs and names
                model_info = []
                for model in models_data:
                    model_id = model.get('id', 'Unknown ID')
                    model_name = model.get('name', 'Unknown Name')
                    context_length = model.get('context_length', 'Unknown')
                    pricing = model.get('pricing', {})
                    
                    # Check if it's a free model
                    is_free = 'free' in model_id.lower()
                    
                    model_info.append({
                        'id': model_id,
                        'name': model_name,
                        'context_length': context_length,
                        'pricing': pricing,
                        'is_free': is_free
                    })
                
                # Sort to show free models first
                model_info.sort(key=lambda x: (not x['is_free'], x['id']))
                
                print("\n== Available Models on OpenRouter ==\n")
                for model in model_info:
                    free_tag = "[FREE]" if model['is_free'] else ""
                    print(f"{model['id']} {free_tag}")
                    print(f"  Name: {model['name']}")
                    print(f"  Context Length: {model['context_length']}")
                    print("")
                
                print(f"Total models available: {len(model_info)}")
                print(f"Free models: {len([m for m in model_info if m['is_free']])}")
                
                return model_info
            
            except json.JSONDecodeError:
                logging.error("Failed to parse response as JSON")
                logging.error(f"Response: {response.text[:200]}")
                return None
        else:
            logging.error(f"Error getting models: {response.status_code}")
            logging.error(f"Response: {response.text[:200]}")
            return None
    
    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        return None

if __name__ == "__main__":
    models = list_available_models()
    if not models:
        print("Failed to retrieve models from OpenRouter")
