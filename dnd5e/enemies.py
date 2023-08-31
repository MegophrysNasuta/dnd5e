from . import Character, roll_dice


kobold = Character(str_score=7, dex_score=15, con_score=9,
                   int_score=8, wis_score=7, cha_score=8,
                   hit_dice=roll_dice('2d6') - 2, level=2)
