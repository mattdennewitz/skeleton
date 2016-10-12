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


def test_untyped_list_field():
    class Model(Skeleton):
        value = ListField()

    assert Model.convert({'value': [1, 2]}).value[0] == 1


def test_int_typed_list_field():
    class Model(Skeleton):
        value = ListField(field=IntField())

    assert Model.convert({'value': [1, 2]}).value[0] == 1

    with pytest.raises(ValidationError):
        Model.convert({'value': ['x', 2]})


def test_object_typed_list_field():
    class Member(Skeleton):
        name = StringField()

    class Model(Skeleton):
        value = ListField(field=ObjectField(Member))

    assert Model.convert({'value': [{'name': 'Matt'}]}).value[0].name == 'Matt'


def test_object_field():
    class AlbumRating(Skeleton):
        title = StringField()
        score = NumericField()

    class Review(Skeleton):
        album_rating = ObjectField(AlbumRating)

    # ok review
    review = Review.convert({
        'album_rating': {
            'title': 'Hello Ambition',
            'score': 10.0
        }
    })

    assert review.album_rating.title == 'Hello Ambition'

    with pytest.raises(ValidationError):
        # bad review, bad score
        review = Review.convert({
            'album_rating': {
                'title': 'Hello Ambition',
                'score': 'hard pass',
            }
        })

