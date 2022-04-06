from asyncio import Handle
from dotenv import load_dotenv
from random import choice
from flask import Flask, request 
import os
import openai
from gpt import GPT
from gpt import Example
import json

load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")
HALF1 = "sk-eM9uloe6yYSIUew4PVCyT3Bl"
HALF2 = "bkFJ6hVbyqKbivJ5AyIbkMCl"
openai.api_key = HALF1+HALF2
completion = openai.Completion()

start_sequence = "\nLoneX:"
restart_sequence = "\n\nPerson:"
session_prompt = "Hello there, my name is LoneX, how can I help you?"
gpt = None
def ask(question, chat_log=None):
    prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
    response = openai.Completion.create(
      engine="davinci",
      prompt=prompt_text,
      temperature=0.8,
      max_tokens=150,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0.3,
      stop=["\n"],
    )
    story = response['choices'][0]['text']
    return str(story)

def show_da_way():
    global gpt 
    gpt = GPT(engine="davinci",
          temperature=0.5,
          max_tokens=100)
    gpt.add_example(Example('Fetch unique values of color from Car table.', 
                        'Select distinct color from Car;'))
    gpt.add_example(Example('Print the first three characters of brand from Car table.', 
                        'Select substring(brand,1,3) from Car;'))
    gpt.add_example(Example("Find the position of the alphabet ('a') in the first name column 'Audi' from Car table.", 
                        "Select INSTR(brand, BINARY'a') from Car where brand = 'Audi';"))
    return gpt
                        
def ask_sql(question):
    if gpt is not None:
        print(f"///////////gpt intialized...asking question {question}///////////")
        output = gpt.submit_request(question)
        return output.choices[0].text
    else:
        show_da_way()
        ask_sql(question)
    return "ERROR: GPT is None !"

def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
