

def readFile(filename):
	f = open(filename)
	lines = f.readlines()
	f.close()
	for line in lines:
		if line == "\n":
			print "**line deleted**"
			del line
		else:
			print line
	return lines

def readDict(filename):
	dictionary = {}
	f = open(filename)
	lines = f.readlines()
	f.close()
	for line in lines:
		germanWord = line[:line.index(' ')].strip()
		engDef = line[(line.index(' ') + 1):].strip()
		print "the german word is %s with the english def %s" %(germanWord, engDef)
		dictionary[germanWord] = engDef
	return dictionary


lines = readFile('text.txt')
dictionary = readDict('EGdict.txt')

print lines
print dictionary
translatedWords = []
for line in lines:
	line = line.strip()
	wordVector = line.split()
	for word in wordVector:
		word = word.strip(".,\"()")
		print "the word %s translates to %s" %(word, dictionary[word])
		translatedWords.append(dictionary[word])

print translatedWords
