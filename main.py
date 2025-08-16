from abc import ABC,abstractmethod
from character import *
from use_spell import *
from archer import *
from mage import *
from archer_turn import *
from mage_turn import *

# in each round character
distance=50

MAGE = Mage()
print(MAGE)

ARCHER = Archer()
print(ARCHER)

i =1
while True:
    print(f"{'-'*15} ROUND {i} {'-'*15}")


    if i%2==0:
        whose_turn = "mage"
    else:
        whose_turn = "archer"

    if whose_turn == "mage":
        use_spell("mage")
    else:
        use_spell("archer")
    x= MAGE.check_if_alive()
    y = ARCHER.check_if_alive()

    if x==0 or y==0:
        break