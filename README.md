This is a simple application to clone the mercuiral repo, then post it over to 
Github to allow it code to be used by other tools like Travis CI.

## Setup

Clone the original mercurial repo and then setup REPO_PATH in settings.py to point to that directory.

Run the app with gunicorn,

```
gunicorn mirror:app
```
