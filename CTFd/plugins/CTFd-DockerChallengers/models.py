from CTFd.models import db

class ContainerInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    container_id = db.Column(db.String(128))