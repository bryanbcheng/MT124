def readFile(filename):
	f = open(filename)
	lines = f.readlines()
	f.close()
	for line in lines:
		if line == "\n":
			# print "**line deleted**"
			del line
		# else:
		# 	print line
	return lines

def readDict(filename):
	dictionary = {}
	f = open(filename)
	lines = f.readlines()
	f.close()
	for line in lines:
		germanWord = line[:line.index(' ')].strip()
		engDef = line[(line.index(' ') + 1):].strip()
		# print "the german word is %s with the english def %s" %(germanWord, engDef)
		dictionary[germanWord] = engDef
	return dictionary


lines = readFile('text.txt')
dictionary = readDict('EGdict.txt')

# print lines
# print dictionary
translatedWords = []
for line in lines:
	line = line.strip()
	wordVector = line.split()
	newSentence = ""
	wordsFromVecSeen = 0
	totalNumWords = len(wordVector) + line.count(".") + line.count(",") + line.count("(") + line.count(")")
	# for word in wordVector:
	# 	word = word.strip(".,\"()")
	# 	# print "the word %s translates to %s" %(word, dictionary[word])
	# 	wordsFromVecSeen += 1
	# 	newSentence += dictionary[word]
	# 	if wordsFromVecSeen == totalNumWords:
	# 		newSentence += "\n"
	# 	else:
	# 		newSentence += " "
	# 	translatedWords.append(dictionary[word])
	# 	print "%s" %(word)

	for word in wordVector:
		word = word.replace(".", " .")
		word = word.replace(",", " ,")
		word = word.replace("(", "( ")
		word = word.replace(")", " )")
		word = word.strip("\"")
		word = word.strip()
		word = word.split(" ")
		# print word
		for word_or_punct in word:
			# print "the word %s translates to %s" %(word, dictionary[word])
			wordsFromVecSeen += 1
			newSentence += dictionary[word_or_punct]
			if wordsFromVecSeen == totalNumWords:
				newSentence += "\n"
			else:
				newSentence += " "
			translatedWords.append(dictionary[word_or_punct])
			# print "%s" %(word_or_punct)
	print newSentence

# print translatedWords
