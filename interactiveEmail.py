import os
from argparse import ArgumentParser as parser
from classifier import *
import re
from datetime import datetime


spam_examples=input("Enter spam examples location: ")
ham_examples=input("Enter ham examples location: ")
test=input("Enter e-mail archive location: ")


#Get messages from files
spam_example_messages = messages(spam_examples)
ham_example_messages = messages(ham_examples)
test_messages = messages(test)

#Spam and ham words with their occurences per message
spam_words = word_occurences(spam_example_messages)
ham_words = word_occurences(ham_example_messages)
test_words = word_occurences(test_messages)

#Spam and ham word frequencies
spam_word_frequencies = word_frequencies(spam_words)
ham_word_frequencies = word_frequencies(ham_words)

#Set initial probability of spam
init_prob_spam = 0.5
occurence_threshold = 10  #minimum no of times a word must be present in spam dataset to classify it as spam       
score_threshold = 0.9   #minimum spam score to classify message as spam message

#Probability of a word being spam
word_spam_prob = word_spam_prob(spam_word_frequencies, ham_word_frequencies, init_prob_spam, occurence_threshold)

#classification count
spam_message_count = 0
ham_message_count = 0

def getdate(f_contents):
	dateobj=re.search("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d\d,\s+\d\d\d\d", f_contents)
	timeobj=re.search("\d{1,2}:\d\d\s+[PA]M", f_contents)
	if dateobj and timeobj:
		date=dateobj.group(0)
		date=''.join(e for e in date if (e.isalnum() or e.isspace()))
		time=timeobj.group(0)
		time=''.join(e for e in time if (e.isalnum() or e==':'))
		date_time=date+" "+ time
		datetime_object = datetime.strptime(date_time, '%b %d %Y %I:%M%p')
		return datetime_object
	else:
		return datetime.strptime('Jan 1 1975  1:00PM', '%b %d %Y %I:%M%p')

def get_title(f_contents):
	title=""
	for i in range(0, len(f_contents)):
		if f_contents[i]=='>':
			i+=2;
			while not(f_contents[i]=='\n'):
				title+=f_contents[i]
				i+=1
			break;
	print(title)	
class Stack:
	def __init__(self):
		self.items = []
	def isEmpty(self):
		return self.items == []
	def pushT(self, item):
		self.items.append(item)
	def push(self, item):
		temp=Stack()
		if self.isEmpty():
			self.pushT(item)
		elif getdate(item)>getdate(self.peek()):
			self.pushT(item)
		else:
			while not(self.isEmpty()):
				if getdate(item)<getdate(self.peek()): 
					temp.pushT(self.pop())
		self.pushT(item)
		while not(temp.isEmpty()):
			self.pushT(temp.pop())
	def pop(self):
		return self.items.pop()
	def peek(self):
		return self.items[len(self.items)-1]
	def size(self):
		return len(self.items)
spam_stack=Stack()
ham_stack=Stack()

#MAIN FUNCTION TO CLASSIFY
curPath=os.getcwd()
spam_file=open("spam_mails.txt", "w+", encoding="utf-8", errors="ignore")
ham_file=open("ham_mails.txt", "w+", encoding="utf-8", errors="ignore")
os.chdir(test)
tempcount=0
for key in sorted(test_words):
    message_score = spam_score(test_words[key], word_spam_prob)
    if message_score > score_threshold:
    	f=open(key, 'r', encoding="utf-8", errors="ignore")
    	f_contents=f.read()
    	if tempcount==0:
    		spam_stack.pushT(f_contents)
    	else:
    		spam_stack.push(f_contents)
    	tempcount+=1
    	spam_message_count += 1
    	
os.chdir(curPath)
os.chdir(test)
tempcount=0
for key in sorted(test_words):
    message_score = spam_score(test_words[key], word_spam_prob)
    if message_score < score_threshold:
    	f=open(key, 'r', encoding="utf-8", errors="ignore")
    	f_contents=f.read()
    	if tempcount==0:
    		ham_stack.pushT(f_contents)
    	else:
    		ham_stack.push(f_contents)
    	tempcount+=1
    	ham_message_count += 1

#Calculate percentage of spam and ham messages
spam_percentage = spam_message_count / len(test_messages)
ham_percentage = ham_message_count / len(test_messages)
print("Spam percentage: {0:.2f}%".format(spam_percentage * 100))
print("Ham percentage: {0:.2f}%".format(ham_percentage * 100))

#Writing to Files
while not(spam_stack.isEmpty()):
	spam_file.write("==================================================================================================================================\n")
	spam_file.write("==================================================================================================================================\n")
	spam_file.write(spam_stack.pop())
while not(ham_stack.isEmpty()):
	get_title(ham_stack.peek())
	ham_file.write("==================================================================================================================================\n")
	ham_file.write("==================================================================================================================================\n")
	ham_file.write(ham_stack.pop())
spam_file.close()
ham_file.close()

os.chdir(curPath)
flag=1

#INTERACTIVE MENU
while flag!=0:
	in_title=input("Input title of the e-mail you wish to read [Press ? to EXIT]: ")
	if in_title=='?':
		flag=0
		break
	else:
		ham_file=open("ham_mails.txt", "r")
		ham_contents=ham_file.read()
		m_title=re.search(in_title, ham_contents)
		if m_title:
			(_, last_index)=m_title.span()
			for i in range(last_index+1, len(ham_contents)):
				if ham_contents[i]=='=' and ham_contents[i+5]=='=':
					break
				else:
					print(ham_contents[i], end="")
