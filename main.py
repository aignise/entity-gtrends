import json
import time
import openai
from dotenv import load_dotenv
import os

import requests

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=openai_api_key)

def setup():
    assistant = client.beta.assistants.create(
        name="Weather Forecast Bot",
        instructions="You are a bot to fetch weather forecasts based on user's location.",
        model="gpt-4-turbo-preview",  # Assuming this is suitable for weather forecasts
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "fetch_weather_forecast",
                    "description": "Fetches weather forecast based on user's location.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Location name (e.g., New York)"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ]
    )

    return assistant.id

def fetch_weather_forecast(location):
    find_places_url = "https://ai-weather-by-meteosource.p.rapidapi.com/find_places"
    find_places_querystring = {"text": location, "language": "en"}
    find_places_headers = {
        "X-RapidAPI-Key": os.getenv("X_RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "ai-weather-by-meteosource.p.rapidapi.com"
    }
    find_places_response = requests.get(find_places_url, headers=find_places_headers, params=find_places_querystring)

    # Check if the response is successful
    if find_places_response.status_code == 200:
        # Extract latitude and longitude from the first location
        first_location = find_places_response.json()[0]
        latitude = first_location['lat']
        longitude = first_location['lon']

        # Second API call to get hourly weather
        hourly_weather_url = "https://ai-weather-by-meteosource.p.rapidapi.com/hourly"
        hourly_weather_querystring = {
            "lat": latitude,
            "lon": longitude,
            "timezone": "auto",
            "language": "en",
            "units": "auto"
        }
        hourly_weather_headers = {
            "X-RapidAPI-Key": os.getenv("X_RAPIDAPI_KEY"),
            "X-RapidAPI-Host": "ai-weather-by-meteosource.p.rapidapi.com"
        }
        hourly_weather_response = requests.get(hourly_weather_url, headers=hourly_weather_headers, params=hourly_weather_querystring)

        # Check if the second API call is successful
        if hourly_weather_response.status_code == 200:
            return hourly_weather_response.json().get('hourly', {}).get('data', [])
        else:
            return None
    else:
        return None

def create_thread():
    """Creates a thread for conversation."""
    thread = client.beta.threads.create()
    return thread.id

def start(thread_id, user_query):
    """Starts a conversation in the specified thread with the given user query."""
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_query
    )
    
def get_response(thread_id, assistant_id, user_query):
    """Retrieves the response from the OpenAI API."""
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Answer user questions using custom functions available to you."
    )
    
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status == 'requires_action':
            submit_tool_outputs(thread_id, run.id, run_status, user_query)
        
        time.sleep(1)
    
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    response = messages.data[0].content[0].text.value
    return response

def submit_tool_outputs(thread_id, run_id, run_status, user_query):
    """Submits tool outputs to the OpenAI API."""
    location = user_query
    output = fetch_weather_forecast(location=location)  # Fetch weather forecast
    output_str = json.dumps(output)
    
    tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
    
    tool_outputs = []
    for tool_call in tool_calls:
        tool_outputs.append({
            "tool_call_id": tool_call.id,
            "output": output_str
        })
    
    # Submit tool outputs to OpenAI API
    client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_outputs
    )

def main():
    # Create a thread for conversation
    thread_id = create_thread()

    user_query_prompt = "Please provide the location for weather forecast: "
    user_query = input(user_query_prompt)
    assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
    
    start(thread_id, user_query)

    response = get_response(thread_id, assistant_id, user_query)

    print("Weather Forecast:", response)


if __name__ == "__main__":
    main()
