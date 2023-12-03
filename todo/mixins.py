import calendar
from collections import deque
import datetime
import itertools
from django import forms


class BaseCalendarMixin:
    first_weekday = 0
    week_names = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']

    def setup_calendar(self):
        self._calendar = calendar.Calendar(self.first_weekday)

    def get_week_names(self):
        week_names = deque(self.week_names)
        week_names.rotate(-self.first_weekday)
        return week_names


class MonthCalendarMixin(BaseCalendarMixin):
    def get_prev_month(self, date):
        if date.month == 1:
            return date.replace(year=date.month - 1, month=12, day=1)
        else:
            return date.replace(month=date.month - 1, day=1)

    def get_next_month(self, date):
        if date.month == 12:
            return date.replace(year=date.year + 1, month=1, day=1)
        else:
            return date.replace(month=date.month + 1, day=1)

    def get_month_days(self, date):
        return self._calendar.monthdatescalendar(date.year, date.month)

    def get_current_month(self):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self):
        """Returns a dictionary containing monthly calendar information"""
        self.setup_calendar()
        current_month = self.get_current_month()
        calendar_data = {
            'now': datetime.date.today(),
            'month_days': self.get_month_days(current_month),
            'month_current': current_month,
            'month_previous': self.get_prev_month(current_month),
            'month_next': self.get_next_month(current_month),
            'week_names': self.get_week_names(),
        }
        return calendar_data


class WeekCalendarMixin(BaseCalendarMixin):
    """Mixin that provides weekly calendar functionality"""

    def get_week_days(self):
        """Returns all days of the week"""
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()

        for week in self._calendar.monthdatescalendar(date.year, date.month):
            if date in week:
                return week

    def get_week_calendar(self):
        """Returns a dictionary containing weekly calendar information"""
        self.setup_calendar()
        days = self.get_week_days()
        first = days[0]
        last = days[-1]
        calendar_data = {
            'now': datetime.date.today(),
            'week_days': days,
            'week_previous': first - datetime.timedelta(days=7),
            'week_next': first + datetime.timedelta(days=7),
            'week_names': self.get_week_names(),
            'week_first': first,
            'week_last': last,
        }
        return calendar_data


class WeekWithScheduleMixin(WeekCalendarMixin):
    """Mixin provides weekly calendar with schedule"""

    def get_week_schedules(self, start, end, days):
        """Returns each day and schedule"""
        lookup = {
            # Dynamically create 'For example, date__range: (1st, 31st)'
            '{}__range'.format(self.date_field): (start, end)
        }
        # For example, Schedule.objects.filter(date__range=(1st, 31st))
        queryset = self.model.objects.filter(**lookup)

        # Create a dictionary like {datetime of the 1st: all schedules of the 1st, datetime of the 2nd: all of the schedule of the 2nd...}
        day_schedules = {day: [] for day in days}
        for schedule in queryset:
            schedule_date = getattr(schedule, self.date_field)
            day_schedules[schedule_date].append(schedule)
        return day_schedules

    def get_week_calendar(self):
        calendar_context = super().get_week_calendar()
        calendar_context['week_day_schedules'] = self.get_week_schedules(
            calendar_context['week_first'],
            calendar_context['week_last'],
            calendar_context['week_days']
        )
        return calendar_context


class MonthWithScheduleMixin(MonthCalendarMixin):
    """Mixin provides a monthly calendar with schedule"""

    def get_month_schedules(self, start, end, days):
        """Returns each day and schedule"""
        lookup = {
            '{}__range'.format(self.date_field): (start, end)
        }
        queryset = self.model.objects.filter(**lookup)

        day_schedules = {day: [] for week in days for day in week}
        for schedule in queryset:
            schedule_date = getattr(schedule, self.date_field)
            day_schedules[schedule_date].append(schedule)

        # Divide the day_schedules dictionary into rounds. [{1st: 1st schedule...}, {8th: 8th schedule...}, ...]
        # Take out and divide into 7
        size = len(day_schedules)
        return [{key: day_schedules[key] for key in itertools.islice(day_schedules, i, i + 7)} for i in
                range(0, size, 7)]

    def get_month_calendar(self):
        calendar_context = super().get_month_calendar()
        month_days = calendar_context['month_days']
        month_first = month_days[0][0]
        month_last = month_days[-1][-1]
        calendar_context['month_day_schedules'] = self.get_month_schedules(
            month_first,
            month_last,
            month_days
        )
        return calendar_context


class MonthWithFormsMixin(MonthCalendarMixin):
    """Mixin provides a monthly calendar with schedule"""

    def get_month_forms(self, start, end, days):
        """Create a form associated with each day"""
        lookup = {
            '{}__range'.format(self.date_field): (start, end)
        }
        queryset = self.model.objects.filter(**lookup)
        days_count = sum(len(week) for week in days)
        FormClass = forms.modelformset_factory(self.model, self.form_class, extra=days_count)
        if self.request.method == 'POST':
            formset = self.month_formset = FormClass(self.request.POST, queryset=queryset)
        else:
            formset = self.month_formset = FormClass(queryset=queryset)

        day_forms = {day: [] for week in days for day in week}

        # Place one new creation form for each day
        for empty_form, (date, empty_list) in zip(formset.extra_forms, day_forms.items()):
            empty_form.initial = {self.date_field: date}
            empty_list.append(empty_form)

        # Place a form for updating the schedule on each day that has a schedule
        for bound_form in formset.initial_forms:
            instance = bound_form.instance
            date = getattr(instance, self.date_field)
            day_forms[date].append(bound_form)

        return [{key: day_forms[key] for key in itertools.islice(day_forms, i, i + 7)} for i in range(0, days_count, 7)]

    def get_month_calendar(self):
        calendar_context = super().get_month_calendar()
        month_days = calendar_context['month_days']
        month_first = month_days[0][0]
        month_last = month_days[-1][-1]
        calendar_context['month_day_forms'] = self.get_month_forms(
            month_first,
            month_last,
            month_days
        )
        calendar_context['month_formset'] = self.month_formset
        return calendar_context
