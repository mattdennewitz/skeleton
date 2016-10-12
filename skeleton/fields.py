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
    'ObjectField',
    'ListField',
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


# composite fields

class ObjectField(Field):
    def __init__(self, object_class, **kwargs):
        self.object_class = object_class
        super(ObjectField, self).__init__(**kwargs)

    def to_python(self, value):
        return self.object_class.convert(value)


class ListField(Field):
    def __init__(self, field=None, **kwargs):
        """Allows optionally-typed list of data

        Args:
            field: A `Field` instance for member validation. Optional.

        Returns:
            A `list`
        """

        self.field = field
        kwargs['default'] = []
        super(ListField, self).__init__(**kwargs)

    def to_python(self, value):
        if self.field is not None:
            return [self.field.to_python(v) for v in value]
        return value
