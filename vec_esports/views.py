# As per any django project; a views file.

from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect

from google.appengine.api import users

from vec_esports.models import *

import urllib


def main_esports(request):
    return direct_to_template(request, 'esports/index.html')

def brackets(request):
    teams = Team.all()
    baracket_vars = {
        'teams': teams,
    }
    return direct_to_template(request, 'esports/brackets.html', baracket_vars)

def team_register(request):
    if request.method == 'POST':
        team_name = request.POST.get('tmn')
        team_captain = request.POST.get('cap')
        team_p2 =  request.POST.get('pl2')
        team_p3 =  request.POST.get('pl3')
        team_p4 =  request.POST.get('pl4')
        team_p5 =  request.POST.get('pl5')
        team_p6 =  request.POST.get('pl6')
        team_p7 =  request.POST.get('pl7')
        team_contact =  request.POST.get('eml')
        team = Team(key_name=team_name,
                    name=team_name,
                    captain=team_captain,
                    player_2=team_p2,
                    player_3=team_p3,
                    player_4=team_p4,
                    player_5=team_p5,
                    player_6=team_p6,
                    player_7=team_p7,
                    contact_email=team_contact)
        team.put()
    return HttpResponseRedirect('/')

def bracket_make(request):
    if request.method == 'POST':
        team_one = request.POST.get('teamone')
        team_two = request.POST.get('teamtwo')
        bracket_date =  request.POST.get('date')
        bracket = Matchup(team_1=team_one, team_2 = team_two, date=bracket_date)
        bracket.put()
    return HttpResponseRedirect('/')

