#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
trancriber mg1.4
'''

import sys, re
import collections

class TranscriberRegexp:

# http://cmusphinx.sourceforge.net/wiki/tutorialam
#   Do not use case-sensitive variants like “e” and “E”. Instead, all your phones must be different even in case-insensitive variation. Sphinxtrain doesn't support some special characters like '*' or '/' and supports most of others like ”+” or ”-” or ”:” But to be safe we recommend you to use alphanumeric-only phone-set. Replace special characters in the phone-set, like colons or dashes or tildes, with something alphanumeric. For example, replace “a~” with “aa” to make it alphanumeric only.


# 1 - nosinė, 2 - šnipštimas(ž,š), e3 ė _-ilgumas($/:) .-minkštumas(')
    graphemeToPhonemeMap = [
        ("iu", "IU"),#Svarbu jei be minkštumo
        ("ių", "IU_"),#Svarbu jei be minkštumo
        ("io", "IO_"),#Svarbu jei be minkštumo
        #("ui", "UI"),
        #("uo", "UO"),
        ("ia", "E"),
        ("ią", "E_"),
        #("tst", "T S T"), #atstatyk# nebėra versijoje z1.3
        #("ts", "C"),#atsakymą,atsiųsk# nebėra versijoje z1.3
        ("tsi", "C I"), #atsisakyk
        ("iau", "E U"),
        ("ja", "J. E"), #jau, japonas
        ("ją", "J. E_"), #naują
        

        #Dantiniai priebalsiai {S, Z, C, DZ} prieš alveolinius {S2, Z2, C2, DZ2} keičiami atitinkamai į alveolinius {S2, Z2, C2, DZ2} (slenksčiai -> S L E N K S2 C2 E I).
        ("sž","S2 Z2"),#?
        ("sč","S2 C2"),#kunigaikštysčiu
        ("zdž","Z2 DZ2"),#vabzdžiai
        
        # duslieji prieš skardžiuosius
        ("pb", "B B"),
        ("pg", "B G"),#apgadintas
        ("pz", "B Z"),
        ("pž", "B Z2"),
        ("pdz", "B DZ"),
        ("pdž", "B DZ2"),
        ("pd", "B D"),
        ("ph", "B H"),
        ("tb", "D B"),#atbaidyti
        ("tg", "D G"),#atgabenti
        ("tz", "D Z"),
        ("tž", "D Z2"),#atžvilgiu
        ("tdz", "D DZ"),
        ("tdž", "D DZ2"),
        ("td", "D D"),
        ("th", "D H"),
        ("kb", "G B"),
        ("kdz", "G DZ"),
        ("kdž", "G DZ2"),
        ("kd", "G D"),#atlikdavo
        ("kg", "G G"),
        ("kz", "G Z"),
        ("kž", "G Z2"),

        ("kh", "G H"),
        ("sb", "Z B"),#feisbukas

        ("sg", "Z G"),
        ("sz", "Z Z"),
        ("sž", "Z Z2"),
        ("sdz", "Z DZ"),
        ("sdž", "Z DZ2"),
        ("sd", "Z D"),#kasdami
        ("sh", "Z H"),
        ("šb", "Z2 B"),#išbandyti
        ("šg", "Z2 G"),#išgaubti
        ("šz", "Z2 Z"),
        ("šž", "Z2 Z2"),
        ("šdz", "Z2 DZ"),
        ("šdž", "Z2 DZ2"),
        ("šd", "Z2 D"),#neišdildoma
        ("šh", "Z2 H"),
        ("cb", "DZ B"),
        ("cg", "DZ G"),
        ("cz", "DZ Z"),
        ("cž", "DZ Z2"),
        ("cdz", "DZ DZ"),
        ("cdž", "DZ DZ2"),
        ("cd", "DZ D"),
        ("ch", "DZ H"),
        ("čb", "DZ2 B"),
        ("čg", "DZ2 G"),
        ("čz", "DZ2 Z"),
        ("čž", "DZ2 Z2"),
        ("čdz", "DZ2 DZ"),
        ("čdž", "DZ2 DZ2"),
        ("čd", "DZ2 D"),
        ("čh", "DZ2 H"),
        ("chb", "H B"),
        ("chg", "H G"),
        ("chz", "H Z"),
        ("chž", "H Z2"),
        ("chdz", "H DZ"),
        ("chdž", "H DZ2"),
        ("chd", "H D"),
        ("chh", "H H"),
        
        #skardieji prieš dusliuosius
        ("bp", "P P"),
        ("bt", "P T"),
        ("bk", "P K"),
        ("bs", "P S"),
        ("bš", "P S2"),
        ("bc", "P C"),
        ("bč", "P C2"),
        ("bch", "P CH"),

        ("dp", "T P"),
        ("dt", "T T"),
        ("dk", "T K"),
        ("ds", "T S"),
        ("dš", "T S2"),
        ("dch", "T CH"),
        ("dc", "T C"),
        ("dč", "T C2"),


        ("gp", "K P"),
        ("gt", "K T"),#vašingtonas, jungtinių
        ("gk", "K K"),#angkoras -> A N K K O_ R A S
        ("gs", "K S"),
        ("gš", "K S2"),
        ("gch", "K CH"),
        ("gc", "K C"),
        ("gč", "K C2"),

        ("zp", "S P"),
        ("zt", "S T"),#megztinis
        ("zk", "S K"),
        ("zs", "S S"),
        ("zš", "S S2"),
        ("zch", "S CH"),
        ("zc", "S C"),
        ("zč", "S C2"),

        ("žp", "S2 P"),
        ("žt", "S2 T"),
        ("žk", "S2 K"),#grįžk
        ("žs", "S2 S"),
        ("žš", "S2 S2"),
        ("žch", "S2 CH"),
        ("žc", "S2 C"),
        ("žč", "S2 C2"),

        ("dzp", "C P"),
        ("dzt", "C T"),
        ("dzk", "C K"),
        ("dzs", "C S"),
        ("dzš", "C S2"),
        ("dzch", "C CH"),
        ("dzc", "C C"),
        ("dzč", "C C2"),

        ("džp", "C2 P"),
        ("džt", "C2 T"),
        ("džk", "C2 K"),
        ("džs", "C2 S"),
        ("džš", "C2 S2"),
        ("džch", "C2 CH"),
        ("džc", "C2 C"),
        ("džč", "C2 C2"),

        ("hp", "CH P"),
        ("ht", "CH T"),
        ("hk", "CH K"),
        ("hs", "CH S"),
        ("hš", "CH S2"),
        ("hch", "CH CH"),
        ("hc", "CH C"),
        ("hč", "CH C2"),




        

        ("ch", "CH"),
        ("dž", "DZ2"),
        ("dz", "DZ"),

                
        #grafemos
        ("a", "A"),
        ("ą", "A_"),
        ("b", "B"),
        ("c", "C"),
        ("č", "C2"),
        ("d", "D"),
        ("e", "E"),
        ("ę", "E_"),
        ("ė", "E3_"),
        ("f", "F"),
        ("g", "G"),
        ("h", "H"),
        ("i", "I"),
        ("į", "I_"),
        ("y", "I_"),
        ("j", "J."),
        ("k", "K"),
        ("l", "L"),
        ("m", "M"),
        ("n", "N"),
        ("o", "O_"),
        ("p", "P"),
        ("r", "R"),
        ("s", "S"),
        ("š", "S2"),
        ("t", "T"),
        ("u", "U"),
        ("ų", "U_"),
        ("ū", "U_"),
        ("v", "V"),
        ("w", "V"),
        ("z", "Z"),
        ("ž", "Z2"),
        ]

        #daug gale b,d,g,z,ž(skardieji) kaip p,t,k,s,š(duslieji)+
        #grįžk skardieji prieš duslieji š
        #minkštumas: džiaugsmas prieš e, i, ė yra minkšti
        #minkštumas: ankstenė - k ir g sustabdomas minkšumas anks't'enė
        #!Neitraukiant minkšrumo! tai butinai reikia iu ir io kaip atskiros fonemos. 

    preprocesorMap = [
        ("^ie","jie"),
        ("b$","p"),
        ("d$","t"),
        ("g$","k"),#daug->dauk
        ("z$","s"),
        ("ž$","š"),
        ("dz$","c"),
        ("dž$","č"),
        ("h$","ch"),
        ("facebookas","feisbukas"),
        ("unesco","junesko"),
    ]

    def __init__(self):
        transcribation_keys = map(lambda x: x[0], self.graphemeToPhonemeMap)
        self.transcribation_rulesDict = dict(self.graphemeToPhonemeMap)
        transcribation_regexStr = "(%s)" % "|".join(map(re.escape, transcribation_keys))
        # Create a regular expression  from the dictionary keys
        self.transcribation_regex = re.compile(transcribation_regexStr)

        #preprocess_keys = map(lambda x: x[0], self.preprocesorMap)
        #self.preprocess_rulesDict = dict(self.preprocesorMap)
        #preprocess_regexStr = "(%s)" % "|".join(map(re.escape, preprocess_keys))
        ## Create a regular expression  from the dictionary keys
        #self.preprocess_regex = re.compile(preprocess_regexStr)
        self.preprocess_regex_map = []
        for key, value in self.preprocesorMap:
            pattern = re.compile(r"("+key+")")
            self.preprocess_regex_map.append((pattern, value));

    def preprocessText(self,text):
        for key, value in self.preprocess_regex_map:
            text = key.sub(value,text)
        return text

    def multiple_replace(self,  text):
        #preprocesedText = self.preprocess_regex.sub(lambda mo: " " + self.preprocess_rulesDict[mo.string[mo.start():mo.end()]] + " ", text)
        preprocesedText = self.preprocessText(text)
        #print "[{}=>{}]".format(text,preprocesedText)
        # For each match, look-up corresponding value in dictionary
        return self.transcribation_regex.sub(lambda mo: " " + self.transcribation_rulesDict[mo.string[mo.start():mo.end()]] + " ", preprocesedText)

    def transcribe(self, word):
        lowerWord = word.decode('utf-8').lower().encode('utf-8')
        transcibedWord = self.multiple_replace(lowerWord)
        transcibedWord = re.sub(r'\s+', ' ', transcibedWord)
        transcibedWord = transcibedWord.upper().strip()
        return transcibedWord;

    def transcribeDictionary(self, text):
        translatedMap = {}
        lowerText = text.decode('utf-8').lower().encode('utf-8')
        lowerText = re.sub(r"[\.\,\?\!\"\/\_><]+", r" ", lowerText)
        for wortEntry in lowerText.split():
            wordTranslated = self.transcribe(wortEntry)
            translatedMap[wortEntry] = wordTranslated
        translatedMap = collections.OrderedDict(sorted(translatedMap.items(), key=lambda t: t[0]))
        return translatedMap







import argparse

def processWords(words):
    transcriber = TranscriberRegexp()
    sphinx_dictionary = transcriber.transcribeDictionary(words)
    return sphinx_dictionary

def processFile(input_file):
    sphinx_dictionary = collections.OrderedDict()
    for line in input_file:
        loop_dictionary = processWords(line)
        sphinx_dictionary.update(loop_dictionary)
    sphinx_dictionary = collections.OrderedDict(sorted(sphinx_dictionary.items(), key=lambda t: t[0]))
    return sphinx_dictionary

        
def writeToFile(sphinx_dictionary, output_file):
    for key, value in sphinx_dictionary.iteritems():
        output_file.write("{}\t{}\n".format(key, value))
        
def writeToConsole(sphinx_dictionary):
    for key, value in sphinx_dictionary.iteritems():
        print "{}\t{}".format(key, value)


def main():
    usage='%(prog)s --help'
    description='''Transcription text to phone for CMU Sphinx recognition. Example: %(prog)s -i zodziai.txt -o zodziai.dict
    '''
    parser = argparse.ArgumentParser(usage=usage,description=description)    
    parser.add_argument('-o', '--output_file', help='Output text dictionary file: word   W O R D', metavar='out-file', type=argparse.FileType('wt'))
    parser.add_argument('-v', '--verbose', action='store_true',help='Verbose output for debuging')
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("input_words",  nargs='?', help="echo the string you use here")
    group.add_argument('-i', '--input_file', help='Input text file one word per line, \'-\' for standard input', metavar='in-file', type=argparse.FileType('rt'))

    
    args = parser.parse_args()
    if args.verbose: print args
    sphinx_dictionary = {}
    
    if args.input_file:
        sphinx_dictionary = processFile(args.input_file)
    elif args.input_words:
        sphinx_dictionary = processWords(args.input_words)
    else:
        sphinx_dictionary = processWords("bandom besikiškiakopūstaudavome")
        
    if args.output_file:
        writeToFile(sphinx_dictionary, args.output_file)
    else:
        writeToConsole(sphinx_dictionary)

if __name__ == "__main__":
    main()


