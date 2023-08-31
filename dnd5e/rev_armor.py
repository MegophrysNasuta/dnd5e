from .items import Armor, ArmorType


L = ArmorType.LIGHT
M = ArmorType.MEDIUM
H = ArmorType.HEAVY


# Light Armor
padded_armor = Armor('Padded', 11, L)
leather_armor = Armor('Leather', 11, L)
hardened_leather_armor = Armor('Hardened Leather Armor', 12, L)

# Medium Armor (best layer)
mail_hauberk = Armor('Mail hauberk', 13, M)
scale_mail = Armor('Scale mail', 14, M, disadvantages_stealth=True)
breastplate = Armor('Breastplate', 14, M)
brigandine = Armor('Brigandine', 14, M)
chest_and_limb_plates = Armor('Chest and limb plates', 15, M,
                              disadvantages_stealth=True)

# Heavy armor
transitional_plate = Armor('Transitional Plate (starter quality)', 16, H,
                           min_str_requirement=13)
plate_armor = Armor('Plate (better quality)', 17, H, min_str_requirement=15)
fullplate = Armor('Full Plate (best quality)', 18, H, min_str_requirement=15)
