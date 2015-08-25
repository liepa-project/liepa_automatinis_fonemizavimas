#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'../src')

import unittest
import re
from transcriber_re import TranscriberRegexp



class TrasncriberTest(unittest.TestCase):
    transcriber = TranscriberRegexp()
    transcriptionMap = [
        ("facebookas","F E I Z B U K A S"),
        ("daug","D A U K"),
        ("atsisakyk","A C I S A K I_ K"),
        ("spausdink","S P A U Z D I N K"),
        ("vašingtonas","V A S2 I N K T O_ N A S"),
        ("atbaidyti","A D B A I D I_ T I"),
        ("išbandyti","I Z2 B A N D I_ T I"),
        ("atlikdavo","A T L I G D A V O_"),
        ("kasdami","K A Z D A M I"),
        ("neišdildoma","N E I Z2 D I L D O_ M A"),
        ("išgaubti","I Z2 G A U P T I"),
        ("atžvilgiu","A D Z2 V I L G IU"),
        ("grįžk","G R I_ S2 K"),
        ("megztinis","M E G S T I N I S"),
        ("ieškok", "J. I E S2 K O_ K")
        ] 
    
    def test(self):
        for word,expected in self.transcriptionMap:
            actual = self.transcriber.transcribe(word)
            self.assertEqual(expected, actual,"for word:{} was expected:{}, but got:{}".format(word,expected,actual))
        
if __name__ == '__main__':
    unittest.main()
