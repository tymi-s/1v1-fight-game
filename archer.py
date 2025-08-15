from character import Character
from main import distance
class Archer(Character):

    def __init__(self,hp=100,dmg=15,name="ARCHER",stamina=50):
        Character.__init__(self,hp,dmg,name)
        self.stamina = stamina


    def __str__(self):
        return Character.__str__(self)+ f" stamina: {self.stamina}"

    def spell1(self):
        if self.stamina >= 10:
            distance -= 7
            return 1
        else:
            return 0

    def spell2(self):
        if distance <= 55:
            return 15  # deals more dmg
        else:
            return 25  # deals basic dmg

    def get_dmg(self, damage):
        self.hp -= damage

    def check_if_alive(self):
        if self.hp <= 0:
            print(f"{self.name} LOST!")
            return 0
        else:
            print(f"{self.name} HP: {self.hp}")
            return 1