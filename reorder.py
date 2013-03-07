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

# Get starting index and ending index of noun phrase assuming only 1 noun in noun phrase
def findNounPhrase(sentence, index):
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

	return (subStart, subEnd)

sentences = readFile('translated.txt')
tagged = readFile('translated-tagged.txt')
posDict = {}

# Create dict of words and their POS tag
for line in tagged:
	words = string.split(line.strip(), ' ')
	for word in words:
		tags = string.split(word, '_')
		if tags[0] == '-LRB-':
			posDict['('] = '('
		elif tags[0] == '-RRB-':
			posDict[')'] = ')'
		else:
			posDict[tags[0]] = tags[1]

nouns = set(['NN','NNP','NNPS','NNS','PRP'])
verbs = set(['VB','VBD','VBG','VBN','VBP','VBZ'])
adverbs = set(['RB','RBR','RBS'])

vowels = set(['a','e','i','o','u'])

transform = []

# Define reordering rules
for sentence in sentences:
	# Rule 1 - first sentence
	sentence = sentence.strip().split(' ')
	if posDict[sentence[0]] == "IN": #preposition
		#Find subject of prepositional phrase
		subPos = None
		for i in range(1,len(sentence)):
			if posDict[sentence[i]] in nouns:
				subPos = i
				break
		
		#Find next subject
		(subStart, subEnd) = findNounPhrase(sentence, subPos + 1)

		if subEnd != None:
			for i in range(subStart, subEnd + 1):
				subPos += 1
				sentence.insert(subPos, sentence.pop(i))
	
	#Rule 2 - swap verb and pronoun after it
	for i in range(len(sentence) - 1):
		if posDict[sentence[i]] in verbs and posDict[sentence[i + 1]] == "PRP":
			sentence[i], sentence[i + 1] = sentence[i + 1], sentence[i]
		
	#Rule 3 - swap modal and nouns/prp
	for i in range(len(sentence)):
		if posDict[sentence[i]] == 'MD':
			(subStart, subEnd) = findNounPhrase(sentence, i + 1)
			sentence.insert(subEnd, sentence.pop(i))
			break
			
	#Rule 4 - move verb at end of sentence after modal
	if posDict[sentence[-2]] in verbs:
		for i in range(len(sentence)):
			if posDict[sentence[i]] == 'MD':
				ind = i + 1
				while posDict[sentence[ind]] in adverbs:
					ind += 1
				sentence.insert(ind, sentence.pop(-2))
				

	#Rule 5 - change the after comma to which, move verb at end after comma
	for i in range(len(sentence) - 1):
		if sentence[i] == ',' and sentence[i + 1] == 'the':
			sentence[i + 1] = 'which'
			
			sentence.insert(i + 2, sentence.pop(-2))

	#Rule 6 - make sure subject and verb agree
	
	#Rule 7 - swap consec VBN

	#Rule 8 - replace 'are it' -> 'there exists'

	#Rule 10
	for i in range(len(sentence) - 1):
                if sentence[i] == 'a' and sentence[i + 1][0] in vowels:
                        sentence[i] = 'an'
		elif sentence[i] == 'an' and sentence[i + 1][0] not in vowels:
			sentence[i] = 'a'

	# Post processing, capitalize first letter, add period at end.
	sentence[0] = sentence[0].capitalize()
	if sentence[0] == '(':
		sentence[1] = sentence[1].capitalize()
	joined = ' '.join(sentence)
	
	# remove space before periods, commas and ()
	joined = string.replace(joined, ' ,', ',')
	joined = string.replace(joined, ' .', '.')
	joined = string.replace(joined, '( ', '(')
	joined = string.replace(joined, ' )', ')')

	transform.append(joined)

# Display final output
print transform
