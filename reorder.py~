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
	numPreps = 0
	numNouns = 0
	# print "looking at sentence %s" %sentence
	for i in range(index, len(sentence)):
		if posDict[sentence[i]] == "IN":
			numPreps += 1

		if posDict[sentence[i]] in nouns:
			numNouns += 1
			if numNouns > numPreps:
				subEnd = i
				break

	subStart = subEnd
	while subStart > index - 1:
		pos = posDict[sentence[subStart - 1]]
		if pos in adjectives or pos in adverbs or pos == "DT":
			subStart -= 1
		else:
			break
	# print "returning substart = "
	# print subStart
	# print "and subend = "
	# print subEnd
	return (subStart, subEnd)

sentences = readFile('translated.txt')
tagged = readFile('translated-tagged.txt')
vp = readFile('verb-prepositions.txt')
posDict = {}
vpDict = {}

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

for line in vp:
	l = string.split(line.strip(), ' ')
	vpDict[l[0]] = l[1]

nouns = set(['NN','NNP','NNPS','NNS','PRP'])
verbs = set(['VB','VBD','VBG','VBN','VBP','VBZ'])
adverbs = set(['RB','RBR','RBS'])
adjectives = set(['JJ', 'JJR', 'JJS'])

vowels = set(['a','e','i','o','u'])

transform = []

# Define reordering rules
for sentence in sentences:
	sentence = sentence.strip().split(' ')

	#Rule 8 - replace 'are it' -> 'there exists'
	for i in range(len(sentence) - 1):
		if ((sentence[i] == 'are' and sentence[i + 1] == 'it') or
		   (sentence[i] == 'it' and sentence[i + 1] == 'are')):
			sentence[i], sentence[i + 1] = 'there', 'is'

			
	# Rule 1 - first sentence - if the sentence begins a prepositional phrase, then find the subject and move it to the front of the verb
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
	
	# Rule 2 - swap verb and pronoun after it
	for i in range(len(sentence) - 1):
		if posDict[sentence[i]] in verbs and posDict[sentence[i + 1]] == "PRP":
			sentence[i], sentence[i + 1] = sentence[i + 1], sentence[i]
		
	#Rule 3 - swap modal and nouns/prp
	for i in range(len(sentence)):
		if posDict[sentence[i]] == 'MD':
			(subStart, subEnd) = findNounPhrase(sentence, i + 1)
			if subEnd != None:
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
			posDict['which'] = 'WDT'
			sentence.insert(i + 2, sentence.pop(-2))

	#Rule 6 - abbreviated match verb with preposition
	for i in range(len(sentence)):
		if posDict[sentence[i]] in verbs:
			ind = i + 1
			while ind < len(sentence):
				if posDict[sentence[ind]] == 'IN':
					root = sentence[i]
					roots = [root]
					if root.endswith('es') or root.endswith('ed'):
						roots.append(root[:-2])
					if root.endswith('s') or root.endswith('d'):
						roots.append(root[:-1])

					for r in roots:
						if r in vpDict:
							sentence[ind] = vpDict[r]
							posDict[vpDict[r]] = 'IN'
					break
				ind += 1
	
	#Rule 7 - swap consec VBN
	for i in range(len(sentence) - 1):
                if posDict[sentence[i]] == 'VBN' and posDict[sentence[i + 1]] == 'VBN':
                        sentence[i], sentence[i + 1] = sentence[i + 1], sentence[i]
			
	# Rule 8 - fixed genitive tense in lines 
	# #4 ('a part the pupils' -> 'a part of the pupils'), 
	# #8 ('an other part the pupils' -> '... an other part of the pupils'), 
	# #9 ('... the termination the middle maturation' -> '... the termination of the middle maturation')
	indicesToAddOf = []

	subPos = None
	if posDict[sentence[0]] == "IN": #preposition
		#Find subject of prepositional phrase
		for i in range(1,len(sentence)):
			if posDict[sentence[i]] in nouns:
				subPos = i
				break
		
	#Find next subject
	if subPos == None:
		beginIndex = 0
	else:
		beginIndex = subPos+1

	# print "looking at range %d and %d" %(beginIndex, len(sentence)-1)
	for i in range(beginIndex, len(sentence) - 1):
		if posDict[sentence[i]] in nouns:
			# print "noun is %s and next word is %s and pos is %s" %(sentence[i], sentence[i+1], posDict[sentence[i+1]])
			if posDict[sentence[i+1]] == "DT":
				# print "looking at sentence:"
				# print sentence
				# print "****added %d****" %(i+1)
				indicesToAddOf.append(i+1)

	for index in indicesToAddOf:
		sentence.insert(index, 'of')
		for indexPos in range(len(indicesToAddOf)):
			indicesToAddOf[indexPos] += 1


	#Rule 11 - fix a and an
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
i = 0
for line in transform:
	i += 1
	print "(%d) %s" %(i, line)
