# Google Trends Bot

The Google Trends Bot is a Python script that interacts with the Google Trends website to fetch rising queries based on user input. It utilizes Pytrends, a Python library for accessing Google Trends data.

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
