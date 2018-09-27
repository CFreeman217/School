#! /usr/bin/env python3

print("Automate the Boring Stuff Chapter Examples")

# theBoard = {"1A" : "   " , "1B" : "   " , "1C" : "   ", \
#             "2A" : "   " , "2B" : "   " , "2C" : "   ", \
#             "3A" : "   " , "3B" : "   " , "3C" : "   " }

# def printBoard(board):
#     print("\n TIC-TAC-TOE: \n")
#     print("    A   B   C \n")
#     print("1: " + board['1A'] + "|" + board['1B'] + "|" + board['1C'])
#     print("   ---+---+---")
#     print("2: " + board['2A'] + "|" + board['2B'] + "|" + board['2C'])
#     print("   ---+---+---")
#     print("3: " + board['3A'] + "|" + board['3B'] + "|" + board['3C'])
#     print("\n" * 2)

# turn = " X "

# for i in range(9):
#     printBoard(theBoard)
#     print("Turn for " + turn + ". Move on which space?")
#     move = input()
#     theBoard[move] = turn
#     if turn == " X ":
#         turn = " O "
#     else:
#         turn = " X "










# allGuests = {"Alice" : {"Apples" : 5, "Pretzels" : 12},\
#              "Bob"   : {"Ham Sandwiches" : 3, "Apples"  : 2},\
#              "Carol" : {"Cups" : 3, "Apple Pies" : 1}}

# def totalBrought(guests,item):
#     numBrought = 0
#     for k ,v in guests.items():
#         numBrought += v.get(item, 0)
#     return numBrought

# print("Number of things being brought: ")
# print(" - Apples     " + str(totalBrought(allGuests, "Apples")))
# print(" - Cups     " + str(totalBrought(allGuests, "Cups")))
# print(" - Cakes     " + str(totalBrought(allGuests, "Cakes")))
# print(" - Ham Sandwiches     " + str(totalBrought(allGuests, "Ham Sandwiches")))
# print(" - Apple Pies     " + str(totalBrought(allGuests, "Apple Pies")))









# character = {"Arrow" : 12 ,\
#              "Gold Coin" : 42 ,\
#              "Rope" : 1 ,\
#              "Torch" : 6 ,\
#              "Dagger" : 1}

# loot = ['Gold Coin', 'Dagger', 'Gold Coin', 'Gold Coin', 'Ruby']

# def displayInventory(pack):
#     item_total = 0
#     print("\n" * 2 + "Inventory:\n")
#     for item, qty in pack.items():
#         print(str(qty) + "  " + str(item))
#         item_total += qty
#     print("\nTotal Number of items:" + str(item_total) + "\n" * 2)

# def addToInventory(inventory, addedItems):
#     print("Monster killed!\nHere is your Loot:\n")
#     for add_item in addedItems:
#         if add_item in inventory.keys():
#             inventory[add_item] += 1
#             print(str(add_item) + " added. New Quantity: " + str(inventory[add_item]))
#         else:
#             inventory[add_item] = 1
#             print(str(add_item) + " is a new item.")

# displayInventory(character)
# addToInventory(character,loot)
# displayInventory(character)









# while True:
#     print("Enter your name : ")
#     name = input()
#     if age.isalpha():
#         break
#     print("Please enter a name containing only letters")

# while True:
#     print("Enter your age : ")
#     age = input()
#     if age.isdecimal()
#         break
#     print("Please enter a number for your age")

# while True:
#     print("Select a new password (letters and numbers only) : ")
#     password = input()
#     if password.isalnum():
#         break
#     print("Passwords can only have letters and numbers.")









# def printPicnic(itemsDict, leftWidth, rightWidth):
#     print("PICNIC ITEMS".center(leftWidth + rightWidth, '-'))
#     for k,v in itemsDict.items():
#         print(k.ljust(leftWidth, '.') + str(v).rjust(rightWidth, '~'))
        
# picnicItems = {"Sandwiches" : 4, "Apples" : 12, "Cups" : 4 , "Cookies" : 1000}
# printPicnic(picnicItems,12,5)
# printPicnic(picnicItems,20,6)








# '''
# # Windows
# #! python3
# '''
# # OSX
# #! /usr/bin/env python3
# '''
# # Linux
# #! /usr/bin/python3
# '''
# # pw.py - An insecure password locker program.

# passwords = {"Email" : "yourName@email.com" ,\
#              "Blog" : "yourBlog.com" ,\
#              "Luggage" : "12345"}

# import sys, pyperclip
# if len(sys.argv) < 2:
#     print('Usage: python pw.py [account] - copy account password')
#     sys.exit()

# account = sys.argv[1]   # First command line arg is the account name

# if account in passwords:
#     pyperclip.copy(passwords[account])
#     print("Password for " + account + " copied to clipboard.")
# else:
#     print("There is no account named " + account)










# #! python3
# # bulletpointAdder.py - Adds wikipedia bullet points to the start
# # of each line of text on the clipboard.

# import pyperclip
# text = pyperclip.paste()

# # TO DO: Separate lines and add stars.
# lines = text.split("\n")
# for line in range(len(lines)):  # Loop through all of the lines in the clipboard text
#     lines[line] = "* " + str(lines[line])    # Add star to each string in "lines"
# text = "\n".join(lines)
# pyperclip.copy(text)
# print(text)









''' import os
# path = os.path.join('usr','bin','spam')
# print(path)

# myFiles = ['Accounts.txt', 'Details.txt', 'Invite.docx']

# for filename in myFiles:
#     print(os.path.join('usr','bin','python',filename))

current = os.getcwd()
path = os.path.join['Users', 'CFreeman', 'Documents', 'pythonPrograms']
# os.chdir(os.path.join('usr', 'bin', 'env'))
print(current)
# print(new)
for line in os.listdir(path):
    print(line)
print(current)
 '''

 
''' 
#! python3
# mapIt.py - Launches a google map in the browser  using an address from the
# command line or clipboard.

import webbrowser, sys, pyperclip

if len(sys.argv) > 1 :
    # Get address from the command line.
    address = ' '.join(sys.argv[1:])
    
    # TODO: Get address from clipboard.
else:
    # Get address from clipboard.
    address = pyperclip.paste()

webbrowser.open('https://www.google.com/maps/place/' + address) 
'''