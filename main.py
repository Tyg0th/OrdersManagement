import os
from flask_migrate import upgrade
from app import create_app
from app import db
import click

from app.api.products.models import Products
from app.api.orders.models import Orders, OrderDetail
from app.api.clients.models import Clients

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db,
    Products=Products,
    Clients=Clients,
    Orders=Orders,
    OrderDetail=OrderDetail
    )


@click.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

