import os
import pytest
import json
import pydantic

match_id_list = [8108, 8269, 10787, 11365, 2975393]


@pytest.mark.parametrize("match_id", match_id_list)
def test_validate_match(request, match_id):
    import lol_qq_parser.schemas.match_detail

    raw_dump_folder = os.path.join("data", "matchDetail")
    with open(file=os.path.join(raw_dump_folder, f"{match_id}.json"), mode="r+") as f:
        match_detail_raw = json.load(f)

    assert match_detail_raw

    lol_qq_parser.schemas.match_detail.Model(**match_detail_raw)

    request.config.cache.set(f"{match_id}_raw", match_detail_raw)


def test_not_validate_match():
    """
    Making sure the schema does not validate faulty JSONs
    """
    import lol_qq_parser.schemas.match_detail

    with pytest.raises(pydantic.ValidationError):
        lol_qq_parser.schemas.match_detail.Model(**{"Hello": "World"})


@pytest.mark.parametrize("match_id", match_id_list)
def test_create_lol_series(request, match_id):
    """
    Creates a lol series based on its matchId
    """
    # We have to create from the raw cache as the cache object does not support pydantic models
    from lol_qq_parser.parsers.match_detail import match_detail_to_lol_series
    import lol_qq_parser.schemas.match_detail

    match_detail_raw = request.config.cache.get(f"{match_id}_raw", None)
    match_detail = lol_qq_parser.schemas.match_detail.Model(**match_detail_raw)

    assert match_detail

    series = match_detail_to_lol_series(match_detail)

    assert series.winner
    assert series.games

    score = {}

    for game in series.games:
        assert game.winner in ("BLUE", "RED")

        for side in ("BLUE", "RED"):
            team = getattr(game.teams, side)

            assert team.sources.qq.id
            assert isinstance(team.endOfGameStats.hordeKills, int)
            assert isinstance(team.endOfGameStats.riftHeraldKills, int)

            if team.sources.qq.id not in score:
                score[team.sources.qq.id] = 0

            if game.winner == side:
                score[team.sources.qq.id] += 1

            for player in team.players:
                assert player.sources.qq.id
                assert player.sources.qq.name

                assert player.championId
                assert player.role in ["TOP", "JGL", "MID", "BOT", "SUP"]
                assert player.sources.qq.id

    assert score == series.score
