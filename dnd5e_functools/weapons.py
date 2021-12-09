from .items import Weapon, WeaponDamageType

P = WeaponDamageType.PIERCING
S = WeaponDamageType.SLASHING
B = WeaponDamageType.BLUDGEONING

# Simple Melee
club = Weapon('Club', '1d4', None, B, is_light=True, is_simple=True)
dagger = Weapon('Dagger', '1d4', None, P, finesse_weapon=True, is_light=True,
                can_be_thrown=True, is_simple=True)
greatclub = Weapon('Greatclub', '1d8', None, B, requires_two_hands=True,
                   is_simple=True)
handaxe = Weapon('Handaxe', '1d6', None, S, is_light=True, can_be_thrown=True,
                 is_simple=True)
javelin = Weapon('Javelin', '1d6', None, P, can_be_thrown=True,
                 range_increment=(30, 120), is_simple=True)
lt_hammer = Weapon('Light hammer', '1d4', None, B, is_light=True,
                   can_be_thrown=True, is_simple=True)
mace = Weapon('Mace', '1d6', None, B, is_simple=True)
quarterstaff = Weapon('Quarterstaff', '1d6', '1d8', B, versatile=True,
                      is_simple=True)
sickle = Weapon('Sickle', '1d4', None, S, is_light=True, is_simple=True)
spear = Weapon('Spear', '1d6', '1d8', P, can_be_thrown=True, versatile=True,
               is_simple=True)

# Simple Ranged
lt_xbow = Weapon('Light crossbow', '1d8', None, P, requires_ammo=True,
                 slow_loading=True, requires_two_hands=True, is_simple=True,
                 range_increment=(80, 320))
dart = Weapon('Dart', '1d4', None, P, finesse_weapon=True, can_be_thrown=True,
              is_simple=True)
shortbow = Weapon('Shortbow', '1d6', None, P, requires_ammo=True, is_simple=True,
                  requires_two_hands=True, range_increment=(80, 320))
sling = Weapon('Sling', '1d4', None, B, requires_ammo=True,
               range_increment=(80, 320), is_simple=True)

# Martial Melee
battleaxe = Weapon('Battleaxe', '1d8', '1d10', S, versatile=True)
flail = Weapon('Flail', '1d8', None, B)
glaive = Weapon('Glaive', '1d10', None, S, is_heavy=True, has_reach=True,
                requires_two_hands=True)
greataxe = Weapon('Greataxe', '1d12', None, S, is_heavy=True,
                  requires_two_hands=True)
greatsword = Weapon('Greatsword', '2d6', None, S, is_heavy=True,
                    requires_two_hands=True)
halberd = Weapon('Halberd', '1d10', None, S, is_heavy=True, has_reach=True,
                 requires_two_hands=True)
lance = Weapon('Lance', '1d12', None, P, has_reach=True)
longsword = Weapon('Longsword', '1d8', '1d10', S, versatile=True)
maul = Weapon('Maul', '2d6', None, B, is_heavy=True, requires_two_hands=True)
morningstar = Weapon('Morningstar', '1d8', None, P)
pike = Weapon('Pike', '1d10', None, P, is_heavy=True, has_reach=True,
              requires_two_hands=True)
rapier = Weapon('Rapier', '1d8', None, P, finesse_weapon=True)
scimitar = Weapon('Scimitar', '1d6', None, S, finesse_weapon=True,
                  is_light=True)
shortsword = Weapon('Shortsword', '1d6', None, P, finesse_weapon=True,
                    is_light=True)
trident = Weapon('Trident', '1d6', '1d8', P, can_be_thrown=True, versatile=True)
war_pick = Weapon('War pick', '1d8', None, P)
warhammer = Weapon('Warhammer', '1d8', '1d10', B, versatile=True)
whip = Weapon('Whip', '1d4', None, P, finesse_weapon=True, has_reach=True)

# Martial Ranged
blowgun = Weapon('Blowgun', '1d1', None, P, requires_ammo=True,
                 slow_loading=True, range_increment=(25, 100))
hand_xbow = Weapon('Hand crossbow', '1d6', None, P, requires_ammo=True,
                   slow_loading=True, is_light=True, range_increment=(30, 120))
heavy_xbow = Weapon('Heavy crossbow', '1d10', None, P, requires_ammo=True,
                    is_heavy=True, slow_loading=True, requires_two_hands=True,
                    range_increment=(100, 400))
longbow = Weapon('Longbow', '1d8', None, P, requires_ammo=True, is_heavy=True,
                 requires_two_hands=True, range_increment=(150, 600))
net = Weapon('Net', None, None, None, can_be_thrown=True,
             range_increment=(5, 15))
