#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# try:
	# from xml.etree import ElementTree
# except ImportError:
	# import gdata.calendar.service
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time
import getpass

class MyGCalendar():

	def __init__(self, email, password):
		""" Constructor de la clase MyGCalendar.
		email y password son los parametros necesarios para el login.
		"""
		self.cal_client = gdata.calendar.service.CalendarService()
		self.cal_client.email = email
		self.cal_client.password = password
		self.cal_client.source = 'Google-Calendar_Python_Sample-1.0'
				
	
	def login(self):
		self.cal_client.ProgrammaticLogin()

	def printCalendars(self):
		feed = self.cal_client.GetAllCalendarsFeed()
		print 'Printing allcalendars: %s' % feed.title.text
		for i, a_calendar in zip(xrange(len(feed.entry)), feed.entry):
			print '\t%s. %s' % (i, a_calendar.title.text,)
	
	def printEventsDefaultCalendar(self):
		feed = self.cal_client.GetCalendarEventFeed()
		print 'Events on Primary Calendar: %s' % (feed.title.text,)
		for i, an_event in zip(xrange(len(feed.entry)), feed.entry):
			print '\t%s. %s' % (i, an_event.title.text,)
			for p, a_participant in zip(xrange(len(an_event.who)), an_event.who):
				print '\t\t%s. %s' % (p, a_participant.email,)
				print '\t\t\t%s' % (a_participant.name,)
				print '\t\t\t%s' % (a_participant.attendee_status.value,)

	def ahora(self):
		return time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time()))
	
	def ahoraMasMinutos(self, minutos=0):
		return time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + minutos*60))
	
	def insertarVuelo(self, vuelo):
		#titulo = "VUELAS EL " + vuelo.dia
		mensaje = vuelo.toEventString()
		event = gdata.calendar.CalendarEventEntry()
		#event.title = atom.Title(text=titulo)
		event.title = atom.Title(text=mensaje)
		#event.content = atom.Content(text=mensaje)
		event.content = atom.Content(text="")
		event.where.append(gdata.calendar.Where(value_string="LECU"))
		# start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + self.ahoraMasMinutos(10)))
		# end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + self.ahoraMasMinutos(60)))
		start_time = self.ahoraMasMinutos(10)
		end_time = self.ahoraMasMinutos(60)
		event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
		metodo = {'method' : 'sms'}
		reminder = gdata.calendar.Reminder(minutes=5, extension_attributes=metodo)
		event.when[0].reminder.append(reminder)
		new_event = self.cal_client.InsertEvent(event, '/calendar/feeds/default/private/full')
		return new_event
	
	def enviarSms(self, mensaje):
		event = gdata.calendar.CalendarEventEntry()
		event.title = atom.Title(text=mensaje)
		event.content = atom.Content(text="")
		event.where.append(gdata.calendar.Where(value_string="HT"))
		start_time = self.ahoraMasMinutos(10)
		end_time = self.ahoraMasMinutos(60)
		event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
		metodo = {'method' : 'sms'}
		reminder = gdata.calendar.Reminder(minutes=5, extension_attributes=metodo)
		event.when[0].reminder.append(reminder)
		new_event = self.cal_client.InsertEvent(event, '/calendar/feeds/default/private/full')
		return new_event
	
	def estaVuelo(self, vuelo):
		feed = self.cal_client.GetCalendarEventFeed()
		for an_event in feed.entry:
			if vuelo.toEventString() == an_event.title.text:
				return True
		return False

	def insertarEvento(self, title='TituloEvento', 
      content='ContenidoEvento', where='LugarEvento',
      start_time=None, end_time=None, recurrence_data=None, reminderMinutes=5):
		
		event = gdata.calendar.CalendarEventEntry()
		event.title = atom.Title(text=title)
		event.content = atom.Content(text=content)
		event.where.append(gdata.calendar.Where(value_string=where))
		if start_time is None:
			# Use current time for the start_time and have the event last 1 hour
			start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 15*60))
			end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 3600))
		event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
		metodo = {'method' : 'sms'}
		reminder = gdata.calendar.Reminder(minutes=reminderMinutes, extension_attributes=metodo)
		event.when[0].reminder.append(reminder)
		new_event = self.cal_client.InsertEvent(event, '/calendar/feeds/default/private/full')
		return new_event
	
	def estaEvento(self, calendario, event):
		pass
	
	def addSmsReminder(self, event, minutes):
		for a_when in event.when:
			if len(a_when.reminder) > 0:
				a_when.reminder[0].extension_attributes['method'] = 'sms'
				print 'len >0'
				a_when.reminder[0].minutes = minutes
			else:
				metodo = {'method' : 'sms'}
				print 'else'
				a_when.reminder.append(gdata.calendar.Reminder(minutes=minutes, extension_attributes=metodo))

		print 'Adding %d minute reminder to event' % (minutes)
		return self.cal_client.UpdateEvent(event.GetEditLink().href, event)

	
	def addEmailReminder(self, calendar, event, minutes=10):
		pass
		
	def nuevoEventoConAvisoSms(self):
			pass


##mygc = MyGCalendar('betisman@gmail.com', 'logaritmo')
#####
# username = raw_input('email: ')
# password = getpass.getpass('password: ')
# mygc = MyGCalendar(username, password)
######
##mygc.login()
##mygc.printCalendars()
##evento = mygc.insertarEvento(title='Ramon', content='Avisar al gayer del Ramón', where='casa de Martita',start_time=None, end_time=None, recurrence_data=None, reminderMinutes=10)
#print "\n".join(dir(evento))
##print evento.when[0].reminder
#evento = mygc.addSmsReminder(evento, 0)
#print evento.when[0].reminder[0]
#print "\n".join(dir(gdata.calendar.CalendarEventEntry))
#print gdata.calendar.Reminder.__doc__