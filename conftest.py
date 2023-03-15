CUR_DIR = path.dirname(path.abspath(__file__))
APP = path.join(CUR_DIR, '..', 'mobile', 'TheApp.app.zip')
APPIUM = 'http://localhost:4723'


@pytest.fixture
def driver():
    caps = {
        'platformName': 'iOS',
        'platformVersion': '16.2',
        'deviceName': 'iPhone 14 Pro',
        'automationName': 'XCUITest',
        'app': APP,
    }

    driver = webdriver.Remote(APPIUM, caps)
    yield driver
    driver.quit()
