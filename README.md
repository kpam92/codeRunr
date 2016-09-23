# codeRnr

codeRnr is a JavaScript interpreter turned full-stack application. Users can sign on to their account and see a list of their saved code snippets. Users can then run these code snippets on our interpreter, as well as title the code snippets individually.

## Technologies

This application was written in Flask, a Python 'microframework' that makes writing small applications manageable for a small team in a short amount of time. We knew nothing about Flask when we embarked on this journey, and learned how to implement entirely from online tutorials and documentation.

For the code editor, we implemented CodeMirror. CodeMirror specializes in exactly that, making it easy to edit and view code in a browser. It provides the formatting and the input box for the browser, we just had to make sure the styles matched out site.

We spent lots of time doing styling for this site entirely, making everything feel modern and easy to use.

## Features

There are a few major features to keep in mind when using our application:

### Running code

This one is the most important. It was the basis for creating this application from the start. A user can run code from a CodeMirror texteditor with a 'run' button that evaluates this code and prints the result to the right box on the screen.

### Saving code snippets

When signed on to an account, the user can save code snippets with a title for future use. The code will remain the same with spacing and new lines and everything upon loading the code again.

### User authentication

Users can create accounts easily, sign on and sign off easily as well. This functionality was written by us in Python with the Flask documentation. Flask makes it easy for a developer to create user authentication.

## Flask

Python is a new language in development for us. We both started the project never using Python to develop any application. Flask is a very simple framework that utilizes Python and makes it very easy to create simple applications. In order to render a page on the browser, it takes as little as three lines, one creating the route to the application, one being a function declaration, and the third calling the Flask method render_template() on an HTML page.

Flask uses Jinja2 in order to render smart HTML pages. This makes it easy to push Python data directly to the HTML and it is implemented on render of the page.

Here is an example of the main page method of our program. All it took was a few lines in order to check if a user is present, get all code snippet titles from the database, and render the index.html page with the new data.

```javascript
  @app.route('/home', methods=['PATCH', 'GET'])
  def index():
      if not g.user:
          return redirect(url_for('login'))
      code_menu = query_db('select title, id from snippets where snippets.user_id = ?', [session['user_id']])
      return render_template('index.html', menu_items=code_menu)
```


## Thank You

We are both very proud of codeRnr, and we hope you enjoy the application. If you have any issues with codeRnr, please post them in the issues tab, it would mean a lot to us.

This app was developed by:
- [Kevin Mathews](https://github.com/kpam92)
- [Jack Tilly](https://github.com/jackftilly)
