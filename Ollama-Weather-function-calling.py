import ollama
import requests
from rich import print

def get_current_weather(city: str) -> str:
    """Fetches the current weather for a given city."""
    base_url = f"http://wttr.in/{city}?format=j1"
    response = requests.get(base_url)
    response.raise_for_status()  # Ensure we handle potential HTTP errors
    data = response.json()
    temperature = data['current_condition'][0]['temp_C']
    return f"The current temperature in {city} is: {temperature}°C"

def handle_weather_query(model: str, query: str) -> None:
    """Handles a weather query using the given model."""
    response = ollama.chat(
        model=model,
        messages=[{'role': 'user', 'content': query}],
        tools=[{
            'type': 'function',
            'function': {
                'name': 'get_current_weather',
                'description': 'Get the current weather for a city',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'city': {
                            'type': 'string',
                            'description': 'The name of the city',
                        },
                    },
                    'required': ['city'],
                },
            },
        }]
    )

    tool_calls = response['message']['tool_calls']
    if not tool_calls:
        print("No tool calls were made.")
        return

    tool_call = tool_calls[0]
    tool_name = tool_call['function']['name']
    arguments = tool_call['function']['arguments']
    city = arguments['city']

    if tool_name == 'get_current_weather':
        result = get_current_weather(city)
        print(result)
    else:
        print(f"Unknown tool call: {tool_name}")

if __name__ == "__main__":
    handle_weather_query(model='llama3.1', query='What is the weather in Toronto?')
