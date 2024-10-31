from SPARQLWrapper import SPARQLWrapper
from flask import current_app, g


def get_db_connection():
    """
    Returns the database connection.
    """
    if 'db' not in g:
        url = current_app.config['knowledge_url']
        g.db = SPARQLWrapper(url)
    return g.db


def close_db(e=None):
    g.pop('db', None)
