# Test Runners and Frameworks

| Helpful Industry Terms |  |
| ---- | ---- |
| Feature | Group of user flows in your app (e.g., Login) |
| Testcase | A single possible path through a feature |
| Testsuite | A group of testcases that run together |
| Build | The system(s) that compile and test an app |
| Continuous Integration (CI) Server | System for defining and running builds |
| Test Runner | Program that collects and runs testcases| 
| Test Framework | 1st or 3rd party tooling to handle or abstract away common test-writing tasks |

Let's talk about test runners and frameworks, which will be the technical garden bed within which your testsuite will grow. But first, let's give a little glossary of terms to make sure we're all on the same page about everything that we've been talking about and will be talking about.

1. Feature. When I talk about a feature, I mean a general app feature that the user might move through in multiple ways. Login is a feature that we want to test, for example, but a test of the login feature will actually consist of multiple test cases.
2. Testcase. A test case is an extraction of a single possible path through a feature. It might be a positive testcase, like the happy path case we talked about earlier. Or it might be a negative testcase, designed to test the app behaves properly when the user input is invalid, and so on.
3. Test suite. A suite is a set of testcases that are grouped together for some reason or another. It could be simply all the testcases, or it could be the smoke tests or the regression tests.
4. Build. Sometimes, we use the word build to refer to the test suite, but that's not totally accurate. The word build comes from software development more than testing, and it refers to the process by which an app is compiled and all its components brought together and made ready to run. Nowadays, automated tests are considered to be part of a build, even though they're usually not part of the app compilation step, and even though the app is usually ready to run before it's tested. Build can refer to the overall system including compilation, testing, and reporting. It can also refer to a particular instance or run of those systems. So, for example, I could say, "our build is slow," meaning that the whole pipeline is generally slow. Or I could say, "that build was slow," referring to a specific run of the tests. Context should make it clear which is meant.
5. Continuous Integration Server or CI server. This is a server that usually has a web app running on the front end, which you either host yourself or use in another hosted environment. CI servers allow you to define pipelines of functionality that should run when different actions take place. For example, if a developer makes a change to the app and proposes it on GitHub, a CI server might automatically pick up that change, then build the new version of the app, then run a test server with the app's web backend, then pass the built app to an Appium testsuite to run on devices, and then gather data from the testsuite, and then finally determine whether a build actually passed. The website for the CI server would allow you to configure all of this or view the history of previous builds so you have an idea of the health of your app and of your build pipeline.
6. Test runner. A test runner is a program that will find and collect testcases, run them in the programming language you have adopted, and provide reports about which tests passed and failed. The test runner we'll be using in this course is called pytest. Since we're using Pytest, we don't have to worry about building fancy reporters for our tests. And Pytest can also easily be integrated with CI servers.
7. Test framework. A test framework is a collection of classes and utilities that make your life easier when writing tests. There's really two levels of a test framework. One is the standard test tooling that comes with any generic framework you might use. This would include features like conventions for defining tests, the ability to specify the set up or clean up behavior for groups of tests, and so on. Pytest is also a test framework in this sense. Most test runners are also test frameworks in this sense, in that they provide the basic patterns and conventions for writing your tests. But typically we also build our own framework on top of them, in a way which is custom for our own app or in a way which is generic to Appium or Selenium. So in our custom framework we might create a base class which has utilities for finding elements in our app, or starting sessions, or custom expected conditions that make sense for us. Basically anything which we notice is useful in more than one place in our testsuite is a good candidate for becoming part of our test framework. And the framework we end up using is almost always a hybrid of some open source framework like Pytest, plus all the custom stuff that we build on top that's useful throughout our testsuite.

?et's stop talking theory and start talking about how we'd take some of the automation we've written so far and embed it within a very basic test framework. Alright, I'm in my code editor, and I'm going to start with one of the Appium scripts we wrote earlier. It's called <code>elements_ios.py</code>, and it's in the <code>mobile</code> directory in our project. 

    from os import path
    from appium import webdriver
    from appium.webdriver.common.mobileby import MobileBy
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    CUR_DIR = path.dirname(path.abspath(__file__))
    APP = path.join(CUR_DIR, 'TheApp.app.zip')
    APPIUM = 'http://localhost:4723'
    CAPS = {
        'platformName': 'iOS',
        'platformVersion': '16.2',
        'deviceName': 'iPhone Pro 14',
        'automationName': 'XCUITest',
        'app': APP,
    }

    driver = webdriver.Remote(APPIUM, CAPS)
    try:
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
    finally:
        driver.quit()

For now I'm going to copy and paste the contents of this file, and then create a new directory within our project called <code>suite</code>, since this is where our first test suite examples will live. Within this directory, I'll create a new file called <code>test_echo_box.py</code>. The name of this file is important, because by default, Pytest will look to run tests inside files that begin with <code>test_</code>. We don't *need* to follow this convention, but it makes life easier, and it's nice to know that this is a file that defines testcases. 

As you might have guessed, we are going to work on testing the Echo Box functionality of The App. We've already automated this user flow, and now we are going to reconfigure it so that it works well within Pytest. Now that I have this file open I'll paste in the code from the previous example. All I'm going to do is take the actual test code, beginning with the <code>driver</code> initialization, and indent it one block. And to head up this block, I'm going to define a function. I'll call it <code>test_echo_box</code>:

    def test_echo_box():
        <previous code>

It doesn't need any parameters. Its sole purpose is to hold the logic for our test. And again, the name here is important, because when Pytest is looking for testcases to run, it will look for functions inside test files whose function name begins with <code>test_</code>, just like with the test file itself. This is actually the bare minimum we need to do to get this running with Pytest. So let's give it a try. I'll head over to my terminal, and now I'll change into the directory called <code>suite</code>. Because I had already installed Pytest, I should now be able to just run the pytest command, and Pytest should pick up my test file and my test case and run it. 

    pytest

Oh my, it failed immediately. And actually, I knew this was going to happen, but I wanted to illustrate what it looks like when a Pytest run fails.

Notice that we don't just get an exception printed out. We get a whole lot of other information as well, including the summary of the test report at the very bottom, where we see that <code>1 test failed in 0.30s</code>. And immediately above that, we have the short description of the error that caused the test to fail:

    Message: An unknown server-side error occurred while processing the command.
    Original error: Bad app:
    /Users/jlipps/Code/appium-pro/foundations-code/suite/TheApp.app.zip. App paths
    need to be absolute or an URL to a compressed app

What is this? Somehow Appium thinks my app is bad? Well let me look at the path to it here. Aha! I see what's wrong. I copied and pasted the code from the *other* directory where I had downloaded my mobile app. But now I'm in a *new* directory, and the code hasn't been updated to reflect that. So let's go back to the editor, and make sure that this file can actually find the app correctly. To fix it, I'll just help Python navigate back up a directory, and then down into the <code>mobile</code> directory where the app file is actually located:

    APP = path.join(CUR_DIR, '..', 'mobile', 'TheApp.app.zip')

If you haven't seen this before, the two dots in a path means the parent directory. So here we're telling Python to start at the current directory (which is now the <code>suite directory</code>), go up to the parent, then go into the <code>mobile</code> directory from there, where the app file will be found. Alright, let's try to run the <code>pytest</code> command again with that change. It's taking a lot longer to do something this time, so that's a good sign. Notice how it said that it collected 1 item---that was Pytest doing the hard work of finding our test method. But let me switch over to my simulator, and sure enough, it's doing its thing! And the test is already over. Pytest gives us a nice report that our single test passed, which is also represented by a single green dot.

Pytest's philosophy is similar to most other test runners, which is that a passing test is nothing to be remarked on really, so all we get is a little dot for output, whereas a failing test would produce a big red F, making it really easy to see in context. So this is technically all we need to do to get our test running in Pytest. But there are lots of ways we could improve what we've done so far. Let's take a look at the code. One of the things I don't like about all of this is the fact that we have to use this <code>try/finally</code> pattern. It's pretty unsightly and requires a more indentation than seems totally necessary. And in fact we can take advantage of a Pytest feature called Pytest "fixtures" to help here.

Pytest fixtures are basically just functions wrapped with a special annotation so that Pytest knows they are to be treated as fixtures. Fixtures can be used as arguments for test methods, and when they are included in the argument list for a test function, that test has access to whatever the fixture returns. Let's take the first step in this direction by defining a fixture function. Let's call it <code>driver</code>, since the purpose of this fixture is to provide a driver for our test:

    def driver():
        pass

Right now it's just a function. To make it a fixture, we have to annotate it with <code>pytest.fixture</code>. The way we do it is as follows. First, we need to import the Pytest library so we can use it, which I'll do up top:

    import pytest

Now, I can annotate the driver method with <code>pytest.fixture</code>:

    @pytest.fixture
    def driver():
        pass

What does it mean to annotate a function? It means to place another function name immediately above it, with the <code>@</code> symbol in front. This causes Python to treat <code>pytest.fixture</code> as an annotation. This is not the place to go into the details of annotations. For now, all you need to know is that this particular annotation turns a regular old function into a Pytest fixture for us. Now, we need to make the fixture return something. So let's take the capabilities definition and the driver instantiation and put it inside the fixture:

    @pytest.fixture
    def driver():
        CAPS = {
            'platformName': 'iOS',
            'platformVersion': '16.2',
            'deviceName': 'iPhone 14 Pro',
            'automationName': 'XCUITest',
            'app': APP,
        }
        driver = webdriver.Remote(
            command_executor=APPIUM,
            desired_capabilities=CAPS
        )
        return driver

This is nice, because we've taken driver creation and abstracted it out of the test. But how do we use it? Well, we need to tell Pytest that our test method actually needs this driver. The way we do that is by putting the name of the fixture as an argument to the test method:

    def test_echo_box(driver):

Now, whenever we start executing this method, Pytest will guarantee that we have a driver object which has been created by the fixture. I like this approach because we will have many different tests that use the same driver creation logic. All the tests we write for the iOS version of our app will use the same driver instantiation logic, so we don't want to reproduce it at the top of every test case! That would make our tests totally unreadable. But we haven't yet solved the problem with the <code>try/finally</code>. To solve this problem, Pytest will want us to use another advanced feature of Python, which is a special keyword called <code>yield</code>. <code>yield</code> is kind of like <code>return</code> but it allows for the caller of the function to actually return control back to the called function at any point! It's pretty wild, and not necessary to really understand at this point. But let's see how we use it.

Now, rather than <code>return</code>ing the driver, we are going to <code>yield</code> it.

      yield driver

What we are telling Pytest when we do this is basically, "Hey, Pytest. Give this driver value to whomever is calling this fixture. But then whenever *they're* done with the test, come back here and keep running whatever code is next." So what do we want to do next, after the test is finished? We want to quit the driver! Pytest will make sure to come back to this point and keep running our fixture code whether the test past or failed, and whether there was any exception during the course of the test. This is one of the great things about using a framework like Pytest: we don't have to worry about implementing any of this logic. It's all done for us. So we can simply delete the <code>driver.quit</code> below, and pull it up immediately below the <code>yield</code> statement:

      yield driver
      driver.quit()

Now, I can get rid of the <code>try</code> and the <code>finally</code>, and dedent all of this code. Wow, this looks so much cleaner! I now have good abstraction and separation of concerns, together with much more readable code. The <code>driver</code> fixture is responsible for starting the session and ending the session cleanly, and the test function is responsible only for running the test itself. We merely have to tell Pytest that our test relies on the <code>driver</code> fixture, and we're good to go! But before we get too excited, let's run it to make sure we didn't break anything.

It appears to be taking some time doing something, which is a good sign because it means a test is probably starting. I'll head over to my simulator, and yep, here we go. Same test logic of course, so nothing new to see, but, it worked, and we got the nice green report from Pytest.

Now there's one more improvement I want us to make right now. At the moment, the Pytest fixture and the test code are in the same file. But we could imagine that we might have many test files for our application. I generally recommend having one test file per feature, so that everything stays organized. My test app has a number of features, so I'd expect to have a number of files for a full-on testsuite. That means that we don't want our <code>driver</code> fixture in any of the test files. It should live somewhere else entirely. But where? Pytest to the rescue! Luckily, Pytest has a convention for where to put things like fixtures, so that they are loaded automatically and made available to all tests.

What we want is to create a new file called <code>conftest.py</code>, right in our <code>suite</code> directory. In this blank file, I'm simply going to cut and paste the fixture we created, along with all of the constant values we define up top:

    CUR_DIR = path.dirname(path.abspath(__file__))
    APP = path.join(CUR_DIR, '..', 'mobile', 'TheApp.app.zip')
    APPIUM = 'http://localhost:4723'


    @pytest.fixture
    def driver():
        caps = {
            'platformName': 'iOS',
            'platformVersion': '13.6',
            'deviceName': 'iPhone 11',
            'automationName': 'XCUITest',
            'app': APP,
        }

        driver = webdriver.Remote(APPIUM, caps)
        yield driver
        driver.quit()

I notice that I don't have the appropriate imports, so I'll move them over from the test file as well:

    import pytest
    from os import path
    from appium import webdriver

We need Pytest, the path stuff for finding the app, and of course the webdriver module itself. Now if I go back to my test file, it looks much more beautiful and clean.

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

It's just the test logic and nothing more. But let's make sure this refactor works. So we'll go over to the terminal and run <code>pytest</code> again. Off we go, and it's done. So this is where we are going to end our discussion of runners and frameworks. But before we stop, let's set the stage for some future improvements. One question you might have had is, OK, this works for one version of The App, the iOS version. But what about the Android version? How would we test that here as well? And it is certainly a challenge, because there are many ways to add Android support to this testsuite which would involve a lot of duplication of code, which we'd want to avoid. We might also still not be happy about the readability of this test method. I know I'm not! It's easy for our eyes to get lost in a maze of locator strategies and expected conditions. As a new person coming to this code, it would be a bit difficult to know what it's meant to test, just by reading it, without any help from the test method title itself. And these are all problems we're going to address






