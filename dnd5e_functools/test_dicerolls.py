import operator
import pytest

from dnd5e_functools import roll, reroll_if
from dnd5e_functools.dicerolls import parse_condition


def test_roll():
    results = tuple(map(int, roll('1d1')))
    assert len(results) == 1
    assert results[0] == 1

    result = tuple(roll('1d1'))[0]
    assert result.result == 1
    assert result.die_max_value == 1

    with pytest.raises(AttributeError):
        result.result = 2

    with pytest.raises(AttributeError):
        result.die_max_value = 2

    results = tuple(map(int, roll('2d6')))
    assert len(results) == 2
    assert all(1 <= x <= 6 for x in results)

    results = tuple(map(int, roll('3d5')))
    assert len(results) == 3
    assert all(1 <= x <= 5 for x in results)

    results = tuple(map(int, roll('4d20')))
    assert len(results) == 4
    assert all(1 <= x <= 20 for x in results)

    results = tuple(map(int, roll('0d0')))
    assert len(results) == 0

    with pytest.raises(ValueError):
        list(roll(None))

    with pytest.raises(ValueError):
        list(roll(1))


def test_reroll():
    results = tuple(reroll_if(roll('4d6'), 'x<2'))
    assert len(results) == 4

    r1, r2, r3 = roll('3d1')
    r1_, r2_, r3_ = reroll_if((r1, r2, r3), 'x>1')
    assert r1 is r1_
    assert r2 is r2_
    assert r3 is r3_

    r1_, r2_, r3_ = reroll_if((r1, r2, r3), 'x==1')
    assert r1 is not r1_
    assert r2 is not r2_
    assert r3 is not r3_

    r1_, r2_, r3_ = reroll_if((r1, r2, r3), ('x>0', 'x==3'))
    assert r1 is not r1_
    assert r2 is not r2_
    assert r3 is not r3_

    r1_, r2_, r3_ = reroll_if((r1, r2, r3), ('x<0', 'x==3'))
    assert r1 is r1_
    assert r2 is r2_
    assert r3 is r3_


def test_parse_condition():
    op, val = parse_condition('x < 1')
    assert op == operator.lt
    assert val == 1

    op, val = parse_condition('x > 1')
    assert op == operator.gt
    assert val == 1

    op, val = parse_condition('x <= 1')
    assert op == operator.le
    assert val == 1

    op, val = parse_condition('x >= 1')
    assert op == operator.ge
    assert val == 1

    op, val = parse_condition('x == 1')
    assert op == operator.eq
    assert val == 1

    op, val = parse_condition('x != 1')
    assert op == operator.ne
    assert val == 1

    op, val = parse_condition('x<1')
    assert op == operator.lt
    assert val == 1

    op, val = parse_condition('x>1')
    assert op == operator.gt
    assert val == 1

    op, val = parse_condition('x<=1')
    assert op == operator.le
    assert val == 1

    op, val = parse_condition('x>=1')
    assert op == operator.ge
    assert val == 1

    op, val = parse_condition('x==1')
    assert op == operator.eq
    assert val == 1

    op, val = parse_condition('x!=1')
    assert op == operator.ne
    assert val == 1

    op, val = parse_condition('x < 16')
    assert op == operator.lt
    assert val == 16

    op, val = parse_condition('x > 16')
    assert op == operator.gt
    assert val == 16

    op, val = parse_condition('x <= 16')
    assert op == operator.le
    assert val == 16

    op, val = parse_condition('x >= 16')
    assert op == operator.ge
    assert val == 16

    op, val = parse_condition('x == 16')
    assert op == operator.eq
    assert val == 16

    op, val = parse_condition('x != 16')
    assert op == operator.ne
    assert val == 16

    op, val = parse_condition('x<16')
    assert op == operator.lt
    assert val == 16

    op, val = parse_condition('x>16')
    assert op == operator.gt
    assert val == 16

    op, val = parse_condition('x<=16')
    assert op == operator.le
    assert val == 16

    op, val = parse_condition('x>=16')
    assert op == operator.ge
    assert val == 16

    op, val = parse_condition('x==16')
    assert op == operator.eq
    assert val == 16

    op, val = parse_condition('x!=16')
    assert op == operator.ne
    assert val == 16

    op, val = parse_condition('1 < x')
    assert op == operator.gt
    assert val == 1

    op, val = parse_condition('1 > x')
    assert op == operator.lt
    assert val == 1

    op, val = parse_condition('1 <= x')
    assert op == operator.ge
    assert val == 1

    op, val = parse_condition('1 >= x')
    assert op == operator.le
    assert val == 1

    op, val = parse_condition('1 == x')
    assert op == operator.eq
    assert val == 1

    op, val = parse_condition('1 != x')
    assert op == operator.ne
    assert val == 1

    op, val = parse_condition('1<x')
    assert op == operator.gt
    assert val == 1

    op, val = parse_condition('1>x')
    assert op == operator.lt
    assert val == 1

    op, val = parse_condition('1<=x')
    assert op == operator.ge
    assert val == 1

    op, val = parse_condition('1>=x')
    assert op == operator.le
    assert val == 1

    op, val = parse_condition('1==x')
    assert op == operator.eq
    assert val == 1

    op, val = parse_condition('1!=x')
    assert op == operator.ne
    assert val == 1

    op, val = parse_condition('16 < x')
    assert op == operator.gt
    assert val == 16

    op, val = parse_condition('16 > x')
    assert op == operator.lt
    assert val == 16

    op, val = parse_condition('16 <= x')
    assert op == operator.ge
    assert val == 16

    op, val = parse_condition('16 >= x')
    assert op == operator.le
    assert val == 16

    op, val = parse_condition('16 == x')
    assert op == operator.eq
    assert val == 16

    op, val = parse_condition('16 != x')
    assert op == operator.ne
    assert val == 16

    op, val = parse_condition('16<x')
    assert op == operator.gt
    assert val == 16

    op, val = parse_condition('16>x')
    assert op == operator.lt
    assert val == 16

    op, val = parse_condition('16<=x')
    assert op == operator.ge
    assert val == 16

    op, val = parse_condition('16>=x')
    assert op == operator.le
    assert val == 16

    op, val = parse_condition('16==x')
    assert op == operator.eq
    assert val == 16

    op, val = parse_condition('16!=x')
    assert op == operator.ne
    assert val == 16

    with pytest.raises(ValueError):
        parse_condition('x * 1')

    with pytest.raises(ValueError):
        parse_condition('x + y')
