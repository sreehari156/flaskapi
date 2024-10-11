from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

# Function to get bill amount using Selenium
def get_bill_amount(consumer_number):
    # Configure Selenium to use headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the website
        driver.get("https://www.recharge1.com/online-electricity-bill-payment/kseb-kerala-state-electricity-borad.aspx")
        time.sleep(8)  # Wait for page to load

        # Locate the consumer number input field and send keys
        consumer_number_input = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_UtilityControlId_TXT_Consumer_Number")
        consumer_number_input.send_keys(consumer_number)

        # Locate and click the 'Check Bill' button
        button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_UtilityControlId_BtnCheckBill")
        button.click()

        time.sleep(10)  # Wait for the bill amount to load

        # Get the bill amount
        bill_amount_field = driver.find_element(By.ID, "ctl00_ContentPlaceHolder2_UtilityControlId_ctl01_txtbillamount")
        bill_amount = bill_amount_field.get_attribute("value")

        driver.quit()
        return bill_amount
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return None

# API endpoint to get the bill amount
@app.route('/get-bill', methods=['POST'])
def get_bill():
    # Extract consumer number from the POST request
    data = request.get_json()
    consumer_number = data.get('consumer_number')

    if not consumer_number:
        return jsonify({"error": "Consumer number is required"}), 400

    # Get the bill amount using Selenium
    bill_amount = get_bill_amount(consumer_number)

    if bill_amount:
        return jsonify({"consumer_number": consumer_number, "bill_amount": bill_amount}), 200
    else:
        return jsonify({"error": "Failed to retrieve bill amount"}), 500

if __name__ == '__main__':
    # Enable debug mode for troubleshooting (Don't use this in production)
    app.run(debug=True)
