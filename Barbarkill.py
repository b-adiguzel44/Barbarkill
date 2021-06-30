import random
import os
import time

# TO-DO List
# Hard-coded
# [DONE] Bir Enemy class tan obje türet ve sinirlet, sakinleştir hata var mı gör
# [DONE] Boss yap onu da dene
# [DONE] Ana menüyü tasarla
# [DONE] Savaş menüsünü tasarla
# [DONE] Zorluk ayarı
# [KIND OF DONE] Tur sistemi kur
# [DONE] Boss ların damage oranını ayarlar zorluğa göre
#  ---- KNOWN BUGS ----
# [BUG] Düşman ölünce saldırmaya devam ediyor bir dahaki saldırma yaptığında ölüp listeden siliniyor
# [FIXED] [BUG] Oyuncunun yüzdelik sağlık barı, maksimum can 100'ün katsayısı olmadığı zaman sapıtıyor
# [BUG] Düşmanlar her tur iyileşmiyor veya -1 iyileşiyor diye gözüküyor
# [HALF DONE] Damage leri ayarla
#

# region Other variables
AUTHOR = "b-adiguzel44"
VERSION = "0.1.2a"
PY_VERSION = "3.9.5"
WHO_IS_HARDAL = "My own very cat and he's really extremely dangerous send help"
# difficulty -- damage modifier
DIFF_MODIFIER = {0: 1.5,    # +%50
                 1: 1.2,    # +%20
                 2 : 1,     # %0
                 3: 0.2,    # -%20
                 4: 0.1}    # -%10
# endregion


# region Functions

def main_menu():
    print \
        (f'''
    WELCOME TO THE BARBARKILL GAME!
    author = {AUTHOR}
    version = {VERSION}

    DISCLAIMER : This game is still in development! Therefore, this isn't the final version. 
    Features you can see here might be changed or removed. I'm releasing this for only test purposes
    I have no intention of making fun of any race, religion or nation

   ( ͡° ͜ʖ ͡°)
    Have you ever wanted to get rid of these filthy barbarians that invaded your cities?
    But they are too powerful, and even have a technological advance over you?
    Fear no more my friend! Here, you can beat their uncivilized asses while you hang out in your terminal
    (For full experience please play in full-screen)

    Shall we get started?
    Press Enter to continue                               
    ''')


def set_up_the_game():
    '''Set up the game environment'''
    global diff
    global player
    global enemies

    while True:
        try:
            name = input("Who's this brave soldier that challanges barbarians?\n\n>> ")
            assert name != ""
            nation = input("\nWhere is he from? (Lose where? Lose where?)\n\n>> ")
            assert nation != ""
        except AssertionError:
            continue

        break

    # diff = 2  # For now
    player = You(name, nation)
    player.get_info()
    diff = choose_difficulty()

    enemies = generate_enemies(diff)
    # list_enemies(enemies)
    # input()

    terminal_clean()
    print("Game is starting!\nGet ready!")
    terminal_clean()
    # return player, enemies


def gain_experience(dodge_state, difficulty, critical_hit=0):
    '''Returns an integer depending on dodge status and difficulty'''
    if difficulty in [2, 3, 4]:
        if critical_hit == 0:
            # the enemy dodged the attack but still received damage
            if dodge_state == 0:
                return 5
            # If the enemy couldn't dodge the player's damage
            elif dodge_state != 1:
                return 15
        else:
            # the enemy dodged the attack but still received damage
            if dodge_state == 0:
                return 15
            # If the enemy couldn't dodge the player's damage
            elif dodge_state != 1:
                return 30

    else:
        if critical_hit == 0:
            # the enemy dodged the attack but still received damage
            if dodge_state == 0:
                return 15
            # If the enemy couldn't dodge the player's damage
            elif dodge_state != 1:
                return 30
        else:
            # the enemy dodged the attack but still received damage
            if dodge_state == 0:
                return 25
            # If the enemy couldn't dodge the player's damage
            elif dodge_state != 1:
                return 50

    return 10


def in_game():
    '''Actual game is happening in this function'''
    global dodge_chances
    global killed_enemies
    killed_enemies = {}
    dodge_chances = [-1, 0, 1]
    is_player_dead = False  # False means the game continues
    # All enemies are alive and the player is still alive
    while enemies and not is_player_dead:

        # Let the player choose what to do (Send the enemy list)
        isdead = actions(enemies)
        input("\nPress Enter the continue\n")

        # If the unit dies
        if isdead:
            print(str(5 * '*') + " Congratz! You killed the enemy onto the next one! " + str(5 * '*'))
            player.gaining_xp(50)
            if enemies[0].status != 3:
                # Counting how many enemies have been killed
                killed_enemies.setdefault(enemies[0].name.split("_")[0], 0)
                killed_enemies[enemies[0].name.split("_")[0]] += 1
            else:
                # Counting how many bosses have been killed
                killed_enemies.setdefault(enemies[0].name.split("-")[1], 0)
                killed_enemies[enemies[0].name.split("-")[1]] += 1

            del enemies[0]
            Enemy.decrease_the_num_of_enemies()
        # If the unit is still alive / dodges the unit / Choose to do nothing (Equals to None)
        else:
            print(str(30*'*'))
            is_player_dead = enemy_turn(enemies)
        input("\n\nPress Enter the continue\n")
        terminal_clean()


def terminal_clean():
    '''İşletim sistemine göre terminaldeki ekranı temizler'''
    if os.name == 'nt':
        os.system('cls')   # Terminal ekranını temizler (Windows için)
    elif os.name == 'posix':
        os.system('clear')  # Terminal ekranını temizler (Linux için)


def game_over():
    '''When you die'''
    print("You've lost!")
    return True


def generate_enemies(difficulty, count=10):
    '''Generates random enemie & bosses'''

    #  Generating random enemies & bosses & enemy behaviour depending on difficulty
    if difficulty == 0:     # Very Easy
        enemies = [Enemy(random.choice(Enemy.get_names_keys()),
                    random.choice(Enemy.healths[difficulty]), difficulty)
                   for i in range(5)]
        player.dmg += round(player.dmg * DIFF_MODIFIER[difficulty])

    elif difficulty == 1:    # Easy
        enemies = [Enemy(random.choice(Enemy.get_names_keys()),
                     random.choice(Enemy.healths[difficulty]), random.randint(0, 1))
               for i in range(10)]
        enemies[4].become_a_boss(difficulty)
        enemies[9].become_a_boss(difficulty)
        player.dmg += round(player.dmg * DIFF_MODIFIER[difficulty])
    elif difficulty == 2:   # Normal
        enemies = [Enemy(random.choice(Enemy.get_names_keys()),
                         random.choice(Enemy.healths[difficulty]), random.randint(0, 2))
                   for i in range(15)]
        enemies[4].become_a_boss(difficulty)
        enemies[9].become_a_boss(difficulty)
        enemies[14].become_a_boss(difficulty)
    elif difficulty == 3:   # Hard
        enemies = [Enemy(random.choice(Enemy.get_names_keys()),
                         random.choice(Enemy.healths[difficulty]), random.randint(1, 2))
                   for i in range(20)]
        enemies[4].become_a_boss(difficulty)
        enemies[9].become_a_boss(difficulty)
        enemies[14].become_a_boss(difficulty)
        enemies[19].become_a_boss(difficulty)
        player.dmg += round(player.dmg * DIFF_MODIFIER[difficulty])
    else:                   # Extremely Hard
        enemies = [Enemy(random.choice(Enemy.get_names_keys()),
                         random.choice(Enemy.healths[difficulty]), 2)
                   for i in range(30)]
        for i in range(19, 30):
            enemies[i].become_a_boss(difficulty)
        # enemies[29].become_a_super_boss() --> just tested this for become_A_super_boss method
        player.dmg += round(player.dmg * DIFF_MODIFIER[difficulty])


    # Listing the enemies (for to visualize)
    # for i, j in enumerate(enemies):
    #      print((i+1), ") ", j.name + "\nHP : " + str(j.hp) + "\nDmg : " + str(j.dmg)+"\nStatus : "+ str(j.status))
    # print(f"{difficulty} difficulty for player's dmg : {player.dmg}")

    return enemies


def list_enemies(list_of_enemy):
    '''Takes a list of instances of Enemy class and prints their attirubute'''
    try:
        for i, j in enumerate(list_of_enemy):
            print((i + 1), ") ", j.name + "\nHP : " + str(j.hp) + "\nDmg : " + str(j.dmg) + "\nStatus : "
                  + str(j.status))
    except TypeError:
        print("Expecting a list of Enemy class instances")


def actions(list_of_enemies):
    '''Decide what to do (Player action menu)'''
    terminal_clean()
    if player.hp == player.max_hp:
        # No need to heal
        state_of_hp = "(Full)"
    else:
        # Might heal himself
        state_of_hp = ""

    print(f"{list_of_enemies[0].name} has shown up!")
    print(f'''\nChoose the following
    1 - Attack ⚔ 
    2 - Heal Up {state_of_hp}
    3 - Critical Chance 
    4 - Show Your Current Enemy Info 
    5 - Show Your Info 
    6 - How many enemies left?
    7 - Exit (Closes the game)\n''')

    while True:
        try:
            action = int(input(">> "))
            if action not in [1, 2, 3, 4, 5, 6, 7]:
                raise ValueError
            break
        except ValueError:
            continue

    print(f"You chose {action}")
    if action in [1, 2, 3]:

        # Deciding the dodge status for enemy randomly
        dodge_state = random.choice(dodge_chances)

        if action == 1:
            damage_output = int(player.dmg + (1 - (DIFF_MODIFIER[diff] / 100)))
            # Returns True if an unit dies, false if an unit is still alive
            result = list_of_enemies[0].damaged(damage_output, dodge_state)

            # Player gaining XP based on the difficulty and dodge status
            player.gaining_xp(gain_experience(dodge_state, diff))

            return result

        elif action == 2 and state_of_hp == "":
            if player.level != 0:
                healing_factor = (player.level * 10) + int(DIFF_MODIFIER[diff])
            else:
                healing_factor = 30
            player.healed(healing_factor)

        elif action == 3:
            critical_hit = random.randint(1, 100)
            print(f"You're going to try your luck to hit a critical hit\n"
                  f"Your chances of getting a critical crit : %{critical_hit}")
            input("\nPress Enter the continue\n")
            damage_output = round(player.dmg * (critical_hit / 10))
            result = list_of_enemies[0].damaged(damage_output, dodge_state)
            player.gaining_xp(gain_experience(dodge_state, diff, 1))
            return result
        else:
            print("You don't need a healing right now")
            input("\nPress Enter the continue\n")
            actions(list_of_enemies)
    # Information related actions [That means player's turn shouldn't be ended here and ask his decision again
    else:
        terminal_clean()
        if action == 4:
            # 0 all the time because when an unit dies we delete them from the list
            print(list_of_enemies[0].get_info())
        elif action == 5:
            player.get_info()
        elif action == 6:
            print(Enemy.how_many_enemies(), "\n")
        elif action == 7:
            terminal_clean()
            print("Thanks for playing!")
            exit(0)

        # Proceed to ask again
        input("\nPress Enter the continue\n")
        return actions(list_of_enemies)


def enemy_turn(list_of_enemies):
    '''Determines what enemy does in their turn'''
    print(f"Now it's {list_of_enemies[0].name} turn! Brace yourself")

    # If It's a boss
    if list_of_enemies[0].status == 3 and diff >= 3:
        list_of_enemies[0].healed(int((1-DIFF_MODIFIER[4-diff]) * 1.2))
    elif diff >= 3:
        list_of_enemies[0].healed(int((1-DIFF_MODIFIER[4-diff]) * 1.05))

    # Non-boss attacks
    if list_of_enemies[0].status != 3:
        flag = player.damaged(list_of_enemies[0].dmg, random.choice(dodge_chances))
    else:
        flag = player.damaged(int(list_of_enemies[0].dmg + (1-DIFF_MODIFIER[4-diff])), random.choice(dodge_chances))
    if flag:
        return game_over

    # If you got attacked and healing the player (on Very easy and Easy difficulties)
    if flag is not None and diff in [0, 1]:
        if player.level == 0:
            player.healed(20)
        else:
            player.healed(10)


def choose_difficulty():
    '''Player chooses a difficuly that alters the game mechanics'''
    terminal_clean()
    print(f'''\nChoose difficulty:
        0 - Very easy
        1 - Easy
        2 - Normal
        3 - Hard
        4 - Extremely Hard
        ''')
    while True:
        try:
            diff = int(input(">> "))
            if diff not in [0, 1, 2, 3, 4]:
                raise ValueError
            return diff
        except ValueError:
            continue

# endregion

# region Classes


class Humanity:

    _lists_of_death = ["has been slayed", "has been killed", "has been backstabbed",
                       "cried to death", "KGB'd",
                       "has been devoured by sharp teethed hungry cannibals",
                       "fell to his/her death while fighting",
                       "electrocuted", "ate a banana and angered monkeys ate him/her",
                       "had a stroke", "was hunter'd by Hardal", "bled to death due to his/her wounds"]

    _lists_of_healing = ["had a personal time with KGB", "his/her called mom", "has been exercising",
                         "ate a pineapple pie", "won an argument over a Greek person",
                         "loved the every second of spent his/her time with men",
                         "found his god", "beat a 'MAP'",
                         "petted its cat", "ate a banana while monkeys were asleep"]

    _lists_of_attack = ["got shot in the face", "was stabbed in the neck",
                        "was attacked by an angered monke",
                        "choked on opponent's handbag",
                        "was scratched by Hardal", "was impaled through the chest",
                        "got punched", "was poked in the eyes", "was forced to drink an acid",
                        "had to listen Cultured's high-school story for the 500th time",
                        "was tore down by a M60 machine gun"]

    _lists_of_defending = ["used his/her shield", "wore his/her facemask", "hid in the bush",
                           "got inside of a tank", "got behind his doctor", "jumped to the ground",
                           "disguised as a governor", "took the vitamin pills the mom gave",
                           "got inside a tunnel", "got in cover"]

    def __init__(self, name, hp):
        '''Sets the name and HP for everyone'''
        self.name = name
        self.hp = hp

    def get_info(self):
        return f"Type : {self.name}\nHP : {str(self.hp)} ♥"

    def damaged(self, dmg, dodged=-1):
        '''When an unit gets attacked (If the unit dies returns true otherwise false)'''
        # dodged ( 0 : Failed, 1 : Succesfull, -1 : No protection)
        # Dodge unsuccesful / Defend yourself failed but still receieve the half of the damage
        if dodged == 0:
            dmg //= 2
            self.hp -= dmg
            quote = f"{self.name} {random.choice(Humanity._lists_of_defending)} but"
        # Dodge succcesful / Defend yourself sucessful
        elif dodged == 1:
            print(f"{self.name} {random.choice(Humanity._lists_of_defending)} and succesfully avoided the damage!")
            return False
        # No protection
        else:
            self.hp -= dmg
            quote = self.name
        # How many damages the unit had taken
        print(f"{quote} {random.choice(Humanity._lists_of_attack)} that inflicted {dmg} damage(s)")
        # When you die, what happens
        if self.hp < 0 or self.hp == 0:
            death_by = random.choice(Humanity._lists_of_death)
            print(f"☠ --- {self.name} {death_by} --- ☠")
            return True
        else:
            print(f"{self.name} has {self.hp} HP left")
            # THe unit is till alive
            return False


    def healed(self, multiplier):
        '''When an unit heals up'''
        # If the unit is not dead or something
        if self.hp > 0:
            self.hp += multiplier
            print(f"{self.name} {random.choice(Humanity._lists_of_healing)} and that gives him/her {multiplier} HP")
            return f"{self.name} {random.choice(Humanity._lists_of_healing)} and that gives him/her {multiplier} HP"
        else:
            print("You are dead, not big souprise")


class You(Humanity):

    def __init__(self, name, nation, hp=100):

        super().__init__(name, hp)
        if nation == "Greek":
            self.nation = "Cultured"

        self.xp = 0
        self.max_hp = hp
        self.nation = nation
        self.level = 0
        self.dmg = 20

    def increase_max_hp(self, multiplier):
        # Increase the max HP
        self.max_hp += multiplier
        # Set the current HP to max HP
        self.hp = self.max_hp
        print(f"{self.name}'s max HP has been increased by {multiplier}")

    def get_info(self):

        # region Health Bar percentage design
        # Source = https://stackoverflow.com/questions/48035367/python-text-game-health-bar
        percent = int((self.hp/self.max_hp)*100)
        # endregion
        xp_status = f"{self.xp}/100"
        if self.level <= 5:
            _title = "Rookie"
        elif self.level <= 10:
            _title = "Warrior"
        elif self.level <= 14:
            _title = "Protector"
        else:
            _title = "Barbarian Slayer"
            self.xp = 100
            xp_status = f"MAX"
        print(f'''{str(30*'*')}\n{str(7*'*')} GENERAL STATS {str(8*'*')}
>>   Name = {self.name} 
>>   HP = {str(self.hp)}/{str(self.max_hp)} ♥
>>   Strength = {self.dmg} 💪
>>   Nation = {self.nation}

Level {self.level} - {_title} ✪ 
[{str( '#' * self.xp ) + str('_'*(100-self.xp))}] {xp_status}

Health Percentage - ♥
[{str(percent * '#') + str((100-percent) * '_')}] {percent}%
''')


    # Player healing up
    def healed(self, multiplier):
        # Parent Class called
        quote = super().healed(multiplier)
        # Already at maximum health?
        if self.hp == self.max_hp:
            # Set to max HP lmfao
            return "Who do you think you are? A medic? You can't overheal yourself."
        else:
            # Overhealing?
            if (multiplier + self.hp) >= self.max_hp:
                # Set current HP to max HP
                self.hp = self.max_hp
                return quote + " (Overhealed)"
            # No? Then do this
            else:
                self.hp += multiplier
            return quote

    # Player gaining XP, increasing max HP cap, increasing strength etc.
    def gaining_xp(self, experience):
        '''Player getting level up and gaining xp'''
        def adjust_settings():
            # Increase your strength
            self.dmg += 15
            # Increase max HP
            self.increase_max_hp(10*self.level)

        # When you reached the max level, you don't need to see this info
        if self.level != 15:
            print(f"You've gained {experience} XP!")
        if experience >= 100 and self.level != 15:
            # Level up
            self.level += round(experience / 100)
            adjust_settings()
            # Readjust the XP bar
            self.xp += experience % 100
            if self.xp >= 100:
                self.xp = experience % 100
                print(f"You're leveled up! -- Level {self.level}")
        elif self.level == 15:
            self.xp = 100
            print("You're max level thus you cannot level up anymore")
        else:
            if (self.xp + experience) >= 100:
                # Set XP bar to zero
                self.xp = (self.xp + experience) - 100
                # Level up
                self.level += 1
                adjust_settings()
                print(f"You're leveled up! -- Level {self.level}")
            else:
                self.xp += experience


    # Cheat code (Hard-coded)
    def set_health_and_dmg(self, hp, dmg):
        '''Sets player's HP and damage'''
        self.hp = hp
        self.dmg = dmg


class Enemy(Humanity):
    '''Enemy behaviours, their strength etc.'''

    # Possible random enemy types
    names = {"Barbarian" : 1,
             "Pirate" : 1,
             "Terrorist" : 1,
             "Barbarian Supporter" : 1,
             "Corrupt Politician" : 1,
             "Br't'sh" : 1,
             "Viking" : 1
             }
    # Enemies health modifier depending on the difficulty
    healths = {0 : [50, 75, 100],       # I can fight
               1 : [100, 150, 200],     # Challenge with the big bois
               2 : [175, 250, 325],     # I'm more mightier than you think
               3 : [200, 350, 600],     # I wanna fight to the death
               4 : [300, 600, 800]}     # Mom pick me up please!
    # Enemies damage modifier depending on the difficulty
    _damages = {
                0 : [5, 10, 15, 20, 25],
                1 : [20, 25, 30, 35, 40],
                2 : [50, 55, 60, 65, 70],
                3 : [60, 65, 70, 75, 80],
                4 : [65, 70, 75, 80, 85]
                }
    # Counts how many enemies in the game
    _count = 0
    # Enemy status
    _dict_status = { 0: "Weak",
                     1: "Normal",
                     2: "Agressive",
                     3: "BOSS",
                     4: "SUPER BOSS"}

    def __init__(self, name="Barbarian", hp=100, status=0):
        # Initialize the Enemy class
        super().__init__(name, hp)

        # Adding suffix counts depending on how many of them are exist such as Barbarian_1, Pirate_3
        if name in Enemy.names:
            self.name = name + '_' + str(Enemy.names[name])
            Enemy.names[name] += 1
        self.status = status
        Enemy._count += 1

        # Set every enemies' damage multiplier depending on their status
        # Afraid
        if self.status == 0:
            self.dmg = random.choice(Enemy._damages[diff])
        # Normal
        elif self.status == 1:
            self.dmg = random.choice(Enemy._damages[diff])
            self.dmg += 10
        # Agressive
        elif self.status == 2:
            self.dmg = random.choice(Enemy._damages[diff])
            self.dmg += 15
        # BOSS
        elif self.status == 3:
            self.dmg = round(80 * DIFF_MODIFIER[diff])

    def angered(self):
        '''When an enemy unit gets angered'''
        # An enemy unit cannot become a boss and BOSS cannot be angered
        if (self.status+1) != 3 and self.status != 3:
            self.status += 1
            self.dmg += 25
            return f"{self.name} gets angry! Be careful!"

    def calmed(self):
        '''When an enemy unit gets chill'''
        # BOSS cannot be lowered neither the lower status ones
        if self.status != 3 and (self.status-1) != -1:
            self.status -= 1
            self.dmg -= 25
            return f"{self.name} gets calmed down! Get ready to strike!"

    def become_a_boss(self, diff):
        '''Makes an enemy unit into a boss'''
        # Find the index of "_" & split, append " BOSS()" into the first element of that list
        self.name = self.name.split("_")[0] + "-(BOSS)"
        self.hp = Enemy.healths[diff][2]
        self.dmg = Enemy._damages[diff][4]
        if diff != 2:
            self.hp += round(self.hp * DIFF_MODIFIER[4 - diff])
            self.dmg += round(self.dmg * DIFF_MODIFIER[4 - diff])
        else:   # Normal Difficulty (DIFF_MODIFIER has 0)
            self.hp += random.choice(Enemy.healths[diff])
            self.dmg += random.choice(Enemy._damages[diff])
        self.status = 3

    # This method will be used later (Unused right now)
    def become_a_super_boss(self):
        '''Makes an enemy unit into a super boss'''
        self.name = self.name.split("_")[0] + "-(SUPER BOSS)"
        self.hp = Enemy.healths[4][2] * 5
        self.dmg = Enemy._damages[4][4] * 5
        self.status = 4                   # Title becomes (SUPER BOSS)

    def get_info(self):
        '''Displays the enemy unit's general info'''
        quote = super().get_info()
        return f"{quote}\nStrength : {self.dmg} 💪\nStatus : {Enemy._dict_status[self.status]}"

    @classmethod
    def get_names_keys(cls):
        '''returns a list of the keys of names dictionary'''
        return list(cls.names.keys())

    @classmethod
    def how_many_enemies(cls):
        '''Checking how many enemies are there'''
        if cls._count == 0:
            return "There is no enemy"
        elif cls._count > 1:
            return "There are " + str(cls._count) + " enemies available"
        else:
            return "There is only one enemy available"

    @classmethod
    def decrease_the_num_of_enemies(cls):
        '''When an enemy unit gets killed, decrease the sum of enemies'''
        cls._count -= 1
        return "An enemy unit has been killed"


# endregion

# region Main Program


if __name__ ==  "__main__":
    terminal_clean()
    main_menu()
    input()
    # Sets up a game (creating a player, generating enemies, choosing difficulty etc.)
    set_up_the_game()
    # list_enemies(enemies)
    in_game()
    print("Congratz! You won the game (or lost the game)")
    if killed_enemies:
        print(f"{str('-' * 5)} Total killed enemies {str('-' * 5)}")
        for key, value in killed_enemies.items():
            print(key, "--", value)
        print(f"Total killed enemies : {len(killed_enemies)}")

    # # Gonna run this loop until the enemies list gets deleted
    # while enemies:
    #     for j in enemies:
    #         if j.damaged(100):
    #             del j
    #             Enemy.decrease_the_num_of_enemies()

# endregion