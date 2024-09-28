# Testing-out-function-calling-Ollama
To test it out function calling so it work also offline


This code uses the `ollama` library to interact with an Ollama language model, enabling it to answer questions about the weather by calling a custom function `get_current_weather`.  

**1. Imports:** Imports the `ollama` library for interacting with the Ollama language model, `requests` for making HTTP requests, and `rich` for enhanced printing.

**2. `get_current_weather` Function:**

```python
def get_current_weather(city: str) -> str:
    # ...
```

* Takes a `city` name as input.
* Constructs the URL for the wttr.in weather service.  This service provides a simple way to get weather information in plain text or JSON format.
* Makes a GET request to the URL.
* `response.raise_for_status()`: This is a crucial improvement for error handling; it raises an exception if the HTTP request fails (e.g., 404 Not Found).
* Parses the JSON response and extracts the temperature in Celsius.
* Returns a formatted string with the temperature.

**3. `handle_weather_query` Function:**

```python
def handle_weather_query(model: str, query: str) -> None:
    # ...
```

* Takes the `model` name and the user's `query` as input.
* `ollama.chat(...)`:  This is the core interaction with the Ollama language model.
    * `model`: Specifies the Ollama model to use.
    * `messages`:  Provides the user's query as a message.
    * `tools`: This is where you define the external tools (functions) the model can use. In this case, you define `get_current_weather`.
        - `type`: Set to 'function'.
        - `function`:  Provides details about the function.
            - `name`, `description`: Name and description of the function.
            - `parameters`: Defines the function's parameters as a JSON schema. This tells the model what kind of input the function expects.  It requires the "city" as a string and makes it mandatory with the `required` field.
* The code then checks if any tool calls were made by the language model.
* If tool calls were made:
    - Extracts the tool name and arguments.
    - If the tool is `get_current_weather`:
        - Calls the `get_current_weather` function with the city argument extracted from the model's response.
        - Prints the result.
    - Handles unknown tool calls.

**4. Main Execution Block:**

```python
if __name__ == "__main__":
    handle_weather_query(model='llama2', query='What is the weather in Toronto?')  # Replace with your model
```
* Calls `handle_weather_query` with the model name ('llama2', which you might need to adjust) and the user's weather query.
