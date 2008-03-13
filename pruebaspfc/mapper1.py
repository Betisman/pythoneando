from sqlalchemy import *
from sqlalchemy.orm import *

db = create_engine('sqlite:///joindemo.db')
db.echo = True

metadata = MetaData(db)

users = Table('users', metadata, autoload=True)
emails = Table('emails', metadata, autoload=True)

class User(object):
	pass
class Email(object):
	pass

usermapper = mapper(User, users)
emailmapper = mapper(Email, emails)

session = create_session()

mary = session.query(User).selectfirst(users.c.name=='Mary')
mary.age += 1
session.flush()

fred = User()
fred.name = 'Fred'	
fred.age = 37

print 'about to flush() without a save()...'
session.flush()
session.save(fred)
print 'just called save(). Now flush will actually do something.'
session.flush()

session.delete(fred)
session.flush()