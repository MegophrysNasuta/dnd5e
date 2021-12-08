import enum
from typing import List, Optional, Tuple


class ArmorType(enum.Enum):
    LIGHT = enum.auto()
    MEDIUM = enum.auto()
    HEAVY = enum.auto()


class Armor:
    def __init__(self, name: str, armor_class: int,
                 armor_type: Optional[ArmorType]=None,
                 max_dex_modifier: Optional[int]=None,
                 min_str_requirement: Optional[int]=None,
                 disadvantages_stealth: bool=False):
        self.name = str(name)
        self.armor_class = int(armor_class)
        self.armor_type = armor_type
        self.max_dex_modifier = max_dex_modifier and int(max_dex_modifier)
        self.min_str_requirement = min_str_requirement and int(min_str_requirement)
        self.disadvantages_stealth = bool(disadvantages_stealth)

    def __repr__(self):
        return ('Armor("%s", %r, armor_type=%r, max_dex_modifier=%r, '
                'min_str_requirement=%r, disadvantages_stealth=%r)') % (
                self.name, self.armor_class, self.armor_type,
                self.max_dex_modifier, self.min_str_requirement,
                self.disadvantages_stealth)

    def __str__(self):
        return '<%sArmor: %s (AC %i)>' % (self.armor_type.name.title(),
                                          self.name, self.armor_class)


RangeIncrement = Tuple[int, int]


class WeaponDamageType(enum.Enum):
    PIERCING = 'P'
    SLASHING = 'S'
    BLUDGEONING = 'B'


class Weapon:
    def __init__(self, name: str, damage: Optional[str]=None,
                 two_handed_damage: Optional[str]=None,
                 damage_type: Optional[WeaponDamageType]=None,
                 is_simple: bool=False,
                 range_increment: Optional[RangeIncrement]=None,
                 requires_ammo: bool=False, finesse_weapon: bool=False,
                 is_heavy: bool=False, is_light: bool=False,
                 slow_loading: bool=False, has_reach: bool=False,
                 can_be_thrown: bool=False, requires_two_hands: bool=False,
                 versatile: bool=False):
        self.name = str(name)
        self.damage = damage and str(damage)
        self.two_handed_damage = two_handed_damage and str(two_handed_damage)
        self.damage_type = damage_type
        self.is_simple = bool(is_simple)
        self.range_increment = range_increment and tuple(map(int,
                                                             range_increment))
        self.requires_ammo = bool(requires_ammo)
        self.finesse_weapon = bool(finesse_weapon)
        self.is_heavy = bool(is_heavy)
        self.is_light = bool(is_light)
        assert not (self.is_heavy and self.is_light)
        self.slow_loading = bool(slow_loading)
        self.has_reach = bool(has_reach)
        self.can_be_thrown = bool(can_be_thrown)
        if self.can_be_thrown:
            assert self.range_increment is not None
        assert not (self.can_be_thrown and self.requires_ammo)

        self.requires_two_hands = bool(requires_two_hands)
        self.versatile = bool(versatile)
        assert not (self.versatile and self.requires_two_hands)
        if self.versatile:
            assert self.two_handed_damage is not None

    @property
    def has_range(self) -> bool:
        return self.range_increment is not None

    @property
    def type_(self) -> str:
        if self.has_range:
            return 'Simple Ranged' if self.is_simple else 'Martial Ranged'
        else:
            return 'Simple Melee' if self.is_simple else 'Martial Melee'

    @property
    def properties(self) -> List[str]:
        prop_list = []
        if self.requires_ammo:
            assert self.range_increment is not None
            prop_list.append('Ammunition (range %i/%i)' % self.range_increment)
        if self.finesse_weapon:
            prop_list.append('Finesse')
        if self.is_heavy:
            prop_list.append('Heavy')
        if self.is_light:
            prop_list.append('Light')
        if self.slow_loading:
            prop_list.append('Loading')
        if self.has_reach:
            prop_list.append('Reach')
        if self.can_be_thrown:
            assert self.range_increment is not None
            prop_list.append('Thrown (range %i/%i)' % self.range_increment)
        if self.requires_two_hands:
            prop_list.append('Two-handed')
        if self.versatile:
            prop_list.append('Versatile (%s)' % self.two_handed_damage)
        return prop_list

    def __repr__(self):
        return ('Weapon("%s", %r, two_handed_damage=%r, '
                'damage_type=%r, is_simple=%r, range_increment=%r, '
                'requires_ammo=%r, finesse_weapon=%r, is_heavy=%r, is_light=%r, '
                'slow_loading=%r, has_reach=%r, can_be_thrown=%r, '
                'requires_two_hands=%r, versatile=%r)') % (
                self.name, self.damage, self.two_handed_damage,
                self.damage_type, self.is_simple, self.range_increment,
                self.requires_ammo, self.finesse_weapon, self.is_heavy,
                self.is_light, self.slow_loading, self.has_reach,
                self.can_be_thrown, self.requires_two_hands, self.versatile,
               )

    def __str__(self):
        str_rep = ['<Weapon: %s, %s']
        str_rep_contents = [self.name, self.type_]
        if self.has_range:
            str_rep.append(' %s')
            str_rep_contents.append(self.range_increment)
        str_rep.append(' %s (%s)>')
        str_rep_contents.extend([self.damage, self.damage_type.value])
        return ''.join(str_rep) % tuple(str_rep_contents)
