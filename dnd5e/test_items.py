from .items import Weapon


def test_weapon_properties():
    club = Weapon('Club', '1d4', is_light=True)
    assert club.properties == ['Light']
    dagger = Weapon('Dagger', '1d4', finesse_weapon=True, is_light=True,
                    can_be_thrown=True, range_increment=(20, 60))
    assert dagger.properties == ['Finesse', 'Light', 'Thrown (range 20/60)']
    greatclub = Weapon('Greatclub', '1d8', requires_two_hands=True)
    assert greatclub.properties == ['Two-handed']
    handaxe = Weapon('Handaxe', '1d6', is_light=True, can_be_thrown=True,
                     range_increment=(20, 60))
    assert handaxe.properties == ['Light', 'Thrown (range 20/60)']
    javelin = Weapon('Javelin', '1d6', can_be_thrown=True,
                     range_increment=(20, 60))
    assert javelin.properties == ['Thrown (range 20/60)']
    mace = Weapon('Mace', '1d6')
    assert mace.properties == []
    quarterstaff = Weapon('Quarterstaff', '1d6', '1d8', versatile=True)
    assert quarterstaff.properties == ['Versatile (1d8)']
    spear = Weapon('Spear', '1d6', '1d8', can_be_thrown=True, versatile=True,
                   range_increment=(20, 60))
    assert spear.properties == ['Thrown (range 20/60)', 'Versatile (1d8)']

    lt_xbow = Weapon('Light crossbow', '1d8', requires_ammo=True,
                     slow_loading=True, requires_two_hands=True,
                     range_increment=(80, 320))
    assert lt_xbow.properties == ['Ammunition (range 80/320)', 'Loading',
                                  'Two-handed']
    dart = Weapon('Dart', '1d4', finesse_weapon=True, can_be_thrown=True,
                  range_increment=(20, 60))
    assert dart.properties == ['Finesse', 'Thrown (range 20/60)']

    glaive = Weapon('Glaive', '1d10', is_heavy=True, has_reach=True,
                    requires_two_hands=True)
    assert glaive.properties == ['Heavy', 'Reach', 'Two-handed']
