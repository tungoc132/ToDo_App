import calendar
from collections import deque
import datetime
import itertools
import django.urls


class BaseCalendarMixin:
    """Base class for calendar-related mixins"""
    first_weekday = 0
    week_names = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

    def setup_calendar(self):
        """Internal calendar setting process

         Instantiate the calendar.Calendar class to use its functionality.
         I am using the monthdatescalendar method of the Calendar class, but the default is from Monday,
         This is a setup process to handle cases such as wanting to display from Tuesday (first_weekday=1).

         """
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        """Shift week_names according to first_weekday (first day of the week displayed)"""
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)
        return week_names


def get_previous_month(date):
    """Return previous month"""
    if date.month == 1:
        return date.replace(year=date.year - 1, month=12, day=1)
    else:
        return date.replace(month=date.month - 1, day=1)


def get_next_month(date):
    """Return next month"""
    if date.month == 12:
        return date.replace(year=date.year + 1, month=1, day=1)
    else:
        return date.replace(month=date.month + 1, day=1)


def get_current_month():
    """Returns the current month"""
    month = kwargs.get('month')
    year = kwargs.get('year')
    if month and year:
        month = datetime.date(year=int(year), month=int(month), day=1)
    else:
        month = datetime.date.today().replace(day=1)
    return month


class MonthCalendarMixin(BaseCalendarMixin):
    """Mixin that provides monthly calendar functionality"""

    def get_month_days(self, date):
        """Returns all days of the month"""
        return self._calendar.monthdatescalendar(date.year, date.month)

    def get_month_calendar(self):
        """Returns a dictionary containing monthly calendar information"""
        self.setup_calendar()
        current_month = get_current_month()
        calendar_data = {
            'now': datetime.date.today(),
            'month_days': self.get_month_days(current_month),
            'month_current': current_month,
            'month_previous': get_previous_month(current_month),
            'month_next': get_next_month(current_month),
            'week_names': self.get_week_names(),
        }
        return calendar_data
