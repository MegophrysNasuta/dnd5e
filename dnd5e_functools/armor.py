from .items import Armor, ArmorType


L = ArmorType.LIGHT
M = ArmorType.MEDIUM
H = ArmorType.HEAVY


# Light Armor
padded_armor = Armor('Padded', 11, L, disadvantages_stealth=True)
leather_armor = Armor('Leather', 11, L)
studded_armor = Armor('Studded Leather', 12, L)

# Medium Armor
hide = Armor('Hide', 12, M)
chain_shirt = Armor('Chain shirt', 13, M)
scale_mail = Armor('Scale mail', 14, M, disadvantages_stealth=True)
breastplate = Armor('Breastplate', 14, M)
half_plate = Armor('Half plate', 15, M, disadvantages_stealth=True)

# Heavy armor
ring_mail = Armor('Ring mail', 14, H)
chain_mail = Armor('Chain mail', 16, H, min_str_requirement=13)
splint_mail = Armor('Splint mail', 17, H, min_str_requirement=15)
plate_mail = Armor('Plate mail', 18, H, min_str_requirement=15)
