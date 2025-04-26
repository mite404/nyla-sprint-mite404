import os, requests, json
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path)

def check_model_availability():
    """Check if the specific model is available on OpenRouter"""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        return "API key not found"
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    # Try to get available models
    try:
        logging.info("Sending request to get available models")
        r = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=15
        )
        
        logging.info(f"Request completed with status code {r.status_code}")
        
        if r.status_code == 200:
            models = r.json()
            logging.info(f"Found {len(models)} models")
            
            # Check if our model is in the list
            model_id = "meta-llama/llama-4-maverick:free"
            available_models = [model.get('id') for model in models]
            
            if model_id in available_models:
                return f"Model '{model_id}' is available!"
            else:
                logging.warning(f"Model '{model_id}' not found in available models")
                close_matches = [m for m in available_models if "llama-4" in m]
                if close_matches:
                    return f"Model '{model_id}' not found. Similar models: {close_matches}"
                else:
                    return f"Model '{model_id}' not found. Available Llama models: {[m for m in available_models if 'llama' in m.lower()]}"
        else:
            return f"Error checking models: {r.status_code} - {r.text[:200]}"
    
    except Exception as e:
        return f"Error: {str(e)}"

def test_simple_completion():
    """Test a simple completion with a very short prompt"""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        return "API key not found"
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nyla-nonprofit.org",
        "X-Title": "Nyla Test"
    }
    
    # Let's try different models
    models_to_try = [
        "meta-llama/llama-3-70b-instruct:free",  # Try a different free model
        "anthropic/claude-3-opus:free",
        "google/gemini-pro:free"
    ]
    
    for model in models_to_try:
        try:
            logging.info(f"Testing model: {model}")
            
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": "Say hello in one sentence."}],
                "temperature": 0.7,
                "max_tokens": 100  # Keep it very small
            }
            
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=15  # Short timeout
            )
            
            logging.info(f"Request for {model} completed with status {r.status_code}")
            
            if r.status_code == 200:
                response = r.json()
                return f"Success with {model}: {response['choices'][0]['message']['content']}"
            else:
                logging.warning(f"Error with {model}: {r.status_code} - {r.text[:200]}")
        
        except Exception as e:
            logging.error(f"Exception with {model}: {str(e)}")
    
    return "All model tests failed"

if __name__ == "__main__":
    print("Checking model availability...")
    print(check_model_availability())
    
    print("\nTesting a simple completion...")
    print(test_simple_completion())
