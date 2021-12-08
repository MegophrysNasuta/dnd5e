from __future__ import annotations

import enum
from typing import Optional, Tuple
from .dicerolls import roll, DieResult
from .items import Armor, Weapon


class HitType(enum.Enum):
    FULL = enum.auto()
    SHIELD_GLANCE = enum.auto()
    ARMOR_GLANCE = enum.auto()


class AttackResult:
    def __init__(self, hit_type: Optional[HitType]=None, damage: int=0,
                 attack_roll: Optional[DieResult]=None, modifier: int=0,
                 proficiency_bonus: int=0,
                 damage_roll: Optional[DieResult]=None):
        self.hit_type = hit_type
        self.damage = int(damage)
        self.attack_roll = attack_roll
        self.damage_roll = damage_roll
        self.modifier = int(modifier)
        self.proficiency_bonus = int(proficiency_bonus)


class CharacterStat:
    def __init__(self, full_name: str, base_value: Optional[int]=None,
                 bonus: Optional[int]=None):
        self.__fullname = str(full_name)
        self.base_value = base_value and int(base_value) or 10
        self.bonus = bonus and int(bonus) or 0

    @property
    def full_name(self) -> str:
        return self.__fullname.title()

    @property
    def abbr(self) -> str:
        return self.__fullname[:3].upper()

    @property
    def modifier(self) -> int:
        if self.value >= 10:
            return int((self.value - 10) / 2)
        else:
            return int((self.value - 11) / 2)

    @property
    def value(self) -> int:
        return self.base_value + self.bonus

    def __add__(self, value):
        self.bonus = int(value)
        return self

    def __repr__(self):
        return 'CharacterStat(%r, base_value=%r, bonus=%r)' % (self.full_name,
                                                               self.base_value,
                                                               self.bonus)

    def __str__(self):
        str_rep_line = '<CharacterStat: %s (%s) [%i (Mod %+i; Bonus %+i)]>'
        return str_rep_line % (self.full_name, self.abbr, self.value,
                               self.modifier, self.bonus)

CharacterStats = Tuple[Optional[CharacterStat], Optional[CharacterStat],
                       Optional[CharacterStat], Optional[CharacterStat],
                       Optional[CharacterStat], Optional[CharacterStat]]


class Character:
    def __init__(self, name: Optional[str]=None,
                 race: Optional[str]=None,
                 class_: Optional[str]=None,
                 base_armor_class: int=10,
                 armor: Optional[Armor]=None,
                 uses_shield: bool=False,
                 include_stats_in_AC: Tuple[str, ...]=(),
                 proficiency_bonus: int=2,
                 str_bonus: Optional[int]=None,
                 str_score: Optional[int]=None,
                 dex_bonus: Optional[int]=None,
                 dex_score: Optional[int]=None,
                 con_bonus: Optional[int]=None,
                 con_score: Optional[int]=None,
                 int_bonus: Optional[int]=None,
                 int_score: Optional[int]=None,
                 wis_bonus: Optional[int]=None,
                 wis_score: Optional[int]=None,
                 cha_bonus: Optional[int]=None,
                 cha_score: Optional[int]=None):
        self.name = name
        self.race = race
        self.class_ = class_
        self.base_armor_class = int(base_armor_class)
        self.armor = armor
        self.uses_shield = bool(uses_shield)
        self.include_stats_in_AC = tuple(include_stats_in_AC)
        self.proficiency_bonus = int(proficiency_bonus)
        self.STR = CharacterStat('Strength', str_score, str_bonus)
        self.DEX = CharacterStat('Dexterity', dex_score, dex_bonus)
        self.CON = CharacterStat('Constitution', con_score, con_bonus)
        self.INT = CharacterStat('Intelligence', int_score, int_bonus)
        self.WIS = CharacterStat('Wisdom', wis_score, wis_bonus)
        self.CHA = CharacterStat('Charisma', cha_score, cha_bonus)
        self.__main_hand: Optional[Weapon] = None
        self.__off_hand: Optional[Weapon] = None

    @property
    def AC(self) -> int:
        ac = self.base_armor_class

        if self.armor:
            ac = self.armor.armor_class + min(self.DEX.modifier or 0,
                                              self.armor.max_dex_modifier or 99)
        else:
            ac += self.DEX.modifier or 0

        if self.uses_shield:
            ac += 2

        if not self.armor and not self.uses_shield:
            for stat_name in self.include_stats_in_AC:
                try:
                    ac += getattr(self, stat_name.upper()[:3]).modifier
                except AttributeError:
                    continue

        return ac

    def attack(self, other: Character, main_hand: bool=True,
               using_two_hands: bool=False, ranged: bool=False) -> AttackResult:
        if not isinstance(other, Character):
            raise ValueError("Unsure how to attack a(n) "
                             "%s." % other.__class__.__name__)

        damage = None
        weapon = None
        if using_two_hands and self.wielding[0] is not None:
            damage = self.wielding[0].two_handed_damage
            weapon = self.wielding[0]
        elif main_hand and self.wielding[0] is not None:
            damage = self.wielding[0].damage
            weapon = self.wielding[0]
        elif not main_hand and self.wielding[1] is not None:
            damage = self.wielding[1].damage
            weapon = self.wielding[1]

        if damage is None:
            damage = '1d4'

        if ranged:
            modifier = self.DEX.modifier
        else:
            if weapon and weapon.finesse_weapon:
                modifier = max(self.STR.modifier, self.DEX.modifier)
            else:
                modifier = self.STR.modifier

        attack_roll = tuple(roll('1d20'))[0]
        attack_roll += modifier + self.proficiency_bonus
        result = AttackResult(
            attack_roll=attack_roll,
            modifier=modifier,
            proficiency_bonus=self.proficiency_bonus,
        )
        if attack_roll > other.AC:
            damage_roll = tuple(roll(damage))[0]
            result.damage_roll = damage_roll
            result.hit_type = HitType.FULL
            result.damage = damage_roll + modifier
        elif other.uses_shield and attack_roll > (other.AC - 2):
            result.hit_type = HitType.SHIELD_GLANCE
        elif attack_roll > 10:
            result.hit_type = HitType.ARMOR_GLANCE

        return result

    @property
    def stats(self) -> CharacterStats:
        return self.STR, self.DEX, self.CON, self.INT, self.WIS, self.CHA

    def wield_main(self, weapon: Weapon):
        self.__main_hand = weapon

    def wield_off(self, weapon: Weapon):
        self.__off_hand = weapon
        self.uses_shield = False

    @property
    def wielding(self) -> Tuple[Optional[Weapon], Optional[Weapon]]:
        return (self.__main_hand, self.__off_hand)

    def __repr__(self):
        return ('Character("%s", race="%s", class_="%s", '
                'base_armor_class=%r, armor=%r, proficiency_bonus=%r, '
                'uses_shield=%r, include_stats_in_AC=%r, '
                'str_bonus=%r, str_score=%r, '
                'dex_bonus=%r, dex_score=%r, '
                'con_bonus=%r, con_score=%r, '
                'int_bonus=%r, int_score=%r, '
                'wis_bonus=%r, wis_score=%r, '
                'cha_bonus=%r, cha_score=%r)') % (
                self.name, self.race, self.class_,
                self.base_armor_class, self.armor, self.proficiency_bonus,
                self.uses_shield, self.include_stats_in_AC,
                self.STR.bonus, self.STR.base_value,
                self.DEX.bonus, self.DEX.base_value,
                self.CON.bonus, self.CON.base_value,
                self.INT.bonus, self.INT.base_value,
                self.WIS.bonus, self.WIS.base_value,
                self.CHA.bonus, self.CHA.base_value)

    def __str__(self):
        return '<Character: %s, %s %s %s>' % (self.name, self.race,
                                              self.class_, self.stats)
