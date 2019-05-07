import os

from api.app_factory import create_app
from api.lib.database import db


app = create_app(os.getenv('FLASK_ENV'))


@app.cli.command('db_create_all')
def db_create_all():
    db.create_all()


if __name__ == '__main__':
    app.run(port=5050)
