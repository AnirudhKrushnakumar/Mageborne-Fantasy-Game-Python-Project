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
    player_class_selection = input("Please choose one of the classes below:\n A) Warrior: A martial fighter, focusing on strength.\n B) Mage: An arcane user of magic, focusing on intelligence but with low health.\n C) Thief: A cunning rogue, focusing on stealth to sneak around.\n").strip().upper()
    if player_class_selection == "A":
        player_class = "Warrior"
        strength_p = 15
        dexterity_p = 14
        constitution_p = 13
        intelligence_p = 8
        health_p = 10 * level_p + (constitution_p / 10)
        valid_input1 = True

    elif player_class_selection == "B":
        player_class = "Mage"
        strength_p = 8
        dexterity_p = 12
        constitution_p = 13
        intelligence_p = 15
        health_p = 10 * level_p + (constitution_p / 10)
        valid_input1 = True

    elif player_class_selection == "C":
        player_class = "Thief"
        strength_p = 12
        dexterity_p = 15
        constitution_p = 13
        intelligence_p = 14
        health_p = 10 * level_p + (constitution_p / 10)
        valid_input1 = True

    else:
        print("Please enter a valid option (A, B, or C)!")

print("You have selected: " + player_class)
name_p = input("Please enter a name for your character: ")
print("Player description:\n Name: " + name_p + "\n Class: " + player_class + "\n Health: " + str(health_p) + "\n Strength: " + str(strength_p) + "\n Dexterity: " + str(dexterity_p) + "\n Constitution: " + str(constitution_p) + "\n Intelligence: " + str(intelligence_p) + "\n ========================================")
print("Welcome to Mageborne! below is a little preface to the story (Beta Version)")
print("Hello, " + name_p + ". You have been hired by the townspeople of Emberpine to investigate the nearby woods, after large monster tracks were found.\n The game starts with you at the entrance of the woods, where you'll walk through and face different types of monsters.")
print("========================================")
print(" ")
path_1 = input("You enter the woods, what would you like to do?\n A) Search for clues\n B) Follow the trail\n C) Try to attract a monster\n").strip().upper()
valid_input2 = False
while not valid_input2:
    if path_1 == "A":
        roll = random.randint(1, 20) + (intelligence_p / 10)
        print("You rolled a " + str(roll) + " total for perception.")
        if roll >= 14:
            print("You find some torn fabric on the branches, leading towards a clearing. Inside, stands 3 small goblins. Prepare for combat!")
            valid_input2 = True
        else:
            print("You don't notice any evidence of monsters, maybe you should try again or a different tactic.")
    elif path_1 == "B":
        print("You follow the trail and eventually find a log laying across it, a further look reveals that it was deliberatly placed there. As you look around, you notice a new, smaller path leading towards a clearing. Inside, stands 3 small goblins. Prepare for combat!")
        valid_input2 = True
    elif path_1 == "C":
        print("You make some noise and lay out some aromatic food around you, hoping to attract a monster. After a few minutes, you hear hushed voices leading towards a clearing. Inside, stands 3 small goblins. Prepare for combat!")
        valid_input2 = True