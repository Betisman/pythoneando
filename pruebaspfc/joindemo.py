from sqlalchemy import *

db = create_engine('sqlite:///joindemo.db')

metadata = MetaData(db)

users = Table('users', metadata,
	Column('user_id', Integer, primary_key=True),
	Column('name', String(40)),
	Column('age', Integer),
	Column('password', Text),
	)
# users.create()

emails = Table('emails', metadata,
	Column('email_id', Integer, primary_key=True),
	Column('address', Text),
	Column('user_id', Integer, ForeignKey('users.user_id')),
	)
# emails.create()

# i = users.insert()
# i.execute(name='Mary', age=30, password='secret')
# i.execute({'name':'John', 'age':42}, {'name':'Susan', 'age':57}, {'name':'Carl', 'age':33})

# i = emails.insert()
# i.execute({'address':'mary@example.com', 'user_id':1},
	# {'address':'john@nowhere.com', 'user_id':2},
	# {'address':'john@example.org', 'user_id':2},
	# {'address':'carl@nospam.net', 'user_id':4},
# )

def run(stmt):
	rs = stmt.execute()
	for row in rs:
		print row
	print '\n----------------------------------'

s = select([users, emails])
run(s)

s = select([users, emails], emails.c.user_id == users.c.user_id)
run(s)

s = select([users.c.name, emails.c.address], emails.c.user_id == users.c.user_id)
run(s)

s = join(users, emails).select()
run(s)

s = outerjoin(users, emails).select()
run(s)

s = outerjoin(emails, users).select()
run(s)