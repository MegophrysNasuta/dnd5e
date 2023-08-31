from .items import SimpleWeapon, MartialWeapon, WeaponDamageType

P = WeaponDamageType.PIERCING
S = WeaponDamageType.SLASHING
B = WeaponDamageType.BLUDGEONING

# Simple Melee
club = SimpleWeapon('Club', '1d4', None, B, is_light=True)
throwing_knife = SimpleWeapon('Throwing Knife', '1d4', None, P, finesse_weapon=True,
                              is_light=True, can_be_thrown=True)
throwing_axe = SimpleWeapon('Throwing Axe', '1d4', None, P,
                            is_light=True, can_be_thrown=True)
parrying_dagger = SimpleWeapon('Parrying Dagger', '1d6', None, P, is_light=True)
axe = SimpleWeapon('Axe', '1d6', None, P, is_light=True)
dirk = SimpleWeapon('Dirk', '1d6', None, P, is_light=True)
hammer = SimpleWeapon('Hammer', '1d6', None, P, is_light=True)
javelin = SimpleWeapon('Javelin', '1d6', None, P, can_be_thrown=True,
                       range_increment=(30, 120))
rondel = SimpleWeapon('Rondel', '1d6', '1d8', P, versatile=True, is_light=True)
spear = SimpleWeapon('Spear', '1d6', '1d8', P, versatile=True)
lance = SimpleWeapon('Lance', '1d6', '1d8', P, versatile=True)
mace = SimpleWeapon('Mace', '1d6', '1d8', B, versatile=True)
flail = SimpleWeapon('Flail', '1d6', '1d8', B, versatile=True)
quarterstaff = SimpleWeapon('Quarterstaff', '1d6', '1d8', B, versatile=True)
shortsword = SimpleWeapon('Shortsword', '1d6', '1d8', S, finesse_weapon=True,
                          is_light=True, versatile=True)
scimitar = SimpleWeapon('Scimitar', '1d6', '1d8', S, finesse_weapon=True,
                        is_light=True, versatile=True)
khopesh = SimpleWeapon('Khopesh', '1d6', '1d8', S, finesse_weapon=True,
                       is_light=True, versatile=True)

# Simple Ranged
war_dart = SimpleWeapon('War Dart', '1d6', None, P, can_be_thrown=True,
                        range_increment=(30, 120))
shortbow = SimpleWeapon('Shortbow', '1d6', None, P, requires_ammo=True,
                        requires_two_hands=True, range_increment=(80, 320))
longbow = SimpleWeapon('Longbow', '1d8', None, P, requires_ammo=True,
                       requires_two_hands=True, range_increment=(150, 600),
                       is_heavy=True)
sling = SimpleWeapon('Sling', '1d4', None, B, requires_ammo=True,
                     range_increment=(80, 320))

# Martial Melee
arming_sword = MartialWeapon('Arming Sword', '1d8', None, S)
battleaxe = MartialWeapon('Battleaxe', '1d8', '1d10', S, versatile=True)
longsword = MartialWeapon('Longsword', '1d8', '1d10', S, versatile=True)
warhammer = MartialWeapon('Warhammer', '1d8', '1d10', B, versatile=True)
polearm = MartialWeapon('Polearm', '1d12', None, P, is_heavy=True, has_reach=True,
                        requires_two_hands=True)
glaive = MartialWeapon('Glaive', '1d12', None, P, is_heavy=True, has_reach=True,
                       requires_two_hands=True)
halberd = MartialWeapon('Halberd', '1d12', None, P, is_heavy=True, has_reach=True,
                        requires_two_hands=True)
poleaxe = MartialWeapon('Poleaxe', '1d12', None, P, is_heavy=True, has_reach=True,
                        requires_two_hands=True)
bec_de_corbin = MartialWeapon('Bec de Corbin', '1d12', None, P, is_heavy=True,
                              has_reach=True, requires_two_hands=True)
greatsword = MartialWeapon('Greatsword', '1d12', None, P, is_heavy=True,
                           has_reach=True, requires_two_hands=True)
pike = MartialWeapon('Pike', '2d6', None, P, is_heavy=True, has_reach=True,
                     requires_two_hands=True)
horsemans_lance = MartialWeapon("Horseman's Lance", '2d6', None, P, is_heavy=True,
                                has_reach=True, requires_two_hands=True)
rapier = MartialWeapon('Rapier', '1d8', None, P, finesse_weapon=True)
saber = MartialWeapon('Saber', '1d8', None, S, finesse_weapon=True)
smallsword = MartialWeapon('Smallsword', '1d8', None, S, finesse_weapon=True)

# Martial Ranged
lt_xbow = MartialWeapon('Light crossbow', '1d8', None, P, requires_ammo=True,
                        slow_loading=True, requires_two_hands=True,
                        range_increment=(80, 320))
heavy_xbow = MartialWeapon('Heavy crossbow', '1d10', None, P,
                           is_heavy=True, slow_loading=True,
                           requires_ammo=True,
                           requires_two_hands=True, range_increment=(100, 400))
pistol = MartialWeapon('Pistol', '1d10', None, P, is_light=True, slow_loading=True,
                       requires_ammo=True, range_increment=(60, 120))
carbine = MartialWeapon('Carbine', '1d12', None, P, slow_loading=True,
                        requires_two_hands=True, is_heavy=True,
                        requires_ammo=True, range_increment=(100, 240))
musket = MartialWeapon('Musket', '1d12', None, P, slow_loading=True,
                       requires_two_hands=True, is_heavy=True,
                       requires_ammo=True, range_increment=(100, 180))
rifle = MartialWeapon('Rifle', '2d8', None, P, slow_loading=True,
                      requires_two_hands=True, is_heavy=True,
                      requires_ammo=True, range_increment=(100, 240))
