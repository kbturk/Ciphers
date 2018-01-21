#! python3
# Ciphers.py - a dictionary of ciphers that can be used to encrypt or decrypt messages.

import pyperclip, sys, random, string, copy

#Global variable list:
SYMBOLS= """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\] 
^_`abcdefghijklmnopqrstuvwxyz{|}~""" #keep the space at the beginning. 
LETTERS= string.ascii_uppercase
LETTERDICTIONARY={l : [] for l in string.ascii_uppercase}
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
englishLetterFreq={'E': 12.70, 'T': 9.06, 'A': 8.17, 
	'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 
	'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 
	'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 
	'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 
	'X': 0.15, 'Q': 0.10, 'Z': 0.07}

def FunctionList(): #lists all the ciphers programmed in the library.
	print('FunctionList: \n\n reverse \n ceaser \n\n ceaserBruteForce \n\n transpositionEncrypt \n transpostionEncryptMessage \n',
	'transpositionDecrypt \n transpostionDecryptMessage \n transpositionTest \n',
	'transpostionHacker \n hackTransposition \n\n gcd \n findModInverse \n',
	'KeyASolutions \n affineCipherMain \n','getAffineKeyParts \n','checkAffineKeys \n',
	'affineEncryptMessage \n','affineDecryptMessage \n','getRandomKey \n','affineHacker \n',
	'hackAffine \n\n simpleSubCipher \ncheckSimpleSubValidKey \n',
	'translateSimSubMessage) \n')

def reverse(): #The reverse cipher. First time encrypts, second decrypts.
	message=input('Please input your message: ')
	translated = ''
	i=len(message)-1
	while i>=0:
		translated=translated+message[i]
		i=i-1
	print(translated)
	pyperclip.copy(translated)
	
def ceaser():#The ceaser cipher. requires a 'key' 0-25 int to encrypt. that key is required to decrypt. This currently does not translate symbols or numbers.
	#user inputs:
	message=input('Please input your message for the ceaser cipher: ')
	key=int(input('please choose a key [0-25]: '))
	modedecision=int(input('for encrypt, select 1. for decrypt, select 2.: ')) #set to encrypt or decrypt
	if modedecision ==1:
		mode='encrypt'
	elif modedecision ==2:
		mode='decrypt'
	else:
		mode='encrypt'
		print('''You didn't enter either 1 or 2. Program will encrypt by default.''')
	LETTERS='ABCDEFGHIJKLMNOPQRSTUVWXYZ' #this won't encrypt anything other than a letter right now.
	translated='' #start with an empty string
	message=message.upper()
	
	for symbol in message:
		if symbol in LETTERS:
		#get the encrypted or decrypted number for this symbol:
			num=LETTERS.find(symbol) # get the number of the symbol.
			if mode =='encrypt':
				num=num+key
			elif mode =='decrypt':
				num=num-key
			
			#handle the wrap-around if the num is larger than the length of
			#LETTERS or less than 0
			if num >= len(LETTERS):
				num=num-len(LETTERS)
			elif num<0:
				num=num+len(LETTERS)
			
			#add encrypted/decrypted number's symbol at the end of translated string.
			translated=translated+LETTERS[num]
		else:
			#just add the symbol without encrypting/decrypting:
			translated=translated+symbol
	#print translated to the screen.
	translated=translated.lower()
	print(translated)
	#copy translated to the clipboard.
	pyperclip.copy(translated)

def ceaserBruteForce(): #This is a brute force to solve the ceaser cipher.
	message=input('Please input the encrypted message: ')
	LETTERS='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	
	#loop through every possible key.
	for key in range(len(LETTERS)):
		#clear 'translated'
		translated=''
		#the rest of this is very similar to the ceaser program.
		for symbol in message:
			if symbol in LETTERS:
				num= LETTERS.find(symbol) #get the number of the symbol.
				num=num-key
				
				#handle the wrap around if num is 26 or larger or less than 0
				if num<0:
					num=num+len(LETTERS)
				elif num>= len(LETTERS):
					num=num-len(LETTERS)
				translated+=LETTERS[num]
			else:
				#just add the symbol without encrypting/decrypting
				translated=translated+symbol
			#display the current key being tested along with the decryption
		print('Key #%s: %s' %(key, translated))
		
def transpositionEncrypt(): #Simple transposition Encryption. Dependent on transpositionEncryptMessage.
	myMessage=input('Please input your message: ')
	myKey=int(input('Please provide a key length: '))
	if myKey>=len(myMessage)/2:
		myKey=int((len(myMessage)/2)-1)
		print('given key was too long, key was changed to %s' % myKey)
	ciphertext=transpositionEncryptMessage(myKey, myMessage)

	#print the encrypted string with a pipe character(|)
	print(ciphertext+'|')
	pyperclip.copy(ciphertext)
def transpositionEncryptMessage(key,message): #meat and potatoes of transpositionEncrypt. Can be stand alone called.
	#Each string in ciphertext represents a column in the grid.
	ciphertext=['']*key
	
	#loop through each column in ciphertext.
	for col in range(key):
		pointer=col
		#keep looping until pointer goes past the length of the message.
		while pointer<len(message):
			#place the character at pointer in message at the end of the current column in the cipher list.
			ciphertext[col]+=message[pointer]
				
			#move the pointer over.
			pointer +=key
	#convert the ciphertext list into a single string value and return it.
	return ''.join(ciphertext)
		
def transpositionDecrypt(): #Simple transposition Decryption. Dependent on transpositionDecryptMessage.
	
	myMessage=input('Please input your message: ')
	myKey = int(input('Please provide a key length: '))
	
	if myMessage[len(myMessage)-1]=="|":
		myMessage=myMessage[0:len(myMessage)-1]
	plaintext=transpositionDecryptMessage(myKey,myMessage)
	#print the pipe character at the end of the line. |
	print(plaintext+'|')
	pyperclip.copy(plaintext)
def transpositionDecryptMessage(key, message): #meat and potatoes of transpostionDecrypt. Can be stand alone called.
	import math
	#the transposition decrypt function will simulate the 'columns' and 'rows of the grid. 
	#first we need to calculate a few values.
	
	#the number of 'columns' in our transposition grid:
	numOfColumns=math.ceil(len(message)/key)
	#the number of rows in our grid:
	numOfRows=key
	#the number of 'shaded boxes' in the last 'column' of the grid:
	numOfShadedBoxes=(numOfColumns*numOfRows)-len(message)
	
	#each string in plaintext represents a column in the grid:
	plaintext=['']*numOfColumns
	col=0
	row=0
	for symbol in message:
		plaintext[col] +=symbol
		col +=1 #points to the next column.
		if (col==numOfColumns) or (col==numOfColumns-1 and row>=numOfRows-numOfShadedBoxes):
			col = 0
			row+=1
	return''.join(plaintext)

def transpositionTest(): #tests the transposition encryption/decryption. Kind of useless.
	import random, sys

	random.seed(42) #set the random "seed" to a static value.
	for i in range(20): #run 20 tests. this is a totally arbitrary number.
		#generate random messages to test.
		
		#this message will have a random length 4-20 long:
		message='ABCDEFGHIJKLMNOPQRSTUVWXYZ'*random.randint(4,20)
		
		#convert the message string to a list to shuffle it.
		message=list(message)
		random.shuffle(message)
		message=''.join(message) #converts the list to a string.
		
		print('test #%s: "%s..."' % (i+1,message[:50]))
		#check all possible keys for each message.
		for key in range(1,len(message)):
			encrypted=transpositionEncryptMessage(key,message)
			decrypted=transpositionDecryptMessage(key, encrypted)
			
			#if the decription doesn't match the original message, 
			#display error and quit.
			if message != decrypted:
				print('Mismatch with key %s and message %s.'(key,message))
				print(decrypted)
				sys.exit()
	print('Transposition cipher test passed.')

def transpositionHacker():#brute force solver for the transposition hacker.
	
	myMessage=input('Enter what you want to decrypt: ')
	if myMessage == '':
		myMessage="""Cb b rssti aieih rooaopbrtnsceee er es no npfgcwu  plri ch nitaalr eiuengiteehb(e1  hilincegeoamn fubehgtarndcstudmd nM eu eacBoltaeteeoinebcdkyremdteghn.aa2r81a condari fmps" tad   l t oisn sit u1rnd stara nvhn fsedbh ee,n  e necrg6  8nmisv l nc muiftegiitm tutmg cm shSs9fcie ebintcaets h  aihda cctrhe ele 1O7 aaoem waoaatdahretnhechaopnooeapece9etfncdbgsoeb uuteitgna.rteoh add e,D7c1Etnpneehtn beete" evecoal lsfmcrl iu1cifgo ai. sl1rchdnheev sh meBd ies e9t)nh,htcnoecplrrh ,ide hmtlme. pheaLem,toeinfgn t e9yce da\' eN eMp a ffn Fc1o ge eohg dere.eec s nfap yox hla yon. lnrnsreaBoa t,e eitsw il ulpbdofgBRe bwlmprraio po  droB wtinue r Pieno nc ayieeto\'lulcih sfnc  ownaSserbereiaSm-eaiah, nnrttgcC  maciiritvledastinideI  nn rms iehn tsigaBmuoetcetias rn"""
	print(myMessage) #just a check.
	
	hackedMessage=hackTransposition(myMessage)
	
	if hackedMessage== None:
		print('Failed to hack encryption.')
	else:
		print('Copying hacked message to clipboard.\n')
		print(hackedMessage)
		pyperclip.copy(hackedMessage)
def hackTransposition(message): #meat and potatoes of the transposition hacker.
	import detectingEnglish
	print('Hacking...')
	
	#python programs can be stopped at any time by pressing Ctrl-C (on Windows)
	#or Ctrl-D (on Mac)
	print('(press Ctrl-C or Ctrl-D to quit at any time.)')
	
	#brute-force by looping through every possible key...
	for key in range(1,len(message)):
		print('Trying key #%s...'% (key))
		decryptedText=transpositionDecryptMessage(key, message)
		
		if detectingEnglish.isEnglish(decryptedText):
			print()
			print('possible solution found.')
			print('Key %s:%s' % (key, decryptedText[:100]))
			print()
			print('''Enter D for done, or
			just press Enter to continue hacking: ''')
			response = input('> ')
			
			if response.strip().upper().startswith('D'):
				return decryptedText
	return None

def gcd(a,b): #Euclid Algorithm, greatest common denominator of two numbers.
	while a !=0:
		a, b=b%a,a
	return b
def findModInverse(a,m): #Extended Euclidean algorithm. Returns the modular inverse of a%m, which is the number x such that a*x%m=1
	if gcd(a,m) !=1:
		return None #no mod inverse if a&m aren't relatively prime.
	u1,u2,u3,v1,v2,v3=1,0,a,0,1,m
	while v3!=0:
		q=u3//v3 #// is the integer division operator.
		v1,v2,v3,u1,u2,u3=(u1-q*v1),(u2-q*v2), (u3-q*v3),v1,v2,v3
	return u1%m
def KeyASolutions(a,b): #this is hot garbage right now.
	keySolutions={}
	B=list(b)
	for n in range(2,a):
		key=n*len(b)+1
		if gcd(len(b),key)==1:
			print(n)
			[j*key%len(B) for j in range(0,len(B))]
			keySolutions[n]=n%len(b)
	return keySolutions

def affineCipherMain(): #This uses the Euclid Algorithm and the ceaser cipher.
	myMessage=input('please enter your message: ')
	if myMessage=='':
		myMessage='''"A computer would deserve to be called intelligent if it could decieve a human into
		believing it was a human." - Alan Turing'''
		print('Using default message: %s' % (myMessage))
	myKey=input('please enter key or type Random for a random key : ')
	if myKey=='':
		myKey=2023
	elif myKey.strip().upper().startswith('R'):
		myKey=getRandomAffineKey()
		print('using %s' % (myKey))
	else:
		myKey=int(myKey)
	myMode=input('Please enter (E)ncrypt or (D)ecrypt :')
	if myMode.upper().strip().startswith('E'):
		myMode='encrypt'
		translated=affineEncryptMessage(myKey,myMessage)
	elif myMode.upper().startswith('D'):
		myMode='decrypt'
		translated=affineDecryptMessage(myKey,myMessage)
	else:
		print('not a valid input. Default will encrypt')
		myMode='encrypt'
		translated=affineEncryptMessage(myKey,myMessage)
	print('key: %s' % (myKey))
	print('%sed text:'%(myMode.title()))
	print(translated)
	pyperclip.copy(translated)
	print('full %sed text copied to clipboard.' %(myMode))
def getAffineKeyParts(key):
	keyA=key//len(SYMBOLS)
	keyB=key%len(SYMBOLS)
	return(keyA,keyB)
def checkAffineKeys(keyA, keyB, mode):
	if keyA == 1 and mode == 'encrypt':
		sys.exit('The affine cipher becomes incredibly weak when key A is set to 1. Choose a different key.')
	if keyB == 0 and mode == 'encrypt':
		sys.exit('The affine cipher becomes incredibly weak when key B is set to 0. Choose a different key.')
	if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS) - 1:
		sys.exit('Key A must be greater than 0 and Key B must be between 0 and %s.' % (len(SYMBOLS) - 1))
	if gcd(keyA, len(SYMBOLS)) != 1:
		sys.exit('Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' % (keyA, len(SYMBOLS)))
def affineEncryptMessage(key,message):
	keyA,keyB=getAffineKeyParts(key)
	checkAffineKeys(keyA,keyB,'encrypt')
	ciphertext=''
	for symbol in message:
		if symbol in SYMBOLS:
		#encrypt the sucker.
			symIndex=SYMBOLS.find(symbol)
			ciphertext +=SYMBOLS[(symIndex*keyA+keyB)%len(SYMBOLS)]
		else:
			ciphertext += symbol
	return ciphertext
def affineDecryptMessage(key, message):
	keyA,keyB=getAffineKeyParts(key)
	checkAffineKeys(keyA,keyB,'decrypt')
	plaintext=''
	modInverseOfKeyA=findModInverse(keyA,len(SYMBOLS))
	
	for symbol in message:
		if symbol in SYMBOLS:
		#decrypt the sucker.
			symIndex=SYMBOLS.find(symbol)
			plaintext+=SYMBOLS[(symIndex-keyB)*modInverseOfKeyA%len(SYMBOLS)]
		else: 
			plaintext +=symbol #just append the symbol undecrypted.
	return plaintext
def getRandomAffineKey(): #if you can't think of a key.
	while True:
		keyA=random.randint(2,len(SYMBOLS))
		keyB=random.randint(2,len(SYMBOLS))
		if gcd(keyA, len(SYMBOLS))==1:
			return keyA*len(SYMBOLS)+keyB
def affineHacker(): #Brute force affine hacker.
	myMessage=input('please enter your message: ')
	if myMessage=='':
		myMessage='''U&'<3dJ^Gjx'-3^MS'Sj0jxuj'G3'%j'<mMMjS'g{GjMMg9j{G'g"'gG '<3^MS'Sj<jguj'm'P^dm{'g{G3'%jMgjug{9'GPmG'gG'-m0'P^dm{LU'5&Mm{'_^xg{9'''
	hackedMessage=hackAffine(myMessage)
	
	if hackedMessage !=None:
		print('affineHacker found a solution. Copying to clipboard.')
		print(hackedMessage)
		pyperclip.copy(hackedMessage)
	else:
		print('Failed to find a solution.')
def hackAffine(message): #meat and potatoes of affineHacker.
	import detectingEnglish
	SILENT_MODE=True #true only prints solution, false prints everything.
	print('hacking...')
	print('press Ctrl-C or Ctrl-D to quit at any time.')
	
	for key in range(len(SYMBOLS)**2):
		keyA=getAffineKeyParts(key)[0]
		if gcd(keyA, len(SYMBOLS)) !=1:
			continue
		
		decryptedText=affineDecryptMessage(key, message)
		if not SILENT_MODE:
			print('Tried Key %s...(%s)' % (key, decryptedText[:40]))
		if detectingEnglish.isEnglish(decryptedText):
		
			print('\nPossible hack found :\nKey %s' % (key))
			print('Decrypted message: '+decryptedText[:200]+'\n')
			print('Enter D for done or just press Enter to continue:')
			response=input('> ')
			
			if response.strip().upper().startswith('D'):
				pyperclip.copy(decryptedText)
				return decryptedText
	return None
	
def simpleSubCipher(): #simple substitution. Like grandma used to solve in the newspaper.

	myMessage=input('please enter your message: ')
	if myMessage=='':
		myMessage='If a man is offered a fact which goes against his instincts, he will scrutinize it closely, and unless the evidence is overwhelming, he will refuse to believe it. If, on the other hand, he is offered something which affords a reason for acting in accordance to his instincts, he will accept it even on the slightest evidence. The origin of myths is explained in this way. -Bertrand Russell'
	myKey=input('Please provide a key. Default is LFWOAYUISVKMNXPBDCRJTQEGHZ. Type (Random) for a random key. ')
	if myKey=='':
		myKey='LFWOAYUISVKMNXPBDCRJTQEGHZ'
	elif myKey.upper()=='RANDOM':
		myKey=getRandomSubKey()
		print(myKey)
	myMode=input('Please enter (E)ncrypt or (D)ecrypt :')
	if myMode.upper().startswith('E'):
		myMode='encrypt'
	elif myMode.upper().startswith('D'):
		myMode='decrypt'
	else:
		print('not a valid input. Default will encrypt')
		myMode='encrypt'
	
	checkSimpleSubValidKey(myKey)
	
	if myMode=='encrypt':
		translated=translateSimSubMessage(myKey,myMessage,'encrypt')
	elif myMode=='decrypt':
		translated=translateSimSubMessage(myKey,myMessage,'decrypt')
	print('using key %s' % (myKey))
	print('The %sed message is:' %(myMode))
	print(translated)
	pyperclip.copy(translated)
	print()
	print('This message has been copied to the clipboard')
def checkSimpleSubValidKey(key): #checks for valid key.
	keyList=list(key)
	lettersList=list(LETTERS)
	keyList.sort()
	lettersList.sort()
	if keyList != lettersList:
		sys.exit('There is an error in the key or symbol set.')	
def translateSimSubMessage(key,message,mode): #meat and potatoes of simple substitution
	translated=''
	charA=LETTERS
	charB=key
	if mode=='decrypt':
		charA,charB=charB,charA
	for symbol in message:
		if symbol.upper() in charA:
			symIndex=charA.find(symbol.upper())
			if symbol.isupper():
				translated +=charB[symIndex].upper()
			else:
				translated +=charB[symIndex].lower()
		else:
			translated+= symbol
	return translated
def getRandomSubKey(): #if you're lazy, use this to generate a key.
	key=list(LETTERS)
	random.shuffle(key)
	return ''.join(key)
#Cracking the simpleSubCipher:
def getWordPattern(word): #this takes a string of text and creates a pattern with it. It's part of the simple substitution cipher.
	#Returns a string of the pattern form of the given word.
	# e.g. '0.1.2.3.4.1.2.3.5.6.' for 'DUSTBUSTER'
	word=word.upper()
	nextNum=0
	letterNums={}
	wordPattern=[]
	
	for letter in word:
		if letter not in letterNums:
			letterNums[letter]=str(nextNum)
			nextNum +=1
		wordPattern.append(letterNums[letter])
	return '.'.join(wordPattern)
def makeWordPatterns(): #This creates a python file of the dictionary file mapped to patterns.
	import pprint
	allPatterns={}
	
	fo=open('dictionary.txt')
	wordList=fo.read().split('\n')
	fo.close()
	
	for word in wordList:
		#get the pattern for each string in wordList.
		pattern=getWordPattern(word)
		
		if pattern not in allPatterns:
			allPatterns[pattern]=[word]
		else:
			allPatterns[pattern].append(word)
	#Now we're going to add some single digit and double digit words that aren't inlcuded in dictionary.txt for obvious reasons.
	smallWords=('I','A','AS','AM','IT','IS','ON','BE','TO','OF','IN','HE','DO','AT','BY','WE','OR','AN','SO','IF','GO','ME','NO','US')
	for word in smallWords:
		pattern=getWordPattern(word)
		if pattern not in allPatterns:
			allPatterns[pattern]=[word]
		else:
			allPatterns[pattern].append(word)
	#This creates another module called wordPatterns.
	fo=open('wordPatterns.py','w')
	fo.write('allPatterns= ')
	fo.write(pprint.pformat(allPatterns))
	fo.close()
def simpleSubHacker(): #we're ready to implement the solver now that we have a getwordpattern file.
	import os, pprint
	
	if not os.path.exists('wordPatterns.py'): #checks and makes the wordPattern file if it doesn't exist.
		makeWordPatterns()
	import wordPatterns
	
	message=input('please enter your message: ')
	if message=='':
		message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
		print('using default string : %s' % (message))
	print('Hacking...') #what IS hacking anyway? Aren't we just solving?
	letterMapping=hackSimpleSub(message)
	
	pprint.pprint(letterMapping)
	print()
	print('Original ciphertext:')
	print(message)
	print()
	print('Copying hacked message to clipboard: ')
	hackedMessage = decryptWithCipherletterMapping(message, letterMapping)
	print(hackedMessage)
	countOfUnkowns=hackedMessage.count("_")
	if countOfUnkowns >0:
		inputselect=input('Would you like to guess a letter?: ')
		keeptrying=True
		if inputselect.strip().upper().startswith('Y'):
			betterMapping=copy.deepcopy(letterMapping)
			while keeptrying:
				keeptrying=False
				substitution=input('Which letter? :')
				dictsub=input('What should it be? :')
				
				while len(betterMapping[substitution]) !=0:
					for s in betterMapping[substitution]:
						betterMapping[substitution].remove(s)
				print(betterMapping[substitution])
				if len(betterMapping[substitution])==0:
					betterMapping[substitution].append(dictsub)
					betterMapping=removeSolvedLettersFromMapping(betterMapping)
					print(betterMapping[substitution])

				hackedMessage=decryptWithCipherletterMapping(message,betterMapping)
				pprint.pprint(betterMapping)
				print("Original message: ",message)
				print(hackedMessage)
				inputselect=input('Would you like to try another letter? ')
				if inputselect.strip().upper().startswith('Y'):
					keeptrying=True
	pyperclip.copy(hackedMessage)
def getBlankCipherLetterMapping():
	return copy.deepcopy(LETTERDICTIONARY)
def addLettersToMapping(letterMapping, cipherword, candidate): #This function adds the letters of the candidate as potential decryption letters for the cipherletters in the cipherletter mapping.
	#The lettermapping parameter is a cipherletter mapping dictionary
	#value that return value of this function starts as a copy of.
	#The cipherword parameter is a string value of the ciphertext word.
	#The candidate parameter is a possible English word that the 
	#cipherword could decrypt to.
	
	letterMapping=copy.deepcopy(letterMapping)
	for i in range(len(cipherword)):
		if candidate[i] not in letterMapping[cipherword[i]]:
			letterMapping[cipherword[i]].append(candidate[i])
	return letterMapping
def intersectMapping(mapA,mapB):
	# to intersect two maps, create a blank map, then add only the 
	# potential decryption letters if they exist in both maps.
	intersectedMapping=getBlankCipherLetterMapping()
	for letter in LETTERS:
		#an empty list means any letter is possible in this case just 
		#copy the other map entirely.
		if mapA[letter]==[]:
			intersectedMapping[letter]=copy.deepcopy(mapB[letter])
		elif mapB[letter]==[]:
			intersectedMapping[letter]=copy.deepcopy(mapA[letter])
		else:
			#if a letter in mapA exists in mapB, add that letter to 
			#intersectedMapping[letter]
			for mappedLetter in mapA[letter]:
				if mappedLetter in mapB[letter]:
					intersectedMapping[letter].append(mappedLetter)
	return intersectedMapping
def removeSolvedLettersFromMapping(letterMapping):
	#Cipherletters in the mapping that map to only one letter are 
	#'solved' and can be removed from the other letters.
	#for example, if A maps to potential letters M and N and BaseException
	#maps to N, then we know that B must map to N so we can
	#remove N from the list of what A could map to. So then A maps to MS
	#so we can remove M from teh list of letters for every other letter.
	#This is why there is a loop that keeps redcing the map.
	letterMapping=copy.deepcopy(letterMapping)
	loopAgain=True
	while loopAgain:
		#first assume that we will not loop again:
		loopAgain=False 
		#solvedLetters will be a list of uppercase letters that have
		#one possible mapping in letterMapping.
		solvedLetters=[]
		for cipherletter in LETTERS:
			if len(letterMapping[cipherletter])==1:
				solvedLetters.append(letterMapping[cipherletter][0])

		#if a letter is solved, then it cannot possibly be a potential
		#decripted letter for another ciphertext letter so we 
		#should remove it from those other lists.
		for cipherletter in LETTERS:
			for s in solvedLetters:
				if len(letterMapping[cipherletter]) !=1 and s in letterMapping[cipherletter]:
					letterMapping[cipherletter].remove(s)
					if len(letterMapping[cipherletter])==1:
						# A new letter was solved, so loop again.
						loopAgain=True
	return letterMapping
def hackSimpleSub(message):
	import re, wordPatterns
	intersectedMap=getBlankCipherLetterMapping()
	nonLettersOrSpacePattern=re.compile('[^A-Z\s]')
	cipherwordList=nonLettersOrSpacePattern.sub('',message.upper()).split()
	for cipherword in cipherwordList:
		#Get a new cipherletter mapping for each ciphertext word.
		newMap=getBlankCipherLetterMapping()
		
		wordPattern = getWordPattern(cipherword)
		if wordPattern not in wordPatterns.allPatterns:
			continue #this word was not in our dictionary, so continue.
		
		#add the letters of each candidate to the mapping.
		for candidate in wordPatterns.allPatterns[wordPattern]:
			newMap=addLettersToMapping(newMap, cipherword, candidate)
		
		#intersect the new mapping with the existing intersected mapping.
		intersectedMap=intersectMapping(intersectedMap, newMap)
	#remove any solved letters from the other lists:
	return removeSolvedLettersFromMapping(intersectedMap)
def decryptWithCipherletterMapping(ciphertext,letterMapping):
	#return a string of the ciphertext decrypted with the letter mapping,
	#with any ambiguous decrypted letters replaced with an _underscore.
	key=['x']*len(LETTERS)
	for cipherletter in LETTERS:
		if len(letterMapping[cipherletter])==1:
			# if there's only one letter, add it to the key.
			keyIndex=LETTERS.find(letterMapping[cipherletter][0])
			key[keyIndex]=cipherletter

		else:

			ciphertext=ciphertext.replace(cipherletter.lower(),"_")
			ciphertext=ciphertext.replace(cipherletter.upper(),"_")
	key = ''.join(key)
	
	return translateSimSubMessage(key,ciphertext,'decrypt')

def vingenereCipher():
	myMessage=input('please enter your message: ')
	if myMessage=='':
		myMessage="""Alan Mathison Turing was a British mathematician, 
		logician, cryptanalyst, and computer scientist. He was highly 
		influential in the development of computer science, providing a 
		formalisation of the concepts of "algorithm" and "computation" with the
		Turing machine. Turing is widely considered to be the father of computer 
		science and artificial intelligence. During World War II, Turing worked 
		for the Government Code and Cypher School (GCCS) at Bletchley Park, 
		Britain's codebreaking centre. For a time he was head of Hut 8, the section
		responsible for German naval cryptanalysis. He devised a number of 
		techniques for breaking German ciphers, including the method of the bombe,
		an electromechanical machine that could find settings for the Enigma machine. 
		After the war he worked at the National Physical Laboratory, where he created 
		one of the first designs for a stored-program computer, the ACE. In 1948 
		Turing joined Max Newman's Computing Laboratory at Manchester University,
		where he assisted in the development of the Manchester computers and became 
		interested in mathematical biology. He wrote a paper on the chemical basis 
		of morphogenesis, and predicted oscillating chemical reactions such as the 
		Belousov-Zhabotinsky reaction, which were first observed in the 1960s. 
		Turing's homosexuality resulted in a criminal prosecution in 1952, 
		when homosexual acts were still illegal in the United Kingdom. 
		He accepted treatment with female hormones (chemical castration) as an 
		alternative to prison. Turing died in 1954, just over two weeks 
		before his 42nd birthday, from cyanide poisoning. An inquest determined that 
		his death was suicide; his mother and some others believed his death was 
		accidental. On 10 September 2009, following an Internet campaign, 
		British Prime Minister Gordon Brown made an official public apology on 
		behalf of the British government for "the appalling way he was treated." 
		As of May 2012 a private member's bill was before the House of Lords which 
		would grant Turing a statutory pardon if enacted."""
		print('using default: ',myMessage)
	myKey=input('Please provide a key. Default is ASIMOV. Type (Random) for a random key. ')
	if myKey=='':
		myKey='ASIMOV'
	myMode=input('Please enter (E)ncrypt or (D)ecrypt :')
	if myMode.upper().startswith('E'):
		myMode='encrypt'
	elif myMode.upper().startswith('D'):
		myMode='decrypt'
	else:
		print('not a valid input. Default will encrypt')
		myMode='encrypt'
	translated=translateVigenere(myKey,myMessage,myMode)
	
	print('%sed message:' %(myMode.title()))
	print(translated)
	pyperclip.copy(translated)
	print()
	print('The message has been copied to the clipboard.')
	
def translateVigenere(key,message,mode):
	translated=[]
	
	keyIndex=0
	key=key.upper()
	
	for symbol in message:
		num=LETTERS.find(symbol.upper()) # -1 means symbol.upper() was not found in LETTERS.
		if num != -1:
			if mode =='encrypt':
				num+= LETTERS.find(key[keyIndex]) #add if encrypting.
			elif mode =='decrypt':
				num-= LETTERS.find(key[keyIndex]) #subtract if decrypting.
			num%=len(LETTERS)
			#add the encrypted/decrypted symbol to the end of translated:
			if symbol.isupper():
				translated.append(LETTERS[num])
			elif symbol.islower():
				translated.append(LETTERS[num].lower())
				
			keyIndex +=1 #move to the next letter in the key.
			if keyIndex==len(key):
				keyIndex=0
		else:
			translated.append(symbol)
	return ''.join(translated)

#-----cracking the vingenereCipher-----

def freqGetLetterCount(message):
	#returns a dictionary with keys of single letters and values of 
	#the count of how many times they appear in the message parameter.
	LetterCount={l : 0 for l in string.ascii_uppercase}
	
	for letter in message.upper():
		if letter in LETTERS:
			LetterCount[letter] +=1
	return LetterCount

def freqGetItemAtIndexZero(x):
	return x[0]

def freqGetFrequencyOrder(message):
	#returns a string of the alphabet letters arranged in order of most
	#frequently occurring in the message parameter.
	
	#first, get a dictionary of each letter and its frequency count:
	letterToFreq=freqGetLetterCount(message)
	
	#second, make a dictionary of each frequency count to each letter(s)
	#with that frequency
	freqToLetters={}
	for letter in LETTERS:
		if letterToFreq[letter] not in freqToLetters:
			freqToLetters[letterToFreq[letter]]=[letter]
		else:
			freqToLetters[letterToFreq[letter]].append(letter)
	#third, put each list of letters in reverse ETAOIN order, then 
	#convert to a string.
	for freq in freqToLetters:
		freqToLetters[freq].sort(key=ETAOIN.find, reverse=True)
		freqToLetters[freq]=''.join(freqToLetters[freq])
		
	#fourth, convert the freqToLetters dictionary to a list of tuple
	#pairs (key,value), then sort them.
	
	freqPairs=list(freqToLetters.items())
	freqPairs.sort(key=freqGetItemAtIndexZero, reverse=True)
	#now that the letters are ordered by frequency, extract all
	#the letters for the final string.
	return ''.join([l[1] for l in freqPairs])

def englishFreqMatchScore(message):
	#return the number of matches that the string in the message.
	#parameter has when its letter frequency is compared to English
	#letter frequency. A 'match' is how many of its six most frequently
	#and six least frequent letters is among the six most frequent
	#and six least frequent letters for English.
	freqorder= freqGetFrequencyOrder(message)
	
	matchScore=0
	
	for commonLetter in ETAOIN[:6]:
		if commonLetter in freqorder[:6]:
			matchScore +=1
	
	for uncommonLetter in ETAOIN[-6:]:
		if uncommonLetter in freqorder[-6:]:
			matchScore +=1
	return matchScore
	
def vigenereDictionaryHacker():

	
	ciphertext=input('Enter text to decrypt. If left blank, will use a default :')
	if ciphertext=='':
		ciphertext="""Tzx isnz eccjxkg nfq lol mys bbqq I lxcz."""
		hackedMessage=hackVigenereDict(ciphertext)
		
		if hackedMessage != None:
			print('Copying hacked message to clipboard: ')
			print(hackedMessage)
			pyperclip.copy(hackedMessage)
		else:
			print('Failed to hack encryption.')

def hackVigenereDict(ciphertext):
	import detectingEnglish
	fo=open('dictionary.txt')
	words=fo.readlines()
	fo.close()
	
	for word in words:
		word = word.strip()
		decryptedText=translateVigenere(word,ciphertext,'decrypt')
		if detectingEnglish.isEnglish(decryptedText, wordPercentage=40):
			print('\nPossible encryption break: ')
			print('Key '+str(word) + ': '+decryptedText[:100])
			print()
			print('Enter D for done, or just press enter to continue breaking: ')
			response=input('> ')
			
			if response.upper().startswith('D'):
				return decryptedText

def vigernereHacker():
	import itertools, re, detectingEnglish
	SILENT_MODE=False
	Num_most_freq_letters=4
	
	
	
	ciphertext=input('Enter encrypted string: ')
	if ciphertext=='':
		ciphertext = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi, lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum. Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg (GUKE) oo Bdmfqclwg Bomk, Tzuhvif'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi 1948 Tmzubb jgqzsy Msf Zsrmsv'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg, ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny'a tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz 1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa at Haq 2012 i bfdvsbq azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd."""
		
	hackedMessage = hackeVigernere(ciphertext)
	
	if hackedMessage != None:
		print{'Copying hacked message to clipboard:'}
		print(hackedMessage)
		pyperclip.copy(hackedMessage)
	else:
		print('Failed to hack encryption.')

def findRepeatSequencesSpacing(message):

	#finds 3-5 letter sequences that are repeated.
	
	#use a regular expression to remove non-letters from the message:
	message=re.compile('[^A-Z]').sub('',message.upper())
	
	#Compile a list of seqLen-letter sequences found in the message.
	seqSpacing={}
	for seqLen in range(3,6):
		for seqStart in range(len(message)-seqLen):
		#determine what the sequence is, and store it in seq.
			seq=message[seqStart:seqStart+seqLen]
			
			#look for this sequence in the rest of the message.
			for i in range(seqStart+seqLen, len(message)-seqLen):
				if message[i:i+seqLen]==seq:
					#found a repeated sequence.
					if seq not in seqSpacing:
						seqSpacing[seq]=[] #initialize a blank list.
					#otherwise, append the spacing distance between the repeated sequence and the original sequence.
					seqSpacing[seq].append(i-seqStart)
	return seqSpacing

def getUsefulFactors(num):

	#returns a list of useful factors of num. By 'useful', we mean factors 
	#less than max_key_length +1 for example, getUsefulFactors(144)
	#returns [2,72,3,48,4,36,6,24,8,18,9,16,12]
	
	max_key_length=16
	
	if num <2:
		return[] #numbers less than two have no useful factors.
	factors=[]
	for i in range(4, max_key_length+1) #don't test 1
		if num % i ==0:
			factors.append(i)
			factors.append(int(num/i))
	if 1 in factors:
		factors.remove(i)
	return list(set(factors))
	
def getItemAtIndexOne(x):

	returnx[1]
	
def getMostCommonFactors(seqFactor):

	max_key_length=16
	#first, get a count of how many times a factor occurs in seqFactor.
	factorCount={}
	
	#seqFactor keys are sequences, values are lists of factors of the 
	#spacings. seqFactor has a value like: ['GFD':[2,3,4,6,9,12,18,23...],
	# 'ALW': [2,3,4,5...]}
	for seq in seqFactor:
		factorList=seqFactor[seq]
		for factor in factorList:
			factorCount[factor]=0
		factorCount[factor] +=1
	
	#secod, put the factor and its count into a tuple, and make a list
	#of these tuples so we can sort them.
	
	factorsByCount=[]
	for factor in factorCount:
		#exclude anything larger than max_key_length
		if factor <= max_key_length:
			#factorsByCount is a list of tuples: (factor, factorCount)
			#factorsByCount has a value like:[(3,497),(2,487),...]
			factorsByCount.append((factor, factorCount[factor]))
			
	#sort the list by the factor count.
	factorsByCount.sort(key=getItemAtIndexOne, reverse=True)
	
	return factorsByCount
	
def kasiskiExamination(ciphertext):
	#find out the sequences of 3 to 5 letters that occur multiple times
	#in the ciphertext. repeatSeqSpacing has  a value like: 
	#{'EXG': [192],'NAF':[339, 972, 633],...}
	repeatSeqSpacing=findRepeatSequencesSpacing(ciphertext)
	
	#see getmostcommonfactor() for a descripthion of seqFactor.
	