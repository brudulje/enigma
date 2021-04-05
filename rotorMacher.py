# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 19:12:29 2021

@author: jmg
"""
import random
import roman

alphabet = list("!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ÁÉÍÏÐÓÞÆÄØÖÅáéíïðóþæäøöåßΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя")

# for n in range(1, 12):
#     print(roman.toRoman(n))

# Rotor {RomanNumeral:
#           ["NameRoman", "Scrambled alphabet", ["List", "of", "notches"]}

for n in range(1,4):

    nRoman = roman.toRoman(n)

    scrambled = random.sample(alphabet, len(alphabet))
    scrambled = "".join(scrambled)
    # print(scrambled, {len(scrambled)})

    notches = [i for i in alphabet if random.random() < 0.316227766]
    # print(notches, {len(notches)})

    rotor = [nRoman, scrambled, notches]
    print(rotor)