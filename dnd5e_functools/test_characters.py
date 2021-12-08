import pytest
from .characters import Character, CharacterStat
from .items import Armor, Weapon


def test_armor_class():
    leather_armor = Armor('Leather', 11)
    char = Character()
    assert char.AC == 10
    char.armor = leather_armor
    assert char.AC == 11
    char.DEX.base_value = 13
    assert char.AC == 12
    char.include_stats_in_AC = ('wisdom',)
    char.WIS.base_value = 13
    assert char.AC == 12
    char.armor = None
    assert char.AC == 12
    char.include_stats_in_AC = ('wisdom', 'constitution')
    char.CON.base_value = 13
    assert char.AC == 13
    char.armor = leather_armor
    char.uses_shield = True
    assert char.AC == 14


def test_character_stats():
    stat = CharacterStat('strength')
    assert stat.abbr == 'STR'
    assert stat.full_name == 'Strength'
    stat = CharacterStat('dexterity')
    assert stat.abbr == 'DEX'
    assert stat.full_name == 'Dexterity'
    stat = CharacterStat('constitution')
    assert stat.abbr == 'CON'
    assert stat.full_name == 'Constitution'
    stat = CharacterStat('intelligence')
    assert stat.abbr == 'INT'
    assert stat.full_name == 'Intelligence'
    stat = CharacterStat('wisdom')
    assert stat.abbr == 'WIS'
    assert stat.full_name == 'Wisdom'
    stat = CharacterStat('charisma')
    assert stat.abbr == 'CHA'
    assert stat.full_name == 'Charisma'

    expected_mods = (
        (1, -5), (2, -4),
        (3, -4), (4, -3),
        (5, -3), (6, -2),
        (7, -2), (8, -1),
        (9, -1), (10, 0),
        (11, 0), (12, 1),
        (13, 1), (14, 2),
        (15, 2), (16, 3),
        (17, 3), (18, 4),
        (19, 4), (20, 5),
        (21, 5), (22, 6),
        (23, 6), (24, 7),
        (25, 7), (26, 8),
        (27, 8), (28, 9),
        (29, 9), (30, 10),
    )
    for score, expected_mod in expected_mods:
        stat = CharacterStat('', score)
        assert stat.modifier == expected_mod

    stat = CharacterStat('', 10) + 2
    assert stat.bonus == 2
    assert stat.value == 12
    assert stat.modifier == 1

