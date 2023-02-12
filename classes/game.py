import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, hp, mp, atk, df, magic, items):
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkh = atk + 10
        self.atkl = atk - 10
        self.df = df
        self.magic = magic
        self.actions = ['Attack', 'Defence', 'Magic', 'Items']
        self.items = items


    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def generate_spell_damage(self, i):
        return self.magic[i].generate_damage()

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def heal(self, damage):
        self.hp += damage
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_spell_name(self, i):
        return self.magic[i].get_name()

    def get_spell_mp_cost(self, i):
        return self.magic[i].get_cost()

    def choose_action(self):
        i = 1
        print('\n' + bcolors.OKBLUE + bcolors.BOLD + 'Actions:' + bcolors.ENDC)
        for item in self.actions:
            print('    ' + str(i) + ': ', item)
            i += 1

    def choose_magic(self):
        i = 1
        print('\n' + bcolors.OKBLUE + bcolors.BOLD + 'Magic:' + bcolors.ENDC)
        for spell in self.magic:
            print('    ' + str(i) + ': ' + spell.get_name() + "(cost: " + str(spell.get_cost()) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print('\n' + bcolors.OKGREEN + bcolors.BOLD + 'Items: ' + bcolors.ENDC)
        item_set = set(self.items)
        for item in item_set:
            print('    ' + str(i) + '.', item.name, ':', item.desc, 'x' + str(self.items.count(item)))
            i += 1

    def reduce_item(self, item):
        self.items.remove(item)

