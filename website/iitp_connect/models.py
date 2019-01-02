from django.db import models
from django.contrib.auth.models import User
from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from itertools import groupby
from calendar import HTMLCalendar, monthrange
from datetime import datetime
from django.urls import reverse
from datetime import date
from django.utils import timezone
from django.shortcuts import redirect

def upl(instance, filename):
    return 'images/%s/%s' % (instance.user.user.username, filename)


class Document(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    profile_pic = models.FileField(default='')


class Item(models.Model):
    ITEM_TAGS = (
        ('Lost', 'Lost'),
        ('Found', 'Found'),
        ('Buy', 'Buy'),
        ('Sell', 'Sell'),
        ('Other', 'Other')
    )

    ITEM_STATUS = (
        ('Open', 'Open'),
        ('Closed', 'Closed')
    )

    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=250)
    item_pic = models.FileField(default='')
    item_description = models.TextField(max_length=500)
    item_tag = models.CharField(max_length=10, choices=ITEM_TAGS, default='Other')
    item_status = models.CharField(max_length=10, choices=ITEM_STATUS, default='Open')


class CabService(models.Model):
    PLACES = (
        ('Danapur Station', 'Danapur Station'),
        ('Patna Station', 'Patna Station'),
        ('IIT Patna', 'IIT Patna'),
        ('Patna Airport', 'Patna Airport'),
        ('Boys Hostel', 'Boys Hostel'),
        ('Girls Hostel', 'Girls Hostel'),
        ('Other', 'Other')
    )

    BOOK_STATUS = (
        ('Booked', 'Booked'),
        ('Unbooked', 'Unbooked')
    )

    def get_absolute_url(self):
        return 'localhost:8000/iitp_connect/cab_book/{0}/{1}/{2}/$' .format(self.date_time.year, self.date_time.month,
                                                                            self.date_time.day)

    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    source = models.CharField(max_length=100, choices=PLACES, default='Other')
    destination = models.CharField(max_length=100, choices=PLACES, default='Other')
    date_time = models.DateTimeField(default=timezone.now, blank=True)
    book_status = models.CharField(max_length=20, choices=BOOK_STATUS, default='Unbooked')


# class Cab(models.Model):
#     date_of_event = models.DateTimeField(default=datetime.now(), blank=True)


class CabshareCalendar(HTMLCalendar):

    def __init__(self, cab_events):
        super(CabshareCalendar, self).__init__()
        self.cab_events = self.group_by_day(cab_events)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.cab_events:
                cssclass += ' filled'
                body = []

                # body.append('<li>')
                cab_sr = self.cab_events[day][0]
                body.append('<a href="%s">' % cab_sr.get_absolute_url())
                body.append('Bookings(Open in new tab)')
                body.append('</a><br/>')

                # for cab_sr in self.cab_events[day]:
                #     body.append('<li>')
                #     body.append('<a href="%s">' % cab_sr.get_absolute_url())
                #     body.append('Bookings(Open in new tab)')
                #     body.append('</a></li>')
                # body.append('</ul>')

                return self.day_cell(cssclass, '<div class="dayNumber">%d</div> %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, '<div class="dayNumber">%d</div>' % day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year = year
        self.month = month
        return super(CabshareCalendar, self).formatmonth(year, month)

    def group_by_day(self, cab_events):
        field = lambda cab_sr: cab_sr.date_time.day
        return dict(
            [(day, list(items)) for day, items in groupby(cab_events, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)


'''class UserLogo(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    user_logo = models.FileField(default='')    '''

