from pathlib import Path
import readline #gives nicer input line editing
import random
import json
morse_translation_table = {"c": "-.-.", "d": "-..", "e": ".", "f": "..-.", "g": "--.", "h": "....", "i": "..", "j": ".---", "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---", "q": "--.-", "r": ".-.", "s": "...", "t": "-", "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--", "z": "--..", "a": ".-", "b": "-...","p":".--."}
#borrowed from my fuzzy search
def lev(a,b):
	if len(a) == 0:
		return len(b)
	if len(b) == 0:
		return len(a)
	if a[0] == b[0]:
		return lev(a[1:],b[1:])
	return 1+min(lev(a[1:],b),lev(a,b[1:]),lev(a[1:],b[1:]))
def translate_to_morse(word):
	return "".join([morse_translation_table[char]+" " for char in word]).rstrip(" ")
	
class WeightedDict():
	def __init__(self):
		self.weights_path = Path("weights.json")
		self.dictionary_path = Path("dictionary.txt")
		print("loading dictionary...")
		self.load_dictionary()
		print("loading weights...")
		if not self.weights_path.is_file():
			doc = weights_path.open("w")
			doc.write(json.dumps({}))
			doc.close()
		self.load_weights()
		print("ordering dictionary...")
		self.order()
		self.save_weights()
		print("loading complete")
	def save_weights(self):
		with self.weights_path.open("w") as weights_doc:
			weights_doc.write(json.dumps(self.weights,indent=4))
	def order(self):
		#we need to remove the order that they come in the dictionary
		random.shuffle(self.dictionary)
		sorting_filter = lambda word : (-self.weights[word])
		self.dictionary.sort(key=sorting_filter)
	def load_weights(self):
		with self.weights_path.open("r") as weights_dict_doc:
			self.weights = json.loads(weights_dict_doc.read())
		for word in self.dictionary:
			if word not in self.weights:
				self.weights[word] = 0.0
	def load_dictionary(self):
		with self.dictionary_path.open("r") as dict_doc:	
			self.dictionary = [word.rstrip("\n").replace("'","") for word in dict_doc]
	#returns an index in the sorted by weight dictionary
	def __getitem__(self,key):
		return self.weights[key]
	#sets the weight of a word
	def __setitem__(self,key,value):
		self.weights[key] = value
	def __iter__(self):
		for item in self.dictionary:
			yield item
if __name__ == "__main__":
	dict = WeightedDict()
	max_curated = 5
	max_random = 3
	while True:
		words = list(dict)
		#get some weighted picks
		candidates = words[:max_curated]
		#add some random picks
		candidates += random.sample(words[max_curated:],min(len(words[max_curated:]),max_random))
		word = random.choice(candidates)
		#50/50 if they translate to or from morse
		if random.randint(0,1):
			translated_word = list(translate_to_morse(word))
			word_to_translate = word
		else:
			translated_word = list(word)
			word_to_translate = translate_to_morse(word)
		attempt = list(input(f"translate {word_to_translate} >>>"))
		if attempt != translated_word:
			print(f"INCORRECT! should have been {''.join(translated_word)}")
			#calculate margin of error using levenshein distance and adjust the weights accordingly
			weight_increase = 1-(1/lev(attempt,translated_word))
			dict[word] += weight_increase
		else:
			print("correct")
			#adjust the weights to favour the word less
			dict[word] /= 2
		dict.save_weights()
