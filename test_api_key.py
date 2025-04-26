import os, requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_api_key():
    """Test the OpenRouter API key to verify it's working"""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        return "API key not found in environment variables"
    
    # Try to get information about the key
    try:
        r = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        print(f"Status code: {r.status_code}")
        print(f"Headers: {r.headers}")
        
        if r.status_code == 200:
            return f"API key is valid. Response: {r.text[:200]}"
        else:
            return f"API key validation failed. Status: {r.status_code}, Response: {r.text[:200]}"
    
    except Exception as e:
        return f"Error checking API key: {e}"

if __name__ == "__main__":
    result = check_api_key()
    print(result)
