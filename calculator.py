#!/usr/bin/env python

"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

def index(*args):
    page = """
    <h1>WSGI Calculator</h1>
    
    <h2>Use Examples</h2>
      <ol>
        <li>To add: append /add/number1/number2 to URL</li>
        <li>To subtract: append /subtract/number1/number2 to URL</li>
        <li>To multiply: append /multiply/number1/number2 to URL</li>
        <li>To divide: append /divide/number1/number2 to URL</li>
      </ol>
    """
    return page


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    print("Inside Add")
    sum = 0
    for arg in args:
        try:
            sum += int(arg)
        except (ValueError, TypeError):
            pass

    return "{}".format(sum)

# TODO: Add functions for handling more arithmetic operations.

def multiply(*args):
    """ Return a STRING with the product of the arguments """
    print("Inside Multiply")
    product = 1
    print("Product is {}".format(product))
    for arg in args:
        try:
            product *= int(arg)
            print("Product is {}".format(product))
        except (ValueError, TypeError):
            pass

    return "{}".format(product)

def divide(*args):
    """ Return a STRING with the quotient of the first arg to the second arg.
    Allow only two args. """
    print("Inside Divide")
    #if len(*args) > 2:
    #    return "No more than 2 input numbers permitted"

    dividend, divisor = args
    print("The dividend is {} and the divisor is {}".format(dividend, divisor))
    for arg in args:
        try:
            quotient = int(dividend)/int(divisor)
        except (ValueError, TypeError):
            pass

    return "{}".format(quotient)

def subtract(*args):
    """ Return a STRING of the difference of first arg minus second arg.
    Allow only two args."""
    print("Inside Subtract")
    #if len(*args) > 2:
    #    return "No more than 2 input numbers permitted"

    num1, num2 = args
    for arg in args:
        try:
            difference = int(num1) - int(num2)
        except (ValueError, TypeError):
            pass

    return "{}".format(difference)

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        'add': add,
        'multiply': multiply,
        'subtract': subtract,
        'divide' : divide,
        '' : index
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    # Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    # Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    #  Add error handling for a user attempting
    # to divide by zero.

    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        print("The raw path environ is: {}".format(path))
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        print("the parsed func is {} and args are {}".format(func,args))
        body = func(*args)
        print("Func was found and returned body {}".format(body))
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Divide by Zero Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    print("Within main routine")
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
