# Import required libraries
from google.oauth2 import service_account  # For Google Docs API authentication
from googleapiclient.discovery import build  # To build Google Docs service
from googleapiclient.errors import HttpError  # For handling Google API errors
import requests  # For making HTTP requests to Gemini API
import json  # For working with JSON data
import time
# ======================
# CONFIGURATION SECTION
# ======================

# Google Docs Configuration
DOC_ID = "1iP70rizHf-cBa690nJt-x5JnBUYvHObrRS3QPyL47tg"  # Replace with your Google Doc ID
SERVICE_ACCOUNT_FILE = r"C:\Users\jeigf\OneDrive\Documents\projects\summer-gadget-456318-s0-19d120ce90bd.json"  # Path to service account JSON
SCOPES = ["https://www.googleapis.com/auth/documents"]  # Required permissions

# Gemini API Configuration
GEMINI_API_KEY = "AIzaSyDvL2XLpQLXs7new1THyAg5EFq_auYIlug"  # Your Gemini API key
MODEL_NAME = "gemini-pro-1.0"  # Current recommended model
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Generation parameters (adjust as needed)
GENERATION_CONFIG = {
    "temperature": 0.7,  # Controls randomness (0.0-1.0)
    "topP": 0.95,  # Nucleus sampling parameter
    "topK": 40,  # Limits token selection
    "maxOutputTokens": 2048  # Maximum length of response
}

# ======================
# FUNCTION DEFINITIONS
# ======================
def generate_ai_response(prompt):
    """
    Generates AI response using Gemini API.
    
    Args:
        prompt (str): The input prompt/text to send to the AI model
        
    Returns:
        str: The generated AI response text
        
    Raises:
        Exception: If API request fails or response structure is invalid
    """
    try:
        request_data = {
            "contents": {"parts": [{"text": prompt}]},
            "generationConfig": GENERATION_CONFIG
        }

        response = requests.post(
            url=GEMINI_URL,
            headers={"Content-Type": "application/json"},
            json=request_data
        )
        response.raise_for_status()

        result = response.json()
        print("\nDEBUG - Raw API Response:")
        print(json.dumps(result, indent=2))

        if "error" in result:
            error_msg = result["error"].get("message", "Unknown Gemini API error")
            raise ValueError(f"Gemini API Error: {error_msg}")

        if not result.get("candidates"):
            raise ValueError("No response candidates found in API response")

        return result["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise Exception(f"Unexpected response format: {str(e)}")


def write_to_google_doc(text, typing_delay=1.0):
    """
    Writes text to a Google Doc, simulating human-like typing.
    
    Args:
        text (str): The text to insert
        typing_delay (float): Delay between each chunk or word
    """
    import time
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO, scopes=SCOPES
    )
    docs_service = build("docs", "v1", credentials=creds)

    current_index = 1
    chunks = [' '.join(text.split()[i:i+10]) for i in range(0, len(text.split()), 10)]

    for chunk in chunks:
        docs_service.documents().batchUpdate(
            documentId=DOC_ID,
            body={"requests": [{
                "insertText": {
                    "location": {"index": current_index},
                    "text": chunk + " "
                }
            }]}
        ).execute()

    except Exception as e:
        raise Exception(f"Error writing to doc: {str(e)}")


# ======================
# MAIN EXECUTION
# ======================

if __name__ == "__main__":
    """
    Main execution block that ties everything together.
    """
    try:
        # Example prompt
        prompt = "Give me a step-by-step guide on how to increase my bmw 330i horsepower for a good price."
        
        print("\nStarting AI text generation process...")
        print(f"Using model: {MODEL_NAME}")
        
        # Step 1: Generate AI response
        print("\n[1/2] Generating AI response...")
        ai_response = generate_ai_response(prompt)
        print("✅ AI response generated successfully!")
        
        # Step 2: Write to Google Doc
        print("\n[2/2] Writing to Google Doc...")
        write_to_google_doc(ai_response, typing_delay=1.1)
        print("✅ Text successfully added to Google Doc!")
        
        # Success message with doc link
        doc_url = f"https://docs.google.com/document/d/{DOC_ID}/edit"
        print(f"\nProcess completed successfully! View your doc at:\n{doc_url}")
        
    except Exception as e:
        # Error handling
        print(f"\n❌ Error occurred: {str(e)}")
        print("Please check:")
        print("- Your API key and model name")
        print("- Service account permissions")
        print("- Internet connection")

import os
print("🔎 File found?", os.path.isfile(r"C:\Users\jeigf\OneDrive\Documents\projects\summer-gadget-456318-s0-19d120ce90bd.json"))
