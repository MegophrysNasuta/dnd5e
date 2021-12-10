from __future__ import annotations

import enum
from typing import Iterable, List, Optional, Tuple, Union
from .dicerolls import roll_dice, DiceResult
from .items import (Armor, ArmorType, SimpleWeapon, MartialWeapon,
                    Weapon, WeaponType)


class HitType(enum.Enum):
    FULL = enum.auto()
    SHIELD_GLANCE = enum.auto()
    ARMOR_GLANCE = enum.auto()


class AttackResult:
    def __init__(self, hit_type: Optional[HitType] = None, damage: int = 0,
                 attack_roll: Optional[DiceResult] = None, modifier: int = 0,
                 proficiency_bonus: int = 0, critical_hit: bool = False,
                 target: Optional[Character] = None,
                 damage_roll: Optional[DiceResult] = None,
                 attack_with: Optional[Weapon] = None,
                 with_advantage: bool = False,
                 with_disadvantage: bool = False):
        self.hit_type = hit_type
        self.damage = int(damage)
        self.attack_roll = attack_roll
        self.damage_roll = damage_roll
        self.modifier = int(modifier)
        self.proficiency_bonus = int(proficiency_bonus)
        self.critical_hit = bool(critical_hit)
        self.target = target
        self.attack_with = attack_with
        self.with_advantage = bool(with_advantage)
        self.with_disadvantage = bool(with_disadvantage)

    def describe(self):
        if self.attack_with is None:
            attack_type = 'The attack'
        else:
            attack_type = 'The attack with %s' % self.attack_with.name

        if self.target is None:
            target = 'target'
        else:
            target = self.target.name

        if self.hit_type == HitType.SHIELD_GLANCE:
            desc = attack_type + ' glances off %s\'s shield.' % target
        elif self.hit_type == HitType.ARMOR_GLANCE:
            desc = attack_type + (' bounces harmlessly off %s\'s '
                                  'armor.' % target)
        elif self.hit_type == HitType.FULL:
            desc = attack_type + ' hits %s for %i damage!' % (target,
                                                              self.damage)
        else:
            desc = attack_type + ' missed %s.' % target

        if self.target:
            desc += '\n%s is now %s.' % (target, self.target.hp_status)

        print(desc)
        return self


class CharacterStat:
    def __init__(self, full_name: str, base_value: Optional[int] = None,
                 bonus: Optional[int] = None):
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


Proficiency = Union[ArmorType, WeaponType, CharacterStat]


class Character:
    def __init__(self, name: Optional[str] = None,
                 race: Optional[str] = None,
                 class_: Optional[str] = None,
                 base_armor_class: int = 10,
                 armor: Optional[Armor] = None,
                 uses_shield: bool = False,
                 include_stats_in_AC: Tuple[str, ...] = (),
                 level: int = 1, hit_dice: Optional[DiceResult] = None,
                 wounds: int = 0, base_movement_speed: int = 30,
                 proficiencies: Optional[Iterable[Proficiency]] = None,
                 str_bonus: Optional[int] = None,
                 str_score: Optional[int] = None,
                 dex_bonus: Optional[int] = None,
                 dex_score: Optional[int] = None,
                 con_bonus: Optional[int] = None,
                 con_score: Optional[int] = None,
                 int_bonus: Optional[int] = None,
                 int_score: Optional[int] = None,
                 wis_bonus: Optional[int] = None,
                 wis_score: Optional[int] = None,
                 cha_bonus: Optional[int] = None,
                 cha_score: Optional[int] = None):
        self.name = name
        self.race = race
        self.class_ = class_
        self.base_armor_class = int(base_armor_class)
        self.armor = armor
        self.uses_shield = bool(uses_shield)
        self.include_stats_in_AC = tuple(include_stats_in_AC)
        self.level = int(level)
        self.hit_dice = hit_dice
        self.wounds = int(wounds)
        if self.hit_dice:
            assert len(self.hit_dice) == self.level
        self.base_movement_speed = int(base_movement_speed)
        self.STR = CharacterStat('Strength', str_score, str_bonus)
        self.DEX = CharacterStat('Dexterity', dex_score, dex_bonus)
        self.CON = CharacterStat('Constitution', con_score, con_bonus)
        self.INT = CharacterStat('Intelligence', int_score, int_bonus)
        self.WIS = CharacterStat('Wisdom', wis_score, wis_bonus)
        self.CHA = CharacterStat('Charisma', cha_score, cha_bonus)
        self.__main_hand: Optional[Weapon] = None
        self.__off_hand: Optional[Weapon] = None
        self.proficiencies: List[Proficiency] = list(proficiencies or ())

    @property
    def AC(self) -> int:
        ac = self.base_armor_class

        if self.armor:
            max_dex_modifier = self.armor.max_dex_modifier or 99
            ac = self.armor.armor_class + min(self.DEX.modifier or 0,
                                              max_dex_modifier)
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

    def attack(self, other: Character, main_hand: bool = True,
               using_two_hands: bool = False,
               with_advantage: bool = False,
               with_disadvantage: bool = False,
               distance: int = 5) -> AttackResult:
        if not isinstance(other, Character):
            raise ValueError("Unsure how to attack a(n) "
                             "%s." % other.__class__.__name__)

        if self.armor and self.armor.armor_type not in self.proficiencies:
            with_disadvantage = True

        if with_advantage and with_disadvantage:
            with_advantage = with_disadvantage = False

        if self.hp < 1:
            raise RuntimeError("%s is dead and can't attack." % self.name)

        damage = None
        weapon = None
        if using_two_hands and self.wielding[0] is not None:
            if self.wielding[0].versatile:
                damage = self.wielding[0].two_handed_damage
            else:
                damage = self.wielding[0].damage
            weapon = self.wielding[0]
        elif main_hand and self.wielding[0] is not None:
            damage = self.wielding[0].damage
            weapon = self.wielding[0]
        elif not main_hand and self.wielding[1] is not None:
            damage = self.wielding[1].damage
            weapon = self.wielding[1]

        if damage is None:
            damage = '1d1'

        threshold = 5 if not (weapon and weapon.has_reach) else 10
        ranged = distance > threshold
        if not (weapon and weapon.has_range) and ranged:
            weapon_name = weapon and weapon.name or 'unarmed strike'
            raise RuntimeError("Cannot attack with %s at range "
                               "%i." % (weapon_name, distance))

        if ranged:
            modifier = self.DEX.modifier
        else:
            if weapon and weapon.finesse_weapon:
                modifier = max(self.STR.modifier, self.DEX.modifier)
            else:
                modifier = self.STR.modifier

        proficiency_bonus = 0
        if weapon is None or self.is_proficient_with(weapon):
            proficiency_bonus = self.proficiency_bonus

        attack_roll = roll_dice('1d20')
        if with_advantage or with_disadvantage:
            attack_reroll = roll_dice('1d20')
            if ((with_advantage and attack_reroll.total > attack_roll.total) or
                    (with_disadvantage and
                     attack_reroll.total < attack_roll.total)):
                attack_roll = attack_reroll
        critical_threshold = 20
        critical_hit = False
        if attack_roll.total >= critical_threshold:
            critical_hit = True
        attack_roll += modifier + proficiency_bonus
        result = AttackResult(
            attack_roll=attack_roll,
            modifier=modifier,
            proficiency_bonus=proficiency_bonus,
            target=other,
            attack_with=weapon,
            with_advantage=with_advantage,
            with_disadvantage=with_disadvantage,
            critical_hit=critical_hit,
        )
        if attack_roll.total > other.AC or critical_hit:
            if critical_hit:
                damage_roll = roll_dice(damage) + roll_dice(damage)
            else:
                damage_roll = roll_dice(damage)
            result.damage_roll = damage_roll
            result.hit_type = HitType.FULL
            if main_hand:
                damage_modifier = modifier
            else:
                damage_modifier = min(modifier, 0)
            result.damage = max((damage_roll + damage_modifier).total, 1)
            other.wounds += result.damage
        elif other.uses_shield and attack_roll.total > (other.AC - 2):
            result.hit_type = HitType.SHIELD_GLANCE
        elif attack_roll.total > 10:
            result.hit_type = HitType.ARMOR_GLANCE
        else:
            result.hit_type = None

        if ranged and weapon is not None and weapon.can_be_thrown:
            if main_hand:
                self.wield_main(None)
            else:
                self.wield_off(None)

        return result

    def is_proficient_with(self, thing: Weapon | Armor):
        if isinstance(thing, SimpleWeapon):
            return WeaponType.SIMPLE in self.proficiencies
        elif isinstance(thing, MartialWeapon):
            return WeaponType.MARTIAL in self.proficiencies
        elif isinstance(thing, Armor):
            return thing.armor_type in self.proficiencies
        else:
            return False

    @property
    def hp(self) -> int:
        return self.maxhp - self.wounds

    @property
    def hp_percent(self) -> float:
        if self.maxhp == 0:
            return 0.
        return (self.hp / self.maxhp) * 100

    @property
    def hp_status(self) -> str:
        if self.hp < 1:
            return 'dead'
        elif self.hp_percent < 11:
            return 'critically wounded'
        elif self.hp_percent < 25:
            return 'badly wounded'
        elif self.hp_percent < 50:
            return 'bloodied'
        elif self.hp_percent < 70:
            return 'injured'
        elif self.hp_percent < 90:
            return 'roughed up'
        elif self.hp_percent < 99:
            return 'slightly injured'
        else:
            return 'unscathed'

    @property
    def maxhp(self) -> int:
        if not self.hit_dice:
            return 0
        return sum(self.hit_dice) + (self.CON.modifier * self.level)

    @property
    def movement_speed(self) -> int:
        if (self.armor and self.armor.min_str_requirement and
                self.STR.value < self.armor.min_str_requirement):
            return self.base_movement_speed - 10
        else:
            return self.base_movement_speed

    @property
    def proficiency_bonus(self) -> int:
        return 2 + ((self.level - 1) // 4)

    @property
    def stats(self) -> CharacterStats:
        return self.STR, self.DEX, self.CON, self.INT, self.WIS, self.CHA

    def wield_main(self, weapon: Optional[Weapon]):
        self.__main_hand = weapon
        if weapon is not None and weapon.requires_two_hands:
            self.wield_off(None)

    def wield_off(self, weapon: Optional[Weapon]):
        self.__off_hand = weapon
        self.uses_shield = False

    @property
    def wielding(self) -> Tuple[Optional[Weapon], Optional[Weapon]]:
        return (self.__main_hand, self.__off_hand)

    def __repr__(self):
        return ('Character("%s", race="%s", class_="%s", '
                'base_armor_class=%r, armor=%r, level=%r, '
                'uses_shield=%r, include_stats_in_AC=%r, '
                'hit_dice=%r, wounds=%r, proficiencies=%r, '
                'base_movement_speed=%r, '
                'str_bonus=%r, str_score=%r, '
                'dex_bonus=%r, dex_score=%r, '
                'con_bonus=%r, con_score=%r, '
                'int_bonus=%r, int_score=%r, '
                'wis_bonus=%r, wis_score=%r, '
                'cha_bonus=%r, cha_score=%r)') % (
                self.name, self.race, self.class_,
                self.base_armor_class, self.armor, self.level,
                self.uses_shield, self.include_stats_in_AC,
                self.hit_dice, self.wounds, self.proficiencies,
                self.base_movement_speed,
                self.STR.bonus, self.STR.base_value,
                self.DEX.bonus, self.DEX.base_value,
                self.CON.bonus, self.CON.base_value,
                self.INT.bonus, self.INT.base_value,
                self.WIS.bonus, self.WIS.base_value,
                self.CHA.bonus, self.CHA.base_value)

    def __str__(self):
        return '<Character: %s, %s %s %s>' % (self.name, self.race,
                                              self.class_, self.stats)
