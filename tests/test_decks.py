import pytest

from conftest import ac


def test_deckNames(session_with_profile_loaded):
    result = ac.deckNames()
    assert result == ["Default"]


def test_deckNamesAndIds(session_with_profile_loaded):
    result = ac.deckNamesAndIds()
    assert result == {"Default": 1}


def test_createDeck(session_with_profile_loaded):
    ac.createDeck("foo")
    assert {*ac.deckNames()} == {"Default", "foo"}


def test_changeDeck(setup):
    ac.changeDeck(cards=setup.card_ids, deck="bar")
    assert "bar" in ac.deckNames()


def test_deleteDeck(setup):
    before = ac.deckNames()
    ac.deleteDecks(decks=["test_deck"], cardsToo=True)
    after = ac.deckNames()
    assert {*before} - {*after} == {"test_deck"}


def test_deleteDeck_must_be_called_with_cardsToo_set_to_True_on_later_api(setup):
    with pytest.raises(Exception):
        ac.deleteDecks(decks=["test_deck"])
    with pytest.raises(Exception):
        ac.deleteDecks(decks=["test_deck"], cardsToo=False)


def test_getDeckConfig(session_with_profile_loaded):
    result = ac.getDeckConfig(deck="Default")
    assert result["name"] == "Default"


def test_saveDeckConfig(session_with_profile_loaded):
    config = ac.getDeckConfig(deck="Default")
    result = ac.saveDeckConfig(config=config)
    assert result is True


def test_setDeckConfigId(session_with_profile_loaded):
    result = ac.setDeckConfigId(decks=["Default"], configId=1)
    assert result is True


def test_cloneDeckConfigId(session_with_profile_loaded):
    result = ac.cloneDeckConfigId(cloneFrom=1, name="test")
    assert isinstance(result, int)


def test_removedDeckConfigId(session_with_profile_loaded):
    new_config_id = ac.cloneDeckConfigId(cloneFrom=1, name="test")
    assert ac.removeDeckConfigId(configId=new_config_id) is True


def test_removedDeckConfigId_fails_with_invalid_id(session_with_profile_loaded):
    new_config_id = ac.cloneDeckConfigId(cloneFrom=1, name="test")
    assert ac.removeDeckConfigId(configId=new_config_id) is True
    assert ac.removeDeckConfigId(configId=new_config_id) is False


def test_getDeckStats(session_with_profile_loaded):
    result = ac.getDeckStats(decks=["Default"])
    assert list(result.values())[0]["name"] == "Default"


def test_getDeckDescription_default_is_empty(session_with_profile_loaded):
    result = ac.getDeckDescription(deck="Default")
    assert result == ""


def test_setDeckDescription_then_getDeckDescription(session_with_profile_loaded):
    ac.createDeck("desc_target")
    assert ac.setDeckDescription(deck="desc_target",
                                 description="hello world") is True
    assert ac.getDeckDescription(deck="desc_target") == "hello world"


def test_setDeckDescription_overwrites_existing_value(session_with_profile_loaded):
    ac.createDeck("desc_target")
    ac.setDeckDescription(deck="desc_target", description="first")
    ac.setDeckDescription(deck="desc_target", description="second")
    assert ac.getDeckDescription(deck="desc_target") == "second"


def test_setDeckDescription_accepts_empty_string(session_with_profile_loaded):
    ac.createDeck("desc_target")
    ac.setDeckDescription(deck="desc_target", description="something")
    assert ac.setDeckDescription(deck="desc_target", description="") is True
    assert ac.getDeckDescription(deck="desc_target") == ""


def test_getDeckDescription_raises_for_missing_deck(session_with_profile_loaded):
    with pytest.raises(Exception):
        ac.getDeckDescription(deck="no_such_deck")


def test_setDeckDescription_raises_for_missing_deck(session_with_profile_loaded):
    with pytest.raises(Exception):
        ac.setDeckDescription(deck="no_such_deck", description="x")


def test_setDeckDescription_raises_for_non_string_description(session_with_profile_loaded):
    ac.createDeck("desc_target")
    with pytest.raises(Exception):
        ac.setDeckDescription(deck="desc_target", description=123)
