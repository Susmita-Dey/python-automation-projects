import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Function to login using the provided credentials
def login(email, pin):
    # Instantiate the web driver (assuming Chrome for this example)
    driver = webdriver.Chrome()
    driver.get("https://yourwebsite.com/login")  # Replace with the actual login URL

    # Find the email and pin input fields and enter the credentials
    email_field = driver.find_element_by_id("email_input_id")  # Replace with the actual ID of the email input field
    email_field.send_keys(email)
    pin_field = driver.find_element_by_id("pin_input_id")  # Replace with the actual ID of the pin input field
    pin_field.send_keys(pin)

    # Submit the form
    pin_field.send_keys(Keys.RETURN)

    # Wait for the page to load (you might need to adjust the sleep time)
    time.sleep(2)

    return driver

# Function to logout
def logout(driver):
    # Your logout automation code here
    driver.quit()
    print("Logged out")

# Function to automate data entry for a customer using their ID
def automate_data_entry(driver, customer_id):
    # Your automation routine code here
    print(f"Automating data entry for customer with ID: {customer_id}")

    # Example: Find the input field on the website and enter the customer ID
    id_field = driver.find_element_by_id("id_input_id")  # Replace with the actual ID of the input field
    id_field.send_keys(customer_id)

# Load credentials.xlsx
credentials_df = pd.read_excel('credentials.xlsx')

# Load customer details
customers_df = pd.read_excel('customer_details.xlsx')

# Iterate through each credential
for index, credential in credentials_df.iterrows():
    email = credential['email']
    pin = credential['pin']

    # Login with the current credential
    driver = login(email, pin)

    # Filter customers for the current credential
    filtered_customers = customers_df[customers_df['staff'] == email]

    # Iterate through each customer for the current credential
    for index, customer in filtered_customers.iterrows():
        customer_id = customer['ID_NUMBER']
        
        # Attempt to automate data entry for the current customer
        try:
            automate_data_entry(driver, customer_id)
        except Exception as e:
            print(f"Error automating data entry for customer ID {customer_id}: {str(e)}")
            continue  # Skip to the next customer if an error occurs
        
    # Logout after processing all customers for the current credential
    logout(driver)

print("Process completed.")
