from nltk.tag.stanford import StanfordNERTagger
english_nertagger = StanfordNERTagger('yourpath/classifiers/english.all.3class.distsim.crf.ser.gz','yourpath/stanford-ner.jar')
myfile = open("filename.txt")
str = myfile.read()
str_split = english_nertagger.tag(str.split())
file = open("newfile.txt", "w")
print >> file, str_split
file.close()
