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
        out.write(f"{monthString : >31} \n\n")
        out.write(87 * "-" + "\n")
        out.write("|Tag |   Walzenlage   |Ringstellung|      "
                  + "Steckerverbindungen       |   Kenngruppen   |\n")
        out.write(87 * "-" + "\n")

        # Get, format and write daykey for each day
        # For simplicity, each month will have 31 daykeys.
        for day in range(31, 0, -1):
            walzen = getWalzen()
            rings = getRings()
            stecker = getStecker()
            kenngruppen = getKenngruppen()

            out.write(f"| {day:02d} | ")
            for walz in walzen:
                out.write(f"{walz:5}")
            out.write("|  ")
            for ring in rings:
                out.write(f"{ring:02} ")
            out.write(" | " + stecker + "  | ")
            for kenn in kenngruppen:
                out.write(f"{kenn:4}")
            out.write("|  \n")
        out.write(87 * "-" + "\n")


def getWalzen():
    walzen = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
    # print(walzen)
    w1 = secrets.choice(walzen)  # Pick one at random
    walzen.pop(walzen.index(w1))  # Remove it from the pool
    # print(walzen)
    w2 = secrets.choice(walzen)
    walzen.pop(walzen.index(w2))
    # print(walzen)
    w3 = secrets.choice(walzen)
    walzen.pop(walzen.index(w3))
    # print(walzen)
    return w1, w2, w3


def getRings():
    rings = range(1, 26 + 1)
    r1 = secrets.choice(rings)
    r2 = secrets.choice(rings)
    r3 = secrets.choice(rings)
    return r1, r2, r3


def getStecker():
    # TODO: Make proper function.
    return "AB CD EF GH IJ KL MN OP QR ST"


def getKenngruppen():
    # TODO: Make proper function.
    return "ABC", "DEF", "GHI", "JKL"


if __name__ == "__main__":
    main()
