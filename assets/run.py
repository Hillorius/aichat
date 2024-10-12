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

# Initialize colorama for colored output
colorama.init(autoreset=True)

# Helper function to print colored gradient ASCII art
def print_gradient_art(lines):
    colors = [colorama.Fore.CYAN, colorama.Fore.LIGHTBLUE_EX, colorama.Fore.CYAN, colorama.Fore.LIGHTBLUE_EX, colorama.Fore.CYAN, colorama.Fore.BLUE]
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(color + line)

# Load intents from a file
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

# Match user input with predefined intents
def match_intent(user_input, intents):
    for intent in intents:
        for pattern in intent['patterns']:
            if pattern.lower() in user_input.lower():
                return intent
    return {"name": "default", "responses": ["Sorry, I didn't understand that. Can you try again?"]}

# Clean the AI response (removing unnecessary artifacts)
def clean_ai_response(response):
    if '*' in response:
        response = response.replace('*', '')
    return response.strip()

# Call API for AI-generated responses
def generate(messages, model="Sao10K/L3-70B-Euryale-v2.1", max_tokens=550, max_retries=3, max_length=4096):
    """Send a request to the AI model and handle long conversations by truncating the message history."""
    
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    # Truncate the message history before making the API call
    messages = truncate_messages(messages, max_length)

    json_data = {
        'model': model,
        'messages': messages,
        'stream': False,
        'max_tokens': max_tokens,
    }

    retry_count = 0

    while retry_count < max_retries:
        response = requests.post('https://api.deepinfra.com/v1/openai/chat/completions', headers=headers, json=json_data)
        
        if response.status_code == 200:
            response_json = response.json()
            if 'choices' in response_json and len(response_json['choices']) > 0:
                return response_json['choices'][0]['message']['content']
            else:
                return {'error': 'No choices found in API response'}

        # Retry on 500 or other server errors
        elif 500 <= response.status_code < 600:
            retry_count += 1
            print(f"Server error {response.status_code}. Retrying {retry_count}/{max_retries}...")
            time.sleep(2 ** retry_count)  # Exponential backoff
        else:
            # For other status codes, return error message immediately
            return {'error': f"API Error: {response.status_code}", 'message': response.text}
    
    # If retries fail, return the final error
    return {'error': f"API Error: {response.status_code} after {max_retries} retries", 'message': response.text}

def truncate_messages(messages, max_length=4096):
    """Truncate the message history to keep the total token count under a limit."""
    token_count = sum(len(msg['content']) for msg in messages)
    while token_count > max_length and len(messages) > 1:
        messages.pop(0)  # Remove the oldest message
        token_count = sum(len(msg['content']) for msg in messages)
    return messages

# Simulate a real-time typing effect
def simulate_real_time_response(response, color=Fore.GREEN, delay=0.03, variance=0.01):
    """Simulate AI typing out the response in real-time, without typing indicator."""
    # Print AI response with typing effect
    for char in response:
        print(color + char, end='', flush=True)
        time.sleep(delay + random.uniform(-variance, variance))
    print()  

# Save chat history to a JSON file
def sanitize_filename(filename):
    """Remove invalid characters for filenames."""
    # Replace invalid characters with underscores or remove them
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def save_chat_history(messages, cleaned_prompt):
    chat_data = {
        "messages": messages
    }

    # Sanitize the cleaned prompt to ensure valid file names
    sanitized_prompt = sanitize_filename(cleaned_prompt)

    # Ensure the 'assets' directory exists
    os.makedirs('assets', exist_ok=True)

    # Create a file path using the sanitized prompt
    file_path = f'assets/chat_history_{sanitized_prompt}.json'
    
    # Save chat history to the file
    with open(file_path, 'w') as file:
        json.dump(chat_data, file, indent=4)
    
    # Notify user that the chat history was saved successfully
    print(Fore.GREEN + "Chat history saved successfully!")


def display_main_menu():
    """Display the fancy main menu."""
    clear()
    print_gradient_art(lines=ascii_art_lines)
    print(Fore.LIGHTYELLOW_EX + "\n--- Main Menu ---")
    print(Fore.LIGHTBLUE_EX + "[1] Start new chat")
    print(Fore.LIGHTBLUE_EX + "[2] View chat history")
    print(Fore.LIGHTBLUE_EX + "[3] Exit")

    choice = input(Fore.LIGHTGREEN_EX + "\nSelect an option (1-3): ").strip()
    if choice == '1':
        clear()
        chat_with_ai()
    elif choice == '2':
        clear()
        load_and_display_personality_list()
    elif choice == '3':
        clear()
        print_gradient_art()
        time.sleep(1.5)
        print(Fore.RED + "Goodbye! Have a great day!")
        exit()
    else:
        print(Fore.RED + "\nInvalid option! Returning to menu...")
        time.sleep(1)
        display_main_menu()

# Load and display available chat histories
def load_and_display_personality_list():
    """List saved chats and handle selection."""
    personalities = []
    if os.path.exists('assets'):
        for file_name in os.listdir('assets'):
            if file_name.startswith('chat_history_') and file_name.endswith('.json'):
                personality = file_name.replace('chat_history_', '').replace('.json', '')
                personalities.append(personality)

    if personalities:
        print(Fore.LIGHTCYAN_EX + "\n--- Chat Histories ---")
        for i, personality in enumerate(personalities, 1):
            print(Fore.LIGHTBLUE_EX + f"{i}. {personality}")
        choice = input(Fore.GREEN + "\nSelect a personality (or type 'back' to return): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(personalities):
            selected_personality = personalities[int(choice) - 1]
            continue_chat(selected_personality)
        elif choice.lower() == 'back':
            display_main_menu()
        else:
            print(Fore.RED + "\nInvalid choice, returning to menu.")
            time.sleep(1)
            display_main_menu()
    else:
        print(Fore.RED + "\nNo chat history found.")
        time.sleep(1.5)
        display_main_menu()

# Continue a previous chat
def continue_chat(personality):
    """Load and continue a saved chat."""
    file_path = f'assets/chat_history_{personality}.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            chat_history = json.load(file)
            messages = chat_history['messages']
            print(Fore.CYAN + f"\n--- Continuing chat with AI: {personality} ---")
            for msg in chat_history['messages']:
                role = msg['role']
                content = msg['content']
                if role == "user":
                    print(Fore.CYAN + "You: " + content)
                else:
                    print(Fore.MAGENTA + content)
            chat_with_ai(personality, messages)
    else:
        print(Fore.RED + f"\nNo chat found for personality: {personality}.")
        time.sleep(1.5)
        display_main_menu()

# Clear the console screen
def clear():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

# Main chat loop with the AI
def chat_with_ai(initial_prompt=None, messages=None):
    """Start or continue chatting with the AI."""
    if not initial_prompt:
        initial_prompt = input(Fore.LIGHTGREEN_EX + "\nEnter AI's personality (e.g., witty, friendly): ").strip()
        cleaned_prompt = re.sub(r'[^a-zA-Z0-9_,.\s]', '', initial_prompt)
        print(Fore.LIGHTYELLOW_EX + f"Personality set to: {cleaned_prompt}")

        # Create system message for AI's personality
        messages = [{"role": "system", "content": f"You are {initial_prompt}. Respond in a concise, engaging, and emotional way. Be interactive, ask questions, react, but don't mimic the user. Keep replies under 100 characters."}]

    last_user_input = None

    while True:
        user_input = input(Fore.CYAN + "\nYou: ").strip()

        # Handle special commands like exit, save, reset
        if user_input.lower() in ['exit', 'back', 'menu']:
            print(Fore.RED + "\nReturning to main menu...")
            time.sleep(2)
            save_chat_history(messages, initial_prompt)
            clear()
            display_main_menu()
            break
        elif user_input.lower() == 'save':
            print(Fore.YELLOW + "\nSaving chat history...")
            save_chat_history(messages, initial_prompt)
            continue
        elif user_input.lower() == 'reset':
            print(Fore.YELLOW + "\nResetting conversation...")
            messages = [{"role": "system", "content": f"Reset personality as {cleaned_prompt}."}]
            clear()
            print_gradient_art()
            continue
        elif user_input.lower() == 'retry':
            if last_user_input is None:
                print(Fore.RED + "No previous message to retry.")
                continue
            print(Fore.YELLOW + "Retrying last message...")
            user_input = last_user_input

        # Add user input to the chat history
        messages.append({"role": "user", "content": user_input})

        # Simulate AI response (Placeholder for actual API call)
        ai_response = generate(messages)  # Call your AI API here

        if isinstance(ai_response, dict) and 'error' in ai_response:
            response = ai_response['error']
        else:
            response = clean_ai_response(ai_response)  # Clean response

        # Add AI response to the chat history
        messages.append({"role": "assistant", "content": response})

        # Display AI's response with a typing effect
        simulate_real_time_response(response)

        # Store last user input for 'retry' functionality
        last_user_input = user_input

if __name__ == "__main__":
    display_main_menu()
