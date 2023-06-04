import os
import openai
import requests
import re
from colorama import Fore, Style, init
import argparse

# Initialize colorama
init()

# Constants
API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = 'gpt-4'

def parse_args():
    parser = argparse.ArgumentParser(description='Chatbot conversation simulator.')
    parser.add_argument('--num_turns', type=int, default=10, help='Number of conversation turns')
    parser.add_argument('--api_key_file', type=str, default='api_key.txt', help='File containing the OpenAI API key')
    parser.add_argument('--chat_bot_file1', type=str, default='chat_bot1.txt', help='File containing the first chat bot')
    parser.add_argument('--chat_bot_file2', type=str, default='chat_bot2.txt', help='File containing the second chat bot')
    parser.add_argument('--initial_message', type=str, default='Hello Mr.Editor, I am Miss Writer. I\'ll be starting my assignment now.', help='Initial user message')
    return parser.parse_args()

def open_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            return infile.read()
    except FileNotFoundError:
        raise FileNotFoundError(f'File {file_path} not found')

def save_file(file_path, content):
    with open(file_path, 'a', encoding='utf-8') as outfile:
        outfile.write(content)

def set_api_key(api_key_file):
    api_key = open_file(api_key_file)
    openai.api_key = api_key

def prepare_conversation(conversation, user_input):
    conversation.append({'role': 'user', 'content': user_input})
    return conversation

def make_api_call(api_key, conversation, chat_bot, user_input, temperature=0.9, frequency_penalty=0.2, presence_penalty=0):
    messages_input = conversation.copy()
    prompt = {'role': 'system', 'content': chat_bot}
    messages_input.insert(0, prompt)
    try:
        completion = openai.ChatCompletion.create(
            model=MODEL_NAME,
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            messages=messages_input
        )
        chat_response = completion['choices'][0]['message']['content']
        conversation.append({'role': 'assistant', 'content': chat_response})
        return chat_response
    except Exception as e:
        raise Exception(f'An error occurred: {e}')

def chat_gpt(api_key, conversation, chat_bot, user_input):
    conversation = prepare_conversation(conversation, user_input)
    chat_response = make_api_call(api_key, conversation, chat_bot, user_input)
    return chat_response

def print_colored(agent, text, color):
    print(color + f'{agent}: {text}' + Style.RESET_ALL, end='')

def run_conversation(api_key, num_turns, chat_bot_file1, chat_bot_file2, initial_message):
    conversation1 = []
    conversation2 = []
    chat_bot1 = open_file(chat_bot_file1)
    chat_bot2 = open_file(chat_bot_file2)
    user_message = initial_message
    for i in range(num_turns):
        print_colored('Miss Writer', f'{user_message}\n', Fore.YELLOW)
        save_file('chat_log.txt', 'Miss Writer: ' + user_message + '\n\n')
        response = chat_gpt(api_key, conversation1, chat_bot1, user_message)
        user_message = response
        print_colored('Mr.Editor', f```python
'{user_message}\n', Fore.CYAN)
        save_file('chat_log.txt', 'Mr.Editor: ' + user_message + '\n\n')
        response = chat_gpt(api_key, conversation2, chat_bot2, user_message)
        user_message = response

def main():
    args = parse_args()
    set_api_key(args.api_key_file)
    run_conversation(API_KEY, args.num_turns, args.chat_bot_file1, args.chat_bot_file2, args.initial_message)

if __name__ == '__main__':
    main()
