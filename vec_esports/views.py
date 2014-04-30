# As per any django project; a views file.

from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect

from google.appengine.api import users

from vec_esports.models import *

import urllib
from datetime import datetime

def main_esports(request):
    return direct_to_template(request, 'esports/index.html')

def brackets(request):
    bracket_vars = {
        'last_operation': "None",
        'lo_value': "",
        'lo_reason': "",
        'teams': Team.all(),
        'matchups': Matchup.all()
    }
    return direct_to_template(request, 'esports/brackets.html', bracket_vars)

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
        team_one_n = request.POST.get('teamone')
        q = db.GqlQuery('SELECT * FROM Team WHERE name = :1', team_one_n)
        team_one = q.fetch(1)[0]
        team_two_n = request.POST.get('teamtwo')
        q = db.GqlQuery('SELECT * FROM Team WHERE name = :1', team_two_n)
        team_two = q.fetch(1)[0]
        
        print(team_one)
        print(team_two)
        
        #bracket_date =  request.POST.get('date')
        #format_date = datetime.strptime(bracket_date, '%Y-%m-%dT%H:%M')
        
        if(team_one.name == team_two.name):
            # Can't have a team face itself!
            bracket_vars = {
                'last_operation': "Matchup creation",
                'lo_value': "Fail",
                'lo_reason': "A team cannot face itself"
            }
            return direct_to_template(request, 'esports/brackets.html', bracket_vars)
        
        #print(format_date)
        bracket = Matchup(team_1 = team_one, team_2 = team_two)#, date=format_date)
        bracket.put()

        bracket_vars = {
            'last_operation': "Matchup creation",
            'lo_value': "Success",
            'lo_reason': "Matchup created"
        }
    return direct_to_template(request, 'esports/brackets.html', bracket_vars)

