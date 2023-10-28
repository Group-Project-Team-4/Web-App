import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def test_register():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Webapp's URL
        driver.get("http://localhost:5000")

        # Navigate to registration page
        register_link = driver.find_element(By.LINK_TEXT, "Register")
        register_link.click()

        # Fill out registration form
        username_input = driver.find_element(By.NAME, "username")
        username_input.send_keys("testuser")

        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("password123")

        # Submit form
        password_input.send_keys(Keys.RETURN)

        # Wait for the page to refresh and check whether registration was successful
        time.sleep(3)

        success_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Registration successful" in success_text

    finally:
        # Close the WebDriver instance
        driver.quit()