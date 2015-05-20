import urllib2
import re

from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import JsonResponse

from django.conf import settings
from mos.cal.models import Event
from mos.core.context_processors import custom_settings_main
from mos.members.models import get_active_members
from mos.projects.models import Project
from mos.sources.models import WikiChange

def display_main_page(request):
    events = Event.future.get_n(5)
    changes = WikiChange.objects.order_by('-updated')[:5]
    projects = Project.all.order_by('-created_at')[:5]
    randommembers = list(get_active_members().exclude(contactinfo__image="").order_by('?')[:7])

    return render_to_response('index.html', {
        'event_error_id': ' ',
        'latestevents': events,
        'latestchanges': changes,
        'latestprojects': projects,
        'randommembers': randommembers,
    }, context_instance=RequestContext(request, processors=[custom_settings_main]))

def display_cellardoor(request):
    events = Event.future.all()
    return render_to_response('cellardoor.html', {'latestevents': events}, context_instance=RequestContext(request, processors=[custom_settings_main]))

def spaceapi(request):
    # See http://spaceapi.net/documentation

    projects = Project.all.order_by('-created_at')[:5]

    return JsonResponse({
        'api': '0.13',
        'space': 'Metalab',
        'logo': 'https://metalab.at/site_media/images/logo.png',
        'url': 'https://metalab.at/',
        'location': {
            # https://metalab.at/wiki/Lage
            'address': u'Rathausstra\xdfe 6, 1010 Vienna, Austria',
            'lat': 48.2093723,
            'lon': 16.356099,
        },
        'contact': {
            'twitter': '@metalab_events',
            'irc': 'irc://irc.freenode.net/#metalab',
            'email': 'core@metalab.at',
            'ml': 'metalab@lists.metalab.at',
            'jabber': 'metalab@conference.jabber.metalab.at',
            'phone': '+43 720 00 23 23',
        },
        'issue_report_channels': [
            'email',
        ],
        'feeds': {
            'wiki': {
                'type': 'atom',
                'url': settings.MOS_WIKI_CHANGE_URL,
            },
            'calendar': {
                'type': 'rss',
                'url': 'https://metalab.at/feeds/events/',
            },
            'blog': {
                'type': 'rss',
                'url': 'http://metalab.soup.io/rss',
            },
        },
        'projects': ['https://metalab.at/wiki/%s' % project.wikiPage for project in projects if project.wikiPage],
        'state': {
            # TODO: Implement open state tracking
            'open': None,
        },
    })
