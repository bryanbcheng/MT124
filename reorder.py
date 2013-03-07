import string

def readFile(filename):
        f = open(filename)
        lines = f.readlines()
        f.close()

	i = 0
        while i < len(lines):
		line = lines[i]
                if line == "\n":
                        del lines[i]
		else:
			i += 1
        return lines


sentences = readFile('translated.txt')
tagged = readFile('translated-tagged.txt')
posDict = {}

# Create dict of words and their POS tag
for line in tagged:
	words = string.split(line.strip(), ' ')
	for word in words:
		tags = string.split(word, '_')
		posDict[tags[0]] = tags[1]

		#print posDict

nouns = set(['NN','NNP','NNPS','NNS'])
verbs = set(['VB','VBD','VBG','VBN','VBP','VBZ'])

transform = []

# Define reordering rules
for sentence in sentences:
	# Rule 1
	sentence = sentence.strip().split(' ')
	if posDict[sentence[0]] == "IN": #preposition
		#Find subject of prepositional phrase
		subPos = None
		for i in range(1,len(sentence)):
			if posDict[sentence[i]] in nouns:
				subPos = i
				break
		
		#Find next subject
		subEnd = None
		for i in range(subPos + 1, len(sentence)):
			if posDict[sentence[i]] in nouns:
				subEnd = i
				break
		
		subStart = subEnd
		while subStart > subPos:
			pos = posDict[sentence[subStart - 1]]
			if pos == "JJ" or pos == "DT":
				subStart -= 1
			else:
				break

		if subEnd != None:
			for i in range(subStart, subEnd + 1):
				subPos += 1
				sentence.insert(subPos, sentence.pop(i))
	
	#Rule 2
	for i in range(len(sentence) - 1):
		if posDict[sentence[i]] in verbs and posDict[sentence[i + 1]] == "PRP":
			print "ASDF"
			print sentence[i]
			sentence[i], sentence[i + 1] = sentence[i + 1], sentence[i]
			print sentence[i]
			print sentence
		
	joined = ' '.join(sentence)
	transform.append(joined)

# Display final output
print transform
