from typing import Optional, Tuple


class CharacterStat:
    def __init__(self, name: str, base_value: Optional[int]=10,
                 bonus: Optional[int]=0):
        self.__fullname = str(name)
        self.base_value = base_value and int(base_value)
        self.bonus = bonus and int(bonus)

    @property
    def full_name(self) -> str:
        return self.__fullname.title()

    @property
    def abbr(self) -> str:
        return self.__fullname[:3].upper()

    @property
    def modifier(self) -> int:
        return int((self.value - 10) / 2)

    @property
    def value(self) -> int:
        return self.base_value + self.bonus

    def __add__(self, value):
        self.bonus = int(value)
        return self

    def __repr__(self):
        repr_line = '<CharacterStat: %s (%s) [%i (Mod %+i; Bonus %+i)]>'
        return repr_line % (self.full_name, self.abbr, self.value,
                            self.modifier, self.bonus)

CharacterStats = Tuple[Optional[CharacterStat], Optional[CharacterStat],
                       Optional[CharacterStat], Optional[CharacterStat],
                       Optional[CharacterStat], Optional[CharacterStat]]


class Character:
    def __init__(self, name: Optional[str]=None,
                 race: Optional[str]=None,
                 class_: Optional[str]=None,
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
        self.STR = CharacterStat('Strength', str_score, str_bonus)
        self.DEX = CharacterStat('Dexterity', dex_score, dex_bonus)
        self.CON = CharacterStat('Constitution', con_score, con_bonus)
        self.INT = CharacterStat('Intelligence', int_score, int_bonus)
        self.WIS = CharacterStat('Wisdom', wis_score, wis_bonus)
        self.CHA = CharacterStat('Charisma', cha_score, cha_bonus)

    @property
    def stats(self) -> CharacterStats:
        return self.STR, self.DEX, self.CON, self.INT, self.WIS, self.CHA

    def __repr__(self):
        return '<Character: %s, %s %s %s>' % (self.name, self.race,
                                              self.class_, self.stats)
