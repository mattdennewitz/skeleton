import datetime

import pytest

from skeleton import Skeleton
from skeleton.fields import *


def test_int_field():
    class Model(Skeleton):
        value = IntField()

    with pytest.raises(ValidationError):
        Model.convert({'value': 'asdf'})

    assert Model.convert({'value': '1'}).value == 1


def test_numeric_field():
    class Model(Skeleton):
        value = NumericField()

    with pytest.raises(ValidationError):
        Model.convert({'value': 'asdf'})

    assert Model.convert({'value': '1.599'}).value == 1.599


def test_datetime_field():
    class Model(Skeleton):
        value = DatetimeField(formatter='%Y-%m-%d %H:%M:%S')

    dt = datetime.datetime(2016, 10, 11, 23, 59, 59)
    assert Model.convert({'value': '2016-10-11 23:59:59'}).value == dt

    with pytest.raises(ValidationError):
        Model.convert({'value': '12345'})

    with pytest.raises(ValidationError):
        Model.convert({'value': '2016-01-01'})


def test_date_field():
    class Model(Skeleton):
        value = DateField(formatter='%Y-%m-%d')

    dt = datetime.date(2016, 10, 11)
    assert Model.convert({'value': '2016-10-11'}).value == dt
