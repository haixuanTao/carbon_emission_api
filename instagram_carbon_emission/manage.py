import click
from flask.cli import FlaskGroup

from instagram_carbon_emission.app import create_app


def create_instagram_carbon_emission(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_instagram_carbon_emission)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Init application, create database tables
    and create a new user named admin with password admin
    """
    from instagram_carbon_emission.extensions import db
    from instagram_carbon_emission.models import User
    click.echo("create database")
    db.create_all()
    click.echo("done")

    click.echo("create user")
    user = User(
        username="peterparker",
        email="admin@mail.com",
        password="parkerpeter",
        active=True
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
