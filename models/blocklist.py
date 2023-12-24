from db import db



class BlockListModel(db.Model):
    __tablename__ = "blocklist"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(512), unique = True, nullable = False)