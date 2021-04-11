# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 19:12:29 2021

@author: jmg
"""
import random
import sys

import roman

hardwarefile = "hardware1.py"

alphabet = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[^]_`abcdefghijklmnopqrstuvwxyz{}§ ~ÁÉÍÏÐÓÞÆÄØÖÅáéíïðóþæäøöåΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюяᚠᚢᚦᚨᚬᚱᚲᚴᚷᚹᚺᚼᚾᛁᛃᛅᛇᛈᛉᛊᛋᛏᛒᛖᛗᛘᛚᛜᛞᛟᛦᛮᛯᛰ"
# ß
print({len(alphabet)}, alphabet)
if len(alphabet) % 2 != 0:
    print(f"Error: alphabet has to have an even length,\
          {len(alphabet)} is not ok.")
    sys.exit()
string_alphabet = alphabet[:]
alphabet = list(alphabet)


def genereate_rotors(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                     start=1,
                     stop=4,
                     notch_percentage=0.316227766):
    """Return dict of valid Enigma style rotors."""
    rotors = {}
    # Rotor {RomanNumeral:
    #           ["NameRoman", "Scrambled alphabet", ["List", "of", "notches"]}
    for n in range(start, stop):
        nRoman = roman.toRoman(n)
        scrambled = random.sample(alphabet, len(alphabet))
        scrambled = "".join(scrambled)
        print({len(scrambled)})
        notches = [i for i in alphabet if random.random() < notch_percentage]
        rotors[nRoman] = [nRoman, scrambled, notches]
    return rotors


def generate_reflector(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    # TODO: Make this work
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
    atbash = {}
    scrambled = "".join(alphabet[::-1])
    print({len(scrambled)})
    atbash["B"] = ["B", scrambled]
    return atbash


def choose_letters():
    a0 = "!\"#$%&'()*+,-./0123456789:;<=>?"
    # Not including "\", as is creates problems.
    a3 = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_"
    a5 = "`abcdefghijklmnopqrstuvwxyz{|}~"

    a7 = "\u00c1\u00c9\u00cd\u00cf\u00d0\u00d3\u00deÆÄØÖÅ\u00e1\u00e9\u00ed\u00ef\u00f0\u00f3\u00feæäøöå"
    a8 = "\u00df"

    a9 = "\u0391\u0392\u0393\u0394\u0395\u0396\u0397\u0398\u0399\u039a\u039b\u039c\u039d\u039e\u039f\u03a0\u03a1\u03a3\u03a4\u03a5\u03a6\u03a7\u03a8\u03a9"
    a10 = "\u03b1\u03b2\u03b3\u03b4\u03b5\u03b6\u03b7\u03b8\u03b9\u03ba\u03bb\u03bc\u03bd\u03be\u03bf\u03c0\u03c1\u03c3\u03c4\u03c5\u03c6\u03c7\u03c8\u03c9"

    a11 = "\u0410\u0411\u0412\u0413\u0414\u0415\u0401\u0416\u0417\u0418\u0419\u041a\u041b\u041c\u041d\u041e\u041f\u0420\u0421\u0422\u0423\u0424\u0425\u0426\u0427\u0428\u0429\u042a\u042b\u042c\u042d\u042e\u042f"
    a13 = "\u0430\u0431\u0432\u0433\u0434\u0435\u0451\u0436\u0437\u0438\u0439\u043a\u043b\u043c\u043d\u043e\u043f\u0440\u0441\u0442\u0443\u0444\u0445\u0446\u0447\u0448\u0449\u044a\u044b\u044c\u044d\u044e\u044f"

    a14 = "\u16a0\u16a2\u16a6\u16a8\u16ac\u16b1\u16b2\u16b4\u16b7\u16b9\u16ba\u16bc\u16be\u16c1\u16c3\u16c5\u16c7\u16c8\u16c9\u16ca\u16cb\u16cf\u16d2\u16d6\u16d7\u16d8\u16da\u16dc\u16de\u16df\u16e6\u16ee\u16ef\u16f0"

    asciiChars = a0 + a3 + a5
    nordic = a7 + a8
    greek = a9 + a10
    russian = a11 + a13
    runes = a14
    return asciiChars + nordic + greek + russian + runes

# alphabet = choose_letters()


# print(generate_atbash_reflector(alphabet=alphabet))
# print(genereate_rotors(alphabet=alphabet, start=40, stop=45))
# print({len(alphabet)})

with open(hardwarefile, "w", encoding="utf-8") as out:
    out.write("# -*- coding: utf-8 -*-\n\n")
    out.write("\n\n")
    out.write(f'alphabet = "{string_alphabet}"')
    out.write("\n\n")
    out.write("reflectors = "
              f"{generate_atbash_reflector(alphabet=alphabet)}")
    out.write("\n\n")
    out.write("rotors = ")
    out.write(f"{genereate_rotors(alphabet=alphabet, start=40, stop=45)}")
