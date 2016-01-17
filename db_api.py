from schema import *

def handle_user_login(username, password, session):
	u = User.query.filter(User.username==username).first()
	if u:
		if u.password==password:
			session['username'] = username
			session['user_id'] = u.user_id
		return u.password==password
	else:
		u = User(username=username,password=password)
		db.session.add(u)
		db.session.commit()
		session['username'] = username
		session['user_id'] = u.user_id
		return True

def add_url(owner_id, url):
	l = Url(owner_id=owner_id, url=url)
	db.session.add(l)
	db.session.commit()
	return {'success':True,
			'url_id':l.url_id}

def fetch_urls(owner_id):
	q = 'SELECT url_id, url FROM urls WHERE owner_id={owner_id} AND status={status} ORDER BY date_modified DESC'.format(owner_id=owner_id,status=Url.ON_STACK)
	res = db.engine.execute(q)
	return [dict(r) for r in res]

def pop_url(url_id):
	l = Url.query.filter(Url.url_id==url_id).first()
	l.status = Url.OFF_STACK
	db.session.commit()
	return True