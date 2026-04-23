import pytest

from lab14 import GameSession, Player, SessionManager


def test_create_and_list_sessions():
    manager = SessionManager()
    session = manager.create_session("Adventure Lane", max_players=2)

    assert session.name == "Adventure Lane"
    assert session.max_players == 2
    assert session.is_full() is False
    assert len(manager.list_sessions()) == 1


def test_join_session_success():
    manager = SessionManager()
    session = manager.create_session("Mystic Forest", max_players=2)

    player = manager.join_session(session.session_id, "Ariel")

    assert isinstance(player, Player)
    assert player.name == "Ariel"
    assert session.list_player_names() == ["Ariel"]


def test_join_session_full_error():
    manager = SessionManager()
    session = manager.create_session("Tiny Tavern", max_players=1)
    manager.join_session(session.session_id, "Hero")

    with pytest.raises(ValueError, match="full"):
        manager.join_session(session.session_id, "Rogue")


def test_join_session_duplicate_player_error():
    manager = SessionManager()
    session = manager.create_session("Dragon's Den", max_players=3)
    manager.join_session(session.session_id, "Mage")

    with pytest.raises(ValueError, match="already joined"):
        manager.join_session(session.session_id, "Mage")


def test_get_session_invalid_id_error():
    manager = SessionManager()

    with pytest.raises(ValueError, match="No session with id"):
        manager.get_session("invalid-id")
