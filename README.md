# fix-the-date
A web app to find a suitable date for attendees of an event.

## Components
The app's frontend part is done *html5* and *vue.js*. At the time everything is in a single file: [`index.html`](https://github.com/clemensmanert/fix-the-date/blob/master/html/index.html).
The backend part is done in *python3* with *flask*, *sqlalchemy* and *alembic*.

## Development environment
1. Clone the repo: `git clone https://github.com/clemensmanert/fix-the-date`
2. Setup the *python* enviroment `python -m venv venv` inside the project's root.
3. If you do not want to use *Sqlite*, or want the database to be locate somewhere else, change the database config in the `app.py` to your needs.
4. Create a development configuration for the frontend `cp html/config.js_sample html/config.js`
5. Activate the python environment `source venv/bin/activate`
6. Install requirements `pip install -r ./requirements.txt`.
7. Create the database `flask db upgrade`
8. Run flask `flask run`

Now you can open the app in your browser at [localhost:5000](http://localhost:5000)
