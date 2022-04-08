from app import app
from app.models import User, db, Movies

@app.shell_context_processor
def make_shell_contect():
    return {'db': db, 'User': User, 'Movies': Movies}