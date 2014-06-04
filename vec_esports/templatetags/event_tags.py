from calendar import HTMLCalendar
from django import template
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

register = template.Library()

def do_event_calendar(parser, token):
    """
    The template tag's syntax is {% event_calendar year month event_list %}
    """

    try:
        tag_name, year, month, day, event_list = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires three arguments" % token.contents.split()[0]
    return EventCalendarNode(year, month, day, event_list)


class EventCalendarNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    """

    def __init__(self, year, month, day, event_list):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            self.day = template.Variable(day)
            self.event_list = template.Variable(event_list)
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            # Get the variables from the context so the method is thread-safe.
            my_event_list = self.event_list.resolve(context)
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            my_day = self.day.resolve(context)
            cal = EventCalendar(my_event_list)
            return cal.formatmonth(int(my_year), int(my_month))
        except ValueError:
            return          
        except template.VariableDoesNotExist:
            return


class EventCalendar(HTMLCalendar):
    """
    Overload Python's calendar.HTMLCalendar to add the appropriate events to
    each day's table cell.
    """

    def __init__(self, events):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'

            if day in self.events:
                cssclass += ' filled'
                # body = ['<ul>']
                # for event in self.events[day]:
                #     body.append('<li>')
                #     #body.append('<a href="%s">' % event.get_absolute_url())
                #     #body.append(esc(event.series.primary_name))
                #     body.append('<a href="#">%s</a>' % 'a')
                #     body.append('</li>')
                # body.append('</ul>')
                count = 0
                # Make sure the event is for this month and year!
                for event in filter(lambda x: (x.date.month == self.month and x.date.year == self.year), self.events[day]):
                    count += 1

                # Did we manage to find events on this day for this month/year?
                if count > 0:
                    # Pretty output with correct pluralization
                    plural = ''
                    if count > 1:
                        plural = 's'
                    body=("<span class='mini'>%d game%s</span>" % (count, plural))
                    return self.day_cell(cssclass, '<span class="dayNumber"><strong>%d</strong></span> <br />%s' % (day, body)) #%s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<span class="dayNumberNoEvents">%d</span>' % (day))
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month)

    def group_by_day(self, events):
        #field = lambda event: event.date_and_time.day
        field = lambda event: event.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(events , field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

# Register the template tag so it is available to templates
register.tag("event_calendar", do_event_calendar)