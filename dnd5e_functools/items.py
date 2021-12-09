import enum
from typing import Any, List, Optional, Tuple


class ArmorType(enum.Enum):
    LIGHT = enum.auto()
    MEDIUM = enum.auto()
    HEAVY = enum.auto()

    def __repr__(self):
        return '%s.%s' % (self.__class__.__name__, self.name)


class Armor:
    def __init__(self, name: str, armor_class: int,
                 armor_type: Optional[ArmorType]=None,
                 min_str_requirement: Optional[int]=None,
                 disadvantages_stealth: bool=False):
        self.name = str(name)
        self.armor_class = int(armor_class)
        self.armor_type = armor_type
        self.min_str_requirement = min_str_requirement and int(min_str_requirement)
        self.disadvantages_stealth = bool(disadvantages_stealth)
        if self.armor_type == ArmorType.HEAVY:
            self.disadvantages_stealth = True

    @property
    def max_dex_modifier(self) -> Optional[int]:
        if self.armor_type == ArmorType.LIGHT:
            return None
        elif self.armor_type == ArmorType.MEDIUM:
            return 2
        else:
            return 0

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False

        return (
            self.name == other.name and
            self.armor_class == other.armor_class and
            self.armor_type == other.armor_type and
            self.min_str_requirement == other.min_str_requirement and
            self.disadvantages_stealth == other.disadvantages_stealth
        )

    def __repr__(self):
        return ('Armor(%r, %r, armor_type=%r, '
                'min_str_requirement=%r, disadvantages_stealth=%r)') % (
                self.name, self.armor_class, self.armor_type,
                self.min_str_requirement, self.disadvantages_stealth)

    def __str__(self):
        return '<%sArmor: %s (AC %i)>' % (self.armor_type.name.title(),
                                          self.name, self.armor_class)


RangeIncrement = Tuple[int, int]


class WeaponDamageType(enum.Enum):
    PIERCING = 'P'
    SLASHING = 'S'
    BLUDGEONING = 'B'

    def __repr__(self):
        return '%s.%s' % (self.__class__.__name__, self.name)


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
        self.__requires_ammo = None
        self.requires_ammo = bool(requires_ammo)
        self.finesse_weapon = bool(finesse_weapon)
        self.__is_heavy = None
        self.__is_light = None
        self.is_heavy = bool(is_heavy)
        self.is_light = bool(is_light)
        self.slow_loading = bool(slow_loading)
        self.has_reach = bool(has_reach)
        self.__can_be_thrown = None
        self.can_be_thrown = bool(can_be_thrown)
        if self.can_be_thrown:
            self.range_increment = (20, 60)

        self.__requires_two_hands = None
        self.__versatile = None
        self.requires_two_hands = bool(requires_two_hands)
        self.versatile = bool(versatile)
        if self.damage and self.two_handed_damage:
            self.versatile = True
        if self.versatile:
            assert self.two_handed_damage is not None

    @property
    def can_be_thrown(self):
        return bool(self.__can_be_thrown)

    @can_be_thrown.setter
    def can_be_thrown(self, value):
        self.__can_be_thrown = bool(value)
        if self.__can_be_thrown:
            self.__requires_ammo = False

    @property
    def has_range(self) -> bool:
        return self.range_increment is not None

    @property
    def is_heavy(self):
        return bool(self.__is_heavy)

    @is_heavy.setter
    def is_heavy(self, value):
        self.__is_heavy = bool(value)
        if self.__is_heavy:
            self.__is_light = False

    @property
    def is_light(self):
        return bool(self.__is_light)

    @is_light.setter
    def is_light(self, value):
        self.__is_light = bool(value)
        if self.__is_light:
            self.__is_heavy = False

    @property
    def requires_ammo(self):
        return bool(self.__requires_ammo)

    @requires_ammo.setter
    def requires_ammo(self, value):
        self.__requires_ammo = bool(value)
        if self.__requires_ammo:
            self.__can_be_thrown = False

    @property
    def requires_two_hands(self):
        return bool(self.__requires_two_hands)

    @requires_two_hands.setter
    def requires_two_hands(self, value):
        self.__requires_two_hands = bool(value)
        if self.__requires_two_hands:
            self.__versatile = False

    @property
    def versatile(self):
        return bool(self.__versatile)

    @versatile.setter
    def versatile(self, other):
        self.__versatile = bool(other)
        if self.__versatile:
            self.__requires_two_hands = False

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
