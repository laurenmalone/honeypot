from behave import *

@given('a closed telnet connection')
def step_impl(context):
    # create a telnet connection and close it
    return

@when('starting the plugin')
def step_impl(context):
    try:
        print("foo")
        # send the connection to the constructor
    except SomeClosedConnectionException:
        context.exceptionFound = True

@then('an exception is thrown')
def step_impl(context):
    assert context.exceptionFound is True
