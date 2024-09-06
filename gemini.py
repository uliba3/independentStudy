# Import the Python SDK
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
# Used to securely store your API key
import os
from dotenv import load_dotenv
import time
from queue import Queue

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

model={}
model["flash"] = genai.GenerativeModel('gemini-1.5-flash')
model["pro"] = genai.GenerativeModel('gemini-1.5-pro')

que = {}
que["flash"] = Queue(maxsize = 15)
que["pro"] = Queue(maxsize = 15)

def runModel(modelName, prompt):
    while que[modelName].full() and que[modelName].queue[0] > time.time() - 60:
        time.sleep(1)
    if que[modelName].full():
        que[modelName].get()
    time.sleep(3)
    response = model[modelName].generate_content(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT : HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT : HarmBlockThreshold.BLOCK_NONE
        }
    )
    que[modelName].put(time.time())
    print(f"prompt: {prompt}\nresponse: {response.text}")
    return response.text

if __name__ == "__main__":
    runModel("flash", "Do you like me?")