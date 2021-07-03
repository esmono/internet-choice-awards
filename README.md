# Internet choice awards 🏆

## Installation

This project requieres [`pipenv`](https://pypi.org/project/pipenv/) to work properly.
Documentation describe different methods to install depending on your environment.

Project commands are defined in the [Makefile](Makefile). `make isntall-dev` will install all project dependencies.

Some commands requires [posgresql](https://www.postgresql.org/download/) to be installed locally.

## Development

Configuration for local development is expected to live in a `.env` file that is not checked into version control. Use the `.env.example` tocreate your own `.env`.

Run `make test` to run the unit tests and gather coverage information.

## Running Application locally
* Set up the database: `make create-db` and `make migrate`

* `make start` will start a Django devserver.
You can then hit the admin at [http://localhost:8080/admin/](http://localhost:8080/admin/)
So long as `DEBUG=True` is in your `settings.py` file, this will work and also cover serving static files.

* It's also a good idea to run `make test` to make sure the test suite is running correctly and all tests are passing before starting development.

## Running Application

### Using docker

```
docker-compose build
docker-compose up
docker-compose exec web make migrate
docker-compose exec web make static
docker-compose exec web make loaddata
docker-compose exec web make create-superuser
```

### Using podman!

Builds, (re)creates, starts, and attaches to containers.

`static` will collect static files. Note that gunicorn will not serve the static files it will be done by nginx.

`loaddata` (optional) will populate the database with sample data.

`create-superuser` (optional) will promp for data to create a staff user.

```
podman-compose build
podman-compose up
podman exec internet-choice-awards_web_1 make migrate
podman exec internet-choice-awards_web_1 make static
podman exec internet-choice-awards_web_1 make loaddata
podman exec -it internet-choice-awards_web_1 make create-superuser
```


### gunicorn
This is the program that will actually run the application server. It uses `wsgi.py` in the main project folder, in this case under `awards.wsgi.py`. This will be started and bind to port 8000.

### nginx
This is the program that will serve http requests and static files.

## Notes
This project makes use of these development tools:

* [Black](https://black.readthedocs.io/en/stable/) for opinionated code formatting
* [coverage](https://coverage.readthedocs.io/en/coverage-5.5/) for code coverage information
* [flake8](https://flake8.pycqa.org/en/latest/) for linting and [pep8](https://www.python.org/dev/peps/pep-0008/) enforcement
* [pipenv](https://pypi.org/project/pipenv/) for managing packages
