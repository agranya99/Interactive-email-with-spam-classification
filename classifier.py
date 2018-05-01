#Supporting code that performs Naive Bayes classification. Includes training and testing
import sys
import os
import re

#Regex for a word
word_regex = re.compile("[a-zA-Z']+(?:-[a-zA-Z']+)?")

#Dictionary of messages: keys=filenames & values= messages
def messages(folder):
    messages = {}
    filenames = list(os.walk(folder))[0][2]
    # Parse through all files in folder
    for filename in filenames:
        path = folder + "/" + filename
        with open(path, errors="ignore") as message_file:
            # Add message to dict of messages
            messages[filename] = message_file.read()
    return messages

#Dictionary with keys as filenames and values as dictionaries of word occurences in each file
def word_occurences(messages):
    word_occurences = {}
    for key, message in messages.items():
        words = word_regex.findall(message)
        num_words = len(words)
        message_words = {}
        for word in words:
        	if word not in message_words:
        		message_words[word]=1
        	else:
        		message_words[word]+=1        
        word_occurences[key] = message_words
    
    return word_occurences

#Dictionary of word frequencies with words as keys
def word_frequencies(words):
    word_frequencies = {}
    total_messages = len(words)
    
    #Occurence count of each word in messages
    for key, message in words.items():
        for word in message:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
                
    #Converting occurences to frequencies
    for word, occurences in word_frequencies.items():
        word_frequencies[word] = (occurences / total_messages, occurences)
    
    return word_frequencies

#Dictionary of word spam probability with words as keys
def word_spam_prob(spam_word_frequencies, ham_word_frequencies, init_prob_spam, occurence_threshold):
    spam_prob = {}
    words = set(list(spam_word_frequencies) + list(ham_word_frequencies))
    
    for word in words:
        spam_word_occurences = spam_word_frequencies[word][1] if word in spam_word_frequencies else 0
        ham_word_occurences = ham_word_frequencies[word][1] if word in ham_word_frequencies else 0
        
        #Not including word if it occurs less times than threshold in total
        if spam_word_occurences + ham_word_occurences >= occurence_threshold:
            #Word present in both spam and ham messages
            if word in spam_word_frequencies and word in ham_word_frequencies:                
                prob_word_spam = spam_word_frequencies[word][0] * init_prob_spam
                prob_word_ham = ham_word_frequencies[word][0] * (1 - init_prob_spam)
                spam_prob[word] = prob_word_spam / (prob_word_spam + prob_word_ham)
            #Word not present in spam messages
            elif spam_word_occurences == 0:
                spam_prob[word] = 0.01
            #Word not present in ham messages
            elif ham_word_occurences == 0:
                spam_prob[word] = 0.99
    
    return spam_prob

#Return spam score of a message
def spam_score(message, relevant_words):
    #Ignore words that have not been encountered
    message = [word for word in message if word in relevant_words]
    
    #Get spam_prob of words in message
    spam_prob = [(word, relevant_words[word]) for word in message]
    #Get the top spam_prob, sorted by their distance from neutral (0.5)
    top_spam_prob = sorted(spam_prob, key=lambda x: abs(0.5 - x[1]), reverse=True)[:10]
    prob_spam=1
    prob_spam_inv=1
    for x in top_spam_prob:
    	prob_spam*=x[1]
    	prob_spam_inv*=(1-x[1])
        
    return prob_spam / (prob_spam + prob_spam_inv)
