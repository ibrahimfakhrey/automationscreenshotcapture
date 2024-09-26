from flask import Flask, render_template, request, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

app = Flask(__name__)

# Folder to save screenshots
SCREENSHOTS_FOLDER = os.path.join(os.getcwd(), 'screenshots')

# Ensure the screenshots folder exists
if not os.path.exists(SCREENSHOTS_FOLDER):
    os.makedirs(SCREENSHOTS_FOLDER)


# Configure the WebDriver (You can use any browser, here I use Chrome)
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    return driver


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/capture', methods=['POST'])
def capture_screenshot():
    # Get the URL from the form
    url = request.form.get('url')

    if not url:
        return "No URL provided", 400

    driver = get_driver()

    try:
        # Open the webpage
        driver.get(url)
        print("i am here ")

        # Generate a unique filename for the screenshot
        timestamp = int(time.time())
        print(f"this is the timestamp{timestamp}")
        screenshot_filename = f"screenshot_{timestamp}.png"
        print(f"this is the screen {screenshot_filename}")
        screenshot_path = os.path.join(SCREENSHOTS_FOLDER, screenshot_filename)

        # Take a screenshot and save it
        driver.save_screenshot(screenshot_path)

        # Close the driver
        driver.quit()

        # Provide a download link or display the screenshot
        return render_template('screenshot.html', screenshot_file=screenshot_filename)

    except Exception as e:
        driver.quit()
        return f"An error occurred: {str(e)}", 500





if __name__ == '__main__':
    app.run(debug=True)
