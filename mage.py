from character import Character
import main

class Mage(Character):

    def __init__(self, hp=100, dmg=15, name="MAGE", mana=50):
        Character.__init__(self,hp,dmg,name,)
        self.mana = mana

    def __str__(self):
        return super().__str__() + f", Mana: {self.mana}"

    def spell1(self):
        if self.mana >=10:
            main.distance +=7
            return 1
        else:
            return 0


    def spell2(self):
        if main.distance >=55:
            return 25 #deals more dmg
        else:
            return 15 #deals basic dmg


    def get_dmg(self,damage):
        self.hp -= damage

    def check_if_alive(self):
        if self.hp <= 0:
            print(f"{self.name} LOST!")
            return 0
        else:
            print(f"{self.name} HP: {self.hp}")
            return 1


