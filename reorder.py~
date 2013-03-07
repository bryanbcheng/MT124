import string

def readFile(filename):
        f = open(filename)
        lines = f.readlines()
        f.close()
        for line in lines:
                if line == "\n":
                        del line
        return lines


sentences = readFile('translated.txt')
tagged = readFile('translated-tagged.txt')
posDict = {}

for line in tagged:
	words = string.split(line.strip(), ' ')
	for word in words:
		tags = string.split(word, '_')
		posDict[tags[0]] = tags[1]

	print posDict

print sentences
