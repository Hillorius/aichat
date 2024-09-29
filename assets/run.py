import requests
import colorama
import re
from colorama import Fore
import json
import os
import random
import time 

colorama.init(autoreset=True)

ascii_art_lines = [
    r"                                                                                 ,----, ",
    r"                                                       ,--,                    ,/   .`| ",
    r"         ,---,         ,---,          ,----..        ,--.'|   ,---,          ,`   .'  : ",
    r"        '  .' \     ,`--.' |         /   /   \    ,--,  | :  '  .' \       ;    ;     / ",
    r"       /  ;    '.   |   :  :        |   :     :,---.'|  : ' /  ;    '.   .'___,/    ,'  ",
    r"      :  :       \  :   |  '        .   |  ;. /|   | : _' |:  :       \  |    :     |   ",
    r"      :  |   /\   \ |   :  |        .   ; /--` :   : |.'  |:  |   /\   \ ;    |.';  ;   ",
    r"      |  :  ' ;.   :'   '  ;        ;   | ;    |   ' '  ; :|  :  ' ;.   :`----'  |  |   ",
    r"      |  |  ;/  \   \   |  |        |   : |    '   |  .'. ||  |  ;/  \   \   '   :  ;   ",
    r"      '  :  | \  \ ,'   :  ;        .   | '___ |   | :  | ''  :  | \  \ ,'   |   |  '   ",
    r"      |  |  '  '--' |   |  '        '   ; : .'|'   : |  : ;|  |  '  '--'     '   :  |   ",
    r"      |  :  :       '   :  |        '   | '/  :|   | '  ,/ |  :  :           ;   |.'    ",
    r"      |  | ,'       ;   |.'         |   :    / ;   : ;--'  |  | ,'           '---'      ",
    r"      `--''         '---'            \   \ .'  |   ,/      `--''                        ",
    r"                                      `---`    '---'                                    ",
    r"",
    r"By-Hillorius",
    r"",
    r"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┣━",
    r"                                                                                                    "
]

colorama.init(autoreset=True)

def print_gradient_art(lines):
    colors = [colorama.Fore.CYAN, colorama.Fore.LIGHTBLUE_EX, colorama.Fore.CYAN, colorama.Fore.LIGHTBLUE_EX, colorama.Fore.CYAN, colorama.Fore.BLUE]
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(color + line)

def load_intents(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{file_path}' contains invalid JSON.")
        return None

def match_intent(user_input, intents):
    for intent in intents:
        for pattern in intent['patterns']:
            if pattern.lower() in user_input.lower():
                return intent
    return {"name": "default", "responses": ["Sorry, I didn't understand that. Can you try again?"]}

def clean_ai_response(response):
    return response.strip()

def generate(messages, model="Sao10K/L3-70B-Euryale-v2.1", max_tokens=550):
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    json_data = {
        'model': model,
        'messages': messages,
        'stream': False,
        'max_tokens': max_tokens,
    }

    response = requests.post('https://api.deepinfra.com/v1/openai/chat/completions', headers=headers, json=json_data)
    if response.status_code == 200:
        response_json = response.json()
        if 'choices' in response_json:
            return response_json['choices'][0]['message']['content']
        else:
            return {'error': 'No choices found'}
    else:
        return {'error': f"API Error: {response.status_code}", 'message': response.text}

def simulate_real_time_response(response, color=colorama.Fore.GREEN, delay=0.015, variance=0.01):
    for char in response:
        print(color + char, end='', flush=True)
        time.sleep(delay + random.uniform(-variance, variance))
    print()


def save_chat_history(messages, initial_prompt):
    chat_data = {
        "personality": initial_prompt,
        "messages": messages
    }

    os.makedirs('assets', exist_ok=True)

    file_path = f'assets/chat_history_{initial_prompt}.json'
    with open(file_path, 'w') as file:
        json.dump(chat_data, file, indent=4)
    print(Fore.GREEN + "Chat history saved successfully!")

def display_main_menu():
    print_gradient_art(ascii_art_lines)
    print(Fore.YELLOW + "\n--- Main Menu ---")
    print("1. Start new chat")
    print("2. View chat history")
    print("3. Exit")
    choice = input(Fore.GREEN + "Select an option: ")

    if choice == '1':
        clear()
        print_gradient_art(ascii_art_lines)
        chat_with_ai()
    elif choice == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        load_and_display_personality_list()
    elif choice == '3':
        os.system('cls' if os.name == 'nt' else 'clear')
        print_gradient_art(ascii_art_lines)
        time.sleep(1.5)
        print(Fore.RED + "Exiting. Goodbye!")
        exit()
    else:
        print(Fore.RED + "Invalid option! Returning to menu.")
        display_main_menu()

def load_and_display_personality_list():
    personalities = []

    if os.path.exists('assets'):
        for file_name in os.listdir('assets'):
            if file_name.startswith('chat_history_') and file_name.endswith('.json'):
                personality = file_name.replace('chat_history_', '').replace('.json', '')
                personalities.append(personality)

    if personalities:
        print(Fore.CYAN + "\n--- Chat Histories ---")
        for i, personality in enumerate(personalities, 1):
            print(Fore.LIGHTBLUE_EX + f"{i}. {personality}")

        choice = input(Fore.GREEN + "Select a personality to continue the chat, or type 'back' to return: ")

        if choice.isdigit() and 1 <= int(choice) <= len(personalities):
            selected_personality = personalities[int(choice) - 1]
            continue_chat(selected_personality)
        elif choice.lower() == 'back':
            display_main_menu()
        else:
            print(Fore.RED + "Invalid choice, returning to menu.")
            display_main_menu()
    else:
        print(Fore.RED + "No chat history found.")
        display_main_menu()

# Function to continue chat with a selected personality
def continue_chat(personality):
    file_path = f'assets/chat_history_{personality}.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            chat_history = json.load(file)
            messages = chat_history['messages']
            print(Fore.CYAN + f"\n--- Continuing chat with AI Personality: {personality} ---")
            for msg in chat_history['messages']:
                role = msg['role']
                content = msg['content']
                if role == "user":
                    print(Fore.CYAN + "You: " + content)
                else:
                    print(Fore.MAGENTA + content)

            chat_with_ai(personality, messages)
    else:
        print(Fore.RED + f"No chat found for personality: {personality}.")
        display_main_menu()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to chat with the AI
def chat_with_ai(initial_prompt=None, messages=None):
    if not initial_prompt:
        initial_prompt = input(Fore.GREEN + "Enter the initial personality or prompt for the AI (e.g., witty, friendly, formal): ")
        if initial_prompt and not re.match('^[a-zA-Z0-9_]+$', initial_prompt):
            print(Fore.RED + "Invalid personality name. Only alphabets, numbers and underscores are allowed.")
            initial_prompt = input(Fore.GREEN + "Enter the initial personality or prompt for the AI (e.g., witty, friendly, formal): ")
        print(Fore.YELLOW + f"Personality set to: {initial_prompt}")
        messages = [
            {"role": "system", "content": f"You are a person with a {initial_prompt} personality. Be engaging and provide short responses full of emotion. Do not mimic the user. PLEASE SHORT RESPONDDD PLEASE.."},
        ]

    last_user_input = None

    while True:
        user_input = input(Fore.CYAN + "You: ")

        if user_input.lower() in ['exit', 'back', 'menu']:
            print(Fore.RED + "Returning to main menu...")
            save_chat_history(messages, initial_prompt)
            clear()
            display_main_menu()
            break

        elif user_input.lower() == 'save':
            print(Fore.YELLOW + "Saving chat history...")
            save_chat_history(messages, initial_prompt)
            continue


        elif user_input.lower() == 'reset':
            print(Fore.YELLOW + "Resetting conversation...")
            messages = [
                {"role": "system", "content": f"Reset personality. Respond as a {initial_prompt} character."},
            ]
            clear()
            print_gradient_art(ascii_art_lines)
            continue

        elif user_input.lower() == 'retry':
            if last_user_input is None:
                print(Fore.RED + "No previous message to retry.")
                continue
            print(Fore.YELLOW + "Retrying last message...")
            user_input = last_user_input

        messages.append({"role": "user", "content": user_input})

        ai_response = generate(messages)
        if isinstance(ai_response, dict) and 'error' in ai_response:
            response = ai_response['error']
        else:
            response = clean_ai_response(ai_response)
        messages.append({"role": "assistant", "content": response})

        simulate_real_time_response(response)
        last_user_input = user_input


display_main_menu()
