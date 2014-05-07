# As per any django project; a views file.

from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.template.defaultfilters import stringfilter
from urllib import unquote

from google.appengine.api import users

from vec_esports.models import *

import urllib
from datetime import datetime

games = {
    'lol': "League of Legends",
    'dota': "DOTA2"
}

data_vars = {
    'last_operation': "None",
    'teams': Team.all(),
    'matchups': Matchup.all(),
    'games': games
}

match_lengths = {
    'BO1': 1,
    'BO2': 2,
    'BO3': 3,
    'BO5': 5,
    'Informal': 1
}

def main_index(request):
    e_vars = data_vars.copy()
    return direct_to_template(request, 'esports/index.html', e_vars)

def main_results(request):
    e_vars = data_vars.copy()
    if request.method == 'POST':
        # We are adding a new result
        m_result(request, e_vars)
    return direct_to_template(request, 'esports/results.html', e_vars)

def main_brackets(request):
    e_vars = data_vars.copy()
    if request.method == 'POST':
        if 'matchaddtime' in request.POST:
            # We are modifying an old matchup
            u_bracket(request, e_vars)
        else:
            # We are creating a new matchup
            m_bracket(request, e_vars)

    return direct_to_template(request, "esports/brackets.html", e_vars)

def main_register(request):
    e_vars = data_vars.copy()
    if request.method == 'POST':
        if 'r_team' in request.POST:
            # Team re-registration
            u_team(request, e_vars)
        else:
            # Registering a new team
            m_team(request, e_vars)
    return direct_to_template(request, 'esports/register.html', e_vars)     

def main_contact(request):
    return direct_to_template(request, 'esports/contact.html', None)

def view_teams(request):
    e_vars = data_vars.copy()
    return direct_to_template(request, 'esports/view_teams.html', e_vars)
def view_brackets(request):
    e_vars = data_vars.copy()
    return direct_to_template(request, 'esports/view_brackets.html', e_vars)
def view_results(request):
    e_vars = data_vars.copy()
    return direct_to_template(request, 'esports/view_results.html', e_vars)


def u_team(request, e_vars):
    e_vars.update({'last_operation': "Team re-registration"})

    team_name = unquote(request.POST.get('r_team'))
    
    q = db.GqlQuery('SELECT * FROM Team WHERE name = :1', team_name)
    team = q.fetch(1)[0]
    
    team.active = True
    team.put()
    e_vars.update({'lo_value': "Success"})

def m_team(request, e_vars):
    e_vars.update({'last_operation': "Team Registration"})
    
    team_name = request.POST.get('tmn')

    q = db.GqlQuery('SELECT * FROM Team WHERE name = :1', team_name)
    team_prexist = q.fetch(1)
    if(len(team_prexist) > 0):
        e_vars.update({
            'last_operation': "Team Registration",
            'lo_value': "Fail",
            'lo_reason': "Team already exists"
        })
    else:
        team_game = request.POST.get('game')
        team_captain = request.POST.get('cap')
        team_p2 =  request.POST.get('pl2')
        team_p3 =  request.POST.get('pl3')
        team_p4 =  request.POST.get('pl4')
        team_p5 =  request.POST.get('pl5')
        team_p6 =  request.POST.get('pl6')
        team_p7 =  request.POST.get('pl7')
        team_contact =  request.POST.get('eml')
        team = Team(
            key_name=team_name,
            game=team_game,
            name=team_name,
            captain=team_captain,
            player_2=team_p2,
            player_3=team_p3,
            player_4=team_p4,
            player_5=team_p5,
            sub_1=team_p6,
            sub_2=team_p7,
            contact_email=team_contact,
            active=True,
            paid=False)
        team.put()
        e_vars.update({'lo_value': "Success"})
       

def u_bracket(request, e_vars):
    e_vars.update({'last_operation': "Matchup modification"})
    
    matchid = unquote(request.POST.get('matchaddtime'))
    bracket_date =  request.POST.get('date')
    
    format_date = datetime.strptime(bracket_date, '%m/%d/%Y %H:%M')
    
    if(format_date < datetime.now()):
        # Can't have a game in the past
        e_vars.update({'lo_value': "Fail", 'lo_reason': "Game set for the past"})
    else:
        q = db.GqlQuery('SELECT * FROM Matchup WHERE m_id = :1', matchid)
        match = q.fetch(1)[0]
        match.date = format_date
        match.put()
        e_vars.update({'lo_value': "Success"})

def m_bracket(request, e_vars):
    e_vars.update({'last_operation': "Matchup creation"})
    
    game            = request.POST.get('game')
    team_one_n      = unquote(request.POST.get('teamone'))
    team_two_n      = unquote(request.POST.get('teamtwo'))
    bracket_date    = request.POST.get('date')
    matchtype       = request.POST.get('m_type')
    matchclass      = request.POST.get('m_class')
    
    q = db.GqlQuery('SELECT * FROM Team WHERE name = :1', team_one_n)
    team_one = q.fetch(1)[0]
    
    q = db.GqlQuery('SELECT * FROM Team WHERE name = :1', team_two_n)
    team_two = q.fetch(1)[0]
    
    # Needs error check for date format

    q = db.GqlQuery('SELECT * FROM Matchup WHERE team_1 = :1 AND team_2 = :2 AND game = :3', team_one, team_two, game)
    matchlist = q.fetch(limit=100)
    matchid = game + "." + team_one.name + "." + team_two.name + "." + str(len(matchlist))

    if(team_one.name == team_two.name):
        # Can't have a team face itself!
        e_vars.update({'lo_value': "Fail", 'lo_reason': "A team cannot face itself"})
    elif bracket_date == '':
        # A date has not been set
        bracket = Matchup(
            team_1 = team_one, 
            team_2 = team_two, 
            game=game, 
            m_type=matchtype,
            m_id=matchid, 
            m_class=matchclass, 
            completed=False)
        bracket.put()
        e_vars.update({'lo_value': "Success"})
    else:
        # A date is set and we should check it
        format_date = datetime.strptime(bracket_date, '%m/%d/%Y %H:%M')
        if(format_date < datetime.now()):
            # Can't have a game in the past
            e_vars.update({'lo_value': "Fail", 'lo_reason': "Game set for the past"})
        else:
            bracket = Matchup(
                team_1 = team_one, 
                team_2 = team_two, 
                date=format_date, 
                game=game, 
                m_type=matchtype, 
                m_id=matchid, 
                m_class=matchclass, 
                completed=False)
            bracket.put()
            e_vars.update({'lo_value': "Success"})

def m_result(request, e_vars):
    e_vars.update({'last_operation': "Result creation"})
    
    match_string = unquote(request.POST.get('match'))
    score1 = request.POST.get('sc1')
    score2 = request.POST.get('sc2')

    if score1 == '':
        score1 = 0
    else:
        score1 = int(score1)    
    if score2 == '':
        score2 = 0
    else:
        score2 = int(score2)    
     

    q = db.GqlQuery('SELECT * FROM Matchup WHERE m_id = :1', match_string)
    match_id = q.fetch(1)[0]

    m_length = match_lengths[match_id.m_type]
    if int(score1) + int(score2) != m_length:
        # The result is invalid because it contains the wrong number of games
        e_vars.update({'lo_value': "Fail", 'lo_reason': "Incorect number of games" })
    else:
        # The result is valid
        match_id.score_1 = score1
        match_id.score_2 = score2
        match_id.completed = True
        match_id.put()

        e_vars.update({'lo_value': "Success"})