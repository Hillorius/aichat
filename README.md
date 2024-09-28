# AIChat

AIChat is an interactive chat application that uses AI to simulate real-time conversations. This project leverages natural language processing to understand user inputs and generate contextual responses.

![AIChat Example](assets/Example.png)

## Features

- **Intent Matching**: The application can understand user input by matching it to predefined intents.
- **Real-Time Response Simulation**: Responses are displayed in real-time, creating a more engaging user experience.
- **Customizable AI Personality**: Users can set an initial prompt to define the personality of the AI.
- **Supports *NSFW***: The AI can infact generates Not Safe For Work (*NSFW*) Responds.

## Installation

Requirements :
- [colorama](https://pypi.org/project/colorama/)
- [json](https://docs.python.org/3/library/json.html) (part of the Python standard library)
- [re](https://docs.python.org/3/library/re.html) (part of the Python standard library)
- [requests](https://pypi.org/project/requests/)

- **Dont worry the .bat files automaticly install the requirements if you already have *pip*.**

  ## Information

 **Additional Commands:**
- exit or back: Exit the conversation and return to the main menu.
- save: Save the current conversation to a file.
- reset: Reset the conversation while retaining the current AI personality.
- retry: Retry the AI's response to the last message.

 **AI Model**
 AIChat uses the following model for generating responses:

 Model: Sao10K/L3-70B-Euryale-v2.1
 API Endpoint: https://api.deepinfra.com/v1/openai/chat/completions

 
 

  
