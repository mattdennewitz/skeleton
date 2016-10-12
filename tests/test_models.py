from skeleton import Skeleton
from skeleton.fields import StringField, IntField, NumericField, DatetimeField


def test_that_basic_model_field_access_works():
    class Artist(Skeleton):
        name = StringField()

    # skip the conversion process, fill the value directly
    artist = Artist(name='Coltrane Motion')
    assert artist.name == 'Coltrane Motion'


def test_simple_mapping():
    class Artist(Skeleton):
        name = StringField(mapping='artist_name')

    artist = Artist.convert({'artist_name': 'Coltrane Motion'})
    assert artist.name == 'Coltrane Motion'


def test_nested_dict_mapping():
    class Artist(Skeleton):
        name = StringField(mapping='artist__name')

    artist = Artist.convert({'artist': {'name': 'Coltrane Motion'}})
    assert artist.name == 'Coltrane Motion'


def test_nested_array_mapping():
    class Artist(Skeleton):
        name = StringField(mapping='artists__0__name')

    # ensure we can grab the 0th item in the array
    artist = Artist.convert({'artists': [{'name': 'Coltrane Motion'}]})
    assert artist.name == 'Coltrane Motion'


def test_callable_mapping():
    def get_artist_name(obj):
        return obj['name']

    class Artist(Skeleton):
        name = StringField(mapping=get_artist_name)

    artist = Artist.convert({'name': 'Coltrane Motion'})
    assert artist.name == 'Coltrane Motion'
