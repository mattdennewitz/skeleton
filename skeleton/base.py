import copy
import types


class BaseField(object):
    def __init__(self, field_name=None, mapping=None, transformer=None,
                 default=None):
        """A representation of a validatable piece of data

        Args:
            field_name: Name of this field, taken upstream by
                skeleton attribute name if not given here.
            mapping: String or callable used to resolve value.
                Django-style `__` paths allowed for nested objects.
            transformer: Transformation function called before
                value is cast to Python representation.
            default: Default value to use.
        """

        self.field_name = field_name

        if mapping is not None:
            if (not callable(mapping)
                and not isinstance(mapping, str)):
                raise Exception('Mapping for {} must be string or callable'
                                .format(field_name))

        self.mapping = mapping
        self.transformer = transformer
        self.default = default

    def __get__(self, obj, owner):
        """Retrieves this field from the skeleton where it lives
        """

        return obj._data.get(self.field_name, self.default)

    def __set__(self, obj, value):
        """Sets given `value` for this field
        """

        obj._data[self.field_name] = value


class SkeletonBase(type):
    """Metaclass providing field support to a skeleton
    """

    def __new__(cls, name, bases, attrs):
        new_cls = super(SkeletonBase, cls).__new__(cls, name, bases, attrs)

        fields = {}

        for field_name, field in attrs.items():
            if isinstance(field, BaseField):
                # set field name from skeleton attribute name if not defined
                # by field instance
                if not field.field_name:
                    field.field_name = field_name

                fields[field_name] = field

        # set fields on the new instance
        new_cls._fields = fields

        return new_cls


class Skeleton(object, metaclass=SkeletonBase):
    """A skeleton, which exists inside of every body.

    A skeleton consists of many typed fields, all children of `BaseField`.
    """

    def __init__(self, **kwargs):
        self._data = {}

        for field_name, field in self._fields.items():
            value = kwargs.get(field_name, None)
            self._data[field_name] = value
            
    def to_primitive(self, obj=None):
        obj = {}

        for key in self._data:
            value = self._data[key]
            if isinstance(value, Skeleton):
                obj[key] = value.to_primitive()
            else:
                obj[key] = value

        return obj

    @classmethod
    def convert(cls, raw_obj):
        data = {}

        # set values for each field
        for field_name, field in cls._fields.items():
            value = None

            if not field.mapping:
                if field.default is not None:
                    value = field.default
                else:
                    value = raw_obj
            elif callable(field.mapping):
                # mapping is callable: pass in entire object
                # for value extraction
                value = field.mapping(raw_obj)
            elif '__' in field.mapping:
                bits = field.mapping.split('__')
                first_bit = bits.pop(0)
                value = raw_obj[first_bit]

                while bits:
                    bit = bits.pop(0)

                    if isinstance(value, dict):
                        value = value.get(bit)
                    elif isinstance(value, (list, tuple)):
                        try:
                            idx = int(bit)
                            value = value[idx]
                        except ValueError:
                            pass
                    else:
                        raise Exception('Dead end query: {}'.format(field.mapping))
            elif field.mapping:
                # pluck value directly from given raw object,
                # falling back to field default if unavailable
                value = raw_obj.get(field.mapping)

            # transform values
            if callable(field.transformer):
                value = field.transformer(value)

            if value is not None:
                value = field.to_python(value)

            # set field value in data
            data[field_name] = value

        return data
