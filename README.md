This is a simple application to clone the mercuiral repo, then post it over to Github
to allow it code to be used by other tools like Travis CI.

## Setup

hg clone the repo and then setup REPO_PATH to point to that directory.

Ammend the settings.py as necessary.

Run the app with gunicorn,

```
gunicorn mirror:app
```
