from mage_turn import *
from main import *

def use_spell(character):

    if character == "mage":
        spell = input("\nChose spell to use:\n1 - dash back\n2 - deal dmg (25 if dist >= 55, else 15)")
        if spell == "1":
            r = MAGE.spell1()

        elif spell == "2":
            r = MAGE.spell2()
            ##################################################################
        else:
            r = ARCHER.spell2()
    elif character == "archer":
        spell = input("\nChose spell to use:\n1 - dash forword (7 blocks, 10 stamina cost) \n2 - deal dmg (25 if dist <= 55, else 15) ")
        if spell == "1":
            r = ARCHER.spell1()

        elif spell == "2":
            r = ARCHER.spell2()
            ##################################################################
        else:
            r = ARCHER.spell2()

    else:
        pass
