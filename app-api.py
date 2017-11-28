import os
from app import create_app
from app.model import db

app = create_app((os.getenv("ENV") or "local").lower())


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)


@app.cli.command()
def tests():
    """Run py.test on the full test suite"""
    import pytest
    pytest.main(['tests', '-v', '-l'])
