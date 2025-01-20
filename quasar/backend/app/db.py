from flask import current_app, g

# NOTE: Redis DB connection for potentially caching session/job ID info
def get_db_connection():
    """
    Returns the database connection.
    """
    if 'db' not in g:
        address = current_app.config['REDIS_ADDRESS']
        # g.db = SPARQLWrapper(url)
    return g.db


def close_db(e=None):
    g.pop('db', None)
