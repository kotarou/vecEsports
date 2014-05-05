# As per any django project; a views file.

from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.template.defaultfilters import stringfilter
from urllib import unquote

from google.appengine.api import users

from vec_esports.models import *

import urllib
from datetime import datetime

data_vars = {
    'last_operation': "None",
    'teams': Team.all(),
    'matchups': Matchup.all(),
    'results': Result.all()
}

match_lengths = {
    'BO1': 1,
    'BO2': 2,
    'BO3': 3,
    'BO5': 5,
    'Informal': 1
}

def main_esports(request):
    main_vars = data_vars.copy()
    return direct_to_template(request, 'esports/index.html', main_vars)

def results(request):
    res_vars = data_vars.copy()
    if request.method == 'POST':
    # We are adding a new result
        match_string = unquote(request.POST.get('match'))
        score1 = request.POST.get('sc1')
        score2 = request.POST.get('sc2')

        if score1 == '':
            score1 = '0'
        if score2 == '':
            score2 = '0'

        q = db.GqlQuery('SELECT * FROM Matchup WHERE m_id = :1', match_string)
        match_id = q.fetch(1)[0]

        m_length = match_lengths[match_id.m_type]
        if int(score1) + int(score2) != m_length:
            # The result is invalid because it contains the wrong number of games
            res_vars.update({
                'last_operation': "Result creation",
                'lo_value': "Fail",
                'lo_reason': "Incorect number of games"
            })
        else:
            # The result is valid
            result = Result(match=match_id, score_1 = score1, score_2=score2)
            result.put()
            res_vars.update({
                'last_operation': "Result creation",
                'lo_value': "Success",
                'lo_reason': "Result created"
            })

            match_id.completed = True
            match_id.put()

    return direct_to_template(request, 'esports/results.html', res_vars)

def brackets(request):
    bracket_vars = data_vars.copy()
    if request.method == 'POST':
    # We are adding a new matchup
        bracket_vars.update({'last_operation': "Matchup creation"})
        game = request.POST.get('game')
        team_one_n = unquote(request.POST.get('teamone'))
        q = db.GqlQuery('SELECT * FROM Team WHERE name = :1', team_one_n)
        team_one = q.fetch(1)[0]
        team_two_n = unquote(request.POST.get('teamtwo'))
        q = db.GqlQuery('SELECT * FROM Team WHERE name = :1', team_two_n)
        team_two = q.fetch(1)[0]

        bracket_date =  request.POST.get('date')
        # Needs error check for date format
        format_date = datetime.strptime(bracket_date, '%m/%d/%Y %H:%M')

        matchtype =  request.POST.get('m_type')
        matchclass =  request.POST.get('m_class')


        q = db.GqlQuery('SELECT * FROM Matchup WHERE team_1 = :1 AND team_2 = :2 AND game = :3', team_one, team_two, game)
        matchlist = q.fetch(limit=100)
        matchid = game + "." + team_one.name + "." + team_two.name + "." + str(len(matchlist))

        if(team_one.name == team_two.name):
            # Can't have a team face itself!
            bracket_vars.update({'lo_value': "Fail", 'lo_reason': "A team cannot face itself"})
        elif(format_date < datetime.now()):
            # Can't have a game in the past
            bracket_vars.update({'lo_value': "Fail", 'lo_reason': "Game set for the past"})
        else:
            bracket = Matchup(team_1 = team_one, team_2 = team_two, date=format_date, game=game, m_type=matchtype, m_id=matchid, m_class=matchclass, completed=False)
            bracket.put()
            bracket_vars.update({
                'last_operation': "Matchup creation",
                'lo_value': "Success",
                'lo_reason': "Matchup created"
            })
    #else:
    # We are merely viewing the bracket page

    return direct_to_template(request, "esports/brackets.html", bracket_vars)


def team_register(request):
    team_vars = data_vars.copy()
    if request.method == 'POST':

        if 'r_team' in request.POST:
            # Team re-registration
            team_name = unquote(request.POST.get('r_team'))
            q = db.GqlQuery('SELECT * FROM Team WHERE name = :1', team_name)
            team = q.fetch(1)[0]
            team.active = True
            team.put()
            team_vars.update({
                'last_operation': "Team re-registration",
                'lo_value': "Success",
                'lo_reason': ""
            })
        else:
            team_name = request.POST.get('tmn')

            q = db.GqlQuery('SELECT * FROM Team WHERE name = :1', team_name)
            team_prexist = q.fetch(1)
            if(len(team_prexist) > 0):
                team_vars.update({
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
                team = Team(key_name=team_name,
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
                            active=True)
                team.put()
                team_vars.update({
                    'last_operation': "Team Registration",
                    'lo_value': "Success",
                    'lo_reason': ""
                })
    return direct_to_template(request, 'esports/team.html', team_vars)



