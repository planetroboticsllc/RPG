import random
import simplejson as json
import os

from classes.game import Person, bcolors
from classes.magic import spell
from classes.inventory import Item
import game_setup

# use json file to load game setup
data = json.loads("{}")
if os.path.isfile('Resources/game_setup.json') and os.stat('Resources/game_setup.json').st_size != 0:
    fp = open('Resources/game_setup.json', 'r+')
    file_content = fp.read()
    data = json.loads(file_content)

players, enemies = game_setup.loadGameSetup(data)

player = players[0]
enemy = enemies[0]

running = True
print(bcolors.FAIL + bcolors.BOLD + 'AN ENEMY ATTACKS!' + bcolors.ENDC)

while running:
    print('============================================================')
    player.choose_action()
    choice = input('Choose action: ')
    index = int(choice) - 1
    player_defence = 0
    enemy_defence = 0

    if index == 0:  # Attack
        damage = player.generate_damage()
        enemy.take_damage(damage)
        print('You attacked for ', damage)
    elif index == 1:  # defence
        player_defence = player.df
        print('You defended enemy attack for ', player_defence)
    elif index == 2:  # Magic
        player.choose_magic()
        magic_choice = int(input('Choose magic: ')) - 1
        if 0 <= magic_choice <= 2:
            spell = player.get_spell_name(magic_choice)
            cost = player.get_spell_mp_cost(magic_choice)

            current_mp = player.get_mp()
            if cost > current_mp:
                print(bcolors.FAIL + "\n Not enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(cost)
            magic_damage = player.generate_spell_damage(magic_choice)

            if (player.magic[magic_choice].type == 'white'):
                player.heal(magic_damage)
            else:
                enemy.take_damage(magic_damage)
            print(bcolors.OKBLUE + '\n You attacked spell ', spell, ' for ' + str(magic_damage) + bcolors.ENDC)

    elif index == 3:  # items
        player.choose_item()
        item_choice = int(input('Choose item: ')) - 1
        if item_choice < 0:
            continue

        item_set = set(player.items)
        if len(item_set) > item_choice:
            item = list(item_set)[item_choice]
            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN + '\n' + item.name + ' ' + item.desc + bcolors.ENDC)
            elif item.type == 'elixer':
                player.hp = player.maxhp
                player.mp = player.maxmp
                print(bcolors.OKGREEN + '\n' + item.name + ' ' + item.desc + bcolors.ENDC)
            elif item.type == 'attack':
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + '\n' + item.name + ' ' + item.desc + bcolors.ENDC)

            player.reduce_item(item)

        else:
            continue

    enemy_choice = random.randrange(1, 10) % 5
    if enemy_choice == 1:  # use enemy spells
        random_num = random.randrange(1, 100)
        num_choices = len(enemy.magic)
        enemy_magic_choice = int(random_num / (100 / num_choices))
        if num_choices > enemy_magic_choice >= 0:
            spell = enemy.get_spell_name(enemy_magic_choice)
            cost = enemy.get_spell_mp_cost(enemy_magic_choice)
            if cost > enemy.get_mp():
                print(bcolors.OKGREEN + "\n Enemy does not have enough MP\n" + bcolors.ENDC)
            else:
                enemy_damage = enemy.generate_spell_damage(enemy_magic_choice)
                if player_defence > 0: enemy_damage = player_defence

                player.take_damage(enemy_damage)
                enemy.reduce_mp(cost)
                print(bcolors.FAIL + 'Enemy attacks for ', enemy_damage,
                      ' points of damage using spell: ' + spell + bcolors.ENDC)
    else:  # use enemy attack
        enemy_damage = enemy.generate_damage()
        if player_defence > 0: enemy_damage = player_defence
        player.take_damage(enemy_damage)
        print(bcolors.FAIL + 'Enemy attacks for ', enemy_damage, ' points of damage' + bcolors.ENDC)

    print('--------------------------')
    print('Enemy HP: ', bcolors.FAIL + str(enemy.get_hp()) + ' / ' + str(enemy.get_max_hp()) + bcolors.ENDC)
    print('Enemy MP: ', bcolors.OKBLUE + str(enemy.get_mp()) + ' / ' + str(enemy.get_max_mp()) + bcolors.ENDC + '\n')
    print('Your HP: ', bcolors.OKGREEN + str(player.get_hp()) + ' / ' + str(player.get_max_hp()) + bcolors.ENDC)
    print('Your MP: ', bcolors.OKBLUE + str(player.get_mp()) + ' / ' + str(player.get_max_mp()) + bcolors.ENDC + '\n')

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + 'YOU WIN!!' + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + 'YOU LOST!!!' + bcolors.ENDC)
        running = False
