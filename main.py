import argparse, os, sys, time, requests, json
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file - specify the path explicitly
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path)

# Debug output to verify environment loading
api_key = os.getenv("OPENROUTER_API_KEY")
logging.info(f"API Key found: {api_key is not None}")
if api_key:
    logging.info(f"API Key length: {len(api_key)}")
    logging.info(f"API Key prefix: {api_key[:10]}...")
# Model and endpoint configuration
# Use default model selection from OpenRouter instead of specifying a model
# This lets OpenRouter choose the best available model
MODEL="openai/gpt-3.5-turbo"  # OpenAI compatible endpoint
ENDPOINT="https://openrouter.ai/api/v1/chat/completions"  # Corrected endpoint with /api/
def build_prompt(args):
    return f"Write five fundraising emails and four social captions for the {args.event} on {args.date} in a {args.tone} tone."
def chat_completion(prompt):
    # Explicitly get the API key from environment
    key = os.environ.get("OPENROUTER_API_KEY")

    # Final check
    if not key:
        sys.exit("missing OPENROUTER_API_KEY")
    
    # Check if API key has the correct format (should start with sk-or-)
    if not key.startswith("sk-or-"):
        print(f"Warning: API key format may be incorrect. OpenRouter keys typically start with 'sk-or-'", file=sys.stderr)
    
    payload={
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,  # Adding reasonable temperature
        "max_tokens": 2000   # Setting reasonable max_tokens
    }
    
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json", 
        "HTTP-Referer": "https://nyla-nonprofit.org", 
        "X-Title": "Nyla Nonprofit Email Generator"
    }
    
    print(f"Sending request to {ENDPOINT}...", file=sys.stderr)
    t0=time.time()
    
    try:
        logging.info(f"Starting request to OpenRouter with payload: {json.dumps(payload)}")
        logging.info(f"Using headers: {headers}")
        # Increase timeout to 90 seconds to allow for longer processing time
        logging.info("Sending request with 90 second timeout...")
        r=requests.post(ENDPOINT, headers=headers, json=payload, timeout=90)
        dt=time.time()-t0
        logging.info(f"Request finished after {dt:.2f}s")
        
        print(f"Request completed in {dt:.2f}s with status code {r.status_code}", file=sys.stderr)
        
        # Print response for debugging
        print(f"Response headers: {r.headers}", file=sys.stderr)
        print(f"Response text (first 200 chars): {r.text[:200]}", file=sys.stderr)
        
        if r.status_code != 200:
            sys.exit(f"HTTP {r.status_code}: {r.text[:120]}")
        
        # Try to parse JSON, handle errors explicitly
        try:
            response_json = r.json()
            return response_json["choices"][0]["message"]["content"]
        except json.JSONDecodeError as e:
            sys.exit(f"Failed to parse JSON response: {e}. Response: {r.text[:200]}")
        except KeyError as e:
            sys.exit(f"Expected key not found in response: {e}. Response structure: {response_json}")
    
    except requests.exceptions.RequestException as e:
        sys.exit(f"Request failed: {e}")
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--event",default="Community Gala"); p.add_argument("--date",default="TBD"); p.add_argument("--tone",default="upbeat"); p.add_argument("--dry-run",action="store_true")
    a=p.parse_args()
    prompt=build_prompt(a)
    if a.dry_run:
        print(prompt); return
    out=chat_completion(prompt)
    os.makedirs("out",exist_ok=True)
    with open("out/campaign.md","w") as f: f.write(out)
    print(out)
if __name__=="__main__":
    main()
