import requests
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_connectivity():
    """Check if we can connect to OpenRouter and other important services"""
    
    sites_to_check = [
        "https://openrouter.ai",
        "https://api.openai.com",
        "https://google.com",
        "https://github.com"
    ]
    
    results = {}
    
    for site in sites_to_check:
        try:
            logging.info(f"Testing connection to {site}")
            start_time = time.time()
            response = requests.get(site, timeout=10)
            elapsed = time.time() - start_time
            
            results[site] = {
                "status": response.status_code,
                "time": f"{elapsed:.2f}s",
                "working": response.status_code < 400
            }
            
            logging.info(f"Connection to {site}: Status={response.status_code}, Time={elapsed:.2f}s")
        
        except requests.exceptions.Timeout:
            logging.error(f"Timeout connecting to {site}")
            results[site] = {"status": "Timeout", "time": ">10s", "working": False}
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Error connecting to {site}: {str(e)}")
            results[site] = {"status": f"Error: {str(e)}", "time": "N/A", "working": False}
    
    return results

if __name__ == "__main__":
    print("Checking network connectivity...")
    results = check_connectivity()
    
    all_working = all(result["working"] for result in results.values())
    
    if all_working:
        print("\n✅ All connectivity checks passed!")
    else:
        print("\n⚠️ Some connectivity checks failed:")
    
    for site, result in results.items():
        status = "✅ " if result["working"] else "❌ "
        print(f"{status}{site}: {result['status']} in {result['time']}")
