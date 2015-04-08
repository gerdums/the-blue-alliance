from google.appengine.ext import ndb

from consts.district_type import DistrictType
from models.team import Team


class DistrictTeam(ndb.Model):
    """
    DistrictTeam represents the "home district" for a team in a year
    key_name is like <year><district_short>_<team_key> (e.g. 2015ne_frc1124)
    district_short is one of DistrictType.type_abbrevs
    """

    team = ndb.KeyProperty(kind=Team)
    year = ndb.IntegerProperty()
    district = ndb.IntegerProperty()  # One of DistrictType constants

    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    updated = ndb.DateTimeProperty(auto_now=True, indexed=False)

    def __init__(self, *args, **kw):
        # store set of affected references referenced keys for cache clearing
        # keys must be model properties
        self._affected_references = {
            'team': set(),
            'year': set(),
        }
        super(DistrictTeam, self).__init__(*args, **kw)

    @property
    def key_name(self):
        return "{}{}_{}".format(self.year, DistrictType.type_abbrevs[self.district], self.team.id())
