from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from paging import send_notification
import traceback
import random


MONTH_TO_CHECK_2025 = frozenset(["January"])


def run():
    # Set up ChromeOptions
    options = webdriver.ChromeOptions()

    # Set up ChromeOptions
    options = webdriver.ChromeOptions()

    # Enable logging
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    # Start the browser with the enhanced capabilitiesdkp
    driver = webdriver.Chrome(options=options)
    # Read the credentials from the file
    with open('credentials.txt', 'r') as file:
        email = file.readline().strip()  # Read the first line (email) and remove any whitespace
        password = file.readline().strip()  # Read the second line (password) and remove any whitespace

    # Go to the website
    driver.get('https://ais.usvisa-info.com/en-ca/niv/users/sign_in')

    # Find the email and password input elements
    email_elem = driver.find_element(By.ID, 'user_email')
    password_elem = driver.find_element(By.ID, 'user_password')

    # Enter the email and password
    email_elem.send_keys(email)
    password_elem.send_keys(password)

    # Check the Privacy Policy and Terms of Use checkbox (if you want to agree to it programmatically)
    checkbox_elem = driver.find_element(By.ID, 'policy_confirmed').find_element(By.XPATH, '..')
    checkbox_elem.click()

    # Submit the login form
    login_button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Sign In"]')
    login_button.click()

    # # After the login, wait for the "Continue" button to be present and visible.
    # After the login, wait for the "Continue" button to be present and visible.
    continue_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@class, "button") and contains(@class, "primary") and contains(@class, "small") and text()="Continue"]')))

    # Click the "Continue" button
    continue_button.click()


    # After the previous action, wait for the "Reschedule Appointment" header to be present and visible.
    reschedule_header = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//h5/span[contains(@class, "fas") and contains(@class, "fa-calendar-minus")]')))

    # Click the "Reschedule Appointment" header to reveal the button
    reschedule_header.click()

    # Now wait for the "Reschedule Appointment" button to be present and visible.
    reschedule_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@class, "button") and contains(@class, "small") and contains(@class, "primary") and text()="Reschedule Appointment"]')))

    # Click the "Reschedule Appointment" button
    reschedule_button.click()

    try:
        # show calendar
        calendar_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'appointments_consulate_appointment_date')))
        calendar_field.click()
    except Exception as e:
        elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'There are no available appointments')]")
        for element in elements:
            send_notification("No appointment", element.text, priority=-2)
            break
        if elements:
            driver.close()
            return

    def click_next_until_year(driver: webdriver.Chrome, target_year):
        notifications = []
        while True:
            year_element = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-year")
            current_year = int(year_element.text)
            month_element = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-month")
            current_month = month_element.text
            if current_year > target_year:
                break
            next_button = driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-next")
            dates = find_available_date(driver)
            print(current_year, current_month, dates)
            
            if dates:
                if current_year <= 2025:
                    notifications.append(f"{current_month} {dates} {current_year}")
                    if current_year <= 2024 or (current_year == 2025 and current_month in MONTH_TO_CHECK_2025):
                        print("Found in 2024!")
                        for _ in range(3):
                            send_notification("Found 2024", f"{current_month} {dates} {current_year}")
                        time.sleep(60 * 60)
            
            next_button.click()
        if notifications:
            send_notification("Current dates", "\n".join(notifications), priority=-2)
    def find_available_date(driver: webdriver.Chrome):
        available_dates = driver.find_elements(By.CSS_SELECTOR, 'a.ui-state-default')
        result = []
        
        for date in available_dates:
            d = int(date.text)
            if date.get_attribute('href'):
                result.append(d)
            return result
    click_next_until_year(driver, 2025)
    time.sleep(random.randint(0, 60))  # Randomly sleep 0-60 sec

    # Close the browser or continue with other tasks
    driver.close()

if __name__ == "__main__":
    while True:
        current_datetime = datetime.now()
        print(f"================================================= {current_datetime.strftime('%Y-%m-%d %H:%M:%S')} ===========================================")
        try:
            run()
        except Exception as e:
            exception_string = traceback.format_exc()
            send_notification("Something is wrong", exception_string, priority=-1)
        send_notification(f"Healty check {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "Good good", priority=-2)
        time.sleep(60 * 10)  # 5 minutes