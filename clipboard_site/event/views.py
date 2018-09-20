from django.http import Http404
from django.shortcuts import render, get_object_or_404
#from .models import Event
import requests
import os
import sys

class EventData:
	events = None

	@staticmethod
	def get_event(event_id):
		return next(e for e in EventData.events if e['id'] == event_id)

def get_env_var(name):
    try:
        return os.environ[name]
    except KeyError:
        print('Error: {0} not set. If this value was recently set, close all python processes and try again'.format(name))
        sys.exit(1)

db_client_ip = get_env_var('DB_CLIENT_IP')

def index(request):
	events_response = requests.get(f'http://clipboard_db_client:5000/getevents', params= {
        'start_timestamp': 0, 
        'end_timestamp': 10000000000
    })
	#all_events = [Event.objects.create(**event) for event in events.json()]
	#all_events = Event.objects.all()
	EventData.events = events_response.json()
	#request.session['events'] = events
	return render(request, 'event/index.html', {'all_events': EventData.events})

def detail(request, event_id):
	#events = request.session['events']

	event = EventData.get_event(event_id)
	#event = get_object_or_404(Event, pk=event_id)
	return render(request, 'event/detail.html', {'event': event})

def url_redirect(request):
	return HttpResponseRedirect('/events')
