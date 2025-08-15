from abc import ABC,abstractmethod
class Character(ABC):


    def __init__(self,hp=100,dmg=15,name="None"):
        self.hp=hp
        self.dmg=dmg
        self.name = name




    def __str__(self):
        return (f"Character name:{self.name} hp:{self.hp} dmg:{self.dmg}")
