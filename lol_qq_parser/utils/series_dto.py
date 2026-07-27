from dataclasses import dataclass, field
from typing import List, Dict

import lol_dto
from lol_dto.classes.sources.empty_dataclass import EmptyDataclass


@dataclass
class LolQQPlayerSource:
    id: int
    name: str
    picture_url: str


@dataclass
class LolQQTeamSource:
    id: int


@dataclass
class LolQQSeriesSource:
    # Also called bmid
    matchId: int
    gridSeriesId: int

    teams: List[LolQQTeamSource]


@dataclass
class LolQQSeries:
    """
    A dictionary representing a League of Legends series (Bo1, Bo3, ...)
    """

    sources: dataclass = field(default_factory=EmptyDataclass)

    # Individual game objects, sorted by date
    games: List[lol_dto.classes.game.LolGame] = field(default_factory=list)

    # Name of the winning team
    winner: str = None

    # {'team_id': score}
    # TODO This is a very raw implementation that is honestly a bit stupid
    #   We need to find something better, as we do for sources
    score: Dict[int, int] = field(default_factory=dict)
