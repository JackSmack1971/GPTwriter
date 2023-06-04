import os
import openai
import requests
import re
from colorama import Fore, Style, init

# Initialize colorama
init()

# Constants
MODEL_NAME = 'gpt-4'
NUM_TURNS = 10
TEMPERATURE = 0.09
FREQUENCY_PENALTY = 0.02
PRESENCE_PENALTY = 0

# Retrieve API key from environment variable
API_KEY = os.environ['OPENAI_API_KEY']

def open_file(file_path):
    """
    Open a file and return its contents as a string.

    Parameters:
    file_path (str): The path of the file to open.

    Returns:
    str: The contents of the file.

    Raises:
    FileNotFoundError: If the file does not exist.
    """
    with open(file_path, 'r', encoding='utf-8') as infile:
        return infile.read()

def save_file(file_path, content):
    """
    Save content to a file.

    Parameters:
    file_path (str): The path of the file to save to.
    content (str): The content to save.
    """
    with open(file_path, 'a', encoding='utf-8') as outfile:
        outfile.write(content)

def chat_gpt(api_key, conversation, chatbot, user_input):
    """
    Make an API call to the OpenAI chat completion endpoint.

    Parameters:
    api_key (str): The OpenAI API key.
    conversation (list): The conversation history.
    chatbot (str): The chatbot's initial message.
    user_input (str): The user's input message.

    Returns:
    str: The chatbot's response.
    """
    conversation.append({'role': 'user', 'content': user_input})
    messages_input = conversation.copy()
    prompt = {'role': 'system', 'content': chatbot}
    messages_input.insert(0, prompt)

    try:
        completion = openai.ChatCompletion.create(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY,
            messages=messages_input
        )
        chat_response = completion['choices'][0]['message']['content']
        conversation.append({'role': 'assistant', 'content': chat_response})
        return chat_response
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

def print_colored(agent, text, color):
    """
    Print text in a specified color if it contains certain keywords.

    Parameters:
    agent (str): The agent's name.
    text (str): The text to print.
    color (str): The color to print the text in.
    """
    print(color + f"{agent}: {text}" + Style.RESET_ALL)

def main(num_turns=NUM_TURNS):
    """
    Main function to run the chatbot conversation.

    Parameters:
    num_turns (int): The number of turns in the conversation.
    """
    conversation1 = []
    conversation2 = []
    chatbot1 = open_file('chatbot7.txt')
    chatbot2 = open_file('chatbot6.txt')
    user_message = "Hello Mr.Editor, I am Miss Writer. I'll be starting my assignment now."

    for i in range(num_turns):
        print_colored('Miss Writer', user_message, Fore.YELLOW)
        save_file('chatlog.txt', 'Miss Writer: ' + user_message + '\n')
        response = chat_gpt(API_KEY, conversation1, chatbot1, user_message)
        user_message = response
        print_colored('Mr.Editor', user_message, Fore.CYAN)
        save_file('chatlog.txt', 'Mr.Editor: ' + user_message + '\n')
        response = chat_gpt(API_KEY, conversation2, chatbot2, user_message)
        user_message = response

if __name__ == "__main__":
    main()
