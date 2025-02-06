class Player:
    def __init__(self, name, level, hp):
        self.name = name
        self.level = level
        self.hp = hp
        self.weapon = None
        self.armor = None
        self.guild = None
        self.damage = 1
        self.defence = 1
    def equip_weapon(self, weapon):
        self.weapon = weapon
        self.damage += self.weapon.damage
        
    def equip_armor(self, armor):
        self.armor = armor
        self.defence += self.armor.defense

    def display_stats(self):
        print(f"=== Player: {self.name} ===")
        print(f"Level: {self.level}")
        print(f"hp: {self.hp}")
        if self.weapon:
            print(f"Weapon: {self.weapon.name_weapon} (Damage: {self.weapon.damage})")
        if self.armor:
            print(f"Armor: {self.armor.name_armor} (Defense: {self.armor.defense})")
            
class Weapon:
    def __init__(self, name_weapon, damage):
        self.name_weapon = name_weapon
        self.damage = damage
        self.description = f"{self.name_weapon} (Damage: {self.damage}"

class Armor:
    def __init__(self, name_armor, defense):
        self.name_armor = name_armor
        self.defense = defense
        
class Guild :
    def __init__(self, name_guild):
        self.name_guild = name_guild
        self.leader = None
        self.members = []

    def display_member(self):
        print(f"Guild: {self.name_guild}, Leader: {self.leader.name}")
        print(f"Members: {[member.name for member in self.members]}")
        
    def add_member(self, player):
        if player not in self.members:
            self.members.append(player)
            if self.leader == None:
                self.leader = player
                
# Example usage:
woodSword = Weapon("Wood Sword", 5)
stoneSword = Weapon("Stone Sword", 10)
ironSword = Weapon("Iron Sword", 20)
diamondSword = Weapon("Diamond Sword", 30)
leatherArmor = Armor("Leather Armor", 5)
goldArmor = Armor("Gold Armor", 10)
ironArmor = Armor("Iron Armor", 20)
diamondArmor = Armor("Diamond Armor", 30)
guild1 = Guild("LoveFromMyMother555")
player1 = Player("Noob_palm", 5, 100)
player1.equip_weapon(ironSword)
player1.equip_armor(leatherArmor)
player1.display_stats()
player2 = Player("TopLukmaeTan", 10, 150)
player2.equip_weapon(diamondSword)
player2.equip_armor(ironArmor)
player2.display_stats()
guild1.add_member(player1)
guild1.add_member(player2)
guild1.display_member()
