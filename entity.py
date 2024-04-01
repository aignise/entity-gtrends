import time
import openai
import os
import json
from function import fetch_weather_forecast
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)

def setup():
    assistant = client.beta.assistants.create(
        name="Weather Forecast Bot",
        instructions="You are a bot to fetch weather forecasts based on user's location.",
        model="gpt-4-turbo-preview",
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

def create_thread():
    thread = client.beta.threads.create()
    return thread.id

def start(thread_id, user_query):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_query
    )
    
def get_response(thread_id, assistant_id, user_query):
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
    location = user_query
    output = fetch_weather_forecast(location=location)
    output_str = json.dumps(output)
    
    tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
    
    tool_outputs = []
    for tool_call in tool_calls:
        tool_outputs.append({
            "tool_call_id": tool_call.id,
            "output": output_str
        })
    
    client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_outputs
    )

def main():
    thread_id = create_thread()
    user_query_prompt = "Please provide the location for weather forecast: "
    user_query = input(user_query_prompt)
    assistant_id = os.getenv("OPENAI_ASSISTANT_ID")
    
    start(thread_id, user_query)

    response = get_response(thread_id, assistant_id, user_query)

    print("Weather Forecast:", response)

if __name__ == "__main__":
    main()
