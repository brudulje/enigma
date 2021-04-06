# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 19:12:29 2021

@author: jmg
"""
import random
import roman

alphabet = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ÁÉÍÏÐÓÞÆÄØÖÅáéíïðóþæäøöåΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяᚠᚢᚦᚨᚬᚱᚲᚴᚷᚹᚺᚼᚾᛁᛃᛅᛇᛈᛉᛊᛋᛏᛒᛖᛗᛘᛚᛜᛞᛟᛦᛮᛯᛰ"

alphabet = list(alphabet)
# for n in range(1, 12):
#     print(roman.toRoman(n))

# Rotor {RomanNumeral:
#           ["NameRoman", "Scrambled alphabet", ["List", "of", "notches"]}


def genereate_rotors(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                     start=1,
                     stop=4,
                     notch_percentage=0.316227766):
    """Return dict of valid Enigma style rotors."""
    rotors = {}
    for n in range(start, stop):
        nRoman = roman.toRoman(n)

        scrambled = random.sample(alphabet, len(alphabet))
        scrambled = "".join(scrambled)
        # print(scrambled, {len(scrambled)})

        notches = [i for i in alphabet if random.random() < notch_percentage]
        # print(notches, {len(notches)})

        rotor = [nRoman, scrambled, notches]
        # print(rotor)
        rotors[nRoman] = rotor

        return rotors


def generate_reflector(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    alphabet = list(alphabet)
    nums = list(range(len(alphabet)))
    while len(nums) != 0:
        n = random.randrange(len(nums))
        m = random.randrange(len(nums))
        while n == m:
            # Make sure n != m
            n = random.randrange(len(nums))
            m = random.randrange(len(nums))
        # Swap elements
        alphabet[n], alphabet[m] = alphabet[m], alphabet[n]
        # Remove elements which are swapped
        _ = nums.pop(n)
        _ = nums.pop(m)
    return alphabet


def generate_atbash_reflector(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    # alphabet = list(alphabet)
    # for n in range(len(alphabet)//2):
    #     alphabet[n], alphabet[len(alphabet) - n - 1] \
    #     = alphabet[len(alphabet) - n - 1], alphabet[n]
    # alphabet = "".join(alphabet)
    # return alphabet
    return "".join(alphabet[::-1])

print(generate_atbash_reflector(alphabet=alphabet))
