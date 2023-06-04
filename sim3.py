import openai
import os
import requests
import re
from colorama import Fore, Style, init


# Initialize colorama
init()

# Define a function to open a file and return its contents as a string
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# Define a function to save content to a file
def save_file(filepath, content):
    with open(filepath, 'a', encoding='utf-8') as outfile:
        outfile.write(content)

# Set the OpenAI API keys by reading them from files
api_key = open_file('openaiapikey2.txt')

# Initialize two empty lists to store the conversations for each chatbot
conversation1 = []
conversation2 = []

# Read the content of the files containing the chatbots' prompts
chatbot1 = open_file('chatbot7.txt')
chatbot2 = open_file('chatbot6.txt')

# Define a function to make an API call to the OpenAI ChatCompletion endpoint
def chatgpt(api_key, conversation, chatbot, user_input, temperature=0.9, frequency_penalty=0.2, presence_penalty=0):

    # Set the API key
    openai.api_key = api_key

    # Update conversation by appending the user's input
    conversation.append({"role": "user","content": user_input})

    # Insert prompt into message history
    messages_input = conversation.copy()
    prompt = [{"role": "system", "content": chatbot}]
    messages_input.insert(0, prompt[0])

    # Make an API call to the ChatCompletion endpoint with the updated messages
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messages_input)

    # Extract the chatbot's response from the API response
    chat_response = completion['choices'][0]['message']['content']

    # Update conversation by appending the chatbot's response
    conversation.append({"role": "assistant", "content": chat_response})

    # Return the chatbot's response
    return chat_response

    
# Add a function to print text in green if it contains certain keywords
def print_colored(agent, text):
    agent_colors = {
        "Miss Writer:": Fore.YELLOW,
        "Mr.Editor:": Fore.CYAN,
    }

    color = agent_colors.get(agent, "")

    print(color + f"{agent}: {text}" + Style.RESET_ALL, end="")  

num_turns = 10  # Number of turns for each chatbot (you can adjust this value)

# Start the conversation with ChatBot1's first message
user_message = "Hello Mr.Editor. I am Miss Writer. I'll be starting my assignment now."

# Update the loop where chatbots talk to each other
for i in range(num_turns):
    print_colored("Miss Writer:", f"{user_message}\n\n")
    save_file("ChatLog.txt", "Miss Writer: " + user_message + "\n\n")
    response = chatgpt(api_key, conversation1, chatbot1, user_message)
    user_message = response

    print_colored("Mr.Editor:", f"{user_message}\n\n")
    save_file("ChatLog.txt", "Mr.Editor: " + user_message + "\n\n")
    response = chatgpt(api_key, conversation2, chatbot2, user_message)
    user_message = response
