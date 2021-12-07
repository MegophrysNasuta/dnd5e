import operator
import random
import re
from typing import Callable, Generator, Iterable, Tuple, Union


class DieResult:
    """
    Stores a max_die_value (e.g. 6 for a 6-sided die) and result, making them
    resistant to rewrites once set.
    """

    def __init__(self, die_max_value, result=None):
        self.__die_max_value = int(die_max_value)
        self.__result =  None
        if result is not None:
            self.result = result

    def reroll(self):
        return self.__class__(result=random.randint(1, self.die_max_value),
                              die_max_value=self.die_max_value)

    @property
    def die_max_value(self):
        return self.__die_max_value

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, x):
        if self.__result is None:
            self.__result = int(x)
        else:
            raise AttributeError("can't set attribute")

    def __float__(self):
        return float(self.result)

    def __int__(self):
        return int(self.result)

    def __add__(self, value):
        return int(self) + int(value)

    def __radd__(self, value):
        return self.__add__(value)

    def __eq__(self, value):
        return int(self) == float(value)

    def __ge__(self, value):
        return int(self) >= float(value)

    def __gt__(self, value):
        return int(self) > float(value)

    def __le__(self, value):
        return int(self) <= float(value)

    def __lt__(self, value):
        return int(self) < float(value)

    def __ne__(self, value):
        return int(self) != float(value)

    def __repr__(self):
        if self.result:
            return '<DieResult: %i (d%i)>' % (self.result, self.die_max_value)
        else:
            return '<DieResult: Undecided>'

DieResultSet = Union[Iterable[DieResult],Generator[DieResult, None, None]]


class DiceResult:
    """Summed iterable of DieResults"""

    def __init__(self, *results: DieResultSet):
        self.rolls = tuple(results)
        self.modifier = 0

    @property
    def total(self):
        return sum(map(int, self.rolls)) + self.modifier

    @property
    def int_results(self):
        return map(int, self.rolls)

    @property
    def str_results(self):
        return map(str, self.int_results)

    def __add__(self, value):
        self.modifier = int(value)
        return self

    def __sub__(self, value):
        self.modifier = -int(value)
        return self

    def __repr__(self):
        rolls = ', '.join(self.str_results)
        return '<DiceResult: %i (Rolled %s; Mod %+i)>' % (self.total,
                                                          rolls,
                                                          self.modifier)


def roll_dice(mDn: str,
              rerolling_if: Iterable[str]=None,
              dropping_lowest: bool=False) -> DiceResult:
    """
    Syntactic sugar for roll with other functions as options.

    roll_dice('4d6', rerolling_if=('x==1',))
    is equivalent to
    reroll_if(roll('4d6'), ('x==1',))

    roll_dice('4d6', rerolling_if='x==1', dropping_lowest=True)
    is equivalent to
    drop_lowest(reroll_if(roll('4d6'), 'x==1'))
    """
    rolls = roll(mDn)
    if rerolling_if:
        rolls = reroll_if(rolls, rerolling_if)
    if dropping_lowest:
        rolls = drop_lowest(rolls)

    return DiceResult(*rolls)


def roll(mDn: str) -> DieResultSet:
    """
    Roll mDn, a standard dice signifier like '3d6' (m=3, n=6)

    Returns a DieResult, like <DieResult: 4 (d6)>

    Raises ValueError or TypeError on improper mDn formatting.
    """
    if not mDn:
        raise ValueError('Must specify a die roll like "3d6"')

    m, n = map(int, str(mDn).split('d', 1))
    for die_roll in range(m):
        yield DieResult(die_max_value=n, result=random.randint(1, n))


def parse_condition(condition: str) -> Tuple[Callable[[int, int], bool], int]:
    """
    Parse a string representing a comparison like 'x < 1', returning
    a function representing the operation, and the int value 1,
    in the example case.

    If a string like '1 > x' is used, it will be converted to 'x < 1' first.
    """
    condition_regex = re.compile(r'^(x|\d+) ?(<|>|<=|>=|==|!=) ?(x|\d+)')
    matches = condition_regex.match(str(condition))
    if not matches:
        raise ValueError('Unrecognized condition string')

    if matches[1] == 'x':
        op, val = matches[2], int(matches[3])
    else:
        op, val = matches[2], int(matches[1])

    op_dict = {
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,
        '>=': operator.ge,
        '>': operator.gt,
    }

    opposite_op = {'<': '>', '<=': '>=', '==': '==',
                   '>': '<', '>=': '<=', '!=': '!=',}

    try:
        if matches[1] == 'x':
            real_op = op_dict[op]
        else:
            real_op = op_dict[opposite_op[op]]
    except KeyError:
        raise ValueError('Unrecognized operation "%s"' % op)

    return real_op, val


def reroll_if(rolls: DieResultSet,
              conditions: Union[str, Iterable[str]]) -> DieResultSet:
    if isinstance(conditions, str):
        conditions = (conditions,)

    for roll in rolls:
        if any(op(roll.result, val) for op, val in map(parse_condition, conditions)):
            yield roll.reroll()
        else:
            yield roll


def drop_lowest(rolls: DieResultSet) -> DieResultSet:
    result = list(rolls)
    result.remove(min(result))
    return result
