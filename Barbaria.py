import random
from Barbarkill import DIFF_MODIFIER    # <--- Dict variable

# region Classes


class People:

    # region Class attributes & variables
    _lists_of_death = ("has been slayed", "has been killed", "has been backstabbed",
                       "cried to death", "KGB'd", "has burnt to death   ",
                       "has been devoured by sharp-toothed hungry cannibals",
                       "fell to his/her death while fighting", "was shot in the heart"
                       "electrocuted", "ate a banana and a group of angered monkeys punched him/her to death!",
                       "had a stroke", "was attacked by Hardal", "bled to death due to his/her wounds")

    _lists_of_healing = ("had a personal time with KGB", "his/her called mom", "has been exercising",
                         "ate a pineapple pie", "won an argument against a corrupt politician",
                         "loved the every second of spent his/her time with ducks",
                         "found his family doctor", "beat a 'MAP'",
                         "had enough, and left the game for an hour",
                         "petted its cat", "ate a banana while monkeys were asleep")

    _lists_of_attack = ("got shot in the face", "was stabbed in the neck",
                        "was attacked by a group of angered monkeys",
                        "was force-choked", "was hit by a Honda Civic 2004",
                        "was scratched by Hardal", "was impaled through the chest",
                        "got punched", "was poked in the eyes", "was forced to drink an acid",
                        "had to listen his/her friend's high-school story for the 500th time",
                        "was tore down by a M60 machine gun")

    _lists_of_defending = ("used his/her shield", "wore his/her facemask", "hid in the bush",
                           "got inside of a tank", "got behind his doctor", "jumped to the ground",
                           "disguised as a governor", "took the vitamin pills the mom gave",
                           "got inside a tunnel", "got in cover", "had the high ground",
                           "wore his/her bullet-proof vest")
    # endregion

    def __init__(self, name, hp):
        """Sets the name and HP for everyone"""
        self.name = name
        self.hp = hp

    # region Instance Methods
    def get_info(self):
        return f"Type : {self.name}\nHP : {str(self.hp)} ♥"

    def damaged(self, dmg, dodged=-1):
        """When an unit gets attacked (If the unit dies returns true otherwise false)"""
        # dodged ( 0 : Failed(still receieve damage), 1 : Succesfull, -1 : No protection)
        # Dodge unsuccesful / Defend yourself failed but still receieve the half of the damage
        if dodged == 0:
            dmg //= 2
            self.hp -= dmg
            quote = f"🛡  >> ️{self.name} {random.choice(People._lists_of_defending)} but"
        # Dodge succcesful / Defend yourself sucessful
        elif dodged == 1:
            print(f"🛡️  >> {self.name} {random.choice(People._lists_of_defending)} and succesfully avoided the damage!")
            return False
        # No protection
        else:
            self.hp -= dmg
            quote = f"⚔️  >> {self.name}"
        # How many damages the unit had taken
        print(f"{quote} {random.choice(People._lists_of_attack)} that inflicted {dmg} damage(s)")
        # When you die, what happens
        if self.hp < 0 or self.hp == 0:
            death_by = random.choice(People._lists_of_death)
            print(f"☠ --- {self.name} {death_by} --- ☠")
            return True
        else:
            print(f"{self.name} has {self.hp} HP left")
            # THe unit is till alive
            return False

    def healed(self, multiplier):
        """When an unit heals up"""
        # If the unit is not dead or something
        if self.hp > 0:
            self.hp += multiplier
            print(f" ➕ -- {self.name} {random.choice(People._lists_of_healing)} "
                  f"and that gives him/her {multiplier} HP -- ➕")
        else:
            print("You are dead, not big souprise")
    # endregion


class Player(People):

    def __init__(self, name, nation, hp=100):

        super().__init__(name, hp)
        self.xp = 0
        self.max_hp = hp
        self.level = 0
        self.dmg = 20

        if nation == "Greek":
            self.nation = "Cultured"
        elif nation == "Cultured":
            self.nation = "Greek"
        elif nation == "GYPSY":
            self.nation = nation
            self.set_player_stats(1150, 250)
        elif nation == "Turkey":
            self.nation = "Turkish"
            self.set_player_stats(1000, 175)
        elif nation == "Pihaş":
            self.nation = "Monkey Tribal"
            self.set_player_stats(125, 100)
        elif nation == "KGB":
            self.nation = "Unknown"
            self.set_player_stats(1, 1500)
        else:
            self.nation = nation

    # region Instance Methods
    def increase_max_hp(self, multiplier):
        # Increase the max HP
        self.max_hp += multiplier
        # Set the current HP to max HP
        self.hp = self.max_hp
        print(f"{self.name}'s max HP has been increased by {multiplier}")

    def get_info(self):

        percent = round((self.hp/self.max_hp) * 100, 1)
        percent_bar = int(percent)
        if percent <= 40.0:
            percent = str(percent) + "% [CRITICAL]"
        else:
            percent = str(percent) + "%"
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
[{str(percent_bar * '#') + str((100-percent_bar) * '_')}] {percent}
''')

    # Player healing up
    def healed(self, multiplier):
        # Parent Class called
        super().healed(multiplier)
        # Already at maximum health?
        if self.hp == self.max_hp:
            # Set to max HP lmfao
            print("Who do you think you are? A medic? You can't overheal yourself.")
        else:
            # Overhealing?
            if (multiplier + self.hp) >= self.max_hp:
                # Set current HP to max HP
                self.hp = self.max_hp

    # Player gaining XP, increasing max HP cap, increasing strength etc.
    def gain_xp(self, experience):
        """Player getting level up and gaining xp"""
        def adjust_settings():
            # Increase your strength
            self.dmg += 15
            # Increase max HP
            self.increase_max_hp(10 * self.level)

        # When you reached the max level, you don't need to see this info
        if self.level != 15:
            print(f"You've gained {experience} XP!")
        if experience >= 100 and self.level != 15:
            # Level up
            self.level += round(experience / 100)
            adjust_settings()
            # Re-adjust the XP bar
            self.xp += experience % 100
            if self.xp >= 100:
                self.xp = experience % 100
                print(f"You're leveled up! -- Level {self.level}")
        elif self.level == 15:
            self.xp = 100
            # print("You're max level thus you cannot level up anymore")
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
    def set_player_stats(self, max_hp, dmg, level=15):
        """Sets player's HP and damage"""
        self.max_hp, self.hp, self.dmg, self.level = max_hp, max_hp, dmg, level
    # endregion


class Enemy(People):
    """Enemy behaviours, their strength etc."""

    # region Class variables & attributes

    # Class attribute for getting difficulty from the user
    _diff = None

    # Possible random enemy types
    _names = {
              "Barbarian": 1,
              "Pirate": 1,
              "Thug": 1,
              "Angler": 1,
              "Corrupt Politician": 1,
              "Barbarian Supporter": 1,
              "Viking Barbarian": 1
              }

    # Enemies health modifier depending on the difficulty
    _healths = {
                0: [50, 75, 100],      # Very Easy
                1: [100, 150, 200],    # Easy
                2: [175, 250, 325],    # Normal
                3: [200, 350, 600],    # Hard
                4: [300, 600, 800]     # Extremely Hard
                }
    # Enemies damage modifier depending on the difficulty
    _damages = {
                0: [5, 10, 15, 20, 25],         # Very Easy
                1: [20, 25, 30, 35, 40],        # Easy
                2: [50, 55, 60, 65, 70],        # Normal
                3: [60, 65, 70, 75, 80],        # Hard
                4: [65, 70, 75, 80, 85]         # Extremely Hard
                }
    # Counts how many enemies in the game
    _count = 0
    # Enemy status
    _dict_status = {
                     0: "Weak",
                     1: "Normal",
                     2: "Agressive",
                     3: "BOSS",
                     4: "SUPER BOSS"
                   }

    # endregion

    def __init__(self, name="Barbarian", hp=125, status=1, difficulty=2):
        # Initialize the Enemy class
        super().__init__(name, hp)

        _diff = difficulty
        # If parameter name doesn't exist in _names dict, add the parameter as a key and set the value to 1
        # If the player wants to include custom names into the _names dict
        if name not in Enemy._names:
            Enemy._names.setdefault(name, 1)

        # Adding suffix counts depending on how many of them are exist such as Barbarian_1, Pirate_3
        self.name = name + '_' + str(Enemy._names[name])
        Enemy._names[name] += 1

        self.status = status
        Enemy._count += 1

        # Set every enemies' damage multiplier depending on their status
        # Afraid
        if status == 0:
            self.dmg = random.choice(Enemy._damages[_diff])
        # Normal
        elif status == 1:
            self.dmg = random.choice(Enemy._damages[_diff])
            self.dmg += 10
        # Agressive
        elif status == 2:
            self.dmg = random.choice(Enemy._damages[_diff])
            self.dmg += 15
        # BOSS
        elif status == 3:
            self.become_a_boss(_diff)
            # self.dmg = round(125 * (1 - DIFF_MODIFIER[diff]))

    # region Instance Methods
    def angered(self):
        """When an enemy unit gets angered"""
        # An enemy unit cannot become a boss and BOSS cannot be angered
        if (self.status+1) != 3 and self.status not in [3, 4]:
            self.status += 1
            self.dmg += 50
            return f"{self.name} gets angry! Be careful!"
        return ''

    def calmed(self):
        """When an enemy unit gets chill"""
        # BOSS cannot be lowered neither the lower status ones
        if self.status not in [3, 4] and (self.status-1) != -1:
            self.status -= 1
            self.dmg -= 25
            return f"{self.name} gets calmed down! Get ready to strike!"
        return ''

    def become_a_boss(self, _diff):
        """Makes an enemy unit into a boss"""
        # Find the index of "_" & split, append " BOSS()" into the first element of that list
        self.name = self.name.split("_")[0] + "-(BOSS)"
        self.hp = Enemy._healths[_diff][2]
        self.dmg = Enemy._damages[_diff][4]
        if _diff != 2:
            self.hp += round(self.hp * DIFF_MODIFIER[4 - _diff])
            self.dmg += round(self.dmg * DIFF_MODIFIER[4 - _diff])
        else:   # Normal Difficulty (DIFF_MODIFIER has 0)
            self.hp += random.choice(Enemy._healths[_diff])
            self.dmg += random.choice(Enemy._damages[_diff])
        self.status = 3

    # This instance method will be used later (Unused right now)
    def become_a_super_boss(self):
        """Makes an enemy unit into a super boss"""
        self.name = self.name.split("_")[0] + "-(SUPER BOSS)"
        self.hp = Enemy._healths[4][2] * 5
        self.dmg = Enemy._damages[4][4] * 5
        self.status = 4                   # Title becomes (SUPER BOSS)

    def get_info(self):
        """Displays the enemy unit's general info"""
        quote = super().get_info()
        return f"{quote}\nStrength : {self.dmg} 💪\nStatus : {Enemy._dict_status[self.status]}"
    # endregion

    # region Class Nethods
    @classmethod
    def get_names_keys(cls):
        """Returns a list of the keys of _names dictionary"""
        return list(cls._names.keys())

    @classmethod
    def get_health_value(cls, key):
        """Returns the value of the given parameter key from _healths dictionary"""
        return cls._healths[key]

    @classmethod
    def how_many_enemies(cls):
        """Checking how many enemies are there"""
        if cls._count == 0:
            return "There is no enemy"
        elif cls._count > 1:
            return "There are " + str(cls._count) + " enemies available"
        else:
            return "There is only one enemy available"

    @classmethod
    def decrease_the_num_of_enemies(cls):
        """When an enemy unit gets killed, decrease the sum of enemies"""
        cls._count -= 1
        return "An enemy unit has been killed"

    @classmethod
    def reset_total_enemies(cls):
        """Resets the necessary class attributes in case player wants to replay again"""
        cls._count = 0
        # Reset the names dict count
        for name in Enemy._names.keys():
            Enemy._names[name] = 1
    # endregion

# endregion
