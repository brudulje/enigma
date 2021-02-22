# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 16:27:47 2021

@author: jmg
"""

import datetime
import secrets

"""
Generate daykeys for the Enigma_M3.

Walzenlage are 3 rotors from a set of 8. They are named by the
roman numbers I - VIII. All 3 must be different, as each Enigma
machine had only one copy of each rotor.

Ringstellung are 3 numbers, all between 1 and 26, inclusive.
The ringstellung of two rotors may be the same.

Steckerverbindungen are 10 pairs of letters from the 26 letter
alphabet. No letter may be present more than once.

The kenngruppen are three-letter groups. These are used to figure
out which key applies to a message. There are 26**3 = 17576 different
kenngruppen. With 4 kenngruppen each day, this is sufficient for 12 years
before a kenngruppen must be used again. Thus, in this key generator, the
kenngruppen are not reused.

Keys are generated for one month at a time. It is assumed that keys are
generated for the month following the current month.
"""


def main():

    today = datetime.date.today()
    nextMonth = datetime.date(today.year, today.month + 1, today.day)
    month = str(nextMonth.strftime("%Y-%m"))
    outfile = "enigmaSchlussel" + month + ".txt"

    with open(outfile, "w") as out:

        # Write header
        out.write("GEHEIM!")
        out.write(f"{'brudulje enigmaSchlussel' : >48}")
        monthString = nextMonth.strftime("%B %Y")
        out.write(f"{monthString : >30} \n\n")
        out.write(86 * "-" + "\n")
        out.write("|Tag |   Walzenlage   |Ringstellung|      "
                  + "Steckerverbindungen      |   Kenngruppen   |\n")
        out.write(86 * "-" + "\n")

        # Get, format and write daykey for each day
        # For simplicity, each month will have 31 daykeys.
        for day in range(31, 0, -1):
            walzen = getWalzen(3)
            rings = getRings(3)
            stecker = getStecker(10)
            kenngruppen = getKenngruppen(4)

            out.write(f"| {day:02d} | ")
            for walz in walzen:
                out.write(f"{walz:5}")
            out.write("|  ")
            for ring in rings:
                out.write(f"{ring:02} ")
            out.write(" | " + stecker + " | ")
            for kenn in kenngruppen:
                out.write(f"{kenn:4}")
            out.write("|  \n")
        out.write(87 * "-" + "\n")


def getWalzen(walzezahl=3):
    walzen = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
    walz = []
    for w in range(walzezahl):
        wa = secrets.choice(walzen)  # Pick one at random
        walz.append(wa)  # Add it to the list
        walzen.pop(walzen.index(wa))  # Remove it from the pool
    return walz


def getRings(ringzahl=3):
    rings = range(1, 26 + 1)
    ring = []
    for r in range(ringzahl):
        # Pick one at random, leave it in the list
        ring.append(secrets.choice(rings))
    return ring


def getStecker(verbindungen=10):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = ""
    for n in range(2 * verbindungen):
        letter = secrets.choice(letters)  # Pick one at random
        letters = letters.replace(letter, "")  # Remove it from the pool
        s += letter
    steck = " ".join(s[i: i + 2] for i in range(0, len(s), 2))
    return steck


def getKenngruppen(gruppen=4):
    """
    This one is slightly more complicated. We want to keep track of the
    kenngruppen we have already used, and not use them again for as long
    as possible.

    """
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    usedfile = "usedKen.txt"
    used = []
    kenngruppen = []

    # Generate all possible kenngruppen
    possibleKen = [a + b + c
                   for a in letters
                   for b in letters
                   for c in letters]

    # Read the ones we have already used from file
    with open(usedfile, "r") as infile:
        used = infile.read().split()

    # TODO : Try to speed up the removal of the used kenngruppen.
    # Remove the used ones from the possible ones.
    # for ken in used:
    #     possibleKen.pop(possibleKen.index(ken))
    possibleKen = [k for k in possibleKen if k not in used]

    # possibleSet = set(possibleKen)
    # # usedSet = set(used)
    # possibleSet = possibleSet.difference(used)

    # Pick the kenngruppen.
    for n in range(gruppen):
        # ken = secrets.choice(possibleSet)
        ken = secrets.choice(possibleKen)
        kenngruppen.append(ken)
        # possibleSet.remove(ken)
        possibleKen.pop(possibleKen.index(ken))

    # Add the newly picked kenngruppen to the used ones.
    with open(usedfile, "a") as out:
        for ken in kenngruppen:
            out.write(" " + ken)
    return kenngruppen


if __name__ == "__main__":
    main()