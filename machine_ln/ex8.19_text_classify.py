#!/usr/bin/env python
import os
import operator
import numpy as np 
from sklearn import model_selection

##############################
###  Read all file paths   ###
##############################

path = '/home/sa0102/ai/aufgaben/kapitel8/mini_newsgroups'
f_paths = [] # list of all paths to text files along with class as number
train_path = []
test_path = []

folderlist = os.listdir(path) #get all folders present in data path
i=0 # Variable defining classes as numbers

# Generate path for each and every file
for folder in folderlist:
    filelist = os.listdir(path + '/' + folder)
    for files in filelist:
        f_paths.append((path + '/' + folder + '/' + files, i)) 
    i += 1

total_classes = i

# Splitting the data using Sklearn in 3:1 ratio
train_path , test_path = model_selection.train_test_split(f_paths)

print('Total number if text file found : {}'.format(len(f_paths))) #400
print('Set number if training files : {}'.format(len(train_path))) #280
print('Set number if test files : {}'.format(len(test_path))) #120
print('Total classes in training files : {}'.format((total_classes))) #120

##############################
###  Probabilty each class  ##
##############################

p_each_class = [0] * total_classes

for k in range(total_classes):
    for doc in train_path: # each file in train path
        if doc[1] == k: #if class is equal to denoted number 'k'
            p_each_class[k] += 1 # increment to count total documetns
    p_each_class[k] = np.log(p_each_class[k] / len(train_path))
#print(p_each_class)

##############################
## Segregate data and class ##
##############################

train_data = []
train_class = []
for i in range(len(train_path)):
    train_data.append(train_path[i][0])
    train_class.append(train_path[i][1])

################################
##       Total Vocabulary     ##
################################

# Reference: https://github.com/AmritK10/20_Newsgroups_Text_classification/
# blob/master/Text_Classification_20_newsgroups.ipynb
import string
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop=set(stopwords.words("english"))
stop_words=list(stop)+list(set(string.punctuation))


vocab  = [] #dictionary
for filename in train_data: # for every file path in training data set
    f = open(filename, 'r', errors='ignore') #open file as read-only
    record = f.read() # read contents
    words = record.split() # split content into words, eliminating spaces
    for w in words: # for all recorded words, append to list if satisfies the conditions
        if len(w)>3 and w.lower() not in stop_words:
            if w.lower() not in vocab:
                vocab.append(w.lower())

print('Total word count : {}'.format(len(vocab))) #~19k
print('Training...')

################################
##  Class - wise Vocabulary   ##
################################

# Class_dict contains the vocabulary per class. It is a list of 4 elements each contains
# ..vocab of 1 class. So if I access (class_vocab[3][1000]), it will give me 1000th word
# .. of class 3. Output will be like ('>go', 3).

# Doing it with dictionary simplifies as items can be named as frequency can be counted easily

class_vocab = [None] * total_classes 

for m in range(total_classes): # for every class in training data set
    class_vocab[m] = {} # initializing empty dictionaray
    temp_dict = class_vocab[m] # temp variable for storing items as dictionary
    
    for tfile in train_path: # for every file path in training data set
        if tfile[1] == m: # if class == m
            
            f = open(tfile[0],'r', errors='ignore') #open file as read-only
            record = f.read() # read contents
            words = record.split()
            for w in words: # for each word (if satisfies condition) -->
                if len(w)>2 :
                    if w.lower() in temp_dict: # if already in dictionary, then increment count by 1
                        temp_dict[w.lower()] += 1
                    else:
                        temp_dict[w.lower()] = 1 # otherwise create a new item and set freq as 1
    #sort wrt freq. This also allows to access items with indexing
    temp_dict = sorted(temp_dict.items(), key= operator.itemgetter(1), reverse= True)
    class_vocab[m] = temp_dict # assign whatever is stored in temp_dict back to class_dict


################################
##      Word probability      ##
################################

# Calculate the probability of each feature occuring in Class 
# ..(count w in class/ count w in V)

# Likelihood is an list size of which is equal to vocab, each element is also a list type.
# .. which has info: ['word', p_class0, p_class1,....p_classi,...]
# eg: [[['the', -2.0830713097304145, -2.1260338194819024, -2.1735292867467355, -2.290120342374059]], 
# [['and', -3.211206037664846, -3.0094834451668153, -2.5781415163383823, -3.1495029419763343]]]

likelihood = [] #

for word in vocab:   
    temphood = [] # temp list for each word which will appended later to main list
    feature = word # set feature as word from total vocab
    temphood.append(feature)
    temp_voc = [] # using if statements is very time consuming, so we make a temp voc from..
    # class_dict with only words (eliminate the frequencies)
    
    for i in range(len(class_vocab)): # to find likelihood in each class
        occ = 0 # se occurence count to zero
        for word in class_vocab[i]: # Simplify vocab (eliminate freq as said above)
            temp_voc.append(word[0])

        if feature in temp_voc: # find if feature also lies in class_dict
            idx = temp_voc.index(feature) # find its index
            #print(class_vocab[i][idx])
            occ += class_vocab[i][idx][1] # find its frequency in class_dict
            temp_voc = [] # empty temp_vocab for next iteration

        else: # if word not found
            occ = 0 # set occurence to zero
            temp_voc = []

        # Probability of each feature in log terms
        l_word = np.log( (occ+1) / ( len(class_vocab[i]) + 1))
        temphood.append(l_word)
    likelihood.append([temphood]) # append to mail list

#print('Likelihood {}'. format(likelihood[2][0][1:]))

# To evalute test data in this 'likelihood' list (for better computation time), we ..
# again take out the first word out and put it in search group
search_group = []
for word in likelihood:
    search_group.append(word[0][0])

#print('Few entries from searh grp {}'. format(search_group[:5]))

################################
##      Evalate test data     ##
################################

print('Testing......')
# Initialize variable
err = 0
tested = 0

for z in range(len(test_path)): # for each file in test_path
    f = open(test_path[z][0],'r', errors='ignore')
    test_dict = [] # to create a vocab of words
    sums = [0] * total_classes # list based on which we predict class (argmax)
    record = f.read()
    words = record.split()
    for w in words: # for each word in test file, append to test_dict if it satisfies conditions
        if len(w)>2:
            if w.lower() not in temp_dict:
                test_dict.append(w.lower())
    #print('Items from test_dict {}'. format(test_dict[:5]))
   
    for word in test_dict: # for each word in test_dict
        
        if word in search_group: # search if same word is also in search group
            tested += 1
            posn = search_group.index(word) # find its index
            sums = [a+b for a,b in zip(sums, likelihood[posn][0][1:])] # add the probability of each class to sums list
            

    sums = [ (a+b) for a,b in zip(sums, p_each_class)] # Add prior probabilities P(c)
    #print(sums)
    new_class = sums.index(max(sums))
    #print('Predicted class is {}'.format(new_class))
    #print('Actual class is {}'.format(test_path[z][1]))
    if new_class != test_path[z][1]:
        err += 1

print('Error rate @ test data is {} %'.format((err*100)/(len(test_path))))
print('Total words that are matched : {}'.format(tested))