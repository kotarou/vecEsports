# As per any django project; a views file.

from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect
from django.template.defaultfilters import stringfilter
from urllib import unquote

from google.appengine.api import users

from vec_esports.models import *

import urllib
from datetime import datetime
import re, calendar 

import ConfigParser
import logging
import pickle

config = ConfigParser.RawConfigParser()
config.read('settings.cfg')

current_tournament_lol  = config.get('CurrentTournaments', 'lol')
current_tournament_dota = config.get('CurrentTournaments', 'dota')
current_phase           = config.get('General', 'phase')

# This data is always relevant, regardless of what the current page is
data_vars = {
    'last_operation': "None",
    'phase': current_phase,
    'current_tournament_lol':current_tournament_lol,
    'current_tournament_dota':current_tournament_dota,
    'all_lol_teams':        Team.gql('WHERE game = :1', 'lol').fetch(None),
    'all_dota_teams':       Team.gql('WHERE game = :1', 'dota').fetch(None),
}

match_lengths = {
    'BO1': 1,
    'BO2': 2,
    'BO3': 3,
    'BO5': 5,
    'Informal': 1
}

def admin(request):
    if users.get_current_user():
        url = users.create_logout_url(request.get_full_path())
        url_linktext = 'Logout'
        url_logintext = ('Logged in as %s' % users.get_current_user().email())
    else:
        url = users.create_login_url(request.get_full_path())
        url_linktext = 'Login'
        url_logintext = ""


    # This commented code is migration code.
    # teams = Team.all()
    # for team in teams:
    #     results = {}
    #     if team.game == 'lol':
    #         results["VECLOL_1"] =  0
    #     else:
    #         results["VECDOTA_1"] = 0
    #     data = pickle.dumps(results)
    #     team.results = data
    #     team.put()
    # teams = Team.all()
    # for team in teams:
    #     res = pickle.loads(team.results)
    #     try:
    #         logging.info("%s" % res['VECLOL_1'])
    #     except KeyError:
    #         logging.info("%s" % res['VECDOTA_1'])

    # Manual score adding
    # teams = Team.all()
    # for team in teams:
    #     if team.name == "The Drill Team":
    #         res = {}
    #         res['VECLOL_1'] = "3"
    #         team.results = pickle.dumps(res)
    #         team.put()


    e_vars = data_vars.copy()
    e_vars['url'] = url
    e_vars['url_linktext'] = url_linktext
    e_vars['url_logintext'] = url_logintext
    if request.method == 'POST':
        m_tournament(request, e_vars)
    
    return direct_to_template(request, 'esports/admin.html', e_vars)

def main_index(request):
    e_vars = data_vars.copy()
    return direct_to_template(request, 'esports/index.html', e_vars)

def teamSort(team, tournament_name):
    # Sort teams in a tournament listing
    res = pickle.loads(team.results)[tournament_name]
    # res can take one of two forms:
    #   exact placing: 1/2/3/4/5
    #   string describing why they don't have a placing
    if type(res) is int or res.isdigit():
        # They have a placing, score by that
        return int(res)
    else:
        # They obtained an approx score
        if(res[0].isdigit()):
            return int(res[0])
        # They did not attain a score
        if res == "Banned":
            return 10000
        if res == "Disqualified":
            return  9999
        if res == "Dropped out":
            return  9998
        if res == "Unpaid":
            return  9002
        if res == "Paid":
            return  9001

def main_views(request, view, value=None, mode='single'):
    # This function takes care of all pages where the info is based on URL parameters
    e_vars = data_vars.copy()
    # The following views are possible:
    #   View the details for a single tournament:
    #       view    = tournament
    #       value   = tournament_name
    #   View the details for a single team:
    #       view    = team
    #       value   = team_name
    #       mode    = single
    #   View the list of all teams registered
    #       view    = team
    #       mode    = all
    #   View all teams in the current tournament
    #       view    = team
    #       mode    = current
    #   Date
    # e_vars.update({'last_operation': "Team re-registration"})

    if view == 'tournament':
        tt = Tournament.gql('WHERE name = :1', value)
        if tt.count() > 0:
            tourney = tt[0]
            entered_teams = filter(lambda x: tourney.name in pickle.loads(x.results).keys(), Team.all())
            entered_teams.sort(key = lambda x: teamSort(x, tourney.name))
            res = []
            for team in entered_teams:
                res.append(pickle.loads(team.results)[tourney.name])
                e_vars.update({
                    'operation': 'tournament',
                    'tournament': tourney,
                    'matches': Matchup.gql('WHERE tournament = :1', tourney.name),
                    'teams': zip(entered_teams, res),
                    })
        else:
            e_vars.update({
                'lo_value': "Fail",
                'lo_reason': "Tournament does not exist"
            })

    elif view == 'team' and mode == 'single':
        # Return the view for a single team
        team = Team.gql('WHERE name = :1', value)[0]
        matches = Matchup.gql('WHERE team_1 = :1', team).fetch(limit=None) +  Matchup.gql('WHERE team_2 = :1', team).fetch(limit=None)
        e_vars.update({
            'operation': 'team',
            'mode': 'single',
            'team': team,
            'matches': matches,
            'results': pickle.loads(team.results),
            'current': current_tournament_lol if team.game == 'lol' else current_tournament_dota,
            'prior': pickle.loads(team.prior_players).values(),
        })

    elif view == 'team' and mode == 'all':
        e_vars.update({
            'operation': 'team',
            'mode': 'all',
            'all_lol_teams':        Team.gql('WHERE game = :1', 'lol').fetch(None),
            'all_dota_teams':       Team.gql('WHERE game = :1', 'dota').fetch(None),
        })
    elif view == 'team' and mode == 'current':
        # Return the view for the current tournament's registered teams
        e_vars.update({
            'operation': 'team',
            'mode': 'current',
            'current_lol_teams':    filter(lambda x: current_tournament_lol in pickle.loads(x.results).keys(), Team.all()),
            'current_dota_teams':   filter(lambda x: current_tournament_dota in pickle.loads(x.results).keys(), Team.all()),
        })

    return direct_to_template(request, 'esports/view.html', e_vars)



    # if view == 'date':
    #     e_vars.update({
    #         'operation': 'date',
    #         'mode': 'single',
    #         'year': value[0:4],
    #         'month': value[4:6],
    #         'day': value[6:8],
    #         'matches': Matchup.all(), #filter(lambda x: x.date.day == value, Matchup.all())
    #     })
    
def main_contact(request):
    e_vars = data_vars.copy()
    return direct_to_template(request, 'esports/contact.html', e_vars) 

def main_results(request, change):
    # This is the wrapper function that will deal to all result related requests
    e_vars = data_vars.copy()
    if change != True:
        return direct_to_template(request, 'esports/view_results.html', e_vars)
    if request.method == 'POST':
        # We are adding a new result
        m_result(request, e_vars)
    return direct_to_template(request, 'esports/results.html', e_vars)

def main_brackets(request, change):
    # This is the wrapper function that will deal to all bracket/matchup related requests
    e_vars = data_vars.copy()
    if change != True:
        return direct_to_template(request, 'esports/view_brackets.html', e_vars)
    if request.method == 'POST':
        if 'matchaddtime' in request.POST:
            # We are modifying an old matchup
            u_bracket(request, e_vars)
        else:
            # We are creating a new matchup
            m_bracket(request, e_vars)

    return direct_to_template(request, "esports/brackets.html", e_vars)

def main_teams(request, change, re):
    # This is the wrapper function that will deal to all team related requests
    e_vars = data_vars.copy()
    if change != True:
        return direct_to_template(request, 'esports/view_teams.html', e_vars) 
    if re:
        e_vars.update({'reregistration':True})
        return direct_to_template(request, 'esports/register.html', e_vars) 
    if request.method == 'POST':
        if 'r_team' in request.POST:
            # Team re-registration
            u_team(request, e_vars)
        else:
            # Registering a new team
            m_team(request, e_vars)
    return direct_to_template(request, 'esports/register.html', e_vars)     

def u_team(request, e_vars):
    # have to totally rework this

    e_vars.update({'last_operation': "Team re-registration"})

    team_name = unquote(request.POST.get('r_team'))
    
    q = db.GqlQuery('SELECT * FROM Team WHERE name = :1', team_name)
    team = q.fetch(1)[0]
    
    entry = pickle.loads(team.results)  

    if( current_tournament_lol in entry.keys() or current_tournament_dota in entry.keys()):
        e_vars.update({
            'lo_value': "Fail",
            'lo_reason': "Team already entered in the current tournament"
        })
        return

    if team.game == 'lol':
        entry[current_tournament_lol] =  0
    else:
        entry[current_tournament_dota] = 0

    results = pickle.dumps(entry)
    team.results = results

    team.put()
    e_vars.update({'lo_value': "Success"})

def m_team(request, e_vars):
    e_vars.update({'last_operation': "Team Registration"})
    
    team_name = request.POST.get('tmn')
    team_game       = request.POST.get('game')
    team_captain    = request.POST.get('cap')
    team_p2         = request.POST.get('pl2')
    team_p3         = request.POST.get('pl3')
    team_p4         = request.POST.get('pl4')
    team_p5         = request.POST.get('pl5')
    team_p6         = request.POST.get('pl6')
    team_p7         = request.POST.get('pl7')
    team_contact    = request.POST.get('eml')
    
    if(Team.get_by_key_name(team_name) != None):
        e_vars.update({
            'lo_value': "Fail",
            'lo_reason': "Team already exists"
        })
        return
    entry = {}
    if team_game == 'lol':
        entry[current_tournament_lol] =  0
    else:
        entry[current_tournament_dota] = 0

    prior = {}

    team = Team(
        key_name=team_name,
        game=team_game,
        name=team_name,
        captain=team_captain, 
        player_2=team_p2, player_3=team_p3,  player_4=team_p4,  player_5=team_p5,
        sub_1=team_p6, sub_2=team_p7,
        contact_email=team_contact,
        results = pickle.dumps(entry),
        prior_players = pickle.dumps(prior),
        )
    team.put()
    
    if team_game == 'lol':
        gameid = current_tournament_lol
    else:
        gameid = current_tournament_dota
    # tt = db.GqlQuery('SELECT * FROM Tournament WHERE name = :1', gameid)
    # tourney = tt.fetch(1)[0]
    # dictt = tourney.teams
    # dictt[team_name] = 0
    # tourney.teams = dictt
    # tourney.put()

    e_vars.update({'lo_value': "Success"})

def m_tournament(request, e_vars):
    e_vars.update({'last_operation': "Tournament Creation"})
    
    tournament_name = request.POST.get('tmn')
    tournament_game = request.POST.get('game')
    tournament_description = request.POST.get('description')
    if(Team.get_by_key_name(tournament_name) != None):
        e_vars.update({
            'lo_value': "Fail",
            'lo_reason': "Tournament already exists"
        })
        return

    tourney = Tournament(
        key_name=tournament_name,
        name=tournament_name,
        game=tournament_game,
        completed=False,
        description=tournament_description,
        )
    tourney.put()
    
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

    team_one = Team.get_by_key_name(team_one_n)
    team_two = Team.get_by_key_name(team_two_n)

    if game == 'lol':
        tourney = current_tournament_lol
    else:
        tourney = current_tournament_dota

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
            key_name=matchid,
            team_1 = team_one, 
            team_2 = team_two, 
            game=game, 
            m_type=matchtype,
            m_id=matchid, 
            m_class=matchclass, 
            completed=False,
            tournament=tourney)
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
                key_name=matchid,
                team_1 = team_one, 
                team_2 = team_two, 
                date=format_date, 
                game=game, 
                m_type=matchtype, 
                m_id=matchid, 
                m_class=matchclass, 
                completed=False,
                tournament=tourney)
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
    if int(score1) + int(score2) > m_length or int(score1) + int(score2) < m_length // 2 + 1:
        # The result is invalid because it contains the wrong number of games
        e_vars.update({'lo_value': "Fail", 'lo_reason': "Incorect number of games" })
    else:
        # The result is valid
        match_id.score_1 = score1
        match_id.score_2 = score2
        match_id.completed = True
        match_id.put()

        e_vars.update({'lo_value': "Success"})

