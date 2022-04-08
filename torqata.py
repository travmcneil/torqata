from app import create_app, db
from app.models import User, Movies

app = create_app()

@app.shell_context_processor
def make_shell_contect():
    return {'db': db, 'User': User, 'Movies': Movies}