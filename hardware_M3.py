# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 19:14:39 2021

@author: jmg
"""

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

rotors = {
    # rotor = ["name", "cipher alpha", [notches]]
    "I": ["I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", ["Q"]],  # Q = 17
    "II": ["II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", ["E"]],  # E = 05
    "III": ["III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", ["V"]],  # V = 22
    "IV": ["IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", ["J"]],  # J = 10
    "V": ["V", "VZBRGITYUPSDNHLXAWMJQOFECK", ["Z"]],  # Z = 26
    # Rotors VI - VIII only on Enigma M3, not on the Enigma I.
    "VI": ["VI", "JPGVOUMFYQBENHZRDKASXLICTW", ["Z", "M"]],  # Z=26, M=13
    "VII": ["VII", "NZJHGRCXMYSWBOUFAIVLPEKQDT", ["Z", "M"]],
    "VIII": ["VIII", "FKQHTLXOCBJSPDZRAMEWNIUYGV", ["Z", "M"]],
}

reflectors = {
    "A": ["A", "EJMZALYXVBWFCRQUONTSPIKHGD"],\
    # reflB is standard on Enigma I.
    "B": ["B", "YRUHQSLDPXNGOKMIEBFZCWVJAT"],\
    "C": ["C", "FVPJIAOYEDRZXWGCTKUQSBNMHL"],\
}
