# Render-test

A basic website -- just enough to test out hooking things up to render, and not much more.

We will go over steps in lecture. You should fill out the following:

## What steps do I need to do when I download this repo to get it running?

fork and or clone repo

## What commands starts the server?

modify pip file to 3.13, my current
pipenv install flask
pipenv run flask --app server.py run
-Don't run pipenv shell
pipenv run gunicorn server:app

## Before render

Before render you will need to set up a more production-grade backend server process. We will do this together in lecture, once that's done you should update the command above for starting the server to be the **production grade** server.

# PSQL

\pset pager off
\dt
\d guestbook
SELECT \* FROM guestbook;
