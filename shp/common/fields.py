# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# """ High-level objects for fields. """

# from datetime import date, datetime, time, timedelta
# import logging
# from xmlrpc.client import MAXINT

# import khayyam
# import pytz

# from odoo import fields
# from odoo.fields import Field
# from khayyam import JalaliDate, JalaliDatetime

# from odoo.tools import date_utils
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from dateutil.relativedelta import relativedelta

# DATE_LENGTH = len(JalaliDate.today().strftime(DATE_FORMAT))
# DATETIME_LENGTH = len(JalaliDatetime.now().strftime(DATETIME_FORMAT))

# _logger = logging.getLogger(__name__)


# def is_gregorian(date_obj):
#     try:
#         temp_date = JalaliDate(date_obj)
#         if temp_date.year < 1000:
#             return False
#         return True
#     except ValueError:
#         return True    

# def Date__add__(self, other):
#     if isinstance(other, date):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDate(other)
#         else:
#             other = JalaliDate(other.year, other.month, other.day)
    
#     if isinstance(other, timedelta):
#         days = self.tojulianday() + other.days
#         return JalaliDate(julian_day=days)

# def Date__sub__(self, other):
#     if isinstance(other, date):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDate(other)
#         else:
#             other = JalaliDate(other.year, other.month, other.day)
    
#     if isinstance(other, timedelta):
#         days = self.tojulianday() - other.days
#         return JalaliDate(julian_day=days)
#     elif isinstance(other, JalaliDate):
#         days = self.tojulianday() - other.tojulianday()
#         return timedelta(days=days)

# def Date__gt__(self, other):
#     if isinstance(other, date):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDate(other)
#         else:
#             other = JalaliDate(other.year, other.month, other.day)
     
#     return self.tojulianday() > other.tojulianday()

# def Date__lt__(self, other):
#     if isinstance(other, date):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDate(other)
#         else:
#             other = JalaliDate(other.year, other.month, other.day)
        
#     return self.tojulianday() < other.tojulianday()

# def Date__ge__(self, other):
#     if isinstance(other, date):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDate(other)
#         else:
#             other = JalaliDate(other.year, other.month, other.day)
    
#     return self.tojulianday() >= other.tojulianday()

# def Date__le__(self, other):
#     if isinstance(other, date):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDate(other)
#         else:
#             other = JalaliDate(other.year, other.month, other.day)
    
#     return self.tojulianday() <= other.tojulianday()
    
# def Datetime__add__(self, other):
#     if isinstance(other, datetime):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDatetime(other)
#         else:
#             other = JalaliDatetime(other.year, other.month, other.day, other.hour, other.minute, other.second)
    
#     if isinstance(other, timedelta):
#         return JalaliDatetime(other + self.todatetime())

# def Datetime__sub__(self, other):
#     if isinstance(other, datetime):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDatetime(other)
#         else:
#             other = JalaliDatetime(other.year, other.month, other.day, other.hour, other.minute, other.second)
    
#     if isinstance(other, timedelta):
#         return JalaliDatetime(self.todatetime() - other)
#     elif isinstance(other, JalaliDatetime):
#         return self.todatetime() - other.todatetime()
#     elif isinstance(other, khayyam.JalaliDate):
#         return self.todatetime() - JalaliDatetime(other).todatetime()

# def Datetime__gt__(self, other):
#     if isinstance(other, datetime):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDatetime(other)
#         else:
#             other = JalaliDatetime(other.year, other.month, other.day,other.hour, other.minute, other.second)
     
#     return self.todatetime() > other.todatetime()

# def Datetime__lt__(self, other):
#     if isinstance(other, datetime):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDatetime(other)
#         else:
#             other = JalaliDatetime(other.year, other.month, other.day, other.hour, other.minute, other.second)
        
#     return self.todatetime() < other.todatetime()

# def Datetime__ge__(self, other):
#     if isinstance(other, datetime):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDatetime(other)
#         else:
#             other = JalaliDatetime(other.year, other.month, other.day, other.hour, other.minute, other.second)
    
#     return self.todatetime() >= other.todatetime()

# def Datetime__le__(self, other):
#     if isinstance(other, datetime):
#         if is_gregorian(other) and other.year > 1:
#             other = JalaliDatetime(other)
#         else:
#             other = JalaliDatetime(other.year, other.month, other.day, other.hour, other.minute, other.second)
    
#     return self.todatetime() <= other.todatetime()

# class Date(Field):
#     """ Encapsulates a python :class:`date <datetime.date>` object. """
#     type = 'date'
#     column_type = ('date', 'date')

#     def __format__(self, format_spec):
#         date_obj = self.to_date()
#         return date_obj.__format__(format_spec)

#     @staticmethod
#     def subtract(value, *args, **kwargs):
#         """
#         Return the difference between ``value`` and a :class:`relativedelta`.

#         :param value: initial date or datetime.
#         :param args: positional args to pass directly to :class:`relativedelta`.
#         :param kwargs: keyword args to pass directly to :class:`relativedelta`.
#         :return: the resulting date/datetime.
#         """
#         new_miladi_date = JalaliDate(value).todate() - relativedelta(*args, **kwargs)
#         new_jalali_date = JalaliDate(new_miladi_date)
#         return new_jalali_date

#     @staticmethod
#     def subtract(value, reldelta:relativedelta):
#         """
#         Return the difference between ``value`` and a :class:`relativedelta`.

#         :param value: initial date or datetime.
#         :param args: positional args to pass directly to :class:`relativedelta`.
#         :param kwargs: keyword args to pass directly to :class:`relativedelta`.
#         :return: the resulting date/datetime.
#         """
#         new_miladi_date = JalaliDate(value).todate() - reldelta
#         new_jalali_date = JalaliDate(new_miladi_date)
#         return new_jalali_date
    
#     @staticmethod
#     def add(value, *args, **kwargs):
#         """
#         Return the sum of ``value`` and a :class:`relativedelta`.

#         :param value: initial date or datetime.
#         :param args: positional args to pass directly to :class:`relativedelta`.
#         :param kwargs: keyword args to pass directly to :class:`relativedelta`.
#         :return: the resulting date/datetime.
#         """
#         new_miladi_date = JalaliDate(value).todate() + relativedelta(*args, **kwargs)
#         new_jalali_date = JalaliDate(new_miladi_date)
#         return new_jalali_date
    
#     @staticmethod
#     def add(value, reldelta: relativedelta):
#         """
#         Return the sum of ``value`` and a :class:`relativedelta`.

#         :param value: initial date or datetime.
#         :param args: positional args to pass directly to :class:`relativedelta`.
#         :param kwargs: keyword args to pass directly to :class:`relativedelta`.
#         :return: the resulting date/datetime.
#         """
#         new_miladi_date = JalaliDate(value).todate() + reldelta
#         new_jalali_date = JalaliDate(new_miladi_date)
#         return new_jalali_date

#     start_of = staticmethod(date_utils.start_of)
#     end_of = staticmethod(date_utils.end_of)
#     add = staticmethod(add)
#     subtract = staticmethod(subtract)

#     @staticmethod
#     def today(*args):
#         """Return the current day in the format expected by the ORM.

#         .. note:: This function may be used to compute default values.
#         """
#         # return date.today()
#         return JalaliDate.today()

#     @staticmethod
#     def context_today(record, timestamp=None):
#         """Return the current date as seen in the client's timezone in a format
#         fit for date fields.

#         .. note:: This method may be used to compute default values.

#         :param record: recordset from which the timezone will be obtained.
#         :param datetime timestamp: optional datetime value to use instead of
#             the current date and time (must be a datetime, regular dates
#             can't be converted between timezones).
#         :rtype: date
#         """
#         today = timestamp or fields.Datetime.now()
#         context_today = None
#         tz_name = record._context.get('tz') or record.env.user.tz
#         if tz_name:
#             try:
#                 today_utc = pytz.timezone('UTC').localize(today, is_dst=False)  # UTC = no DST
#                 timezone = khayyam.Timezone(timedelta(minutes=210),
#                     timedelta(minutes=0),
#                     False
#                     ,'Iran/Tehran')
#                 if is_gregorian(today_utc):
#                     context_today = JalaliDatetime(today_utc).astimezone(timezone)
#                 else:
#                     context_today = JalaliDatetime(today_utc.year,today_utc.month, today_utc.day).astimezone(timezone)
#             except Exception:
#                 _logger.debug("failed to compute context/client-specific today date, using UTC value for `today`",
#                               exc_info=True)
#         return (context_today or today).date()

#     @staticmethod
#     def to_date(value):
#         """Attempt to convert ``value`` to a :class:`date` object.

#         .. warning::

#             If a datetime object is given as value,
#             it will be converted to a date object and all
#             datetime-specific information will be lost (HMS, TZ, ...).

#         :param value: value to convert.
#         :type value: str or date or datetime
#         :return: an object representing ``value``.
#         :rtype: date or None
#         """
#         if not value:
#             return None
#         if (isinstance(value, date) or isinstance(value, JalaliDate)):
#             if (isinstance(value, datetime) or isinstance(value, JalaliDatetime)):
#                 return JalaliDatetime(value).date()
#             return JalaliDate(value)
#         value = str(value)[:DATE_LENGTH]
#         return JalaliDatetime.strptime(str(value)[:10], DATE_FORMAT).date()

#     @staticmethod
#     def from_string(value):
#         if not value:
#             return None
#         if (isinstance(value, date) or isinstance(value, JalaliDate)):
#             if (isinstance(value, datetime) or isinstance(value, JalaliDatetime)):
#                 return JalaliDatetime(value).date()
#             return JalaliDate(value)
#         value = str(value)[:DATE_LENGTH]
#         return JalaliDatetime.strptime(str(value)[:10], DATE_FORMAT).date()

#     # kept for backwards compatibility, but consider `from_string` as deprecated, will probably
#     # be removed after V12
#     # from_string = to_date

#     @staticmethod
#     def to_string(value):
#         """
#         Convert a :class:`date` or :class:`datetime` object to a string.

#         :param value: value to convert.
#         :return: a string representing ``value`` in the server's date format, if ``value`` is of
#             type :class:`datetime`, the hours, minute, seconds, tzinfo will be truncated.
#         :rtype: str
#         """
#         return JalaliDate(value).strftime(DATE_FORMAT) if value else False

#     def convert_to_cache(self, value, record, validate=True):
#         if not value:
#             return None
#         if (isinstance(value, datetime) or isinstance(value, JalaliDatetime)):
#             # TODO: better fix data files (crm demo data)
#             value = value.date()
#             # raise TypeError("%s (field %s) must be string or date, not datetime." % (value, self))
#         return self.to_date(value)

#     def convert_to_export(self, value, record):
#         if not value:
#             return ''
#         return self.from_string(value)

# class Datetime(Field):
#     """ Encapsulates a python :class:`datetime <datetime.datetime>` object. """
#     type = 'datetime'
#     column_type = ('timestamp', 'timestamp')

#     def __format__(self, format_spec):
#         datetime_obj = self.to_datetime()
#         return datetime_obj.__format__(format_spec)

#     @staticmethod
#     def subtract(value, *args, **kwargs):
#         """
#         Return the difference between ``value`` and a :class:`relativedelta`.

#         :param value: initial date or datetime.
#         :param args: positional args to pass directly to :class:`relativedelta`.
#         :param kwargs: keyword args to pass directly to :class:`relativedelta`.
#         :return: the resulting date/datetime.
#         """
#         new_miladi_datetime = JalaliDatetime(value).todatetime() - relativedelta(*args, **kwargs)
#         new_jalali_datetime = JalaliDatetime(new_miladi_datetime)
#         return new_jalali_datetime
    
#     @staticmethod
#     def subtract(value, reldelta: relativedelta):
#         """
#         Return the difference between ``value`` and a :class:`relativedelta`.

#         :param value: initial date or datetime.
#         :param args: positional args to pass directly to :class:`relativedelta`.
#         :param kwargs: keyword args to pass directly to :class:`relativedelta`.
#         :return: the resulting date/datetime.
#         """
#         new_miladi_datetime = JalaliDatetime(value).todatetime() - reldelta
#         new_jalali_datetime = JalaliDatetime(new_miladi_datetime)
#         return new_jalali_datetime

#     @staticmethod
#     def add(value, *args, **kwargs):
#         """
#         Return the sum of ``value`` and a :class:`relativedelta`.

#         :param value: initial date or datetime.
#         :param args: positional args to pass directly to :class:`relativedelta`.
#         :param kwargs: keyword args to pass directly to :class:`relativedelta`.
#         :return: the resulting date/datetime.
#         """
#         new_miladi_datetime = JalaliDatetime(value).todatetime() + relativedelta(*args, **kwargs)
#         new_jalali_datetime = JalaliDatetime(new_miladi_datetime)
#         return new_jalali_datetime

#     @staticmethod
#     def add(value, reldelta: relativedelta):
#         """
#         Return the sum of ``value`` and a :class:`relativedelta`.

#         :param value: initial date or datetime.
#         :param args: positional args to pass directly to :class:`relativedelta`.
#         :param kwargs: keyword args to pass directly to :class:`relativedelta`.
#         :return: the resulting date/datetime.
#         """
#         new_miladi_datetime = JalaliDatetime(value).todatetime() + reldelta
#         new_jalali_datetime = JalaliDatetime(new_miladi_datetime)
#         return new_jalali_datetime
#         if isinstance(other, datetime):
#             other = JalaliDatetime(other)
#             return super(MyDatetime, self).__le__(other)
#         # return NotImplemented

#     start_of = staticmethod(date_utils.start_of)
#     end_of = staticmethod(date_utils.end_of)
#     add = staticmethod(add)
#     subtract = staticmethod(subtract)

#     @staticmethod
#     def now(*args):
#         """Return the current day and time in the format expected by the ORM.

#         .. note:: This function may be used to compute default values.
#         """
#         # microseconds must be annihilated as they don't comply with the server datetime format
#         # return datetime.now().replace(microsecond=0)
#         timezone = khayyam.Timezone(timedelta(minutes=210),
#             timedelta(minutes=0),
#             False
#             ,'Iran/Tehran')
#         return JalaliDatetime.now().astimezone(timezone).replace(microsecond=0)

#     @staticmethod
#     def today(*args):
#         """Return the current day, at midnight (00:00:00)."""
#         return MyDatetime.now().replace(hour=0, minute=0, second=0)

#     @staticmethod
#     def context_today(record, timestamp):
#         """Return the given timestamp converted to the client's timezone.

#         .. note:: This method is *not* meant for use as a default initializer,
#             because datetime fields are automatically converted upon
#             display on client side. For default values, :meth:`now`
#             should be used instead.

#         :param record: recordset from which the timezone will be obtained.
#         :param datetime timestamp: naive datetime value (expressed in UTC)
#             to be converted to the client timezone.
#         :return: timestamp converted to timezone-aware datetime in context timezone.
#         :rtype: datetime
#         """
#         assert isinstance(timestamp, datetime), 'Datetime instance expected'
#         tz_name = record._context.get('tz') or record.env.user.tz
#         utc_timestamp = pytz.utc.localize(timestamp, is_dst=False)  # UTC = no DST
#         if tz_name:
#             try:
#                 # context_tz = TehranTimezone() # pytz.timezone(tz_name)
#                 timezone = khayyam.Timezone(timedelta(minutes=210),
#                     timedelta(minutes=0),
#                     False
#                     ,'Iran/Tehran')
#                 return JalaliDatetime(utc_timestamp).astimezone(timezone)
#             except Exception:
#                 _logger.debug("failed to compute context/client-specific timestamp, "
#                               "using the UTC value",
#                               exc_info=True)
#         return utc_timestamp

#     @staticmethod
#     def context_timestamp(record, timestamp):
#         """Return the given timestamp converted to the client's timezone.

#         .. note:: This method is *not* meant for use as a default initializer,
#             because datetime fields are automatically converted upon
#             display on client side. For default values, :meth:`now`
#             should be used instead.

#         :param record: recordset from which the timezone will be obtained.
#         :param datetime timestamp: naive datetime value (expressed in UTC)
#             to be converted to the client timezone.
#         :return: timestamp converted to timezone-aware datetime in context timezone.
#         :rtype: datetime
#         """
#         assert isinstance(timestamp, datetime), 'Datetime instance expected'
#         tz_name = record._context.get('tz') or record.env.user.tz
#         utc_timestamp = pytz.utc.localize(timestamp, is_dst=False)  # UTC = no DST
#         if tz_name:
#             try:
#                 # context_tz = TehranTimezone() # pytz.timezone(tz_name)
#                 timezone = khayyam.Timezone(timedelta(minutes=210),
#                     timedelta(minutes=0),
#                     False
#                     ,'Iran/Tehran')
#                 return JalaliDatetime(utc_timestamp).astimezone(timezone)
#             except Exception:
#                 _logger.debug("failed to compute context/client-specific timestamp, "
#                               "using the UTC value",
#                               exc_info=True)
#         return utc_timestamp


#     @staticmethod
#     def to_datetime(value):
#         """Convert an ORM ``value`` into a :class:`datetime` value.

#         :param value: value to convert.
#         :type value: str or date or datetime
#         :return: an object representing ``value``.
#         :rtype: datetime or None
#         """
#         if not value:
#             return None
#         if (isinstance(value, date) or isinstance(value, JalaliDate)):
#             if (isinstance(value, datetime) or isinstance(value, JalaliDatetime)):
#                 if value.tzinfo:
#                     raise ValueError("Datetime field expects a naive datetime: %s" % value)
#                 if (isinstance(value, datetime)):
#                     value = JalaliDatetime(value)
#                 return value
#             if (isinstance(value, date)):
#                 value = JalaliDate(value)
#             return JalaliDatetime.combine(value, time.min)

#         # TODO: fix data files
#         return JalaliDatetime.strptime(str(value).replace('T', ' ')[:19] , DATETIME_FORMAT[:len(str(value))-2])

#     @staticmethod
#     def from_string(value):
        
#         if not value:
#             return None
#         if (isinstance(value, date) or isinstance(value, JalaliDate)):
#             if (isinstance(value, datetime) or isinstance(value, JalaliDatetime)):
#                 if value.tzinfo:
#                     raise ValueError("Datetime field expects a naive datetime: %s" % value)
#                 if (isinstance(value, datetime)):
#                     value = JalaliDatetime(value)
#                 return value
#             if (isinstance(value, date)):
#                 value = JalaliDate(value)
#             return JalaliDatetime.combine(value, time.min)

#         # TODO: fix data files
#         return JalaliDatetime.strptime(str(value).replace('T', ' ')[:19] , DATETIME_FORMAT[:len(str(value))-2])


#     # kept for backwards compatibility, but consider `from_string` as deprecated, will probably
#     # be removed after V12
#     # from_string = to_datetime

#     @staticmethod
#     def to_string(value):
#         """Convert a :class:`datetime` or :class:`date` object to a string.

#         :param value: value to convert.
#         :type value: datetime or date
#         :return: a string representing ``value`` in the server's datetime format,
#             if ``value`` is of type :class:`date`,
#             the time portion will be midnight (00:00:00).
#         :rtype: str
#         """
#         return value.strftime(DATETIME_FORMAT) if value else False

#     def convert_to_cache(self, value, record, validate=True):
#         return self.to_datetime(value)

#     def convert_to_export(self, value, record):
#         if not value:
#             return ''
#         value = self.convert_to_display_name(value, record)
#         return self.from_string(value)

#     def convert_to_display_name(self, value, record):
#         if not value:
#             return False
#         return MyDatetime.to_string(MyDatetime.context_timestamp(record, value))

# JalaliDate.__gt__ = Date__gt__
# JalaliDate.__lt__ = Date__lt__
# JalaliDate.__ge__ = Date__ge__
# JalaliDate.__le__ = Date__le__
# JalaliDate.__add__ = Date__add__
# JalaliDate.__sub__ = Date__sub__

# JalaliDatetime.__gt__ = Datetime__gt__
# JalaliDatetime.__lt__ = Datetime__lt__
# JalaliDatetime.__ge__ = Datetime__ge__
# JalaliDatetime.__le__ = Datetime__le__
# JalaliDatetime.__add__ = Datetime__add__
# JalaliDatetime.__sub__ = Datetime__sub__

# fields.Date = Date
# fields.Datetime = Datetime
