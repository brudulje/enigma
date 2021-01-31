# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 21:38:41 2020

@author: jsg
"""

"""Emulates the Enigma I/M3"""

# "Norwegian enigma", brukt av Overvåkningspolitiet med modifiserte valser:
# I	    WTOKASUYVRBXJHQCPZEFMDINLG	Q
# II	GJLPUBSWEMCTQVHXAOFZDRKYNI	E
# III	JWFMHNBPUSDYTIXVZGRQLAOEKC	V
# IV	ESOVPZJAYQUIRHXLNFTGKDCMWB	J
# V 	HEJXQOTZBVFDASCILWPGYNMURK	Z
# UKW	MOWJYPUXNDSRAIBFVLKZGQCHET

# ### Info

# Hard wiring of the rotors

# Eintrittwaltze does not affect cryptation in military models.
# rotor0 is also being used as a shorthand for the plain alphabet.
rotor0 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".replace("", " ").rsplit()

# rotor = ["name", "cipher alpha", [notches]]
rotorI =    ["I",   "EKMFLGDQVZNTOWYHXUSPAIBRCJ", ["Q"]]  # Q = 17
rotorII =   ["II",  "AJDKSIRUXBLHWTMCQGZNPYFVOE", ["E"]]  # E = 05
rotorIII =  ["III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", ["V"]]  # V = 22
rotorIV =   ["IV",  "ESOVPZJAYQUIRHXLNFTGKDCMWB", ["J"]]  # J = 10
rotorV =    ["V",   "VZBRGITYUPSDNHLXAWMJQOFECK", ["Z"]]  # Z = 26
# Rotors VI - VIII only on Enigma M3, not on the Enigma I.
rotorVI   = ["VI",  "JPGVOUMFYQBENHZRDKASXLICTW", ["Z", "M"]]  # Z=26, M=13
rotorVII  = ["VII", "NZJHGRCXMYSWBOUFAIVLPEKQDT", ["Z", "M"]]  # Z=26, M=13
rotorVIII = ["VIII","FKQHTLXOCBJSPDZRAMEWNIUYGV", ["Z", "M"]]  # Z=26, M=13

# Reflector A only on Enigma I, not on the M3.
reflA = ["A", "EJMZALYXVBWFCRQUONTSPIKHGD"]
reflB = ["B", "YRUHQSLDPXNGOKMIEBFZCWVJAT"]  # Standard on Enigma I.
reflC = ["C", "FVPJIAOYEDRZXWGCTKUQSBNMHL"]

# key = [[rotors], [reflector], [startpos],  [ringpos], [plugboard]]
key = [[rotorI, rotorII, rotorV],  # Rotors, left to right
       [reflB],  # Reflector
       ["X", "W", "B"],  # Starting positions
       [6, 22, 14],  # Ring settings
       ["PO.ML.IU.KJ.NH.YT.GB.VF.RE.DC"]]  # Plugboard
plain = "Jau det va no som svarte"

# plain = "Jau det va no som svarte"
# plain = "WFQYV VORIE DQPHY WVVY"

# https://cryptii.com/pipes/enigma-machine
# wfqyv vorie dqphy wvvy

# https://www.101computing.net/enigma-machine-emulator/
# Shows intermediate steps
# WFQYV VORIE DQPHY WVVY
verbose = True

def main():
    """Execute program."""
    # Setting up the hardware
    lft = Rotor(key[0][0], key[2][0], key[3][0])
    mid = Rotor(key[0][1], key[2][1], key[3][1])
    rgt = Rotor(key[0][2], key[2][2], key[3][2])
    ref = Reflector(key[1][0])
    plg = Plugboard(key[4])

    cipher = ""
    # Cleaning plaintext
    print(plain)
    plaintext = clean_plain(plain)
    print(plaintext)

    # Print starting position and settings.
    print_rotors(lft, mid, rgt, end="   ")
    print_pos(lft, mid, rgt, end="   ")
    print_rings(lft, mid, rgt, end="   ")
    print(str(plg))

    _ = lft.get_position()
    posM = mid.get_position()
    posR = rgt.get_position()

    # Turn rotors appropriately
    for ch in plaintext:
        posR = rgt.turn()
        if posM + 1 in mid.get_notch():
            posM = mid.turn()
            _ = lft.turn()
        if posR in rgt.get_notch():
            posM = mid.turn()

        # Print rotor positions
        if verbose:
            print_pos(lft, mid, rgt, end="   ")

        # Encipher text
        if verbose:
            print(f"{ch}  ", end="")
        ch = plg.vor(ch)
        if verbose:
            print(f"-> {ch} ", end="")
        ch = rgt.vor(ch)
        if verbose:
            print(f"-> {ch} ", end="")
        ch = mid.vor(ch)
        if verbose:
            print(f"-> {ch} ", end="")
        ch = lft.vor(ch)
        if verbose:
            print(f"-> {ch} ", end="")
        ch = ref.vor(ch)
        if verbose:
            print(f"-> {ch} ", end="")
        ch = lft.ruck(ch)
        if verbose:
            print(f"-> {ch} ", end="")
        ch = mid.ruck(ch)
        if verbose:
            print(f"-> {ch} ", end="")
        ch = rgt.ruck(ch)
        if verbose:
            print(f"-> {ch} ", end="")
        ch = plg.ruck(ch)
        if verbose:
            print(f"->  {ch}.")

        cipher += ch
    cipher = format_cipher_text(cipher)
    print(cipher)

def clean_plain(s):
    """Clean plain text and prepare it for enciphering."""
    s = s.replace("", " ").rsplit()
    for i, letter in enumerate(s):
        # print(i, s[i])
        if letter.upper() in rotor0:
            # Lower case letter
            s[i] = letter.upper()
        elif letter in rotor0:
            # Upper case letter
            pass
        elif letter == ".":
            s[i] = "X"
        elif letter == ",":
            _ = s.pop(i)
            s.insert(i, "ZZ")
        elif letter == "?":
            _ = s.pop(i)
            s.insert(i, "FRAGE")
        elif letter == "1":
            _ = s.pop(i)
            s.insert(i, "EINS")
        elif letter == "2":
            _ = s.pop(i)
            s.insert(i, "ZWO")
        elif letter == "3":
            _ = s.pop(i)
            s.insert(i, "DREI")
        elif letter == "4":
            _ = s.pop(i)
            s.insert(i, "VIER")
        elif letter == "5":
            _ = s.pop(i)
            s.insert(i, "FUNF")
        elif letter == "6":
            _ = s.pop(i)
            s.insert(i, "SEQS")
        elif letter == "7":
            _ = s.pop(i)
            s.insert(i, "SIEBEN")
        elif letter == "8":
            _ = s.pop(i)
            s.insert(i, "AQT")  # TODO: Operator should do this, not machine.
        elif letter == "9":
            _ = s.pop(i)
            s.insert(i, "NEUN")  # TODO Figure this out
        # print(i, len(s))
        # elif letter == "0" and i+3 < len(s):
        # elif letter == "0" and s[i+1] == "0" and s[i+2] == "0" and s[i+3] == "0":
        #     _ = s.pop(i)
        #     _ = s.pop(i)
        #     _ = s.pop(i)
        #     _ = s.pop(i)
        #     s.insert(i-1, "MYRIAD")
        # # elif letter == "0" and i+2 < len(s):
        # elif letter == "0" and s[i+1] == "0" and s[i+2] == "0":
        #     _ = s.pop(i)
        #     _ = s.pop(i)
        #     _ = s.pop(i)
        #     s.insert(i-1, "MILLE")
        # # elif letter == "0" and i+1 < len(s):
        # elif letter == "0" and s[i+1] == "0":
        #     _ = s.pop(i)
        #     _ = s.pop(i)
        #     s.insert(i-1, "CENTA")
        elif letter == "0":
            _ = s.pop(i)
            s.insert(i, "NULL")
        else:
            # Discard all else
            print(f"Character not allowed. Discarded character: {s[i]}")
            # TODO: Replace some chars
# KLAM = Parenthesis
# ZZ = Comma
# X = Full stop (end of sentence)
# YY = Point or dot
# X****X = Inverted commas

# Question mark (Fragezeichen in German) was usually abbreviated to FRAGE, FRAGEZ or FRAQ. Foreign names, places, etc. are delimited twice by "X", as in XPARISXPARISX or XFEUERSTEINX. The letters CH were written as Q. ACHT became AQT, RICHTUNG became RIQTUNG.

# Numbers were written out as NULL EINZ ZWO DREI VIER FUNF SEQS SIEBEN AQT NEUN

# It was prohibited to encipher the word "NULL" several times in succession, so they used CENTA (00), MILLE (000) and MYRIA (0000). Some examples: 200 = ZWO CENTA, 00780 = CENTA SIEBEN AQT NULL.
            s[i] = ""
    s = "".join(s)
    return s

def format_cipher_text(s):
    """Format the cipher text in groups of five for transmission."""
    # Adds a space every five characters.
    return " ".join(s[i:i+5] for i in range(0, len(s), 5))

def print_rotors(lef, mid, rgt, end="\n"):
    """Print names of active rotors."""
    print(lef.get_name() + " " \
          + mid.get_name() + " " \
          + rgt.get_name(), end=end)

def print_pos(lef, mid, rgt, end="\n"):
    """Print current positions of the rotors."""
    print(chr(lef.get_position() + 65) + " " \
          + chr(mid.get_position() + 65) + " " \
          + chr(rgt.get_position() + 65), end=end)

def print_rings(lef, mid, rgt, end="\n"):
    """Print ring positions on the rotors."""
    print(str(lef.ring) + " " + str(mid.ring) + " " + str(rgt.ring), end=end)


class Disk():
    """A parent class for the rotors and reflectors."""

    def __init__(self, name, wires):
        self._name = name
        self._wires = wires
        self._alpha_plain = rotor0[:]
        self._alpha_vor = self._wires.replace("", " ").rsplit()
        self._alpha_ruck = rotor0[:]
        self.set_ruck()

    def __str__(self):
        """Return string representation of Disk object."""
        return f"Disk, wires {self._wires}."

    def get_name(self):
        """Return the name of this Disk."""
        return self._name

    def vor(self, ch):
        """Substitute letter, according to disk wiring.

        This function substitutes while the signal moves "forward" thru
        the disk, i.e. towards the reflector.
        """
        i = self._alpha_plain.index(ch)
        ch = self._alpha_vor[i]
        return ch

    def set_ruck(self):
        """Build the backward substitution alphabet."""
        for i, l in enumerate(self._alpha_plain):
            self._alpha_ruck[i] = self._alpha_plain[self._alpha_vor.index(l)]


class Rotor(Disk):
    """The rotors in the core of the machine."""

    def __init__(self, hardware, start, ring):
        super(Rotor, self).__init__(hardware[0], hardware[1])
        self._notch = []
        for i, letter in enumerate(hardware[2]):
            # self._notch.append((ord(letter) - 64) % 26)
            self._notch.append(self._alpha_vor.index(letter))
        # print(self._notch)
        self._position = 0
        self.ring = ring
        self._set_ring(ring)
        # self._set_start(ord(start) - 64)
        # print(start)
        # print(ord(start) - 64)
        self._set_start(self._alpha_plain.index(str(start))+1)
        # print(self._alpha_plain.index(str(start)) + 1)

    def _set_start(self, startpos):
        """Set the start position for this rotor."""
        self._startpos = startpos - 1
        self.turn(self._startpos)

    def _set_ring(self, ring):
        """Set ring position for this rotor."""
        self.turn(- ring + 1)

    def get_notch(self):
        """Return Rotor's notch position."""
        return self._notch

    def get_position(self):
        """Return Rotor's position."""
        return (self._position + self.ring - 1) % len(self._alpha_plain)  # 26

    def turn(self, n=1):
        """Turn the rotor the appropriate number of steps."""
        self._alpha_vor = self._alpha_vor[n:] + self._alpha_vor[:n]
        self.set_ruck()
        self._position = (self._position + n) % len(self._alpha_plain)  # 26
        return self.get_position()

    def vor(self, ch):
        """Substitute letter, according to disk setting.

        This function substitutes while the signal moves "forward" thru
        the disk, i.e. towards the reflector.

        This adds to Disk.vor by taking the position of the rotor
        into account.
        """
        ch = Disk.vor(self, ch)
        # i = ord(ch) - self._position
        # if i < 65:
        #     i += 26
        # if i > 90:
        #     i -= 26
        # ch = chr(i)
        i = self._alpha_plain.index(ch) - self._position
        ch = self._alpha_plain[i]
        return ch

    def ruck(self, ch):
        """Substitute letter, according to disk setting.

        This function substitutes while the signal moves "back" thru
        the disk, i.e. from the reflector.
        """
        i = (self._alpha_plain.index(ch) + self._position) \
            % len(self._alpha_plain)  # 26
        ch = self._alpha_ruck[i]
        return ch


class Reflector(Disk):
    """The reflector at the left of the machine."""

    def __init__(self, hardware):
        super(Reflector, self).__init__(hardware[0], hardware[1])
        self._sanity_check()

    def _sanity_check(self):
        if self._alpha_vor != self._alpha_ruck:
            raise ValueError("Reflector wires not correct. "\
                             + "Should be symmetric. "\
                             + f"\n{self._alpha_vor}\n{self._alpha_ruck}")


class Plugboard():
    """The plugboard just after the keyboard and just before the lamps."""

    def __init__(self, connections):
        self._alpha_plain = rotor0[:]
        self._alpha_vor = rotor0[:]
        self._sanity_check(connections)
        self.connections = connections[0].replace(".", " ").rsplit()

        # Build the _alpha_vor
        while len(self.connections) > 0:  # Until the list is empty
            r = self.connections.pop()  # Pop out a tuple to swap
            j, k = self._alpha_vor.index(r[0]), self._alpha_vor.index(r[1])
            self._alpha_vor[j], self._alpha_vor[k] = \
                self._alpha_vor[k], self._alpha_vor[j]  # swap
        # Fill self.connections again, so its not empty when __str__ gets it.
        self.connections = connections[0].replace(".", " ").rsplit()

    def _sanity_check(self, connections):
        """Check plugboard input for sanity."""
        self._alpha_sane = self._alpha_vor[:]
        if len(connections[0].replace(".", "")) % 2 != 0:
            # Odd number of letters not allowed in plugboard settings.
            raise ValueError(f"Invalid plugboard settings: {connections}.")
        for ch in connections[0]:
            try:  # TODO: check the ord
                # if ord("A") <= ord(ch) and ord(ch) <= ord("Z"):
                if ch in self._alpha_plain:
                    self._alpha_sane.pop(self._alpha_sane.index(ch))
            except ValueError:
                # Some letter occurs twice.
                raise ValueError(f"Invalid plugboard settings: {connections}.")

    def __str__(self):
        """Return string representation of plugboard settings."""
        text = ""
        for i, s in enumerate(self.connections):
            text += s + "."
        return text[:-1]

    def vor(self, ch):
        """Substitute letter, according to plugboard setting."""
        i = self._alpha_plain.index(ch)
        ch = self._alpha_vor[i]
        return ch

    def ruck(self, ch):
        """Substitute letter, according to plugboard setting."""
        # Plugboard is symmetric.
        return self.vor(ch)


if __name__ == "__main__":
    main()
