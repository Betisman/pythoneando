from sqlalchemy import *
from sqlalchemy.orm import *

db = create_engine('sqlite:///joindemo.db')
#db.echo = True
metadata = MetaData(db)
users = Table('users', metadata, autoload=True)
emails = Table('emails', metadata, autoload=True)
session = create_session()

class User(object):
	def __init__(self, name=None, age=None, password=None):
		self.name = name
		self.age = age
		self.password = password
	def __repr__(self):
		return self.name
class Email(object):
	def __init__(self, address=None):
		self.address = address
	def __repr__(self):
		return self.address

emailmapper = mapper(Email, emails)
usermapper = mapper(User, users, properties={'emails':relation(emailmapper)})
mary = session.query(User).get_by(name='Mary')
print mary.emails
clear_mappers()

emailmapper = mapper(Email, emails)
usermapper = mapper(User, users, properties={'emails':relation(Email)})
mary = session.query(User).get_by(name='Mary')
print mary.emails
clear_mappers()

mapper(Email, emails)
mapper(User, users, properties={'emails':relation(Email)})
mary = session.query(User).get_by(name='Mary')
print mary.emails
clear_mappers()

try:
	usermapper = mapper(User, users, properties={'emails':relation(Email)})
except exceptions.InvalidRequestError:
	print 'Ignoring the deliberately-provoked error and moving on...'
clear_mappers()

emailmapper = mapper(Email, emails)
usermapper = mapper(User, users, properties={'emails':relation(Email)})
emailmapper.add_property('user', relation(User))
john = session.query(User).get_by(name='John')
print john.emails
carl_address = session.query(Email).get_by(address='carl@nospam.net')
clear_mappers()

emailmapper = mapper(Email, emails)
usermapper = mapper(User, users, properties={'emails':relation(Email, backref='user')})
harry = User(name='Harry', age=47)
em1 = Email('harry@nowhere.com')
em2 = Email('harry@example.org')
em1.user = harry
harry.emails.append(em2)
print em2.user
print harry.emails
session.save(harry)
session.flush()
clear_mappers()

