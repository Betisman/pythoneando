# try:
  # from xml.etree import ElementTree
# except ImportError:
  # from elementtree import ElementTree
from elementtree import ElementTree
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time

email = 'betisman@gmail.com'
password = 'logaritmo'

class MyCalendar():
	
	def login(self, email, password):
		self.cal_client = gdata.calendar.service.CalendarService()
		self.cal_client.email = email
		self.cal_client.password = password
		self.cal_client.source = 'Google-Calendar_Python_Sample-1.0'
		self.cal_client.ProgrammaticLogin()

	def printUserCalendars(self):
		feed = self.cal_client.GetAllCalendarsFeed()
		print 'Printing allcalendars: %s' % feed.title.text
		for i, a_calendar in zip(xrange(len(feed.entry)), feed.entry):
			print '\t%s. %s' % (i, a_calendar.title.text,)
	
	def insertEvent(self, title='Tennis with Beth',
	content='Meet for a quick lesson', where='On the courts',
	start_time=None, end_time=None, recurrence_data=None):

		event = gdata.calendar.CalendarEventEntry()
		event.title = atom.Title(text=title)
		event.content = atom.Content(text=content)
		event.where.append(gdata.calendar.Where(value_string=where))

		if recurrence_data is not None:
			# Set a recurring event
			event.recurrence = gdata.calendar.Recurrence(text=recurrence_data)
		else:
			if start_time is None:
				# Use current time for the start_time and have the event last 1 hour
				start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime())
				end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', 
				time.gmtime(time.time() + 3600))
			event.when.append(gdata.calendar.When(start_time=start_time, 
			end_time=end_time))

		new_event = self.cal_client.InsertEvent(event, 
		'/calendar/feeds/default/private/full')
		return new_event
		
	def addReminder(self, event, minutes=10):
		for a_when in event.when:
			if len(a_when.reminder) > 0:
				a_when.reminder[0].minutes = minutes
			else:
				a_when.reminder.append(gdata.calendar.Reminder(minutes=minutes))

		print 'Adding %d minute reminder to event' % (minutes,)
		return self.cal_client.UpdateEvent(event.GetEditLink().href, event)
	
def getTime(delayMin):
	delaySecs = delayMin * 60
	delaySecs = time.time()+delaySecs
	return time.gmtime(delaySecs)
	
myc = MyCalendar()
print 'mycalendar()'
myc.login(email, password)
print 'login'
myc.printUserCalendars()
time = getTime(10)
event = myc.insertEvent(title='Prueba',
	content='Esto es una prueba', where='hattrick',
	start_time=None, end_time=None, recurrence_data=None)
myc.addReminder(event, minutes=0)