import datetime

from dateutil.parser import parse as dateutil_parse

from .base import BaseField


__all__ = (
    'ValidationError',
    'StringField',
    'IntField',
    'NumericField',
    'DateField',
    'DatetimeField',
)


class ValidationError(Exception):
    "Raised when a value transformation fails"


class Field(BaseField):
    def convert(self, value):
        return value

    def to_python(self, value):
        try:
            return self.convert(value)
        except Exception as exc:
            raise ValidationError('{} ({}) cannot transform {}: {}'
                                  .format(self.field_name,
                                          self.__class__.__name__,
                                          value,
                                          exc))


class StringField(Field):
    def convert(self, value):
        return str(value)


class IntField(Field):
    def convert(self, value):
        return int(value)


class NumericField(Field):
    def convert(self, value):
        return float(value)
FloatField = NumericField # for anyone playing at home


class DateField(Field):
    def __init__(self, formatter, *a, **kw):
        super(Field, self).__init__(*a, **kw)
        self.formatter = formatter

    def convert(self, value):
        value = datetime.datetime.strptime(value, self.formatter)
        return datetime.date(value.year, value.month, value.day)


class DatetimeField(Field):
    def __init__(self, formatter, *a, **kw):
        super(Field, self).__init__(*a, **kw)
        self.formatter = formatter

    def convert(self, value):
        return datetime.datetime.strptime(value, self.formatter)
