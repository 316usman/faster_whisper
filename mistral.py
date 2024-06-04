from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

global text_history

client = Groq(
    api_key="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",
)
system_prompt = "You are a conversational assistant for a bank who replies in a very human like tone. Given the following conversation, generate the next human like response for the user. Keep responses limited to one liner sentences or phrases."
def create_prompt_template(system_prompt, prompt):
    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    return {
            "messages": messages,
            "model": "llama3-8b-8192"
        }

# Function to send the request to the API
def send_request_async(system_prompt, init_reply, prompt):
    prompt_template = create_prompt_template(system_prompt, prompt)
    chat_completion = client.chat.completions.create(prompt_template)
    return chat_completion.choices[0].message.content

def prompt_format(text_history, new_text):
    return f"Text History: {text_history}\nUser: {new_text}"

def summary_former(text):
    return f"{text_history}\nUser: {text}"


@app.post("/chat")
class ChatRequest(BaseModel):
    user_input: str

async def chat(request: ChatRequest):
    user_input = request.user_input
    print(user_input)
    text_history = 'Hello What can I help you with today?'
    formatted_prompt = prompt_format(text_history, user_input)
    print(formatted_prompt)
    response = send_request_async(system_prompt, formatted_prompt)
    print(response)
    assistant_reply = response.get("choices")[0].get("message").get("content")
    text_history += f"User: {user_input}\nAssistant: {assistant_reply}\n"
    return {'text': assistant_reply}