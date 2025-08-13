from character import Character

class Archer(Character):

    def __init__(self,hp=100,dmg=15,name="ARCHER",distance=50,stamina=50):
        Character.__init__(self,hp,dmg,name,distance)
        self.stamina = stamina


    def __str__(self):
        return Character.__str__(self)+ f" stamina: {self.stamina}"

    def spell1(self):
        if self.stamina >= 10:
            self.distance -= 7
            return 1
        else:
            return 0

    def spell2(self):
        if self.distance <= 55:
            return 1  # deals more dmg
        else:
            return 0  # deals basic dmg

    def get_dmg(self, damage):
        self.hp -= damage

    def check_if_alive(self):
        if self.hp <= 0:
            print(f"{self.name} LOST!")
            return 0
        else:
            print(f"{self.name} HP: {self.hp}")
            return 1