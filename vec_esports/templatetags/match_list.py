from django import template
from datetime import datetime
from operator import attrgetter

register = template.Library()

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
            new_list = []
            for match in filter(lambda x: x.m_class == 'Final', m_list):
                new_list.append(match)
            for match in filter(lambda x: x.m_class == 'Upper Bracket', m_list):
                new_list.append(match)
            for match in filter(lambda x: x.m_class == 'Lower Bracket', m_list):
                new_list.append(match)
            for match in filter(lambda x: x.m_class == 'Swiss', m_list):
                new_list.append(match)
            for match in filter(lambda x: x.m_class == 'Round Robin', m_list):
                new_list.append(match)
            m_list = new_list
        # Now we have a sorted list
        # Return it in html form
        body = "<ul>"
        for match in m_list:
            body += ("<li>%s vs %s at %s</li>" % (match.team_1.name, match.team_2.name, match.date))
        body += ("</ul>")
        return body


# Register the template tag so it is available to templates
register.tag("match_list", do_matches)