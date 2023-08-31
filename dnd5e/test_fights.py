import pytest

from . import Character, roll_dice
from .srd_weapons import spear, shortsword


def test_hero_vs_kobold():
    kobold = Character('kobold', hit_dice=roll_dice('1d4'), level=1)
    assert 0 < kobold.hp < 5
    assert kobold.hp_status == 'unscathed'
    hero = Character('hero', hit_dice=roll_dice('5d8'), level=5,
                     str_score=18, dex_score=18)
    assert hero.wielding == (None, None)
    hero.wield_main(spear)
    result = hero.attack(kobold, distance=10)
    assert hero.wielding == (None, None)
    kobold.wounds = 0   # they must have a priest
    assert kobold.hp_status == 'unscathed'
    with pytest.raises(RuntimeError):
        hero.attack(kobold, distance=10)

    hero.wield_main(shortsword)
    result.hit_type = None
    while not result.hit_type:
        result = hero.attack(kobold)
    assert hero.wielding == (shortsword, None)
