import os
import openai
import requests
import re
from colorama import Fore, Style, init

# Initialize colorama
init()

# Constants
API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = "gpt-4"
NUM_TURNS = 10

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
    with open(filepath, 'a', encoding='utf-8') as outfile:
        outfile.write(content)

def chatgpt(api_key, conversation, chatbot, user_input, temperature=0.9, frequency_penalty=0.2, presence_penalty=0):
    """
    Make an API call to the OpenAI ChatCompletion endpoint.
    """
    openai.api_key = api_key
    conversation.append({"role": "user","content": user_input})
    messages_input = conversation.copy()
    prompt = [{"role": "system", "content": chatbot}]
    messages_input.insert(0, prompt[0])
    try:
        completion = openai.ChatCompletion.create(
            model=MODEL_NAME,
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            messages=messages_input
        )
        chat_response = completion['choices'][0]['message']['content']
        conversation.append({"role": "assistant", "content": chat_response})
        return chat_response
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def print_colored(agent, text, color):
    """
    Print text in green if it contains certain keywords.
    """
    print(color + f"{agent}: {text}" + Style.RESET_ALL, end="")  

def main(num_turns=NUM_TURNS):
    """
    Main function to run the chatbot conversation.
    """
    api_key = API_KEY
    conversation1 = []
    conversation2 = []
    chatbot1 = open_file('chatbot7.txt')
    chatbot2 = open_file('chatbot6.txt')
    user_message = "Hello Mr.Editor. I am Miss Writer. I'll be starting my assignment now."
    for i in range(num_turns):
        print_colored("Miss Writer:", f"{user_message}\n\n", Fore.YELLOW)
        save_file("ChatLog.txt", "Miss Writer: " + user_message + "\n\n")
        response = chatgpt(api_key, conversation1, chatbot1, user_message)
        user_message = response
        print_colored("Mr.Editor:", f"{user_message}\n\n", Fore.CYAN)
        save_file("ChatLog.txt", "Mr.Editor: " + user_message + "\n\n")
        response = chatgpt(api_key, conversation2, chatbot2, user_message)
        user_message = response

if __name__ == "__main__":
    main()
