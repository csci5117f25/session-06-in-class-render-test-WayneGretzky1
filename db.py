""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from contextlib import contextmanager
import logging
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    DATABASE_URL = os.environ['DATABASE_URL']
    current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode='require') #This is like having 100 receptionists at a hotel, we don't need to hire a new one for each guest


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn() #This gives us a receptionist
        yield connection
    finally:
        pool.putconn(connection) #Receptionist goes back to front desk when completed


@contextmanager
def get_db_cursor(commit=False): #This gives us a cursor, a tool to run SQL commands
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

def add_person (name):
    # Since we're using connection pooling, it's not as big of a deal to have
    # lots of short-lived cursors (I think -- worth testing if we ever go big)
    with get_db_cursor(True) as cur:
        current_app.logger.info("Adding guest %s", name)
        cur.execute("INSERT INTO guestbook (name) values (%s)", (name,))

def get_people(page = 0, people_per_page = 10):
    ''' note -- result can be used as list of dictionaries'''
    limit = people_per_page
    offset = page*people_per_page
    with get_db_cursor() as cur:
        cur.execute("SELECT * FROM guestbook ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
        return cur.fetchall()