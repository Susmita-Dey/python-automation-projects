import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# https://sites.google.com/chromium.org/driver/ 

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

def get_login_credentials_from_user():
    email = input("Enter your email: ")
    pin = input("Enter your pin: ")
    return email, pin


def login(email,pin):

    driver.get("https://subsiditepatlpg.mypertamina.id/merchant/auth/login") # it will open up a new chrome window with this link in incognito mode

    # Wait for the page to load
    time.sleep(5)

    # wait for 5 sec and if error close the program
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,"mantine-r0"))
    )

    # find the input fields 
    email_field = driver.find_element(By.ID,"mantine-r0")
    # email_field.clear() # clear the input field if needed
    email_field.send_keys(email)
    pin_field = driver.find_element(By.ID, "mantine-r1")  # Replace with the actual ID of the pin input field
    pin_field.send_keys(pin)

    # Submit the form
    pin_field.send_keys(Keys.RETURN)

    print("Logged in")
    # Wait for the page to load
    time.sleep(10)

# Function to log out from the website
def logout():
    try:
        # Locate the logout button by searching for the text "Keluar Akun" within a <b> tag
        logout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span//b[contains(text(), 'Keluar Akun')]"))
        )
        # Click on the logout button
        logout_button.click()
        print("Clicked on logout button successfully.")
    except TimeoutException:
        print("Logout button not found within the specified time limit.")

# Function to automate data entry for a customer using their ID
def automate_data_entry(customer_id):
    print(f"Automating data entry for customer with ID: {customer_id}")

    # Find the input field for customer ID
    id_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Masukkan 16 digit NIK KTP Pelanggan']")))

    print("Found input field for customer ID")

    # Clear the input field and enter the customer ID
    id_field.clear()
    id_field.send_keys(customer_id)
    id_field.send_keys(Keys.RETURN)

    # Click on cek_nik_button
    try:
        cek_nik_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='btnCheckNik']")
        cek_nik_button.click()
        print("Clicked on 'Cek NIK' button")
    except NoSuchElementException:
        print("Failed to find 'Cek NIK' button")
        return False  # Return False if 'Cek NIK' button is not found

    # Check if the error message div is present indicating customer's age is under 17
    try:
        error_message = driver.find_element(By.ID, "mantine-r5-error")
        if "NIK tidak valid karena di bawah 17 tahun" in error_message.text:
            print(f"Customer with ID {customer_id} is under 17 years old, skipping...")
            return False  # Return False to indicate skipping this customer ID
    except NoSuchElementException:
        pass  # Continue if the error message is not found
    
    # Check for the presence of the non-registered user modal
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "mantine-rs-body")))
        # Non-registered user modal found, skip this customer
        print(f"Non-registered user modal found for customer ID {customer_id}, skipping...")
        return False
    except:
        # Non-registered user modal not found, proceed with next steps
        pass
    # Print a message to indicate that we've successfully entered the customer ID
    print("Entered customer ID successfully")

    # Wait for the program to go to the next screen
    # time.sleep(5)

    # Wait for the page to load after clicking 'Cek NIK' button
    time.sleep(5)

    # Click on cek_pesanan_button
    try:
        cek_pesanan_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='btnCheckOrder']")
        cek_pesanan_button.click()
        print("Clicked on 'Cek Pesanan' button")
    except NoSuchElementException:
        print("Failed to find 'Cek Pesanan' button")
        return False  # Return False if 'Cek Pesanan' button is not found

    # Wait for the page to load after clicking 'Cek Pesanan' button
    time.sleep(5)

    # Click on proses_transaksi_button
    try:
        proses_transaksi_button = driver.find_element(By.CSS_SELECTOR, "button[data-testid='btnPay']")
        proses_transaksi_button.click()
        print("Clicked on 'Proses Transaksi' button")
    except NoSuchElementException:
        print("Failed to find 'Proses Transaksi' button")
        return False  # Return False if 'Proses Transaksi' button is not found

    # Wait for the transaction to get completed
    time.sleep(15)

    # Click on the "home" button to go back to the main screen
    try:
        home_button_span = driver.find_element(By.XPATH, "//div[contains(@class, 'styles_headerStruk__oJzhS')]/span[1]")
        home_button_span.click()
        print("Clicked on 'Home' button")
    except NoSuchElementException:
        print("Failed to find 'Home' button")
        return False  # Return False if 'Home' button is not found

    # Wait for the page to load after clicking 'Home' button
    time.sleep(5)

    return True  # Return True to indicate successful data entry

# Prompt user for login credentials
email, pin = get_login_credentials_from_user()

# Login with user-provided credentials
login(email, pin)

# time.sleep(5)

# Load customer details
customers_df = pd.read_excel('testdata-all registered.xlsx')

# Filter customers for the current credential
filtered_customers = customers_df[customers_df['staff'] == email]

# Iterate through each customer
for index, customer in filtered_customers.iterrows():
    customer_id = str(customer['ID_NUMBER'])

    # Attempt to automate data entry for the current customer
    success = automate_data_entry(customer_id)
    
    if not success:
        continue  # Skip to the next customer if an error occurs during data entry

time.sleep(5)

# Logout after processing all customers
logout()

time.sleep(10)
driver.quit()

print("Process completed.")
