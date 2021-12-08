import inspect
import typing
from typing import Optional

from .characters import Character, CharacterStat
from .dicerolls import DieResult, DiceResult, roll_dice
from .items import Armor, ArmorType, Weapon, WeaponDamageType


def repr_test(obj):
    def is_init_func(o):
        return inspect.ismethod(o) and o.__name__ == '__init__'

    try:
        live_obj = obj('name')
    except ValueError:
        live_obj = obj(1)
    except TypeError:
        live_obj = obj('name', 10)

    init_func = inspect.getmembers(live_obj, predicate=is_init_func)[0][1]

    example_of = {
        Optional[str]: "a string",
        int: 14,    # bonus: guaranteed random
        str: "A Required String",
        Optional[Armor]: Armor('Leather armor', 11),
        bool: True,
        typing.Tuple[str, ...]: tuple('abc'),
        Optional[int]: 5,
        Optional[ArmorType]: ArmorType.MEDIUM,
        Optional[WeaponDamageType]: WeaponDamageType.SLASHING,
        Optional[typing.Tuple[int, int]]: (20, 60),
    }

    init_kw = {}
    for attr, attr_type in init_func.__annotations__.items():
        init_kw[attr] = example_of[attr_type]

    created_with_init = obj(**init_kw)
    created_with_eval = eval(repr(created_with_init))

    special_mappings = {
        'str_bonus': 'STR.bonus',
        'dex_bonus': 'DEX.bonus',
        'con_bonus': 'CON.bonus',
        'int_bonus': 'INT.bonus',
        'wis_bonus': 'WIS.bonus',
        'cha_bonus': 'CHA.bonus',
        'str_score': 'STR.base_value',
        'dex_score': 'DEX.base_value',
        'con_score': 'CON.base_value',
        'int_score': 'INT.base_value',
        'wis_score': 'WIS.base_value',
        'cha_score': 'CHA.base_value',
    }

    for attr_name in init_kw:
        try:
            attr_val = getattr(created_with_init, attr_name)
            assert getattr(created_with_eval, attr_name) == attr_val
        except AttributeError:
            attr_name = special_mappings[attr_name]
            attr1, attr2 = attr_name.split('.')
            attr = getattr(getattr(created_with_eval, attr1), attr2)
            attr_val = getattr(getattr(created_with_init, attr1), attr2)
            assert attr == attr_val
        finally:
            attr_val = None


def test_character_repr():
    repr_test(Character)

def test_characterstat_repr():
    repr_test(CharacterStat)

def test_dieresult_repr():
    repr_test(DieResult)

def test_diceresult_repr():
    dice_result = roll_dice('4d6')
    assert isinstance(dice_result, DiceResult)
    assert len(dice_result) == 4
    new_dice_result = eval(repr(dice_result))
    assert new_dice_result == dice_result

def test_armor_repr():
    repr_test(Armor)

def test_weapon_repr():
    repr_test(Weapon)
