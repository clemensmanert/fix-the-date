# fix-the-date
A web app to find a suitable date for attendess of an event.

## Components
The app's frontend part is done *html5* and *vue.js*. At the time everything is in a single file: [`index.html`](https://github.com/clemensmanert/fix-the-date/blob/master/index.html).
The backend part is done in *python3* with *flask*, *sqlalchemy* and *alembic*.

## How to deploy
1. Setup the *python* enviroment: Run `python -m venv venv` inside the project's root.
2. Install requirements: Run `pip install -r ./requirements.txt` inside the project's root.
4. If you do not want to use *Sqlite*, or want the database to be locate somewhere else, change the database config in the [`app.py`](https://github.com/clemensmanert/fix-the-date/blob/fb1ea2d875029585045d020ff2251fd6ede9a7de/app.py#L10) to your needs.
5. Point your webserver to the project root. The frontend does not need any config.
