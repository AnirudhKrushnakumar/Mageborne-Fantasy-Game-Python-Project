# Imports:
import player_classes
import monster_stats
import random

#----------------------------------------
# Actual game code beyond this point!
#----------------------------------------
level_p = 1

valid_input1 = False
while not valid_input1:
    player_class_selection = input("Please choose one of the classes below:\n A) Warrior: A martial fighter, focusing on strength.\n B) Mage: An arcane user of magic, focusing on intelligence but with low health.\n C) Thief: A cunning rogue, focusing on stealth to sneak around.\n")
    if player_class_selection == "A" or "a":
        player_class = "Warrior"
        health_p = 10 * level_p + 1
        strength_p = 15
        dexterity_p = 14
        constitution_p = 13
        intelligence_p = 8
        valid_input1 = True

    elif player_class_selection == "B" or "b":
        player_class = "Mage"
        health_p = 4 * level_p + 1
        strength_p = 8
        dexterity_p = 12
        constitution_p = 13
        intelligence_p = 15
        valid_input1 = True

    elif player_class_selection == "C" or "c":
        player_class = "Thief"
        health_p = 8 * level_p + 1
        strength_p = 12
        dexterity_p = 15
        constitution_p = 13
        intelligence_p = 14
        valid_input1 = True

    else:
        print("Please enter a valid option (A, B, or C)!")

print("You have selected: " + player_class)
name_p == input("Please enter a name for your character: ")
print("Player description:\n Class: " + player_class + "\n Health: " + str(health_p) + "\n Strength: " + str(strength_p) + "\n Dexterity: " + str(dexterity_p) + "\n Constitution: " + str(constitution_p) + "\n Intelligence: " + str(intelligence_p) + "\n ========================================")
