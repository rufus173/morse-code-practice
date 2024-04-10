import random
class initialise:
    def __init__(self) -> None:
        self.letter_list = ["w","q","w","w","q","q","j","j","j",] # just for me as these are my least confident # if you want leave the list empty
        with open("english words.txt","r") as words:
            self.wordlist = []
            for i in words:
                self.wordlist.append(i)
        with open("morse conversion table.txt","r") as translator:
            self.converting_Table = []# [["a",".-"],["b","-..."]]
            for i in translator:
                self.converting_Table.append(i.strip("\n").split(" "))
    def translate(self,phrase):
        converted_phrase = ""
        if phrase[0] == "." or phrase[0] == "-":
            for x in phrase.split(" "):
                for i in self.converting_Table:
                    if i[1] == x:
                        converted_phrase = converted_phrase + i[0]
                        break
        else:#detects the language and auto converts to the other
            for x in phrase:
                for i in self.converting_Table:
                    if i[0] == x:
                        converted_phrase = converted_phrase + i[1] + " "
                        break
            converted_phrase = converted_phrase.strip(" ")
        return converted_phrase
    
    def compare(self,string1,string2):#checking which characters are present in string 1 but not string 2
        not_in_string2 = []
        for i in string2:
            try:
                string1.index(i)
            except:
                not_in_string2.append(i)
        return not_in_string2
    def mainloop(self):
        
        ###
        #this weights the odds to make it more likely to have to translate into english
        random_pool = [1,1,2,2,2,3,4]
        ####
        
        while True:
            english = True
            if self.letter_list != []:
                addon = 2
            else:
                addon = 0
            random_number = random_pool[random.randint(0,len(random_pool)-3+addon)]#if there are incorrect letters we increase the roll to be able to select to translate a single charecter option
            question = self.wordlist[random.randint(1,len(self.wordlist))-1]
            
            ##################
            #rerolling 100 times to try and find a word with one of a previously incorrect characters in it
            #makes it more likely you get a word with characters you got wrong before
            for i in range(100):
                for i in self.letter_list:
                    if i in question:
                        break
                    question = self.wordlist[random.randint(1,len(self.wordlist))-1]
                else:
                    break
            ###################
            #picks from either single character or word, and which way to translate
            match random_number:
                case 1:
                    pass
                case 2:
                    question = self.translate(question)
                    english = False
                case 3:
                    question = self.letter_list.pop(random.randint(1,len(self.letter_list))-1)
                case 4:
                    question = self.translate(self.letter_list.pop(random.randint(1,len(self.letter_list))-1))#if you get one of these correct character gets removed from the mistakes list
                    english = False# this is the only way for items on the incorrect list to be removed
            ###############
            attempt = input("translate "+question+" >>>")
            if attempt == self.translate(question):
                print("correct")
            else:
                print("should have been "+self.translate(question))
                if english == False: # done for when we compare the wrong answer with the correct one so they are in the same language
                    question = self.translate(question)
                else:
                    attempt = self.translate(attempt)
                for i in self.compare(attempt.strip("\n"),question.strip("\n")):# we figure out wich letters the user got wrong, and store them for later
                    self.letter_list.append(i)
initialise().mainloop()