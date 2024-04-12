import os
import time
from dotenv import load_dotenv
import openai
from function import fetch_google_trends

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)

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

def setup():
    assistant = client.beta.assistants.create(
        name="Google Trends Assistant",
        instructions="You are a bot to fetch Google Trends data based on user input, return more analytical table or number based output.",
        model="gpt-4-turbo-preview",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "fetch_google_trends",
                    "description": "Fetches Google Trends data based on user input.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "keywords": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "List of keywords to fetch Google Trends data for"
                            }
                        },
                        "required": ["keywords"]
                    }
                }
            }
        ]
    )

    return assistant.id

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
    dff, df_related_topics_rising, df_related_topics_top, df_related_queries_rising, df_related_queries_top = fetch_google_trends(keywords=user_query)  
    
    output_str = ""
    if dff is not None:
        output_str += "Interest over time data:\n"
        output_str += dff.head().to_string() + "\n\n"

    if not df_related_topics_rising.empty:
        output_str += "Related Topics (Rising):\n"
        output_str += df_related_topics_rising.head().to_string() + "\n\n"

    if not df_related_topics_top.empty:
        output_str += "Related Topics (Top):\n"
        output_str += df_related_topics_top.head().to_string() + "\n\n"

    if not df_related_queries_rising.empty:
        output_str += "Related Queries (Rising):\n"
        output_str += df_related_queries_rising.head().to_string() + "\n\n"

    if not df_related_queries_top.empty:
        output_str += "Related Queries (Top):\n"
        output_str += df_related_queries_top.head().to_string() + "\n\n"

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

