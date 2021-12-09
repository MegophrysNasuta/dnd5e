from .items import SimpleWeapon, MartialWeapon, WeaponDamageType

P = WeaponDamageType.PIERCING
S = WeaponDamageType.SLASHING
B = WeaponDamageType.BLUDGEONING

# Simple Melee
club = SimpleWeapon('Club', '1d4', None, B, is_light=True)
dagger = SimpleWeapon('Dagger', '1d4', None, P, finesse_weapon=True,
                      is_light=True, can_be_thrown=True)
greatclub = SimpleWeapon('Greatclub', '1d8', None, B, requires_two_hands=True)
handaxe = SimpleWeapon('Handaxe', '1d6', None, S, is_light=True,
                       can_be_thrown=True)
javelin = SimpleWeapon('Javelin', '1d6', None, P, can_be_thrown=True,
                       range_increment=(30, 120))
lt_hammer = SimpleWeapon('Light hammer', '1d4', None, B, is_light=True,
                         can_be_thrown=True)
mace = SimpleWeapon('Mace', '1d6', None, B)
quarterstaff = SimpleWeapon('Quarterstaff', '1d6', '1d8', B, versatile=True)
sickle = SimpleWeapon('Sickle', '1d4', None, S, is_light=True)
spear = SimpleWeapon('Spear', '1d6', '1d8', P, can_be_thrown=True,
                     versatile=True)

# Simple Ranged
lt_xbow = SimpleWeapon('Light crossbow', '1d8', None, P, requires_ammo=True,
                       slow_loading=True, requires_two_hands=True,
                       range_increment=(80, 320))
dart = SimpleWeapon('Dart', '1d4', None, P, finesse_weapon=True,
                    can_be_thrown=True)
shortbow = SimpleWeapon('Shortbow', '1d6', None, P, requires_ammo=True,
                        requires_two_hands=True, range_increment=(80, 320))
sling = SimpleWeapon('Sling', '1d4', None, B, requires_ammo=True,
                     range_increment=(80, 320))

# Martial Melee
battleaxe = MartialWeapon('Battleaxe', '1d8', '1d10', S, versatile=True)
flail = MartialWeapon('Flail', '1d8', None, B)
glaive = MartialWeapon('Glaive', '1d10', None, S, is_heavy=True, has_reach=True,
                       requires_two_hands=True)
greataxe = MartialWeapon('Greataxe', '1d12', None, S, is_heavy=True,
                         requires_two_hands=True)
greatsword = MartialWeapon('Greatsword', '2d6', None, S, is_heavy=True,
                           requires_two_hands=True)
halberd = MartialWeapon('Halberd', '1d10', None, S, is_heavy=True, has_reach=True,
                        requires_two_hands=True)
lance = MartialWeapon('Lance', '1d12', None, P, has_reach=True)
longsword = MartialWeapon('Longsword', '1d8', '1d10', S, versatile=True)
maul = MartialWeapon('Maul', '2d6', None, B, is_heavy=True, requires_two_hands=True)
morningstar = MartialWeapon('Morningstar', '1d8', None, P)
pike = MartialWeapon('Pike', '1d10', None, P, is_heavy=True, has_reach=True,
                     requires_two_hands=True)
rapier = MartialWeapon('Rapier', '1d8', None, P, finesse_weapon=True)
scimitar = MartialWeapon('Scimitar', '1d6', None, S, finesse_weapon=True,
                         is_light=True)
shortsword = MartialWeapon('Shortsword', '1d6', None, P, finesse_weapon=True,
                           is_light=True)
trident = MartialWeapon('Trident', '1d6', '1d8', P, can_be_thrown=True,
                        versatile=True)
war_pick = MartialWeapon('War pick', '1d8', None, P)
warhammer = MartialWeapon('Warhammer', '1d8', '1d10', B, versatile=True)
whip = MartialWeapon('Whip', '1d4', None, P, finesse_weapon=True, has_reach=True)

# Martial Ranged
blowgun = MartialWeapon('Blowgun', '1d1', None, P, requires_ammo=True,
                        slow_loading=True, range_increment=(25, 100))
hand_xbow = MartialWeapon('Hand crossbow', '1d6', None, P, requires_ammo=True,
                          slow_loading=True, is_light=True,
                          range_increment=(30, 120))
heavy_xbow = MartialWeapon('Heavy crossbow', '1d10', None, P, requires_ammo=True,
                           is_heavy=True, slow_loading=True,
                           requires_two_hands=True, range_increment=(100, 400))
longbow = MartialWeapon('Longbow', '1d8', None, P, requires_ammo=True,
                        requires_two_hands=True, range_increment=(150, 600),
                        is_heavy=True)
net = MartialWeapon('Net', None, None, None, can_be_thrown=True,
                    range_increment=(5, 15))
