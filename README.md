# LangGraph Weather Information App

This Python application demonstrates the integration of LangChain's LangGraph with OpenWeatherMap to provide weather information for any given city. Utilizing advanced language models and the LangChain framework, this app simplifies the process of querying weather data and interpreting responses in a conversational manner.



## Features

- **Weather Queries**: Allows user to input city names and receive current weather data.
- **LangGraph Integration**: Leverages LangChain's LangGraph to structure queries and process information efficiently.
- **OpenWeatherMap API**: Utilizes OpenWeatherMap for reliable and up-to-date weather information.
- **Human-in-the-loop**: Offers an option for manual intervention to validate tool actions before execution.

## Requirements

- Python 3.8+
- `dotenv`: For loading environment variables
- `langchain`: For LangGraph and other utilities
- An OpenWeatherMap API key
- LangChain API credentials

## Setup

1. Clone the repository and navigate to the project directory.
2. Get the API keys
3. Run the application with `python app.py`.

## Usage

1. Start the application as mentioned in the setup.
2. Enter your query in the format "What is the weather in [City Name]?".
3. The application will process your input and return the current weather data for the specified city.

## Technical Overview

The application is structured around LangGraph's `StateGraph` to model the interaction flow:

- **Agent State**: Holds the conversation history and processes input using the LangChain OpenAI model.
- **Weather Tool**: A custom tool to query the OpenWeatherMap API and parse responses into a structured format.
- **Workflow**: Defines the application's logic flow, integrating the agent, tools, and conditional transitions based on user input and system state.

This simplistic demonstration is an example of integrating language models with external APIs to create conversational interfaces for information retrieval utlizing Langgraph

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your suggestions or improvements.




