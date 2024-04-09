# Google Trends Bot

The Google Trends Bot is a Python script that interacts with the Google Trends website to fetch rising queries based on user input. It utilizes Pytrends, a Python library for accessing Google Trends data.

This Python program utilizes OpenAI's GPT-4 model to create a Google Trends assistant. It fetches Google Trends data based on user input and can return more analytical table or number-based output.

## Functionality
The assistant provides the following functionality:
- Fetch Google Trends data based on user input.
- Return interest over time data, related topics (rising and top), and related queries (rising and top).

## Arguments
The assistant function, `fetch_google_trends`, requires the following argument:
- `keywords`: A list of keywords to fetch Google Trends data for.

## Steps to Run the Program
1. Ensure you have Python installed on your system.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Obtain an OpenAI API key and set it as an environment variable named `OPENAI_API_KEY` in a `.env` file.
4. Run the program by executing the `main.py` file.
5. The program will prompt you to provide keywords for fetching Google Trends data.
6. The assistant will return the requested Google Trends data based on your input.
7. 
## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/google-trends-bot.git
    ```

2. Navigate to the project directory:

    ```bash
    cd google-trends-bot
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
# Setting Up OpenAI Assistant Using OpenAI API

Follow these steps to set up your OpenAI assistant using the OpenAI API:

1. **Sign Up for OpenAI API**:
   - Visit the OpenAI website and sign up for an account if you haven't already.
   - Subscribe to the OpenAI API plan that suits your needs.

2. **Get API Key**:
   - Once subscribed, you'll receive an API key. This key is essential for authenticating your requests.

3. **Install OpenAI Python Library**:
   - Use pip to install the OpenAI Python library:
     ```
     pip install openai
     ```

4. **Import OpenAI Library**:
   - In your Python script or environment, import the OpenAI library:
     ```python
     import openai
     ```

5. **Set API Key**:
   - Set your API key using the `openai.api_key` attribute:
     ```python
     openai.api_key = 'YOUR_API_KEY'
     ```

6. **Invoke OpenAI API**:
   - Use the OpenAI API to interact with the language model. For example:
     ```python
     response = openai.Completion.create(
         engine="text-davinci-003",
         prompt="Once upon a time",
         max_tokens=50
     )
     print(response.choices[0].text.strip())
     ```

7. **Explore API Documentation**:
   - Refer to the official OpenAI API documentation for detailed information on endpoints, parameters, and usage examples.

8. **Understand API Usage and Billing**:
   - Familiarize yourself with usage limits and billing details to avoid exceeding quotas and unexpected charges.

9. **Experiment and Develop**:
   - Start experimenting with the OpenAI models, explore prompts, and develop your applications.

10. **Handle Errors and Exceptions**:
    - Implement error handling mechanisms in your code to gracefully handle any errors during API requests.

By following these steps, you can set up and start using the OpenAI API to interact with powerful language models and build innovative applications leveraging artificial intelligence capabilities.

## Usage

1. Run the `main.py` script:

    ```bash
    python main.py
    ```

2. Follow the prompts to provide a query term for which you want to fetch rising queries from Google Trends.

3. The bot will then fetch the rising queries and display the results.

## Fetching Cookies and Headers

In order to interact with the Google Trends website, the bot requires valid cookies and headers. Follow the steps below to fetch these:

1. Open Google Chrome and navigate to the Google Trends website (https://trends.google.com).

2. Open the Developer Tools:
    - Windows/Linux: Press `Ctrl + Shift + I`.
    - Mac: Press `Cmd + Option + I`.

3. Go to the "Network" tab.

4. Refresh the page (press `Ctrl + R` or `Cmd + R`).

5. Look for a request to `trends.google.com` in the Network tab.

6. Right-click on the request and select "Copy" > "Copy as cURL (bash)".

7. Paste the copied cURL command into a text editor. Extract the cookies and headers from the command.

8. Update the `cookies` and `headers` variables in the `main.py` script with the extracted values.

## Disclaimer

This project is for educational purposes only. Use it responsibly and adhere to Google's Terms of Service.
