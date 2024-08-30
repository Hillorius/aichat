import requests
import colorama
import re
import json
import random
import time 

colorama.init(autoreset=True)

ascii_art_lines = [
    r"                                                                           ,----, ",
    r"                                                 ,--,                    ,/   .`| ",
    r"   ,---,         ,---,          ,----..        ,--.'|   ,---,          ,`   .'  : ",
    r"  '  .' \     ,`--.' |         /   /   \    ,--,  | :  '  .' \       ;    ;     / ",
    r" /  ;    '.   |   :  :        |   :     :,---.'|  : ' /  ;    '.   .'___,/    ,'  ",
    r":  :       \  :   |  '        .   |  ;. /|   | : _' |:  :       \  |    :     |   ",
    r":  |   /\   \ |   :  |        .   ; /--` :   : |.'  |:  |   /\   \ ;    |.';  ;   ",
    r"|  :  ' ;.   :'   '  ;        ;   | ;    |   ' '  ; :|  :  ' ;.   :`----'  |  |   ",
    r"|  |  ;/  \   \   |  |        |   : |    '   |  .'. ||  |  ;/  \   \   '   :  ;   ",
    r"'  :  | \  \ ,'   :  ;        .   | '___ |   | :  | ''  :  | \  \ ,'   |   |  '   ",
    r"|  |  '  '--' |   |  '        '   ; : .'|'   : |  : ;|  |  '  '--'     '   :  |   ",
    r"|  :  :       '   :  |        '   | '/  :|   | '  ,/ |  :  :           ;   |.'    ",
    r"|  | ,'       ;   |.'         |   :    / ;   : ;--'  |  | ,'           '---'      ",
    r"`--''         '---'            \   \ .'  |   ,/      `--''                        ",
    r"                                `---`    '---'                                    ",
    r"",
    r"By-Hillorius",
    r"",
    r"                                                                                                    ",
    r"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┣━",
    r"                                                                                                    "
]

def print_gradient_art(lines):
    colors = [colorama.Fore.CYAN, colorama.Fore.LIGHTBLUE_EX, colorama.Fore.CYAN, colorama.Fore.LIGHTBLUE_EX, colorama.Fore.CYAN, colorama.Fore.BLUE]
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(color + line)

def load_intents(file_path):
    try:
        with open(file_path, 'r') as file:
            intents = json.load(file)
            return intents.get('blyat', [])
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        print("Please make sure the file is present in the same directory as the script.")
        return None

def match_intent(user_input, intents):
    for intent in intents:
        for pattern in intent['patterns']:
            if re.search(r'\b' + re.escape(pattern) + r'\b', user_input, re.IGNORECASE):
                return intent
    return {"name": "default", "responses": ["Sorry, I didn't understand that. Can you try again?"]}

def generate(messages, model="Sao10K/L3-70B-Euryale-v2.1", max_tokens=1024):
    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://deepinfra.com',
        'Referer': 'https://deepinfra.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'X-Deepinfra-Source': 'model-embed',
        'accept': 'text/event-stream',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
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
            return {'error': 'no choices found'}
    else:
        return {'status_code': response.status_code, 'message': response.text}

def simulate_real_time_response(response, color=colorama.Fore.GREEN, delay=0.01):
    # Apply the color to each character as it's being printed in real-time
    for char in response:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print()


def chat_with_ai():
    print_gradient_art(ascii_art_lines)

    intents = load_intents(r'assets/intents.json')
    if intents is None:
        print("Error: Unable to load intents.json file.")
        return

    initial_prompt = input(colorama.Fore.GREEN + "Enter the initial prompt or personality for the AI: ")

    messages = [
        {"role": "system", "content": initial_prompt}
    ]

    while True:
        user_input = input(colorama.Fore.CYAN + "You: ")
        
        if user_input.lower() == 'exit':
            print(colorama.Fore.RED + "Exiting the chat. Goodbye!")
            break

        intent = match_intent(user_input, intents)
        response = random.choice(intent['responses'])
        
        messages.append({"role": "user", "content": user_input})
        response = generate(messages)
        if isinstance(response, dict) and 'error' in response:
            response = response['error']    
        else:
            messages.append({"role": "assistant", "content": response})
        
        simulate_real_time_response(response)

if __name__ == "__main__":
    chat_with_ai()
