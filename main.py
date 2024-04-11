import os
from dotenv import load_dotenv
from entity import create_thread, start, get_response
import json

load_dotenv()

assistant_id = os.getenv("ASSISTANT_ID")
thread_id = create_thread()

print("Hey! Welcome, Please enter a list of keywords(comma separated) to fetch google trends,enter quit to exit the conversation!")
def main():
    while True:
        prompt = input("User:  ")
        if prompt.lower() == "quit":
            break

        start(thread_id, prompt)
        response = get_response(thread_id, assistant_id, prompt)
        print("Agent: ", response)


if __name__ == "__main__":
    main()
