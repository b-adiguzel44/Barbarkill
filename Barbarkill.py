import os
# import gc
import numpy as np
from Barbaria import *


# region Other variables

AUTHOR = "b-adiguzel44"
VERSION = "1.0.0"          # prev version = 0.1.2a (released in github)
PY_VERSION = "3.9.6"
WHO_IS_HARDAL = "My own very cat and he's really extremely dangerous send help"
# difficulty -- damage modifier
DIFF_MODIFIER = {0: 1.50,    # +%50
                 1: 1.20,    # +%20
                 2: 1.0,     # %0
                 3: 0.20,    # -%20
                 4: 0.10}    # -%10

defeat_quote = ("Next time eat your vegetables", "Gonna cry?", "You barbarian lover!",
                "Git gud", "You're weak!", "God always side with the mighty people")

victory_quote = ("You're the best player!", "Are you sure you're not cheating?",
                 "Outstanding move!", ":OOOOOOOOO", "Good playthrough mate!", "Well played!")

one_time = False

# endregion

# region Functions


def main_menu():
    print(f'''
    WELCOME TO THE BARBARKILL GAME!
    author = {AUTHOR}
    version = {VERSION}

    DISCLAIMER : This game is still in development! Therefore, this isn't the final version. 
    Features you can see here might be changed or removed. I have no intention of making fun of any race, 
    religion or nation at all.

    ---------  Based on my hatred aganist barbarians in Sid Meier's Civilization series ---------
    Have you ever wanted to get rid of these filthy barbarians that invaded your cities?
    But they are too powerful, and even have a technological advance over you?
    Fear no more my friend! Here, you can beat their uncivilized arses while you hang out in your terminal
    (For full experience please play in full-screen)

    Shall we get started?
    Press Enter to continue                               
    ''')


def set_up_the_game():
    """Set up the entire game environment"""
    global diff, player, enemies, gmode

    # isspace() = Returns True if string only consists of whitespace -> " "
    while True:
        try:
            name = input("Who's this brave soldier that challanges barbarians?\n\n>> ")
            nation = input("\nWhere is this brave soldier from?\n\n>> ")
            # If any of those conditions below are true, ask for valid input
            if (name == "" or name.isspace() or name.isnumeric() or len(name) > 25) or \
               (nation == "" or nation.isspace() or nation.isnumeric() or len(nation) > 25):
                raise AssertionError
        except AssertionError:
            terminal_clean()
            s = '\\'
            print(f"{str('/')*5} Character length exceeded over (limit 25) or Invalid input {str(s)*5}")
            continue

        break

    name = name.strip()
    nation = nation.strip()
    player = Player(name, nation)
    gmode = choose_mode()
    diff = choose_difficulty()
    enemies = generate_enemies(diff, gmode)

    terminal_clean()


def choose_mode():
    """Player chooses a game mode"""
    terminal_clean()
    print(f'''\nChoose game-mode:
            1 - Classic Mode
            2 - Survival Mode - (Kill barbarians till you die)
            3 - Boss Run Mode [Not Available]
            ''')
    while True:
        try:
            g_mode = int(input(">> "))
            if g_mode not in [1, 2]:
                raise ValueError
            return g_mode
        except ValueError:
            return choose_mode()


def choose_difficulty():
    """Player chooses a difficuly that alters the game mechanics"""
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
            difficulty = int(input(">> "))
            if difficulty not in [0, 1, 2, 3, 4]:
                raise ValueError
            return difficulty
        except ValueError:
            return choose_difficulty()


def generate_enemies(difficulty, mode=1):
    """Generates random enemies & bosses and returns a list of those said enemies"""
    global one_time  # <--- Boosts once player's dmg
    global enemies

    # Classic Mode
    if mode == 1:
        # Generating random enemies & bosses & enemy behaviour depending on difficulty
        if difficulty == 0:  # Very Easy
            enemies = [Enemy(random.choice(Enemy.get_names_keys()),
                       random.choice(Enemy.get_health_value(difficulty)), difficulty, difficulty)
                       for _ in range(5)]
        elif difficulty == 1:  # Easy
            enemies = [Enemy(random.choice(Enemy.get_names_keys()),
                       random.choice(Enemy.get_health_value(difficulty)), random.randint(0, 1), difficulty)
                       for _ in range(10)]
            enemies[4].become_a_boss(difficulty)
            enemies[9].become_a_boss(difficulty)
        elif difficulty == 2:  # Normal
            enemies = [Enemy(random.choice(Enemy.get_names_keys()),
                       random.choice(Enemy.get_health_value(difficulty)), random.randint(0, 2), difficulty)
                       for _ in range(15)]
            enemies[4].become_a_boss(difficulty)
            enemies[9].become_a_boss(difficulty)
            enemies[14].become_a_boss(difficulty)
        elif difficulty == 3:  # Hard
            enemies = [Enemy(random.choice(Enemy.get_names_keys()),
                       random.choice(Enemy.get_health_value(difficulty)), random.randint(1, 2), difficulty)
                       for _ in range(20)]
            enemies[4].become_a_boss(difficulty)
            enemies[9].become_a_boss(difficulty)
            enemies[14].become_a_boss(difficulty)
            enemies[19].become_a_boss(difficulty)
        else:  # Extremely Hard
            enemies = [Enemy(random.choice(Enemy.get_names_keys()),
                       random.choice(Enemy.get_health_value(difficulty)), 2, difficulty)
                       for _ in range(30)]
            for i in range(20, 30):
                enemies[i].become_a_boss(difficulty)
            # enemies[29].become_a_super_boss() --> just tested this for become_A_super_boss method
    # Survival Mode (Generating enemies randomly until the player is dead)
    elif mode == 2:
        enemies = [Enemy(random.choice(Enemy.get_names_keys()), 
                         random.choice(Enemy.get_health_value(difficulty)), random.randint(0, 3), difficulty)]

    # Setting player's damage modifier depending on the difficulty ONCE!
    # This function gets called infinitely in Survival mode  [FIXED]
    if not one_time:
        player.dmg += round(player.dmg * DIFF_MODIFIER[difficulty])
        one_time = True
    
    return enemies


def count_kills(enemy):
    """Counts player's kills till the game over"""
    if enemy.status != 3:
        # Counting how many enemies have been killed
        # Key word : 'Barbarian/Corrupt Politican'
        # Default -> Key : "Barbarian" : 0
        killed_enemies.setdefault(enemy.name.split("_")[0], 0)
        killed_enemies[enemy.name.split("_")[0]] += 1
    else:
        # Counting how many bosses have been killed
        # Key word : 'BOSS' (gets rids of paranthesises, '-' character and so on)
        # Default -> Key : "BOSS" : 0
        # Clipping the name attribute for given an instance of Enemy class (Substringing)
        key = enemy.name.split("-")[1][enemy.name.split("-")[1].index("(")+1:enemy.name.split("-")[1].index(")")]
        killed_enemies.setdefault(key, 0)
        killed_enemies[key] += 1


def in_game(list_of_enemies, mode):
    """Actual game is happening in this function"""
    global dodge_chances
    global killed_enemies
    global turn

    def damage_modifier():
        # Damage multiplier for Survival mode
        damage_multiplier = {10: 1.5,
                             20: 2,
                             30: 2.5,
                             40: 3,
                             50: 3.5,
                             60: 4}
        # Apply a damage multiplier between specified turns
        if 10 <= turn < 20:
            list_of_enemies[0].dmg *= int(damage_multiplier[10])
        elif 20 <= turn < 30:
            list_of_enemies[0].dmg *= int(damage_multiplier[20])
        elif 30 <= turn < 40:
            list_of_enemies[0].dmg *= int(damage_multiplier[30])
        elif 40 <= turn < 50:
            list_of_enemies[0].dmg *= int(damage_multiplier[40])
        elif 50 <= turn < 60:
            list_of_enemies[0].dmg *= int(damage_multiplier[50])
        elif turn >= 60:
            list_of_enemies[0].dmg *= int(damage_multiplier[60])

    turn = 1
    # Kill count
    killed_enemies = {}
    # dodge_chances => No protection - Failed - Succesfullv
    dodge_chances = [-1, 0, 1]
    is_player_dead = False  # False means the player is alive

    # Classic Mode
    if mode == 1:
        # All enemies are alive and the player is still alive
        while list_of_enemies and not is_player_dead:

            # Let the player choose what to do (Send the enemy list)
            isdead = actions(list_of_enemies)
            input("\nPress Enter the continue\n")

            # If the unit dies
            if isdead:
                print(str(5 * '*') + " Congratz! You killed the enemy onto the next one! " + str(5 * '*'))
                player.gain_xp(50)
                count_kills(list_of_enemies[0])
                del list_of_enemies[0]
                Enemy.decrease_the_num_of_enemies()
            # If the unit is still alive / dodges the unit / Choose to do nothing (Equals to None)
            else:
                print(str(30*'*'))
                # Determines if the player is still alive after the enemy attack
                is_player_dead = enemy_turn(list_of_enemies)
            input("\n\nPress Enter the continue\n")
            terminal_clean()

            if not is_player_dead and list_of_enemies:
                # Increment the turn count
                turn += 1
    # Survival Mode
    elif mode == 2:

        # Loop through until Player dies
        while not is_player_dead:
            # Let the player choose what to do (Send the enemy list)
            isdead = actions(list_of_enemies)
            input("\nPress Enter the continue\n")

            # If the unit dies
            if isdead:
                print(str(5 * '*') + " Congratz! You killed the enemy onto the next one! " + str(5 * '*'))
                player.gain_xp(50)
                # Record the enemy's death
                count_kills(list_of_enemies[0])
                del list_of_enemies[0]
                # Decrease the amount of class instances
                Enemy.decrease_the_num_of_enemies()
                # Generate a random enemy again
                list_of_enemies = generate_enemies(diff, mode)
                # Apply a damage multiplier between specified turns
                damage_modifier()

            # If the unit is still alive / dodges the unit / Choose to do nothing (Equals to None)
            else:
                print(str(30 * '*'))
                # Determines if the player is still alive after the enemy attack
                is_player_dead = enemy_turn(list_of_enemies)
            input("\n\nPress Enter the continue\n")
            terminal_clean()

            if not is_player_dead:
                # Increment the turn count
                turn += 1

    # Player lost the game
    if is_player_dead:
        game_over(0)
    # Player won the game
    else:
        game_over(1)


def terminal_clean():
    """Clears terminal screen depending on host's OS"""
    if os.name == 'nt':
        os.system('cls')   # Clears the current terminal screen (For Windows)
    elif os.name == 'posix':
        os.system('clear')  # Clears the current terminal screen (For Linux)
    else:
        raise Exception("An unknown OS type")   # macOS isn't real


def game_over(state):
    """The time that game ends whether you won or lost, or you just wanted to close the program"""
    # 0 - player lost, 1 - player win, -1 - action menu exit, -2 normal exit
    def show_status(flag=-1):
        # If there are any enemies that player has killed, list them
        if killed_enemies:
            print(f'\n{str("-" * 8)} Killed enemies {str("-" * 8)}')
            for key, value in killed_enemies.items():
                print(f">> {str(value).center(5)} --- {key}")
            print(f"\n{str('-' * 8)} Total killed enemies : {sum(list(killed_enemies.values()))} {str('-' * 8)}")

        # DO NOT SHOW how many turns passed unless the player has killed at least one person
        # and didn't exit from action menu
        if flag != -1 or killed_enemies:
            print(f"\nYou have played {turn} turns\n")

    # The condition that player wins (1)
    if state == 1:
        print(f"Congratz! You won the game! {random.choice(victory_quote)}")
    # The condition that player loses (0)
    elif state == 0:
        print(f"You lost the game! Boo-hoo, {random.choice(defeat_quote)}")
    # Actions Menu -> 7 : Exit (-1)
    elif state == -1:
        print("Thanks for playing! Take care now!")
        show_status()
        exit(0)
    # Normal exit (-2)
    else:
        print("Thanks for playing! Take care now!")
        exit(0)

    show_status(state)


def is_restart():
    """Checking whether player wants to play again or not"""
    # global enemies

    while True:
        answer = input("\nWould you like to play again? [y/n] >> ")
        if answer.lower() == "y" or answer == "":
            # Garbage collect
            # del enemies
            # gc.collect()
            # Resets the total enemy count
            Enemy.reset_total_enemies()
            return True
        elif answer.lower() == "n":
            return False
        else:
            continue


def list_enemies(list_of_enemy):
    """Takes a list of instances of Enemy class and prints their attirubute"""
    try:
        print(str("-" * 45))
        for i, j in enumerate(list_of_enemy):
            # Current enemy
            if i == 0:
                # Current enemy isn't a boss
                if j.status != 3:
                    text = " ".expandtabs(40) + ">> Current Enemy <<"
                    name = j.name[:j.name.index("_")]
                else:
                    text = " ".expandtabs(40) + ">>> Current BOSS <<<"
                    name = j.name[:j.name.index("-")]
            # Boss
            elif j.status == 3:
                text = " ".expandtabs(40) + ">>> BOSS <<<"
                name = j.name[:j.name.index("-")]
            # Others
            else:
                text = ""
                name = j.name[:j.name.index("_")]
            print(f">> {str(i+1).center(3)}  {name.center(20)}  {text.center(20)}")
        print(str("-" * 10) + " Total Enemies " + str(len(list_of_enemy)) + " " + str("-" * 10))
    except TypeError:
        print("Expecting a list of Enemy class instances")


def enemy_dodge_probability(difficulty):
    """Enemy's dodge probability depending on the difficulty"""
    # dodge_chances = [-1, 0, 1] => No protection - Failed - Succesfullv
    if difficulty in [0, 1]:
        return np.random.choice(dodge_chances, 1, p=[0.70, 0.15, 0.15])
    elif difficulty == 2:
        return np.random.choice(dodge_chances, 1, p=[0.33, 0.34, 0.33])
    else:
        return np.random.choice(dodge_chances, 1, p=[0.30, 0.35, 0.35])


def actions(list_of_enemies):
    """Decide what to do (Player action menu -> Player's turn)"""

    def gain_experience(_dodge_state, difficulty, critical_state=0):
        """Returns an integer depending on dodge status and difficulty"""
        # enemy_list variable is coming from actions() method

        # critical hit => 0 -- non-critical / 1 -- critical hit
        # Normal, Hard, Very Hard difficulties
        if difficulty in [2, 3, 4]:
            if critical_state == 0:
                # the enemy dodged the attack but still received damage
                if _dodge_state == 0:
                    return 5
                # If the enemy couldn't dodge the player's damage
                elif _dodge_state != 1:
                    return 15
            else:
                # the enemy dodged the attack but still received damage
                if _dodge_state == 0:
                    return 15
                # If the enemy couldn't dodge the player's damage
                elif _dodge_state != 1:
                    return 30
                else:
                    print(list_of_enemies[0].angered())

        # Very Easy and Easy difficulties
        else:
            if critical_state == 0:
                # the enemy dodged the attack but still received damage
                if _dodge_state == 0:
                    return 15
                # If the enemy couldn't dodge the player's damage
                elif _dodge_state != 1:
                    return 30

            else:
                # the enemy dodged the attack but still received damage
                if _dodge_state == 0:
                    return 25
                # If the enemy couldn't dodge the player's damage
                elif _dodge_state != 1:
                    return 50
                else:
                    print(list_of_enemies[0].angered())

        return 10

    terminal_clean()
    # region Developer debugging Action menu

    # Make "True and True" in order to see in the action menu
    if True and False:
        word = "a - Show Instances of Enemy Class (Dev Mode only)"
    else:
        word = ""
    # endregion

    if player.hp == player.max_hp:
        # No need to heal
        state_of_hp = "(Full)"
    else:
        # Might heal himself/herself
        state_of_hp = ""

    print(f"Turn {turn} -- {list_of_enemies[0].name} has shown up!")
    print(f'''\nChoose the following
    1 - Attack ⚔ 
    2 - Heal Up {state_of_hp}
    3 - Critical Hit Chance 
    4 - Show Your Current Enemy Info 
    5 - Show Your Info 
    6 - How many enemies left?
    7 - Exit (Closes the game)
    {word}\n''')

    while True:
        try:
            action = input(">> ")
            if action not in ["1", "2", "3", "4", "5", "6", "7", 'a']:
                raise ValueError
            break
        except ValueError:
            return actions(list_of_enemies)

    # print(f"You chose {action}")
    # Turn-consuming actions - After you decide what to do next. Your current turn will be over
    if action in ["1", "2", "3"]:
        # Deciding the dodge status for enemy randomly
        dodge_state = enemy_dodge_probability(diff)

        # Attack ⚔
        if action == "1":
            damage_output = int(player.dmg + (1 - (DIFF_MODIFIER[diff] / 100)))
            # Returns True if an unit dies, false if an unit is still alive
            result = list_of_enemies[0].damaged(damage_output, dodge_state)

            # Player gaining XP based on the difficulty and dodge status
            player.gain_xp(gain_experience(dodge_state, diff))

            return result

        # Healing up
        elif action == "2" and state_of_hp == "":
            # Healing factor except for level 0
            if player.level != 0:
                healing_factor = (player.level * 10) + int(DIFF_MODIFIER[diff] * 15)
            else:
                healing_factor = 30
            player.healed(healing_factor)

        # Critical Chance
        elif action == "3":
            critical_hit = random.randint(1, 100)
            print(f"You're going to try your best luck to hit as hard as you can\n"
                  f"Your chances of getting a critical crit : %{critical_hit}")
            input("\nPress Enter the continue\n")
            damage_output = round(player.dmg * (critical_hit / 10) + 15)
            result = list_of_enemies[0].damaged(damage_output, dodge_state)
            player.gain_xp(gain_experience(dodge_state, diff, 1))
            return result

        else:
            print("You don't need a healing right now")
            input("\nPress Enter the continue\n")
            return actions(list_of_enemies)

    # Information related actions [That means player's turn shouldn't be ended here and ask his decision again
    else:
        terminal_clean()
        # Current Enemy Info
        if action == "4":
            # 0 all the time because when an unit dies we delete them from the list
            print(list_of_enemies[0].get_info())
        # Player status (XP, HP etc.)
        elif action == "5":
            player.get_info()
        # Printing how many enemies left
        elif action == "6":
            list_enemies(list_of_enemies)
        # Exiting the game
        elif action == "7":
            terminal_clean()
            game_over(-1)
        # region Show Instances of Enemy Class (Dev Mode only) - Passive

        # elif action == 'a':
        #
        #     # region Viewing instances of Enemy class - Active
        #
        #     index = 0
        #     for obj in gc.get_objects():
        #         if isinstance(obj, Enemy):
        #             print((index+1), '---', obj)
        #             index += 1
        #
        #     # endregion

        # endregion

        # Proceed to ask again
        input("\nPress Enter the continue\n")
        return actions(list_of_enemies)


def enemy_turn(list_of_enemies):
    """Determines what enemy does in their turn and returns a boolean value whether player is alive or not"""
    def probability_of_dodge():
        """Deciding dodge probability randomly depending on difficulty (Hardcoded)"""
        # dodge_chances = [-1, 0, 1] => No protection - Failed - Succesfull

        # Normaly enemy
        if list_of_enemies[0].status != 3:
            # Difficulty -> Very Easy, Easy
            if diff in [0, 1]:
                return np.random.choice(dodge_chances, 1, p=[0.25, 0.25, 0.50])
            # Difficulty -> Normal
            elif diff == 2:
                return np.random.choice(dodge_chances, 1, p=[0.33, 0.34, 0.33])
            # Difficulty -> Hard, Extremely Hard
            else:
                return np.random.choice(dodge_chances, 1, p=[0.35, 0.35, 0.30])
        # Boss enemy
        else:
            # Difficulty -> Easy
            if diff == 1:
                return np.random.choice(dodge_chances, 1, p=[0.30, 0.30, 0.40])
            # Difficulty -> Normal
            elif diff == 2:
                return np.random.choice(dodge_chances, 1, p=[0.32, 0.36, 0.32])
            # Difficulty -> Hard, Extremely Hard
            else:
                return np.random.choice(dodge_chances, 1, p=[0.35, 0.40, 0.25])

    print(f">> Now it's {list_of_enemies[0].name} turn! Brace yourself! <<")

    # Deciding dodge probability randomly depending on difficulty
    dodge_state = probability_of_dodge()

    # Healing factor for enemies
    # If It's a boss (Difficulty Hard and greater)
    if list_of_enemies[0].status == 3 and diff >= 3:
        healing_factor = 50 + int(DIFF_MODIFIER[4-diff] * 7)
        list_of_enemies[0].healed(healing_factor)
    # For normal enemies (Difficulty Hard and greater)
    elif diff >= 3:
        healing_factor = 30 + int(DIFF_MODIFIER[4-diff] * 5)
        list_of_enemies[0].healed(healing_factor)

    # Non-boss attacks
    if list_of_enemies[0].status != 3:
        player_state = player.damaged(list_of_enemies[0].dmg, dodge_state)
    # Boss attacks
    else:
        player_state = player.damaged(int(list_of_enemies[0].dmg + 50), dodge_state)

    # If you got attacked (and still alive), heal the player (on Very easy and Easy difficulties)
    if not player_state and diff in [0, 1]:
        if player.level == 0:
            player.healed(20)
        else:
            player.healed(10)

    # If it's true then player has been killed otherwise player is still alive
    return player_state

# endregion

# region Main Program


if __name__ == "__main__":
    terminal_clean()
    restart = True
    main_menu()
    # Waiting for the player to press enter to continue
    input()
    while restart:
        # Sets up a game (creating a player, generating enemies, choosing difficulty etc.)
        set_up_the_game()
        global enemies, gmode, diff, player
        # In-game this is where the game takas place (Attacking enemies, healing up etc.)
        in_game(enemies, gmode)

        # This is the section that game ends (whether the player wins or loses)
        # and asks the player if the player wants to play again or not
        restart = is_restart()
        terminal_clean()

    # Player wanted to close the program
    game_over(-2)

# endregion
