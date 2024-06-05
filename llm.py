from fastapi import FastAPI, HTTPException, Response
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

text_history = ""
client = Groq(
    api_key="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",
)
system_prompt = "You are a conversational assistant for a bank who replies in a very human like tone. Given the following conversation, generate the next human like response for the user on the last user text. Keep responses limited to one liner sentences or phrases."
def create_prompt_template(system_prompt, prompt):
    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    return messages

# Function to send the request to the API
def send_request_async(system_prompt, prompt):
    prompt_template = create_prompt_template(system_prompt, prompt)
    print("++++++++++++++++++++++++")
    print (prompt_template)
    chat_completion = client.chat.completions.create(messages = prompt_template , model="llama3-8b-8192")
    print (chat_completion)
    return chat_completion.choices[0].message.content

def prompt_format(text_history, new_text):
    return f"{text_history}\nUser: {new_text}"

def summary_former(text, user_type):
    global text_history
    if user_type == 'user':
        text_history = f"{text_history}\nUser: {text}"
    if user_type == 'assistant':
        text_history = f"{text_history}\nAssistant: {text}"

app = FastAPI()
@app.post("/chat")
def chat(user_input):
    global text_history 
    summary_former(user_input, 'user')
    formatted_prompt = prompt_format(text_history, user_input)
    response = send_request_async(system_prompt, formatted_prompt)
    summary_former(response, 'assistant')
    print("++++++++++++++++++++++++")
    print (text_history)
    return {'text': response} 
