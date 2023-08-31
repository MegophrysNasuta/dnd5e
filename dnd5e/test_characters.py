from . import roll_dice
from .characters import Character, CharacterStat, HitType
from .items import Armor, WeaponType
from .srd_weapons import longsword, spear


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


def test_proficiency_bonus():
    expected_bonus_by_lvl = (
        (1, 2), (2, 2), (3, 2), (4, 2),
        (5, 3), (6, 3), (7, 3), (8, 3),
        (9, 4), (10, 4), (11, 4), (12, 4),
        (13, 5), (14, 5), (15, 5), (16, 5),
        (17, 6), (18, 6), (19, 6), (20, 6),
    )

    for lvl, bonus in expected_bonus_by_lvl:
        assert Character(level=lvl).proficiency_bonus == bonus


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


def test_swing_weapon():
    char = Character('Test', str_score=16, dex_score=17, dex_bonus=1,
                     hit_dice=roll_dice('5d8'), level=5,
                     proficiencies=(WeaponType.SIMPLE,))
    assert char.wielding == (None, None)
    char.wield_main(spear)
    assert char.wielding == (spear, None)

    dummy = Character('Dummy', base_armor_class=0, str_score=10)
    assert dummy.AC == 0

    ar = char.attack(dummy).describe()
    assert ar.hit_type == HitType.FULL
    assert ar.attack_roll is not None
    assert ar.damage_roll is not None
    assert char.is_proficient_with(spear)
    assert ar.proficiency_bonus == char.proficiency_bonus
    assert ar.modifier == char.STR.modifier
    assert ar.damage_roll[0].die_max_value == 6
    assert char.STR.modifier < ar.damage <= char.STR.modifier + 6

    char.wield_main(longsword)
    assert char.wielding == (longsword, None)

    ar = char.attack(dummy).describe()
    assert ar.hit_type == HitType.FULL
    assert ar.attack_roll is not None
    assert ar.damage_roll is not None
    assert ar.proficiency_bonus == 0
    assert ar.modifier == char.STR.modifier
    assert ar.damage_roll[0].die_max_value == 8
    assert char.STR.modifier < ar.damage <= char.STR.modifier + 8

    ar = char.attack(dummy, using_two_hands=True).describe()
    assert ar.hit_type == HitType.FULL
    assert ar.attack_roll is not None
    assert ar.damage_roll is not None
    assert ar.proficiency_bonus == 0
    assert ar.modifier == char.STR.modifier
    assert ar.damage_roll[0].die_max_value == 10
    assert char.STR.modifier < ar.damage <= char.STR.modifier + 10

    char.wield_main(None)
    ar = char.attack(dummy).describe()
    assert ar.hit_type == HitType.FULL
    assert ar.attack_roll is not None
    assert ar.damage_roll is not None
    assert ar.proficiency_bonus == char.proficiency_bonus
    assert ar.modifier == char.STR.modifier
    assert ar.damage_roll[0].die_max_value == 1
    assert ar.damage == 1 + char.STR.modifier
