from app import db

print('/app/models.py')


class Weight(db.Model):
    rowid = db.Column(db.Integer, primary_key=True)
    mtime = db.Column(db.Integer, index=True, unique=True)
    weight = db.Column(db.Integer)
    pid = db.Column(db.String(12))

    def __repr__(self):
        return '<Weight {}>'.format(self.weight)
