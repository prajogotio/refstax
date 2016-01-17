from app import db
import datetime 

class User(db.Model):
	__tablename__ = 'users'
	user_id = db.Column(db.Integer(), primary_key=True)
	username = db.Column(db.String(), unique=True, nullable=False)
	password = db.Column(db.String(), nullable=False)

	def __repr__(self):
		return '<User[{id}]>'.format(id=user_id)


class Folder(db.Model):
	NOT_DELETED = 0
	DELETED = 1

	__tablename__ = 'folders'
	folder_id = db.Column(db.Integer(), primary_key=True)
	owner_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'), nullable=False)
	parent_id = db.Column(db.Integer(), db.ForeignKey('folders.folder_id'))
	title = db.Column(db.String(), nullable=False)
	date_created = db.Column(db.DateTime, server_default=db.func.now())
	date_modified = db.Column(db.DateTime, server_default=db.func.now())
	deleted = db.Column(db.Integer, default=NOT_DELETED)

	def __repr__(self):
		return '<Folder[{id}]>'.format(id=folder_id)


class Url(db.Model):
	OFF_STACK = 0
	ON_STACK = 1

	__tablename__ = 'urls'
	url_id = db.Column(db.Integer(), primary_key=True)
	owner_id = db.Column(db.Integer(), db.ForeignKey('users.user_id'), nullable=False)
	url = db.Column(db.String(), nullable=False)
	date_created = db.Column(db.DateTime, server_default=db.func.now())
	date_modified = db.Column(db.DateTime, server_default=db.func.now())
	status = db.Column(db.Integer, default=ON_STACK)
	parent_id = db.Column(db.Integer, db.ForeignKey('folders.folder_id'))

	def __repr__(self):
		return '<Url[{id}]>'.format(id=url_id)


def init_db():
	db.drop_all()
	db.create_all()