"""Simple function."""
from reactpy import component, html


@component
def app():
    """Create the app."""
    return html.h1("Hello, world!")
