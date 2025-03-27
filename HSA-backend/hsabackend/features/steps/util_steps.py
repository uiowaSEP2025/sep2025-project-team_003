from behave import given, when, then
from selenium.webdriver.support.wait import WebDriverWait

@then(u'I wait for {n} sec')
def step_impl(context, n):
    """This makes the browser freeze for n secs. use for debugging"""
    try:
        WebDriverWait(context.browser, float(n)).until(
            lambda _: False  
        )
    except:
        pass  