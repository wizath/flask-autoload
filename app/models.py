from app import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64))
    created_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Image %r>' % self.filename
