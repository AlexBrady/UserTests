# UserTests
Application to receive input data from user tests, organise it, and return it.

There are two parts to this project:

1. Import the user data (/importer)
2. Export/show the user data (/exporter)

Note:
You will see the following parameter in a lot of the endpoint for a tester's ID:
```sh
@io.from_header('tester_id', fields.Integer(required=True))
```
This ID should be passed in the headers of your request (using curl or postman/insomnia etc.). I treated it kind of
like an authentication field for getting data for the correct tester. It's just a basic integer that
is incremented for every tester.

#### Run the command to set up the project and install requirements:

```sh
python setup.py install
```

#### Run the command to create the schedule:

```sh
env FLASK_APP=wsgi.py APP_ENV=local flask run -p 7000
```
