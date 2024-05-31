from fastapi import FastAPI, HTTPException, Response
import aiohttp
import nest_asyncio
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from dotenv import load_dotenv

load_dotenv()

global text_history

model_api_url = "http://localhost:8000/v1/chat/completions"
model_api_token = "abc123"

system_prompt = "You are a conversational assistant for a bank who replies in a very human like tone. Given the following conversation, generate the next human like response for the user."
init_reply = ""

async def create_prompt_template(system_prompt, init_reply, prompt):
    
    return {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "messages": [
            {"role": "user", "content": system_prompt},
            {"role": "assistant", "content": init_reply},
            {"role": "user", "content": prompt}
        ]
    }

# Function to send the request to the API
async def send_request_async(system_prompt, init_reply, prompt):
    async with aiohttp.ClientSession() as session:
        prompt_template = await create_prompt_template(system_prompt, init_reply, prompt)
        async with session.post(model_api_url, json=prompt_template, headers={"Authorization": f"Bearer {model_api_token}"}) as response:
            return await response.json()
        
def prompt_format(text_history, new_text):
    return f"Text History:{text_history}\nUser{new_text}"

def summary_former(text):
    return f"{text_history}\nUser: {text}"


app = FastAPI()
@app.post("/chat")
async def chat(user_input: str):
    text_history = 'Hello What can I help you with today?'
    formatted_prompt = prompt_format(text_history, user_input)
    print(formatted_prompt)
    response = await send_request_async(system_prompt, init_reply, formatted_prompt)
    print (response)
    assistant_reply = response.get("choices")[0].get("message").get("content")
    text_history += f"User: {user_input}\nAssistant: {assistant_reply}\n"
    return {'text': assistant_reply}
