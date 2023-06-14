"""CLI entry points."""
from reactpy import run

from .main import app


def main(args=None):
    """Entry point for the application script."""
    return run(app)
