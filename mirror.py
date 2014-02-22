"""
Mirror a Mercurial repository to GitHub.
"""
import hglib
import os.path
import settings

from flask import Flask, request

app = Flask(__name__)

app.config.from_object(settings)

def _log2html(log):
    """Convert a single revision (type hglib.client.revision) to HTML.
    """
    template = '<dt><strong>{0}</strong></dt><dd>{1} <br/><em>-- {2}</em></dd>'
    return template.format(log.date, log.desc, log.author)

_hgrc = """
[extensions]
hgext.bookmarks =
hggit = 
"""

@app.route('/', methods=['GET', 'POST'])
def mirror():
    """Mirror a Mercurial repository on GITHUB.
    If called via an HTTP GET show a list of recent commits (for debugging
    purposes).
    """
    if request.method == 'POST':
        if not (os.path.exists(app.config.get('REPO_PATH')) and
                os.path.isdir(app.config.get('REPO_PATH'))):
            hglib.clone(source=app.config.get('GCODE_URL'),
                        dest=app.config.get('REPO_PATH'))
        # Add hg-git extension to Mercurial.
        with open(app.config.get('REPO_PATH') + '/.hg/hgrc', 'r') as fname:
            config = fname.read()
            if not 'hggit' in config:
                with open(app.config.get('REPO_PATH') + '/.hg/hgrc', 'a') as fnm:
                    fnm.write(_hgrc)
        repo = hglib.open(app.config.get('REPO_PATH'))
        repo.pull(source=app.config.get('GCODE_URL'))
        repo.update(clean=True)
        repo.push(dest=app.config.get('GITHUB_URL'))
        return ''
    elif (request.method == 'GET' and
          (os.path.exists(app.config.get('REPO_PATH')) and
           os.path.isdir(app.config.get('REPO_PATH')))):
        repo = hglib.open(app.config.get('REPO_PATH'))
        log = repo.log(limit=10)
        html_log = [_log2html(revision) for revision in log]
        html = '\n'.join(html_log)
        return ('<html><head></head><body><h1>Recent open-ihm revisions</h1>'
                + '<dl>' + html + '</dl>' + '<h1>Config</h1> <p>'
                + str(repo.config(showsource=True)) + '</p>'
                + '</body></html>')
    elif request.method == 'GET':
        return ('<html><head></head><body><h1>open-ihm mirror (empty)</h1>'
                + '</body></html>')
