from django import template
from datetime import datetime
from operator import attrgetter

register = template.Library()

def matchSort(s):
    if s.m_class == 'Final':
        return 1
    elif s.m_class == 'Semifinal':
        return 2
    elif s.m_class == 'Quarterfinal':
        return 3
    elif s.m_class == 'Upper Bracket':
        return 4
    elif s.m_class == 'Lower Bracket':
         return 5
    elif s.m_class == 'Swiss':
         return 7
    elif s.m_class == 'Round Robin':
        return 8
    elif s.m_class == 'Informal':
        return 9    

def do_matches(parser, token):
    """
    The template tag's syntax is {% match_list type order matchlist %}
    """
    try:
        tag_name, l_type, l_order, l_list = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires three arguments" % token.contents.split()[0]
    return matchlistNode(l_type, l_order, l_list)


class matchlistNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    Parameters:
        l_type:    
            complete    only matches that have finished
            incomplete  only matches have passed thier date but haven't yet had a result recorded
            upcoming    only matches that are scheduled
        l_order:    Ordering of matches:
            date_asc    dates from earliest to latest
            date_dec    dates from latest to earliest
            importance  importance, from finals down to informal
        m_list:        The list of matches to be parsed
    """

    def __init__(self,  l_type, l_order, l_list):
        try:
            self.l_type     = template.Variable(l_type)
            self.l_order    = template.Variable(l_order)
            self.l_list     = template.Variable(l_list)
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            # Get the variables from the context so the method is thread-safe.
            my_type     = self.l_type.resolve(context)
            my_order    = self.l_order.resolve(context)
            my_list     = self.l_list.resolve(context)
            return self.formatList(my_type, my_order, my_list)
        except ValueError:
            return          
        except template.VariableDoesNotExist:
            return

    def formatList(self, m_type, m_order, m_list):
        # First thing we need to do is filter the list to remove anything we don't want
        if m_type == 'complete':
            m_list = filter(lambda x: x.completed == True, m_list)
        elif m_type == 'upcoming':
            m_list = filter(lambda x: x.date > datetime.now(), m_list)
        elif m_type == 'imcomplete':
            m_list = filter(lambda x: x.date < datetime.now() and x.completed == False, m_list)
        # Now we want to sort the list
        if m_order == 'date_asc':
            m_list = sorted(m_list, key=attrgetter('date'))
        elif m_order == 'date_asc':
            m_list = sorted(m_list, key=attrgetter('date'), reverse=True)
        elif m_order == 'importance':
            # This is the difficult one
            m_list = sorted(m_list, key=matchSort)
        # Now we have a sorted list
        # Return it in html form

        body = "<ul>"

        if m_type == 'complete':
            # These matches have results
            for match in m_list:
                if match.score_1 > match.score_2:
                    team1_result = '<font color="green">%d</font>' % match.score_1
                    team2_result = '<font color="red">%d</font>' % match.score_2
                elif match.score_1 < match.score_2:
                    team1_result = '<font color="red">%d</font>' % match.score_1
                    team2_result = '<font color="green">%d</font>' % match.score_2
                else:
                    team1_result = '<font color="black">%d</font>' % match.score_1
                    team2_result = '<font color="black">%d</font>' % match.score_2
                body += ("<li>%s: %s / %s: <strong>%s</strong> (%s) vs <strong>%s</strong> (%s) played %s</li>" % (match.tournament, match.m_class, match.m_type, match.team_1.name, team1_result, match.team_2.name, team2_result, match.date.strftime("%a %d %B, %Y")))         
        elif m_type == 'upcoming':
            for match in m_list:
                body += ("<li>%s: %s / %s: <strong>%s</strong> vs <strong>%s</strong> scheduled for %s</li>" % (match.tournament, match.m_class, match.m_type, match.team_1.name, match.team_2.name, match.date.strftime("%H:%M %a %d %B, %Y")))
        elif m_type == 'incomplete':
            for match in m_list:
                body += ("<li>%s: %s / %s: <strong>%s</strong> vs <strong>%s</strong> played %s</li>" % (match.tournament, match.m_class, match.m_type, match.team_1.name, match.team_2.name, match.date.strftime("%a %d %B, %Y")))
        body += ("</ul>")
        return body


# Register the template tag so it is available to templates
register.tag("match_list", do_matches)