# from flask import db
# from sqlalchemy import func

# class Group(db.Model):
#     idx = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.String(20), db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
#     name = db.Column(db.String(50), nullable=False, unique=True)
#     content = db.Column(db.String(1000), nullable=False)

#     created_at = db.Column(db.DateTime(), server_default=func.now())
#     updated_at = db.Column(db.DateTime(), server_default=func.now(), onupdate=func.now())
#     is_opened = db.Column(db.Boolean(), nullable=False, default=False)
#     is_deleted = db.Column(db.Boolean(), nullable=False, default=False)