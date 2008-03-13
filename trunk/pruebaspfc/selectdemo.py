from sqlalchemy import *

db = create_engine('sqlite:///tutorial.db')

db.echo = True

metadata = MetaData(db)
users = Table('users', metadata, autoload=True)

def run(stmt):
	rs = stmt.execute()
	for row in rs:
		print row

s = users.select(users.c.name == 'John')
run(s)
s = users.select(users.c.age <40)
run(s)

s = users.select(and_(users.c.age < 40, users.c.name != 'Mary'))
run(s)
s = users.select(or_(users.c.age < 40, users.c.name != 'Mary'))
run(s)
s = users.select(not_(users.c.name == 'Susan'))
run(s)

s = users.select((users.c.age < 40) & (users.c.name != 'Mary'))
run(s)
s = users.select((users.c.age < 40) | (users.c.name != 'Mary'))
run(s)
s = users.select(~(users.c.name == 'Susan'))
run(s)

s = users.select(users.c.name.startswith('M'))
run(s)
s = users.select(users.c.name.like('%a%'))
run(s)
s = users.select(users.c.name.endswith('n'))
run(s)

s = users.select(users.c.age.between(30, 39))
run(s)
s = users.select(users.c.name.in_('Mary', 'Susan'))
run(s)

s = users.select(func.substr(users.c.name, 2, 1) == 'a')
run(s)

s = select([users], users.c.name != 'Carl')
run(s)
s = select([users.c.name, users.c.age], users.c.name != 'Carl')
run(s)

s = select([func.count(users.c.user_id)])
run(s)
s = select([func.count("")], from_obj=[users])
run(s)