from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

# Function to get bill amount using Selenium
def get_bill_amount(consumer_number):
    driver = webdriver.Chrome()
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
        driver.quit()
        return None

@app.route('/get-bill', methods=['POST'])
def get_bill():
    data = request.get_json()
    consumer_number = data.get('consumer_number')

    if not consumer_number:
        return jsonify({"error": "Consumer number is required"}), 400

    bill_amount = get_bill_amount(consumer_number)

    if bill_amount:
        return jsonify({"consumer_number": consumer_number, "bill_amount": bill_amount}), 200
    else:
        return jsonify({"error": "Failed to retrieve bill amount"}), 500

if __name__ == '__main__':
    app.run(debug=True)
