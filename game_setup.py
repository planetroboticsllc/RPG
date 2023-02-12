from classes.game import Person
from classes.magic import spell
from classes.inventory import Item


# # black magic
# fire = spell('Fire', 10, 50, 'black')
# thunder = spell('Thunder', 15, 80, 'black')
# blizzard = spell('Blizzard', 20, 100, 'black')
# meteor = spell('Meteor', 15, 90, 'black')
# quake = spell('Earth Quake', 20, 120, 'black')
#
# # white magic
# cure = spell('Cure', -12, 100, 'white')
# cura = spell('Cura', -20, 150, 'white')
#
# # Create some items
# potion = Item('Potion', 'potion', 'Heals 50 HP', 50)
# hipotion = Item('Hi-Potion', 'potion', 'Heals 100 HP', 100)
# superpotion = Item('Super-Potion', 'potion', 'Heals 300 HP', 300)
# elixer = Item('Elixer', 'elixer', 'Fully restores HP/MP of 1 character', 999999)
# hielixer = Item('Mega-Elixer', 'elixer', 'Fully restores HP/MP of all characters of the party', 99999)
#
# grenede = Item('Granade', 'attack', 'Deals 500 damage', 500)
#
# # player magic and items
# player_magic = [fire, thunder, blizzard, meteor, cure, cura]
# player_items = [potion, potion, potion, potion, hipotion, hipotion, superpotion, elixer, grenede]
#
# # enemy magic
# enemy_magic = [fire, thunder, blizzard, meteor, quake]
#
# # instantiate people
# # player = Person(460, 65, 60, 20, player_magic, player_items)
# # enemy = Person(1200, 75, 70, 35, enemy_magic, [])

def loadGameSetup(data):
    players = []
    enemies = []
    spells = {}
    for sp in data["spells"]:
        spells[sp["name"]] = sp

    items = {}
    for it in data["items"]:
        items[it["name"]] = it

    for p in data["players"]:
        player_magic = []
        player_items = []
        mg = p["magic"]
        for m in mg:
            magic = spells[m]
            sp = spell(magic["name"], magic["cost"], magic["damage"], magic["type"])
            player_magic.append(sp)

        it = p["items"]
        it_set = set(it)
        for i in it_set:
            ii = items[i]
            item = Item(ii["name"], ii["type"], ii["desc"], ii["prop"])
            for n in range(it.count(i)):
                player_items.append(item)

        players.append(Person(p["hp"], p["mp"], p["attack"], p["defence"], player_magic, player_items))

    for p in data["enemies"]:
        enemy_magic = []
        enemy_items = []
        mg = p["magic"]
        for m in mg:
            magic = spells[m]
            enemy_magic.append(spell(magic["name"], magic["cost"], magic["damage"], magic["type"]))

        it = p["items"]
        for i in it:
            ii = items[i]
            enemy_items.append(Item(ii["name"], ii["type"], ii["desc"], ii["prop"]))

        enemies.append(Person(p["hp"], p["mp"], p["attack"], p["defence"], enemy_magic, enemy_items))

    return players, enemies
