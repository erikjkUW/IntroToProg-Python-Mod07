#========================================================#
#Title:
#Description:   Dice Roller for Ability Scores Shown by my DM:
#               Showcase of Pickle It module to store data
#               in a file. Implementation of Exceptions
#               using try and except.
#Changelog (Who, When, What):
#erikjk,5.29.2020,Created Script, global variables, pseudo code
#erikjk,5.29.2020,Outlined Function classes, began basic scripting
#erikjk.5.30.2020,Completed Add/Remove and Started Pickle/Unpickle
#erikjk.5.30.2020,Finished Dice Roll Function, random module, rerolls, storing
#erikjk.5.30.2020,Completed Function Comparing summed dice rolls with standard array
#erikjk.5.30.2020,Finished Pickle in Add to File
#erikjk.5.30.2020,Created custom error FantasyNameError
#erikjk.5.30.2020,Finished Unpickle with EOFEError exception
#erikjk.5.30.2020,Testing all options and checking warnings/debugging
#erikjk.5.30.2020,Finished docstrings and comments

#========================================================#

import pickle, random

#DATA====================================================#
strFileName = "CharacterRolls.dat"  #Name of data file
lstTable = []                       #List as table of one or more dicRow
lstDiceRolls1 = []                  #List of dice rolls to be added to dicRow
lstDiceRolls2 = []
dicRow = {}                         #Dictionary as row in Table
    #{Name : "character name", Dice Rolls 1 : [lstDiceRolls1], Dice Rolls 2 : [lstDiceRolls2]}
strChoice = ""                      #Captures user Menu choice
strCharacterName = ""               #Captures user Class choice
strStatus = ""                      #Captures status of Processor function
intAbilityScoreTotal = ""           #Compares Ability Score Total to Standard Array
STANDARD_ARRAY = 15+14+13+12+10+8   #Constant = Total of Standard Array as a sum of ability scores

#ERROR HANDLING==========================================#
class FantasyNameError(Exception):
    """Breaks the program if the user enters any non-alphabetic character
    when creating their Player Character, or to break when trying to remove a
    character by name which doesn't exist. Meant to be tongue-in-cheek to show
    custom error handling and exceptions.
    """
    pass

#PROCESSING==============================================#
class Processor:

    #DICE FUNCTIONS
    @staticmethod
    def dice_roll():
        """Rolls 8d6 dice, rerolling twice any numbers under 4
        :param roll_count:
        :param list_of_rolls: (list) of
        :param roll:
        :return:
        """
        roll_count = 0
        list_of_rolls = [random.randint(1,6) for roll in range(8)]
        while roll_count < 2:
            for roll in list_of_rolls:
                if roll < 4:
                    list_of_rolls.remove(roll)
                    roll = random.randint(1,6)
                    list_of_rolls.append(roll)
                roll_count += 1
        return sorted(list_of_rolls, reverse=True), "\nThis is the result of your 8d6 rolls."

    def compare_to_standard_array(list_of_rolls1, list_of_rolls2):
        """ Sums the total of the two rolled lists, and then adds them together
        :param rolls1: stores sum as int
        :param rolls2: stores sum as int
        :param total_of_rolls: adds rolls1 and rolls2 together
        :return: integer, string
        """
        rolls1 = sum(list_of_rolls1)
        rolls2 = sum(list_of_rolls2)
        total_of_rolls = rolls1 + rolls2
        return total_of_rolls, "Keep in mind, Standard Array is [15, 14, 13, 12, 10, 8]\n"

    #FILE FUNCTIONS
    def read_data_from_file(file_name):
        """ Unpickles data from .dat file into list
        :param file_name: name of file to open and unpickle
        :param list_of_rows: (list) of dictionary rows
        :return: list
        """
        list_of_rows = []
        with (open(file_name, "rb")) as file:
            while True:
                #Handling Exception encountered from empty file
                try:
                    list_of_rows.append(pickle.load(file))
                except EOFError:
                    break
        return list_of_rows

    def save_data_to_file(file_name, list_of_rows):
        """ Pickles data into the .dat file
        :param character: dictionary row from list, player character
        :param list_of_rows: (list) of dictionary rows
        :return: list, string
        """
        file = open(file_name, "wb+")
        for character in list_of_rows:
            pickle.dump(character, file)
        file.close()
        return list_of_rows, "\nYour Character data has been saved.\n"

    #LIST FUNCTIONS
    def add_character_to_list(character_name, dice_rolls1, dice_rolls2, list_of_rows):
        """ Matches values from other functions to keys in the target dictionary,
        then appends that row to the list of rows
        :param row: dictionary row
        :param dice_rolls: (list) of numbers rolled
        :param list_of_rows: (list) of dictionary rows
        :return: list, string
        """
        row = {"Name":character_name.title(), "Dice Rolls 1":dice_rolls1, "Dice Rolls 2":dice_rolls2}
        list_of_rows.append(row)
        return list_of_rows, "\nThe character" + character_name.title() + " has been added.\n"

    def remove_character_from_list(character_name, list_of_rows):
        """ Takes user input and compares it to values in "Name" key of
        dictionary rows, removing that row on a match
        :param row: dictionary row
        :param list_of_rows: (list) of dictionary rows
        :return: list, string
        """
        for row in list_of_rows:
            if row["Name"].lower() == character_name.lower():
                list_of_rows.remove(row)
            else:
                pass
        return list_of_rows, "\nThe character " + character_name.title() + " has been removed.\n"


#PRESENTATION============================================#
class IO:

    #OUTPUT FUNCTIONS
    @staticmethod
    def print_main_menu_options():
        """ Displays a list of options to the user
        :return: nothing
        """
        print("""
                Menu of Options:
        	(1) Roll a Character
	        (2) View Characters
	        (3) Delete Character
	        (4) Save Characters to File
	        (5) Exit
	        """)

    def print_list_of_characters(list_of_rows):
        """ Shows current list of characters and their dice rolls from dictionary rows
        :param row: dictionary row
        :param list_of_rows: (list) of rows you want to display
        :return: nothing
        """
        print("*****************CHARACTERS*****************")
        for row in list_of_rows:
            print(row["Name"], row["Dice Rolls 1"], row["Dice Rolls 2"])
        print() # Add extra line for looks

    def print_compare_to_standard(total_of_rolls):
        """ Compares two integer values and displays whether or not the user
        has a larger value than the constant STANDARD_ARRAY
        param: total_of_rolls: int value calculated from lists of rolled dice
        :return: nothing
        """
        if total_of_rolls >= STANDARD_ARRAY:
            print("Your rolled total = ", total_of_rolls, "You are quite powerful!\n")
        else:
            print("Your rolled total = ", total_of_rolls, "You may be underpowered.\n"
                  "Use may use the Standard Array (72) or consult your DM.\n")

    #INPUT FUNCTIONS
    def input_enter_to_continue(optional_message = ""):
        """ Pauses the program, requesting input to continue
        :param optional_message: string taking its value from other functions
        :return: nothing
        """
        print(optional_message)
        input("Press the [Enter] key to continue.")
        print() # Add extra line for looks

    @staticmethod
    def input_menu_choice():
        """ Captures input for menu choice from user
        :param choice: typically integer value from [1-5]
        :return: string
        """
        choice = str(input("Please make a choice from the above options [1-5]: ")).strip()
        print() # Add extra line for looks
        return choice

    def input_yes_no_choice(message):
        """ Captures yes or no answer from user
        :param message: string displayed to user clarifying input
        :return: string
        """
        return str(input(message)).strip().lower()

    @staticmethod
    def input_name_choice():
        """ Captures user input for character name when processing add/remove
        :param character_name: string that must be alphabetic only
        :return: string
        """
        character_name = str(input("What is the character's name?: ")).title()
        if character_name.isalpha():
            pass
        else:
            raise FantasyNameError("That sounds made up... Cannot compute...")
        return character_name

#MAIN BODY===============================================#

# Read unpickled data from file
lstTable = Processor.read_data_from_file(strFileName)

# Displays an initial splash with some ASCII art
print("""
  ____
 /\\\' .\    _____
/: \___\  / .  /\\
\\\' / . / /____/..\\
 \/___/  \\\'  '\  /
          \\\'__'\/
""")
print("Welcome to the Wonderful\n     "
      "8d6 Method of Ability Scores\n         "
      "for Your Favorite d20 TTRPG Systems!")
while (True) :
    # Displays a menu of options to user
    IO.print_main_menu_options()
    strChoice = IO.input_menu_choice()

    if strChoice.strip() == "1" :
        # Capture character name
        strCharacterName = IO.input_name_choice()
        # Roll first array, automatically rerolls twice
        lstDiceRolls1, strStatus = Processor.dice_roll()
        print(lstDiceRolls1)
        IO.input_enter_to_continue(strStatus)
        # Roll second array, automatically rerolls twice
        lstDiceRolls2, strStatus = Processor.dice_roll()
        print(lstDiceRolls2)
        IO.input_enter_to_continue(strStatus)
        # Add character and their two arrays to the main list
        Processor.add_character_to_list(strCharacterName,lstDiceRolls1, lstDiceRolls2, lstTable)
        # Run a comparison against the standard array, before assigning ability scores
        intAbilityScoreTotal, strStatus = Processor.compare_to_standard_array(lstDiceRolls1, lstDiceRolls2)
        IO.print_compare_to_standard(intAbilityScoreTotal)
        IO.input_enter_to_continue(strStatus)

    if strChoice.strip() == "2" :
        # Displays a list of rolled characters to the user
        IO.print_list_of_characters(lstTable)
        IO.input_enter_to_continue("********************************************")

    if strChoice.strip() == "3" :
        # Allows the user to remove a character from the list
        strCharacterName = IO.input_name_choice()
        lstTable, strStatus = Processor.remove_character_from_list(strCharacterName, lstTable)
        IO.input_enter_to_continue(strStatus)

    if strChoice.strip() == "4" :
        # Pickling the list and saving it to the data file
        strChoice = IO.input_yes_no_choice("Save Character Data? y/n: ")
        if strChoice.lower() == "y":
            lstTable, strStatus = Processor.save_data_to_file(strFileName,lstTable)
            IO.input_enter_to_continue(strStatus)
        else:
            IO.input_enter_to_continue("Save Aborted!")
        continue

    if strChoice.strip() == "5":
        # Asks user to confirm exit
        strChoice = IO.input_yes_no_choice("Confirm you wish to exit? y/n: ")
        if strChoice.lower() == "y":
            print("\nHappy Adventuring!")
            break
        else:
            print("\nAh, a mistake then.")
            continue
