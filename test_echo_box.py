from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_echo_box_displays_message_back(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Echo Box'))).click()
    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'messageInput'))).send_keys('Hello')
    driver.find_element(MobileBy.ACCESSIBILITY_ID, 'messageSaveBtn').click()
    saved = driver.find_element(MobileBy.ACCESSIBILITY_ID, 'savedMessage').text
    assert saved == 'Hello'
    driver.back()

    wait.until(EC.presence_of_element_located(
        (MobileBy.ACCESSIBILITY_ID, 'Echo Box'))).click()
    saved = driver.find_element(MobileBy.ACCESSIBILITY_ID, 'savedMessage').text
    assert saved == 'Hello'
