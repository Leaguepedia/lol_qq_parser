import pytest
from requests.models import HTTPError


def test_working_endpoint():
    """
    Querying an arbitrary endpoint and making sure it works
    """
    # Using LPL 2021 Spring standings
    import lol_qq_parser.utils

    standings = lol_qq_parser.utils.query_tjstats(
        "v1/compound/team?seasonId=148&stageIds=1%2C5"
    )

    assert standings
    assert standings["success"]
    assert standings["data"]
