import os
import openai
import spacy
from spacy import displacy
from termcolor import colored
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Load the spacy model
nlp = spacy.load("en_core_web_sm")

# Initialize the chatbot
chatbot = ChatBot("Miss Writer")
trainer = ListTrainer(chatbot)

# Load the conversation history
with open("ChatLog.txt", "r") as file:
    conversation_history = file.readlines()

# Train the chatbot on the conversation history
trainer.train(conversation_history)

# Initialize the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the chat models
chat_models = ["gpt-4.0-turbo", "text-davinci-003"]

# Define the initial messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello Mr.Editor, I am Miss Writer. I'll be starting my assignment now."},
]

# Start the conversation
for i in range(10):
    # Get the next message from the chatbot
    user_message = chatbot.get_response(messages[-1]["content"]).text

    # Perform NER on the message
    doc = nlp(user_message)
    print("Named Entities:", [(ent.text, ent.label_) for ent in doc.ents])

    # Send the message to the chatbot
    messages.append({"role": "assistant", "content": user_message})

    # Get the response from the OpenAI API
    response = openai.ChatCompletion.create(
        model=chat_models[i % 2],
        messages=messages,
        max_tokens=150,
    )

    # Add the response to the messages
    messages.append({"role": "assistant", "content": response.choices[0].message["content"]})

    # Print the conversation
    print(colored(f"Miss Writer: {user_message}", "yellow"))
    print(colored(f"Mr.Editor: {response.choices[0].message['content']}", "cyan"))

    # Save the conversation to the chat log
    with open("ChatLog.txt", "a") as file:
        file.write(f"Miss Writer: {user_message}\n")
        file.write(f"Mr.Editor: {response.choices[0].message['content']}\n")

    # Train the chatbot on the new conversation
    trainer.train([user_message, response.choices[0].message["content"]])
