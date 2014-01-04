#!/usr/bin/env python
# coding=utf-8

import csv, random, math

cards = []
selectedCards = []
expansions = ['Dominion', 'Intrigue', 'Seaside', 'Alchemy', 'Prosperity', 'Cor­nu­co­pi­a', 'Hin­ter­lands', "Dark Ages", 'Guilds']
possibleCards = []
cardDispersion = []

#Import Card List From CSV File
with open('card_list.csv', 'rb') as csvfile:
	cardreader = csv.reader(csvfile, delimiter=',', quotechar='"')
	count = 0
	for row in cardreader:
		if (row[3] >= '2' or row[3] == '?') and (row[4] >= '1' or row[4] == '?'):
			row.append('Village')
			count += 1
		elif row[4] >= '3':
			row.append('Terminal Action')
			count += 1
		elif (row[3] >= '1' or row[3] == '?') and (row[4] >='2' or row[4] == '?'):
			row.append('Lab')
			count += 1
		elif row[0] in  ["Throne Room", "King's Court", "Procession"]:
			row.append('Duplicator')
			count += 1
		elif row[12] > '1' or row[12] == '?':
			row.append('Trasher')
			count += 1
		elif row[8] != '0':
			row.append('Attack')
			count += 1
		elif row[7] != '0':
			row.append('Victory')
			count += 1
		elif row[0].lower() in ["feast", "embargo", "island", "treasure map", "pillage"]:
			row.append('One-shot')
		else:
			row.append('None')
			count += 1
		cards.append(row)
	print(count)


#Determine Categories for all cards 
#Categories will be in position 19




#Get Number of Players
numPlayers = int(raw_input("Enter the number of players: "))
numCards = numPlayers + 10

#Get Deck Selections From User
selectedDecks = []
for i in range(len(expansions)):
	print(str(i)+ '. ' + expansions[i])
print('Please enter the numbers of the expanion packs you want to play with')
selection = raw_input()
selectedDeckNums = selection.split(',')
for i in range(len(selectedDeckNums)):
	selectedDecks.append(expansions[int(selectedDeckNums[i])])


def mergeSelection():
	#Merge selected decks into a single list
	for deck in selectedDecks:
		for card in cards:
			if card[16] == deck:
				possibleCards.append(card)

#Display Card in Readable Manner
def displayCard(card):
	cardString = card[0] + ' (' + 'Cost: ' + card[2]
	if card[3] != '0':
		cardString += ', Actions: ' + card[3]
	if card[4] != '0':
		cardString += ', Cards: ' + card[4]
	if card[12] != '0':
		cardString += ', Trash: ' + card[12]
	if card[13] != '0':
		cardString += ', Coins: ' + card[13]
	if card[14] != '0':
		cardString += ', Buys: ' + card[14]
	cardString += ', Type: '
	if card[5] == '1':
		cardString += 'Action'
	elif card[6] == '1':
		cardString += 'Tresure'
	elif card[7] == '1':
		cardString += 'Victory'
	if card[8] == '1':
		cardString += ', Attack'
	if card[9] == '1':
		cardString += ', Reaction'
	if card[10] != '0':
		cardString += ', Duration: ' + card[10]
	if card[11] != '0':
		cardString += ', Victory Points: ' + card[11]
	if len(selectedDecks) > 1:
		cardString += ', Expansion: ' + card[16]
	cardString += ', Category: ' + card[18]
	cardString += ')'
	return cardString

#Print Selected Cards
def printkindgom():
	for i in range(len(selectedCards)):
		print(str(i) + '. ' + displayCard(selectedCards[i]))

#Select 12 Random Cards and allow the user to reshuffle the deck
def selectRandom():
	reshuffle = 'y'
	while reshuffle == 'y':
		global selectedCards
		selectedCards = []
		random.shuffle(possibleCards)
		for i in range(numCards):
			selectedCards.append(possibleCards[i])
		printkindgom()
		reshuffle = raw_input('Would you like to reselect the kindgom? (y/n): ')

def saneKingdom():
	usedCateories = []
	reshuffle = 'y'
	while reshuffle == 'y':
		mergeSelection()
		global selectedCards
		selectedCards = []
		numCardsSelected = 0
		random.shuffle(possibleCards)
		while(numCards > numCardsSelected):
			if possibleCards[0][18] != 'None' and possibleCards[0][18] in usedCateories:
				del possibleCards[0]
			else:
				selectedCards.append(possibleCards[0])
				usedCateories.append(possibleCards[0][18])
				del possibleCards[0]
				numCardsSelected += 1
		printkindgom()
		reshuffle = raw_input('Would you like to reselect the kindgom? (y/n): ')


#Select a specified number of cards from a specified deck
def selectSepcific(numToSelect, deck):
	possibleCards = []
	for card in cards:
		if card[16] == deck:
			possibleCards.append(card)
	random.shuffle(possibleCards)
	for i in range(numToSelect):
		selectedCards.append(possibleCards[i])

	

#Get Preferences for ratio of decks
print('How would you like the deck devived?\n1. Completely random from all selected decks.\n2. Certain Percentage from each selected deck.\n3. Generate a sane kingdom')
var = raw_input('Enter selction: ')
if var == '1':
	mergeSelection()
	selectRandom()
elif var == '2':
	reshuffle = 'y'
	while reshuffle == 'y':
		cardDispersion = []
		global selectedCards
		selectedCards = []
		percentageAllocated = 0
		for i in range(len(selectedDecks) - 1):
			cardDispersion.append(int(raw_input('Enter the pergentage to be taken from the ' + selectedDecks[i] + ' deck: ')))
			percentageAllocated += cardDispersion[-1]
		cardDispersion.append(100 - percentageAllocated)

		numSelected = 0
		print(len(cardDispersion))
		for i in range(len(cardDispersion) - 1):
			numToSelect = (int(cardDispersion[i]) * numCards)/100
			selectSepcific(numToSelect, selectedDecks[i])
			numSelected += numToSelect
		selectSepcific(numCards - numSelected, selectedDecks[-1])
		printkindgom()
		reshuffle = raw_input('Would you like to reselect the kindgom? (y/n): ')
elif var == '3':
	saneKingdom()



#Allow veto until they get down to 10 cards
while len(selectedCards) > 10:
	printkindgom()
	veto = raw_input("Enter the number of the card that you would like to veto: ")
	del selectedCards[int(veto)]


print("\nYour Final Kingdom is:")
printkindgom()











