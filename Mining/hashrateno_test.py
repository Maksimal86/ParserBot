# -*- coding: utf-8 -*-
import re


text = ['ALPH  Alephium  Blake3','NH-Ethash NH-Alephium NiceHash Daggerhashimoto NiceHash Alephium ethash','IRON  Iron fish  fishhash']
for i in text:
    print(re.search('\S*', i)[0])

t= 'ALPH  Alephium  Blake3'
print(re.search('\D', 'ALPH  Alephium  Blake3')[0])