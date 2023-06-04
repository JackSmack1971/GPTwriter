import os
import openai
import requests
import re
from colorama import Fore, Style, init

# Initialize colorama
init()

API_KEY_FILE = 'openaiapikey2.txt'
CHATBOT1_FILE = 'chatbot7.txt'
CHATBOT2_FILE = 'chatbot6.txt'
LOG_FILE = 'ChatLog.txt'
MISS_WRITER = "Miss Writer:"
MR_EDITOR = "Mr.Editor:"

def open_file(filepath):
    """
    Open a file and return its contents as a string.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()
    except FileNotFoundError:
        print(f"File {filepath} not found.")
        return None

def save_file(filepath, content):
    """
    Save content to a file.
    """
    try:
        with open(filepath, 'a', encoding='utf-8') as outfile:
            outfile.write(content)
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

def chatgpt(api_key, conversation, chatbot, user_input, temperature=0.9, frequency_penalty=0.2, presence_penalty=0):
    """
    Make an API call to the OpenAI ChatCompletion endpoint.
    """
    try:
        openai.api_key = api_key
        conversation.append({"role": "user","content": user_input})
        messages_input = conversation.copy()
        prompt = [{"role": "system", "content": chatbot}]
        messages_input.insert(0, prompt[0])
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            messages=messages_input
        )
        chat_response = completion['choices'][0]['message']['content']
        conversation.append({"role": "assistant", "content": chat_response})
        return chat_response
    except Exception as e:
        print(f"An error occurred while making the API call: {e}")

def print_colored(agent, text):
    """
    Print text in green if it contains certain keywords.
    """
    agent_colors = {
        MISS_WRITER: Fore.YELLOW,
        MR_EDITOR: Fore.CYAN,
    }
    color = agent_colors.get(agent, "")
    print(color + f"{agent}: {text}" + Style.RESET_ALL, end="")  

def run_conversation(api_key, num_turns=10):
    """
    Run the chatbot conversation.
    """
    conversation1 = []
    conversation2 = []
    chatbot1 = open_file(CHATBOT1_FILE)
    chatbot2 = open_file(CHATBOT2_FILE)
    user_message = "Hello Mr.Editor. I am Miss Writer. I'll be starting my assignment now."
    for i in range(num_turns):
        print_colored(MISS_WRITER, f"{user_message}\n\n")
        save_file(LOG_FILE, MISS_WRITER + user_message + "\n\n")
        response = chatgpt(api_key, conversation1, chatbot1, user_message)
        user_message = response
        print_colored(MR_EDITOR, f"{user_message}\n\n")
        save_file(LOG_FILE, MR_EDITOR + user_message + "\n\n")
        response = chatgpt(api_key, conversation2, chatbot2, user_message)
        user_message = response

def main():
    api_key = open_file(API_KEY_FILE)
    run_conversation(api_key)

if __name__ == "__main__":
    main()
