#!/usr/bin/env python3
# -*- coding: utf8 -*-
# Made by Make http://github.com/mak3e
adjectives=("adorable", "adventurous", "alert", "alive", "amused", "angry", "attractive", "beautiful", "better", "bewildered", "black", "blue", "blushing", "bored", "brainy", "brave", "bright", "busy", "calm", "careful", "cautious", "charming", "cheerful", "clean", "clear", "clever", "cloudy", "colorful", "combative", "comfortable", "concerned", "condemned", "confused", "cooperative", "courageous", "crazy", "creepy", "crowded", "cruel", "curious", "cute", "dangerous", "dark", "dead", "defeated", "defiant", "delightful", "depressed", "determined", "different", "difficult", "disgusted", "distinct", "disturbed", "dizzy", "doubtful", "drab", "dull", "eager", "easy", "elated", "elegant", "embarrassed", "enchanting", "encouraging", "energetic", "enthusiastic", "envious", "evil", "excited", "expensive", "exuberant", "fair", "faithful", "famous", "fancy", "fantastic", "fierce", "filthy", "fine", "foolish", "fragile", "frail", "frantic", "friendly", "frightened", "funny", "gentle", "gifted", "glamorous", "gleaming", "glorious", "good", "gorgeous", "graceful", "grieving", "grotesque", "grumpy", "handsome", "happy", "healthy", "helpful", "hilarious", "homeless", "homely", "hungry", "hurt", "important", "impossible", "inexpensive", "innocent", "inquisitive", "itchy", "jittery", "jolly", "joyous", "kind", "light", "lively", "lonely", "long", "lovely", "lucky", "magnificent", "misty", "modern", "motionless", "muddy", "mushy", "mysterious", "nasty", "naughty", "nervous", "nice", "nutty", "obedient", "obnoxious", "odd", "old-fashioned", "open", "outrageous", "outstanding", "panicky", "perfect", "plain", "poised", "poor", "powerful", "precious", "prickly", "proud", "puzzled", "quaint", "real", "relieved", "repulsive", "rich", "scary", "selfish", "shiny", "shy", "silly", "sleepy", "smiling", "smoggy", "sore", "sparkling", "splendid", "spotless", "stormy", "strange", "stupid", "successful", "super", "talented", "tame", "tender", "tense", "testy", "thankful", "thoughtful", "thoughtless", "tired", "tough", "troubled", "ugliest", "ugly", "uninterested", "unsightly", "unusual", "upset", "uptight", "vast", "victorious", "vivacious", "wandering", "weary", "wicked", "wide-eyed", "wild", "witty", "worrisome", "worried", "wrong", "zany", "zealous")
animals=("alligator", "ant", "bear", "bee", "bird", "camel", "cat", "cheetah", "chicken", "chimpanzee", "cow", "crocodile", "deer", "dog", "dolphin", "duck", "eagle", "elephant", "fish", "fly", "fox", "frog", "giraffe", "goat", "goldfish", "hamster", "hippopotamus", "horse", "kangaroo", "kitten", "lion", "lobster", "monkey", "octopus", "owl", "panda", "pig", "puppy", "rabbit", "rat", "scorpion", "seal", "shark", "sheep", "snail", "snake", "spider", "squirrel", "tiger", "turtle", "wolf", "zebra")

#You can define custom names here
custom={1:"custom name"}

def main():
	"""
	Returns first 1000 names
	"""
	i=0 
	while i<1000:
		print(str(i)+": "+get_name(i))
		i+=1

def get_name(seed):
	"""
	Return a name (adjective + animal) based on seed
	
	Args:
		seed (int):
			seed
	"""
	if seed in custom:
		return custom[seed].capitalize()
	name=[]
	name.append(get_adjectives(seed))
	name.append(get_animal(seed))
	return " ".join(name)

def get_adjectives(seed):
	"""
	Return an adjective based on seed

	Args:
		seed (int):
			seed
	"""
	if int(seed/len(animals))>=len(adjectives):
		return get_adjectives(seed-(len(adjectives)*len(animals)))
	else:
		return adjectives[int(seed/len(animals))].capitalize() 

def get_animal(seed):
	"""
	Return an animal based on seed

	Args:
		seed (int):
			seed
	"""
	return animals[seed%len(animals)].capitalize()

if __name__ == "__main__":
	main()
