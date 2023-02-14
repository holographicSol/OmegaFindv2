""" Written by Benjamin Jack Cullen """

import datetime
import time


def convert_days_to_years(n: int):
    """ Returns years and remaining days """
    days = n
    years = 0
    while days >= 365:
        days = days / 365
        years = int(days)
    return str(f'{years} years {int(n-(years*365))} days')


def calc_convert_seconds_to_hours_minutes_seconds_gmtime(t0: float, t1: float):
    """ Returns Hours:Minutes:Seconds (Limit: 23:59:59) """
    t3 = time.strftime('%H:%M:%S', time.gmtime(t1-t0))
    if t3 == '00:00:00':
        t3 = t1 - t0
    return t3


def calc_convert_seconds_to_hours_minutes_seconds_time_delta(t0: float, t1: float):
    """ Returns Years, Days Hours:Minutes:Seconds.Microseconds """
    t3 = str(datetime.timedelta(seconds=t1-t0))
    if t3 == '0:00:00':
        t3 = t1 - t0
    if 'days' in t3:
        days = int(t3.split(' ')[0])
        years = convert_days_to_years(n=days)
        t3 = years + t3.replace(t3.split(' ')[0], '')
        t3 = t3.replace('days,', '')

    return t3


def convert_seconds_to_hours_minutes_seconds_time_delta(n):
    """ Returns Years, Days Hours:Minutes:Seconds.Microseconds """
    t3 = str(datetime.timedelta(seconds=n))
    if t3 == '0:00:00':
        t3 = n
    if 'days' in t3:
        days = int(t3.split(' ')[0])
        years = convert_days_to_years(n=days)
        t3 = years + t3.replace(t3.split(' ')[0], '')
        t3 = t3.replace('days,', '')

    return t3
