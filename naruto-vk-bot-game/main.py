import threading

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from threading import Thread

import random
import math
import time

vk_session = vk_api.VkApi(token='f803f038424f8e573f7b96a25b2759ef88456ddf22e332ec6f50d340763e2d753d6d90603026a97e373ee')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

keyboard_select = VkKeyboard(one_time=False)
keyboard_select.add_button('РЈС‡РёС…Р°', color=VkKeyboardColor.NEGATIVE)
keyboard_select.add_button('РЈР·СѓРјР°РєРё', color=VkKeyboardColor.POSITIVE)
keyboard_select.add_button('РҐСЊСЋРіРѕ', color=VkKeyboardColor.SECONDARY)

keyboard_village = VkKeyboard(one_time=False)
keyboard_village.add_button('РџРѕРєРёРЅСѓС‚СЊ РљРѕРЅРѕС…Сѓ', color=VkKeyboardColor.NEGATIVE)
keyboard_village.add_button('Р РµР·РёРґРµРЅС†РёСЏ РҐРѕРєР°РіРµ', color=VkKeyboardColor.POSITIVE)
keyboard_village.add_line()
keyboard_village.add_button('РС‡РёСЂР°РєСѓ Р Р°РјРµРЅ', color=VkKeyboardColor.PRIMARY)
keyboard_village.add_button('Р›Р°РІРєР° РўРµРЅРўРµРЅ', color=VkKeyboardColor.PRIMARY)
keyboard_village.add_line()
keyboard_village.add_button('Р”РѕРґР·С‘', color=VkKeyboardColor.PRIMARY)

keyboard_tenten = VkKeyboard(one_time=False)
keyboard_tenten.add_button('РЎСЂРµРґРЅРёР№ СЂСЋРєР·Р°Рє', color=VkKeyboardColor.SECONDARY)
keyboard_tenten.add_line()
keyboard_tenten.add_button('Р‘РѕР»СЊС€РѕР№ СЂСЋРєР·Р°Рє', color=VkKeyboardColor.SECONDARY)
keyboard_tenten.add_line()
keyboard_tenten.add_button('РЈР№С‚Рё', color=VkKeyboardColor.NEGATIVE)

keyboard_ramen = VkKeyboard(one_time=False)
keyboard_ramen.add_button('РС‡РёСЂР°РєСѓ', color=VkKeyboardColor.POSITIVE)
keyboard_ramen.add_line()
keyboard_ramen.add_button('РњРёС€Рѕ', color=VkKeyboardColor.POSITIVE)
keyboard_ramen.add_line()
keyboard_ramen.add_button('РЁСЂРёРјРї', color=VkKeyboardColor.POSITIVE)
keyboard_ramen.add_line()
keyboard_ramen.add_button('РЈР№С‚Рё', color=VkKeyboardColor.NEGATIVE)

keyboard_resident = VkKeyboard(one_time=False)
keyboard_resident.add_button('РџСЂРёРЅСЏС‚СЊ Р·Р°РґР°РЅРёРµ', color=VkKeyboardColor.POSITIVE)
keyboard_resident.add_line()
keyboard_resident.add_button('Р’РµСЂРЅСѓС‚СЊСЃСЏ РІ РґРµСЂРµРІРЅСЋ', color=VkKeyboardColor.NEGATIVE)

keyboard_dojo = VkKeyboard(one_time=False)
keyboard_dojo.add_button('Р’РѕРґРѕРїР°Рґ', color=VkKeyboardColor.POSITIVE)
keyboard_dojo.add_line()
keyboard_dojo.add_button('Р’РµСЂРЅСѓС‚СЊСЃСЏ РІ РґРµСЂРµРІРЅСЋ', color=VkKeyboardColor.NEGATIVE)

keyboard_get_item = VkKeyboard(one_time=False, inline=True)
keyboard_get_item.add_button('Р’Р·СЏС‚СЊ', color=VkKeyboardColor.POSITIVE)

keyboard_skill_up = VkKeyboard(one_time=False)
keyboard_skill_up.add_button('РџРµСЂРІС‹Р№ С‚Р°Р»Р°РЅС‚', color=VkKeyboardColor.POSITIVE)
keyboard_skill_up.add_line()
keyboard_skill_up.add_button('Р’С‚РѕСЂРѕР№ С‚Р°Р»Р°РЅС‚', color=VkKeyboardColor.POSITIVE)
keyboard_skill_up.add_line()
keyboard_skill_up.add_button('РўСЂРµС‚РёР№ С‚Р°Р»Р°РЅС‚', color=VkKeyboardColor.POSITIVE)
keyboard_skill_up.add_line()
keyboard_skill_up.add_button('Р’РµСЂРЅСѓС‚СЊСЃСЏ РІ РіР»Р°РІРЅС‹Р№ Р·Р°Р»', color=VkKeyboardColor.SECONDARY)

keyboard_fight = VkKeyboard(one_time=False)
keyboard_fight.add_button('РђС‚Р°РєР°', color=VkKeyboardColor.NEGATIVE)
keyboard_fight.add_line()
keyboard_fight.add_button('РўРµС…РЅРёРєРё', color=VkKeyboardColor.PRIMARY)
keyboard_fight.add_line()
keyboard_fight.add_button('РРЅРІРµРЅС‚Р°СЂСЊ', color=VkKeyboardColor.SECONDARY)


class Player:

    def __init__(self, user_id, clan, taijutsu, ninjutsu, genjutsu, vital, fuinjutsu, skill, talents):
        self.id = user_id
        self.clan = clan
        self.rank = 'Р“РµРЅРёРЅ'
        self.strength = 5
        self.speed = 5
        self.stamina = 10
        self.taijutsu = taijutsu
        self.ninjutsu = ninjutsu
        self.genjutsu = genjutsu
        self.fuinjutsu = fuinjutsu
        self.vital = vital
        self.skills = skill
        self.talents = talents
        self.location = 1
        self.level = 1
        self.exp = 0
        self.point = 1
        self.inventory = Inventory()
        self.yen = 100
        self.quest = None
        self.keyboard_skills = VkKeyboard(one_time=True)
        self.keyboard_inventory = VkKeyboard(one_time=True)


class Skill:

    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.level = 1


class Talent:

    def __init__(self, description, bonus_skill_cost=None, bonus_vital=None, bonus_dodge=None, bonus_health=None,
                 bonus_genjutsu=None, bonus_damage=None, bonus_fuinjutsu=None, bonus_chakra_burning=None):

        self.description = description
        self.level = 0

        if bonus_health is None: bonus_health = [0, 0, 0, 0, 0]
        if bonus_dodge is None: bonus_dodge = [0, 0, 0, 0, 0]
        if bonus_vital is None: bonus_vital = [0, 0, 0, 0, 0]
        if bonus_skill_cost is None: bonus_skill_cost = [0, 0, 0, 0, 0]
        if bonus_genjutsu is None: bonus_genjutsu = [0, 0, 0, 0, 0]
        if bonus_damage is None: bonus_damage = [0, 0, 0, 0, 0]
        if bonus_chakra_burning is None: bonus_chakra_burning = [0, 0, 0, 0, 0]
        if bonus_fuinjutsu is None: bonus_fuinjutsu = [0, 0, 0, 0, 0]

        self.chakra_burning = bonus_chakra_burning
        self.bonus_skill_cost = bonus_skill_cost
        self.bonus_vital = bonus_vital
        self.bonus_dodge = bonus_dodge
        self.bonus_health = bonus_health
        self.bonus_genjutsu = bonus_genjutsu
        self.bonus_damage = bonus_damage
        self.bonus_fuinjutsu = bonus_fuinjutsu


class Enemy:

    def __init__(self, player):
        if player.quest.rank == '[B]':
            self.skill_name = 'РЁР°СЂРёРє'
            self.skill_damage = 15
            self.skill_cooldown = 3
            self.damage = random.randint(5, 25)
            self.health = random.randint(10, 50)
            self.reward = player.quest.reward
            self.experience = 30
            self.number = random.randint(2, 5)


class Inventory:

    def __init__(self):
        self.max_items = 5
        self.items = []

    def AddItem(self, item):
        if len(self.items) < self.max_items:
            self.items.append(item)
            return 'Р’СЃС‘ РїСЂРѕС€Р»Рѕ СѓСЃРїРµС€РЅРѕ'
        return 'РЈ РІР°СЃ РЅРµС…РІР°С‚РµС‚ РјРµСЃС‚Р° РІ СЂСЋРєР·Р°РєРµ'


class Item:

    def __init__(self, name, regen_health):
        self.name = name
        self.regen_health = regen_health


class Quest:

    def __init__(self, criminal, reward, rank):
        self.criminal = criminal
        self.reward = reward
        self.rank = rank


class Fight:

    def __init__(self, player, enemy):
        self.player_id = player.id
        self.enemy = enemy

        self.player_dodge = player.speed // 5
        self.player_health = player.stamina
        self.player_damage = player.strength
        self.player_skills = player.skills
        self.player_vital = player.vital

        self.player_fuinjutsu = player.fuinjutsu
        self.bonus_skill_cost = 0
        self.chakra_burning = 0

        for index in range(len(player.talents)):
            if player.talents[index].level > 0:
                self.player_health += player.talents[index].bonus_health[player.talents[index].level - 1]
                self.player_dodge += player.talents[index].bonus_dodge[player.talents[index].level - 1]
                self.player_vital += player.talents[index].bonus_vital[player.talents[index].level - 1]
                self.player_damage += player.talents[index].bonus_damage[player.talents[index].level - 1]

                self.bonus_skill_cost = player.talents[index].bonus_skill_cost[player.talents[index].level - 1]
                self.chakra_burning = player.talents[index].chakra_burning[player.talents[index].level - 1]

        self.max_hp_player = self.player_health
        self.max_chakra_player = self.player_vital
        self.max_hp_enemy = enemy.health

        self.step = 0

FIREBALL = Skill('РћРіРЅРµРЅРЅС‹Р№ С€Р°СЂ', 10)
PUNCH = Skill('64 Р›Р°РґРѕРЅРё РЅРµР±РµСЃ', 10)
ENVELOPING = Skill('РћРєСѓС‚С‹РІР°РЅРёРµ', 0)
SHADOW_CLONING = Skill('РўРµРЅРµРІРѕРµ РєР»РѕРЅРёСЂРѕРІР°РЅРёРµ', 0)

SALVE = Item('Р¦РµР»РµР±Р°РЅСЏ РјР°Р·СЏ', 10)

UZUMAKI_1_TALENT = Talent(description="РЈРјРµРЅСЊС€Р°РµС‚ Р·Р°С‚СЂР°С‚С‹ С‡Р°РєСЂС‹ РЅР° С‚РµС…РЅРёРєРё",
                          bonus_skill_cost=[5, 10, 15, 20, 25])
UZUMAKI_2_TALENT = Talent(description="РЈРІРµР»РёС‡РёРІР°РµС‚ РєРѕР»РёС‡РµСЃС‚РІРѕ С‡Р°РєСЂС‹",
                          bonus_vital=[10, 20, 30, 40, 50])
UZUMAKI_3_TALENT = Talent(description="РџРѕРІС‹С€Р°РµС‚ Р¤СѓРёРЅРґР·СЋС†Сѓ",
                          bonus_fuinjutsu=[1, 3, 5, 10, 20])

UCHIHA_1_TALENT = Talent(description="РЈРІРµР»РёС‡РёРІР°РµС‚ РІРµСЂРѕСЏС‚РЅРѕСЃС‚СЊ СѓРєР»РѕРЅРёС‚СЃСЏ",
                         bonus_dodge=[10, 15, 20, 25, 30])
UCHIHA_2_TALENT = Talent(description="РЈРІРµР»РёС‡РёРІР°РµС‚ СЃРёР»Сѓ РіРµРЅРґР·СЋС†Сѓ",
                         bonus_genjutsu=[10, 20, 30, 40, 50])
UCHIHA_3_TALENT = Talent(description="РџРѕРІС‹С€Р°РµС‚ СѓСЂРѕРЅ Рё Р·РґРѕСЂРѕРІСЊРµ",
                         bonus_damage=[25, 50, 75, 100, 150],
                         bonus_health=[10, 20, 30, 40, 50])

HIUGO_1_TALENT = Talent(description="РЈРІРµР»РёС‡РёРІР°РµС‚ РІРµСЂРѕСЏС‚РЅРѕСЃС‚СЊ СѓРєР»РѕРЅРёС‚СЃСЏ",
                        bonus_dodge=[10, 15, 20, 25, 30])
HIUGO_2_TALENT = Talent(description="РЈРІРµР»РёС‡РёРІР°РµС‚ Р¶РёРІСѓС‡РµСЃС‚СЊ",
                        bonus_health=[10, 20, 30, 40, 50])
HIUGO_3_TALENT = Talent(description="РЎР¶РёРіР°РµС‚ С‡Р°РєСЂСѓ РїСЂРѕС‚РёРІРЅРёРєР°",
                        bonus_chakra_burning=[5, 10, 20, 30, 50])

users = [Player(341979469, 'None', 0, 0, 0, 0, 0, 0, 0)]
fights = []


def sender(user_vk_id, text, keyboard):
    vk_session.method('messages.send', {
        'user_id': user_vk_id,
        'message': text,
        'random_id': 0,
        'keyboard': keyboard.get_keyboard()
    })


def execute(vk_event):
    message = vk_event.text.lower()
    user_id = vk_event.user_id

    for user in range(len(users)):

        village_state = f"&#127983;РљРѕРЅРѕС…Р°\n\n" \
                        f"&#127568;РЈСЂРѕРІРµРЅСЊ: {users[user].level}\n" \
                        f"&#128176;Р’Р°Р»СЋС‚Р°: {users[user].yen}"

        tenten_state = "&#9961;Р”РѕР±СЂРѕ РїРѕР¶Р°Р»РѕРІР°С‚СЊ РІ РЅР°С€ РЅРµР±РѕР»СЊС€РѕР№ РјР°РіР°Р·РёРЅС‡РёРє\n" \
                       "&#128276;РћР·РЅРѕРєРѕРјСЊС‚РµСЃСЊ СЃ РєР°С‚Р°Р»РѕРіРѕРј С‚РѕРІР°СЂРѕРІ\n\n" \
                       "&#127890;РЎСЂРµРґРЅРёР№ СЂСЋРєР·Р°Рє:\n" \
                       "&#128196;РњР°РєСЃРёРјР°Р»СЊРЅР°СЏ РІРјРµСЃС‚РёРјРѕСЃС‚СЊ [10] \n &#127991;РЎС‚РѕРёРјРѕСЃС‚СЊ [150]\n\n" \
                       "&#127890;Р‘РѕР»СЊС€РѕР№ СЂСЋРєР·Р°Рє:\n" \
                       "&#128196;РњР°РєСЃРёРјР°Р»СЊРЅР°СЏ РІРјРµСЃС‚РёРјРѕСЃС‚СЊ [25] \n &#127991;РЎС‚РѕРёРјРѕСЃС‚СЊ [500]"

        ichiraku_state = '&#9961;Р”РѕР±СЂРѕ РїРѕР¶Р°Р»РѕРІР°С‚СЊ РІ РС‡РёСЂР°РєСѓ Р Р°РјРµРЅ\n' \
                         '&#128214;РњРµРЅСЋ:\n\n' \
                         '&#127836;РС‡РёСЂР°РєСѓ Р Р°РјРµРЅ - СЂР°Р·РѕРіСЂРµРІР°РµС‚ РІР°С€Рё РјС‹С€С†С‹, ' \
                         'С‚РµР»Рѕ СЃС‚Р°РЅРѕРІРёС‚СЃСЏ СЌР»РѕСЃС‚РёС‡РЅРµРµ Р° СѓРґР°СЂС‹ РјРѕС‰РЅРµРµ [РџРѕРІС‹С€Р°РµС‚ С‚Р°Р№РґР·СЋС†Сѓ РЅР° 20%]\n\n' \
                         '&#127835;РњРёС€Рѕ Р Р°РјРµРЅ - СЂР°Р·РіРѕРЅСЏРµС‚ С‡Р°РєСЂСѓ РїРѕ РІСЃРµРјСѓ С‚РµР»Сѓ, ' \
                         'СЌРЅРµСЂРіРёСЏ РїРµСЂРµРїРѕР»РЅСЏРµС‚ РІР°СЃ [РџРѕРІС‹С€Р°РµС‚ РЅРёРЅРґР·СЋС†Сѓ РЅР° 20%]\n\n' \
                         '&#127837;РЁСЂРёРјРї Р Р°РјРµРЅ - РїРѕРІС‹С€Р°РµС‚ РјРѕР·РіРѕРІСѓСЋ Р°РєС‚РёРІРЅРѕСЃС‚СЊ, ' \
                         'РІС‹ РЅР°С‡РёРЅР°РµС‚Рµ Р·Р°РјРµС‡Р°С‚СЊ РїСЂРёРІС‹С‡РєРё Р»СЋРґРµР№ [РџРѕРІС‹С€Р°РµС‚ РіРµРЅРґР·СЋС†Сѓ РЅР° 20%]'

        dojo_state = '&#9961;Р”РѕР±СЂРѕ РїРѕР¶Р°Р»РѕРІР°С‚СЊ РІ Р»СѓС‡С€РµРµ Р”РѕРґР·С‘\n\n' \
                     '&#127775;Р§С‚РѕР±С‹ СѓР»СѓС‡С€РёС‚СЊ РІСЂРѕР¶РґРµРЅРЅС‹Рµ С‚Р°Р»Р°РЅС‚С‹ РїРѕРґРѕР№РґРёС‚Рµ Рє РІРѕРґРѕРїР°РґСѓ'

        # РќР°С‡Р°Р»Рѕ [0]
        if message == 'РЅР°С‡Р°С‚СЊ':
            for index in range(len(users)):
                if users[index].id == user_id:
                    break
                if index == len(users) - 1:
                    sender(user_id, 'Р’С‹Р±РµСЂРёС‚Рµ РєР»Р°РЅ...', keyboard_select)
                    users.append(Player(user_id, 'None', 0, 0, 0, 0, 0, 0, 0))

        # Р’С‹Р±РѕСЂ РєР»Р°РЅР° [1]
        if users[user].id == user_id and users[user].location == 1:

            if message == "С…СЊСЋРіРѕ" or message == "СѓС‡РёС…Р°" or message == "СѓР·СѓРјР°РєРё":
                if message == "С…СЊСЋРіРѕ":
                    users[user] = Player(user_id, 'РҐСЊСЋРіРѕ', 5, 20, 10, 40, 5, [PUNCH], [HIUGO_1_TALENT,
                                                                                        HIUGO_2_TALENT,
                                                                                        HIUGO_3_TALENT])
                if message == "СѓС‡РёС…Р°":
                    users[user] = Player(user_id, 'РЈС‡РёС…Р°', 5, 25, 25, 25, 5, [FIREBALL], [UCHIHA_1_TALENT,
                                                                                           UCHIHA_2_TALENT,
                                                                                           UCHIHA_3_TALENT])
                if message == "СѓР·СѓРјР°РєРё":
                    users[user] = Player(user_id, 'РЈР·СѓРјР°РєРё', 5, 15, 5, 50, 5, [ENVELOPING], [UZUMAKI_1_TALENT,
                                                                                              UZUMAKI_2_TALENT,
                                                                                              UZUMAKI_3_TALENT])

                sender(user_id, village_state, keyboard_village)
                users[user].location = 2

        # Р”РµСЂРµРІРЅСЏ [2]
        if users[user].id == user_id and users[user].location == 2:

            if message == "РїРѕРєРёРЅСѓС‚СЊ РєРѕРЅРѕС…Сѓ":
                sender(user_id, '&#129517;Р’С‹ РїРѕРєРёРЅСѓР»Рё СЃС‚РµРЅС‹ РљРѕРЅРѕС…Рё Рё РґРІРёРЅСѓР»РёСЃСЊ РЅР° СЃРµРІРµСЂ...', keyboard_village)
                users[user].location = 3

            if message == "СЂРµР·РёРґРµРЅС†РёСЏ С…РѕРєР°РіРµ":
                reward = 0
                rank = ''
                target = ''

                if users[user].rank == 'Р“РµРЅРёРЅ':
                    reward = random.randint(1000, 2500)
                    rank = '[B]'
                    target = 'РћС‚Р±РёС‚СЊ РІСЃРµ Р°С‚Р°Рє222Рё РІСЂР°РіРѕРІ'
                if users[user].rank == 'Р§СѓРЅРёРЅ':
                    reward = random.randint(2500, 10000)
                    rank = '[A]'
                    target = 'РЈР±РёС‚СЊ РїСЂРµРґР°С‚РµР»СЏ'
                if users[user].rank == 'Р”Р¶РѕСѓРЅРёРЅ':
                    reward = random.randint(10000, 25000)
                    rank = '[S]'
                    target = 'РЈРЅРёС‡С‚РѕР¶РёС‚СЊ РѕР±СЉРµРєС‚'

                quest = f'&#127919;Р¦РµР»СЊ: {target} {rank}\n' \
                        f'&#128176;РќР°РіСЂР°РґР°: {reward}'

                sender(user_id, f'&#127963;Р РµР·РёРґРµРЅС†РёСЏ РҐРѕРєР°РіРµ\n\n{quest}', keyboard_resident)
                users[user].quest = Quest(criminal, reward, rank)

                users[user].location = 4

            if message == "РґРѕРґР·С‘":
                sender(user_id, dojo_state, keyboard_dojo)
                users[user].location = 7

            if message == "Р»Р°РІРєР° С‚РµРЅС‚РµРЅ":
                sender(user_id, tenten_state, keyboard_tenten)
                users[user].location = 9

            if message == 'РёС‡РёСЂР°РєСѓ СЂР°РјРµРЅ':
                sender(user_id, ichiraku_state, keyboard_ramen)
                users[user].location = 10


        # РџСѓС‚РµС€РµСЃС‚РІРёРµ [3]
        if users[user].id == user_id and users[user].location == 3:

            users[user].location = 0
            time.sleep(10)

            action = random.randint(1, 10)

            if action <= 10 and users[user].quest is not None:
                if users[user].quest.rank == '[B]':
                    fights.append(Fight(users[user], Enemy(users[user])))
                    users[user].location = 5
                    sender(user_id,
                            f'РќР° РІР°СЃ РЅР°РїР°Р»Рё\n'
                            f'Р—РґРѕСЂРѕРІСЊРµ: {fights[-1].enemy.health}\n'
                            f'РЈСЂРѕРЅ: {fights[-1].enemy.damage}',
                            keyboard_fight)

        # Р РµР·РёРґРµРЅС†РёСЏ РҐРѕРєР°РіРµ [4]
        if users[user].id == user_id and users[user].location == 4:

            if message == 'РїСЂРёРЅСЏС‚СЊ Р·Р°РґР°РЅРёРµ':
                sender(user_id, '&#128272;РќР°Р№РґРё РµРіРѕ Рё РѕС‚РїСЂР°РІСЊС‚Рµ РІ С‚СЋСЂСЊРјСѓ', keyboard_village)
                users[user].location = 2

            if message == "РІРµСЂРЅСѓС‚СЊСЃСЏ РІ РґРµСЂРµРІРЅСЋ":
                sender(user_id, village_state, keyboard_village)
                users[user].quest = None
                users[user].location = 2

        # Р‘РѕР№ [5]
        if users[user].id == user_id and users[user].location == 5:

            for fight in range(len(fights)):
                if fights[fight].player_id == user_id:

                    state = ''
                    if message == "Р°С‚Р°РєР°":
                        u, e = random.randint(1, 101), random.randint(1, 101)
                        enemy_damage = random.randint(fights[fight].enemy.damage - 5, fights[fight].enemy.damage)
                        player_damage = random.randint(fights[fight].player_damage - 5, fights[fight].player_damage)

                        if fights[fight].enemy.health - player_damage > 0 \
                                and fights[fight].player_health - enemy_damage > 0:

                            if fights[fight].enemy.dodge >= e and u > fights[fight].player_dodge:
                                fights[fight].player_health -= enemy_damage
                                state += f"&#128168;Р’С‹ РїСЂРѕРјРѕС…РЅСѓР»РёСЃСЊ\n" \
                                         f"&#128298;РџСЂРѕС‚РёРІРЅРёРє РЅР°РЅРµСЃ {enemy_damage} СѓСЂРѕРЅР°\n\n"
                            if fights[fight].enemy.dodge < e and u <= fights[fight].player_dodge:
                                fights[fight].enemy.health -= player_damage
                                state += f"&#128481;Р’С‹ РЅР°РЅРµСЃР»Рё {player_damage} СѓСЂРѕРЅР°\n" \
                                         f"&#128171;Р’С‹ СѓРєР»РѕРЅРёР»РёСЃСЊ\n\n"
                            if fights[fight].enemy.dodge < e and u > fights[fight].player_dodge:
                                fights[fight].player_health -= enemy_damage
                                fights[fight].enemy.health -= player_damage
                                state += f"&#128481;Р’С‹ РЅР°РЅРµСЃР»Рё {player_damage} СѓСЂРѕРЅР°\n" \
                                         f"&#128298;РџСЂРѕС‚РёРІРЅРёРє РЅР°РЅРµСЃ {enemy_damage} СѓСЂРѕРЅР°\n\n"
                            if fights[fight].enemy.dodge >= e and u <= fights[fight].player_dodge:
                                state += f"&#128168;Р’С‹ РїСЂРѕРјРѕС…РЅСѓР»РёСЃСЊ\n" \
                                         f"&#128171;Р’С‹ СѓРєР»РѕРЅРёР»РёСЃСЊ\n\n"
                        else:
                            if fights[fight].enemy.health - fights[fight].player_damage <= 0:
                                if users[user].quest is not None and fights[fight].enemy.name == users[user].quest.criminal:
                                    sender(user_id, 'Р’С‹ РІС‹РїРѕР»РЅРёР»Рё РјРёСЃСЃРёСЋ Рё РІРµСЂРЅСѓР»РёСЃСЊ РІ РґРµСЂРµРІРЅСЋ', keyboard_village)
                                    users[user].quest = None
                                users[user].exp += fights[fight].enemy.experience
                                users[user].yen += fights[fight].enemy.reward
                                users[user].location = 2
                                fights.pop(fight)
                                break
                            if fights[fight].player_health - fights[fight].enemy.damage <= 0:
                                sender(user_id, "Р’С‹ РїСЂРѕРёРіСЂР°Р»Рё Рё РѕС‡РЅСѓР»РёСЃСЊ РІ РґРµСЂРµРІРЅРµ", keyboard_village)
                                users[user].location = 2
                                fights.pop(fight)
                                sender(user_id, village_state, keyboard_village)
                                break

                        fights[fight].step += 1
                        if fights[fight].step % fights[fight].enemy.skill_cooldown == 0:
                            if fights[fight].player_health - fights[fight].enemy.skill_damage > 0:
                                fights[fight].player_health -= fights[fight].enemy.skill_damage
                                state += f'&#9732;РџСЂРѕС‚РёРІРЅРёРє РёСЃРѕР»СЊР·СѓРµС‚ С‚РµС…РЅРёРєСѓ {fights[fight].enemy.skill_name} Рё РЅР°РЅРѕСЃРёС‚ 10 СѓСЂРѕРЅР°\n'
                            if fights[fight].player_health - fights[fight].enemy.skill_damage <= 0:
                                sender(user_id,
                                       f'Р’С‹ РїСЂРѕРёРіСЂР°Р»Рё Рё РѕС‡РЅСѓР»РёСЃСЊ РІ РґРµСЂРµРІРЅРµ РїРѕСЃР»Рµ С‚РµС…РЅРёРєРё {fights[fight].enemy.skill_name} РїСЂРѕС‚РёРІРЅРёРєР°',
                                       keyboard_village)
                                fights.pop(fight)
                                users[user].location = 2
                                break

                        condition = f"\nР’С‹:\n" \
                                    f"&#10084;HP: {fights[fight].player_health}/{fights[fight].max_hp_player}\n" \
                                    f"&#127744;Chakra: {fights[fight].player_vital}/{fights[fight].max_chakra_player}\n" \
                                    f"РџСЂРѕС‚РёРІРЅРёРє:\n" \
                                    f"&#128154;HP: {fights[fight].enemy.health}/{fights[fight].max_hp_enemy}"

                        if users[user].clan == 'РҐСЊСЋРіРѕ':
                            if users[user].talent[2].level > 0:
                                fights[fight].enemy.vital -= users[user].talent[2].bonus_burning
                            condition += f"\n&#127744;Chakra: {fights[fight].enemy.vital}"

                        sender(user_id,
                               state +
                               condition,
                               keyboard_fight)

                    if message == 'С‚РµС…РЅРёРєРё':
                        users[user].keyboard_skills = VkKeyboard(one_time=True)
                        for index in range(len(fights[fight].player_skills)):
                            users[user].keyboard_skills.add_button(f"{fights[fight].player_skills[index].name}",
                                                                   color=VkKeyboardColor.POSITIVE)
                            if len(fights[fight].player_skills) - 1 != index:
                                users[user].keyboard_skills.add_line()
                        sender(user_id, f'&#127744;РЈ РІР°СЃ {fights[fight].player_vital} С‡Р°РєСЂС‹', users[user].keyboard_skills)
                        users[user].location = 6

                    if message == 'РёРЅРІРµРЅС‚Р°СЂСЊ':
                        salve = 0
                        for item in users[user].inventory.items:
                            if item.name == 'Р¦РµР»РµР±РЅР°СЏ РјР°Р·СЊ':
                                salve += 1
                                users[user].keyboard_inventory = VkKeyboard(one_time=True)
                                users[user].keyboard_inventory.add_button('Р¦РµР»РµР±РЅР°СЏ РјР°Р·СЊ', color=VkKeyboardColor.POSITIVE)
                        sender(user_id, f'&#127802;Р›РµС‡РµР±РЅР°СЏ РјР°Р·СЊ: {salve}', users[user].keyboard_inventory)

                    if message == 'С†РµР»РµР±РЅР°СЏ РјР°Р·СЊ':
                        if fights[fight].player_health + 10 > fights[fight].max_hp_player:
                            fights[fight].player_health = fights[fight].max_hp_player
                            users[user].inventory.items.pop(-1)
                            sender(user_id, '&#128150;Р’С‹ РїРѕР»РЅРѕСЃС‚СЊСЋ РІРѕСЃСЃС‚Р°РЅРѕРІРёР»Рё Р·РґРѕСЂРѕРІСЊРµ', keyboard_fight)
                            break
                        fights[fight].player_health += 10
                        users[user].inventory.items.pop(-1)
                        sender(user_id, '&#128150;Р’С‹ РІРѕСЃСЃС‚Р°РЅРѕРІРёР»Рё 10 РµРґРёРЅРёС† Р·РґРѕРІСЂРѕСЊСЏ', keyboard_fight)


        # Р‘РѕР№ - РўРµС…РЅРёРєРё [6]
        if users[user].id == user_id and users[user].location == 6:

            for fight in range(len(fights)):
                if fights[fight].player_id == user_id:

                    for index in range(len(fights[fight].player_skills)):
                        if message == f"{fights[fight].player_skills[index].name}".lower():

                            state = ''

                            cost = fights[fight].player_skills[index].cost
                            if fights[fight].bonus_skill_cost > 0:
                                cost = int(cost / 100 * (100 - fights[fight].bonus_skill_cost))
                            if fights[fight].player_vital - cost <= 0:
                                sender(user_id, "РЈ РІР°СЃ РЅРµРґРѕСЃС‚Р°С‚РѕС‡РЅРѕ С‡Р°РєСЂС‹", keyboard_fight)
                                users[user].location = 5
                                break
                            fights[fight].player_vital -= cost

                            damage = 0

                            if fights[fight].player_skills[index].name == "РћРєСѓС‚С‹РІР°РЅРёРµ":
                                fights[fight].player_vital = 0

                                if fights[fight].enemy.health - (int(fights[fight].max_hp_enemy / 100) *
                                   fights[fight].player_fuinjutsu) <= 0:
                                    sender(user_id, "Р’С‹ РІС‹РёРіСЂР°Р»Рё Рё СЂРµС€Р°РµС‚Рµ С‡С‚Рѕ РґРµР»Р°С‚СЊ РґР°Р»СЊС€Рµ", keyboard_travel)
                                    users[user].exp += fights[fight].enemy.experience
                                    users[user].yen += fights[fight].enemy.reward
                                    users[user].location = 3
                                    fights.pop(fight)
                                    break
                                if fights[fight].player_health - fights[fight].enemy.damage <= 0:
                                    sender(user_id, "Р’С‹ РїСЂРѕРёРіСЂР°Р»Рё Рё РѕС‡РЅСѓР»РёСЃСЊ РІ РґРµСЂРµРІРЅРµ", keyboard_village)
                                    users[user].location = 2
                                    fights.pop(fight)
                                    break
                                damage = int(fights[fight].max_hp_enemy / 100 * fights[fight].player_fuinjutsu)

                            if fights[fight].player_skills[index].name == "РћРіРЅРµРЅРЅС‹Р№ С€Р°СЂ":
                                damage = int((users[user].vital + users[user].ninjutsu) * \
                                            (0.5 * fights[fight].player_skills[index].level))

                            if fights[fight].player_skills[index].name == "64 Р›Р°РґРѕРЅРё РЅРµР±РµСЃ":
                                damage = int((users[user].taijutsu + users[user].ninjutsu) * \
                                             (0.5 * fights[fight].player_skills[index].level))
                                fights[fight].enemy.damage = int((fights[fight].enemy.damage / 100) * \
                                                                 (100 - int(users[user].vital *
                                                                 (0.2 * fights[fight].player_skills[index].level))))
                                state += f"&#9939;РђС‚Р°РєР° РїСЂРѕС‚РёРІРЅРёРєР° СЃРЅРёР¶РµРЅР°\n"

                            if fights[fight].player_skills[index].name == "РўРµРЅРµРІРѕРµ РєР»РѕРЅРёСЂРѕРІР°РЅРёРµ":
                                damage = int(fights[fight].player_damage / 100 *
                                             (100 + users[user].taijutsu * 0.5))

                            if fights[fight].enemy.health - damage > 0 \
                                    and fights[fight].player_health - fights[fight].enemy.damage > 0:
                                fights[fight].enemy.health -= damage
                                fights[fight].player_health -= fights[fight].enemy.damage
                                state += f"&#128165;Р’С‹ РЅР°РЅРµСЃР»Рё " \
                                         f"{damage} СѓСЂРѕРЅР°\n" \
                                         f"&#128298;РџСЂРѕС‚РёРІРЅРёРє РЅР°РЅРµСЃ " \
                                         f"{fights[fight].enemy.damage} СѓСЂРѕРЅР°\n\n"
                            else:
                                if fights[fight].enemy.health - damage <= 0:
                                    sender(user_id, "Р’С‹ РІС‹РёРіСЂР°Р»Рё Рё СЂРµС€Р°РµС‚Рµ С‡С‚Рѕ РґРµР»Р°С‚СЊ РґР°Р»СЊС€Рµ", keyboard_travel)
                                    users[user].exp += fights[fight].enemy.experience
                                    users[user].location = 3
                                    fights.pop(fight)
                                    break
                                if fights[fight].player_health - fights[fight].enemy.damage <= 0:
                                    sender(user_id, "Р’С‹ РїСЂРѕРёРіСЂР°Р»Рё Рё РѕС‡РЅСѓР»РёСЃСЊ РІ РґРµСЂРµРІРЅРµ", keyboard_village)
                                    users[user].location = 2
                                    fights.pop(fight)
                                    sender(user_id, village_state, keyboard_village)
                                    break

                            sender(user_id,
                                   state +
                                   f"Р’С‹:\n"
                                   f"&#10084;HP: {fights[fight].player_health}/{fights[fight].max_hp_player}\n"
                                   f"&#127744;Chakra: {fights[fight].player_vital}/{fights[fight].max_chakra_player}\n"
                                   f"РџСЂРѕС‚РёРІРЅРёРє: \n"
                                   f"&#128154;HP: {fights[fight].enemy.health}/{fights[fight].max_hp_enemy}",
                                   keyboard_fight)
                            users[user].location = 5

        # Р”РѕРґР·С‘ [7]
        if users[user].id == user_id and users[user].location == 7:

            if message == "РІРѕРґРѕРїР°Рґ":
                if users[user].point > 0:
                    sender(user_id, f"РЈ РІР°СЃ {users[user].point} РѕС‡РєРѕРІ СѓР»СѓС‡С€РµРЅРёСЏ", keyboard_skill_up)
                    users[user].location = 8
                else:
                    sender(user_id, "РЈ РІР°СЃ РЅРµРґРѕСЃС‚Р°С‚РѕС‡РЅРѕ РѕС‡РєРѕРІ СѓР»СѓС‡С€РµРЅРёСЏ", keyboard_resident)

            if message == "РІРµСЂРЅСѓС‚СЊСЃСЏ РІ РґРµСЂРµРІРЅСЋ":
                sender(user_id, village_state, keyboard_village)
                users[user].location = 2

        # Р”РѕРґР·С‘ - Р’РѕРґРѕРїР°Рґ [8]
        if users[user].id == user_id and users[user].location == 8:
            if message == "РїРµСЂРІС‹Р№ С‚Р°Р»Р°РЅС‚":
                if users[user].talent[0].level < 5:
                    users[user].talent[0].level += 1
                    sender(user_id, f"РЈР»СѓС‡С€РµРЅРѕ РґРѕ {users[user].talent[0].level} СѓСЂРѕРІРЅСЏ", keyboard_skill_up)
                    users[user].point -= 1
                    break
                sender(user_id, "Р’С‹ РїСЂРѕРєР°С‡Р°Р»Рё С‚Р°Р»Р°РЅС‚ РЅР° РјР°РєСЃРёРјСѓРј", keyboard_skill_up)

            if message == "РІС‚РѕСЂРѕР№ С‚Р°Р»Р°РЅС‚":
                if users[user].talent[1].level < 5 and users[user].level > 3:
                    users[user].talent[1].level += 1
                    sender(user_id, f"РЈР»СѓС‡С€РµРЅРѕ РґРѕ {users[user].talent[1].level} СѓСЂРѕРІРЅСЏ", keyboard_skill_up)
                    users[user].point -= 1
                    break
                if users[user].level <= 3:
                    sender(user_id, "Р’С‹ РЅРµРґРѕСЃС‚Р°С‚РѕС‡РЅРѕ СЃРёР»СЊРЅС‹ С‡С‚РѕР±С‹ СѓР»СѓС‡С€РёС‚СЊ СЌС‚РѕС‚ С‚Р°Р»Р°РЅС‚", keyboard_skill_up)
                    break
                sender(user_id, "Р’С‹ РїСЂРѕРєР°С‡Р°Р»Рё С‚Р°Р»Р°РЅС‚ РЅР° РјР°РєСЃРёРјСѓРј", keyboard_skill_up)

            if message == "С‚СЂРµС‚РёР№ С‚Р°Р»Р°РЅС‚":
                if users[user].talent[2].level < 5 and users[user].level > 8:
                    users[user].talent[2].level += 1
                    sender(user_id, f"РЈР»СѓС‡С€РµРЅРѕ РґРѕ {users[user].talent[2].level} СѓСЂРѕРІРЅСЏ", keyboard_skill_up)
                    users[user].point -= 1
                    break
                if users[user].level <= 8:
                    sender(user_id, "Р’С‹ РЅРµРґРѕСЃС‚Р°С‚РѕС‡РЅРѕ СЃРёР»СЊРЅС‹ С‡С‚РѕР±С‹ СѓР»СѓС‡С€РёС‚СЊ СЌС‚РѕС‚ С‚Р°Р»Р°РЅС‚", keyboard_skill_up)
                    break
                sender(user_id, "Р’С‹ РїСЂРѕРєР°С‡Р°Р»Рё С‚Р°Р»Р°РЅС‚ РЅР° РјР°РєСЃРёРјСѓРј", keyboard_skill_up)

            if message == "РІРµСЂРЅСѓС‚СЊСЃСЏ РІ РіР»Р°РІРЅС‹Р№ Р·Р°Р»":
                sender(user_id, dojo_state, keyboard_dojo)
                users[user].location = 7

        # Р›Р°РІРєР° РўРµРЅРўРµРЅ [9]
        if users[user].id == user_id and users[user].location == 9:

            if message == "СЃСЂРµРґРЅРёР№ СЂСЋРєР·Р°Рє":
                if users[user].yen < 150:
                    sender(user_id, f"&#128180;РЈ РІР°СЃ РЅРµС…РІР°С‚Р°РµС‚ {150 - users[user].yen}ВҐ", keyboard_tenten)
                    break
                if users[user].inventory.max_items < 10:
                    users[user].inventory.max_items = 10
                    sender(user_id, "Р’С‹ РїСЂРёРѕР±СЂРµР»Рё СЃСЂРµРґРЅРёР№ СЂСЋРєР·Р°Рє [-150ВҐ]", keyboard_tenten)
                    break
                sender(user_id, "РЈ РІР°СЃ СѓР¶Рµ РµСЃС‚СЊ СЌС‚РѕС‚ РїСЂРµРґРјРµС‚", keyboard_tenten)

            if message == "Р±РѕР»СЊС€РѕР№ СЂСЋРєР·Р°Рє":
                if users[user].yen < 500:
                    sender(user_id, f"&#128180;РЈ РІР°СЃ РЅРµС…РІР°С‚Р°РµС‚ {500 - users[user].yen}ВҐ", keyboard_tenten)
                    break
                if users[user].inventory.max_items < 25:
                    users[user].inventory.max_items = 25
                    sender(user_id, "Р’С‹ РїСЂРёРѕР±СЂРµР»Рё Р±РѕР»СЊС€РѕР№ СЂСЋРєР·Р°Рє [-500ВҐ]", keyboard_tenten)
                    break
                sender(user_id, "РЈ РІР°СЃ СѓР¶Рµ РµСЃС‚СЊ СЌС‚РѕС‚ РїСЂРµРґРјРµС‚", keyboard_village)

            if message == "СѓР№С‚Рё":
                sender(user_id, "Р’С‹ РІРµСЂРЅСѓР»РёСЃСЊ РЅР° РіР»Р°РІРЅСѓСЋ РїР»РѕС‰Р°РґСЊ", keyboard_village)
                users[user].location = 2

        # РС‡РёСЂР°РєСѓ [10]
        if users[user].id == user_id and users[user].location == 10:

            if message == 'РёС‡РёСЂР°РєСѓ' or message == "РјРёС€Рѕ" or message == "С€СЂРёРјРї":
                if users[user].yen < 100:
                    sender(user_id, f'&#128180;Р’Р°Рј РЅРµ С…РІР°С‚Р°РµС‚ {100 - users[user].yen}ВҐ', keyboard_ramen)
                    break
                taijutsu, ninjutsu, genjutsu = users[user].taijutsu, users[user].ninjutsu, users[user].taijutsu
                if message == 'РёС‡РёСЂР°РєСѓ':
                    users[user].taijutsu = int(users[user].taijutsu * 1.2)
                    sender(user_id, '&#128074;Р’Р°С€Рµ С‚Р°Р№РґР·СЋС†Сѓ СѓРІРµР»РµС‡РёР»РѕСЃСЊ РЅР° 20%', keyboard_village)
                if message == "РјРёС€Рѕ":
                    users[user].ninjutsu = int(users[user].ninjutsu * 1.2)
                    sender(user_id, '&#11088;Р’Р°С€Рµ РЅРёРЅРґР·СЋС†Сѓ СѓРІРµР»РµС‡РёР»РѕСЃСЊ РЅР° 20%', keyboard_village)
                if message == "С€СЂРёРјРї":
                    users[user].genjutsu = int(users[user].genjutsu * 1.2)
                    sender(user_id, '&#129526;Р’Р°С€Рµ РіРµРЅРґР·СЋС†Сѓ СѓРІРµР»РµС‡РёР»РѕСЃСЊ РЅР° 20%', keyboard_village)
                sender(user_id, village_state, keyboard_village)
                users[user].location = 2
                users[user].yen -= 100
                time.sleep(300)
                users[user].taijutsu, users[user].ninjutsu, users[user].taijutsu = taijutsu, ninjutsu, genjutsu
                sender(user_id, 'Р”РµР№СЃС‚РІРёРµ СЂР°РјРµРЅР° Р·Р°РєРѕРЅС‡РёР»РѕСЃСЊ', keyboard_village)

            if message == 'СѓР№С‚Рё':
                sender(user_id, village_state, keyboard_village)
                users[user].location = 2

        if (100 * users[user].level) <= users[user].exp:
            users[user].level += 1
            users[user].point += 1
            users[user].exp = 0
            sender(user_id, f"Р’Р°С€ СѓСЂРѕРІРµРЅСЊ РїРѕРІС‹С€РµРЅ\n&#127568;РЈСЂРѕРІРµРЅСЊ {users[user].level}", keyboard_travel)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            Thread(target=execute, args=(event,), daemon=True).start()