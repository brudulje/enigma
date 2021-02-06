# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 21:38:41 2020

@author: jsg
"""
import secrets
import re
import datetime

### 2020-05-01: Rewriting with enig_op and enigma_M3 as objects, not functions.

# Hard wiring of the rotors

# Eintrittwaltze does not affect cryptation in military models.
# rotor0 is also being used as a shorthand for the plain alphabet.
rotor0 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".replace("", " ").split()
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
# reflA = ["A", "EJMZALYXVBWFCRQUONTSPIKHGD"]
reflB = ["B", "YRUHQSLDPXNGOKMIEBFZCWVJAT"]  # Standard on Enigma I.
reflC = ["C", "FVPJIAOYEDRZXWGCTKUQSBNMHL"]


def main():
    """Execute enigma program."""
    to = "F"  # May not match regexp [A-Z]{5}
    sender = "Q"  # May not match regexp [A-Z]{5}
#    message = "F Q 2128 = 30 = FTK SAZ\nSQYNB ADEGL JLWLT VSTPM BXYTN IBHOT"
#    message = "F Q 1944 = 30 = FPQ IBD\nMZQRE FMKSW BBMEW GIPUN XQOFC ZYLYR"
    message = "Nå begynner vi å nærme oss. Men først må vi teste om vi kan \
    sende en kjempelang melding, en som ikke får plass i en SMS, så den må \
    deles opp i flere deler, så den ikke bryter med de kryptografiske \
    reglene for enigma. Hvis vi skal få sjekket skikkelig må vi skrive enda \
    litt til, kanskje helt ut hit."
#    message = "F Q 2143 = 14 = FGH ZAS\nDQLOP NWSSD LFBB"
    message = "F Q 1230  = 250 = WZA UHL FDJKM LDAHH YEOEF PTWYB LENDP MKOXL \
        DFAMU DWIJD XRJZY DFRIO MFTEV KTGUY DDZED TPOQX FDRIU CCBFM MQWYE \
        FIPUL WSXHG YHJZE AOFDU FUTEC VVBDP OLZLG DEJTI HGYER DCXCV BHSEE \
        TTKJK XAAQU GTTUO FCXZH IDREF TGHSZ DERFG EDZZS ERDET RFGTT RREOM \
        MJMED EDDER FTGRE UUHKD DLEFG FGREZ ZZSEU YYRGD EDFED HJUIK FXNVB"

    enig_op(message, recipient=to, sender=sender, encipher=True, month=None)

def enig_op(message, recipient=None, sender=None, encipher=True, month=None):
    """Emulates the operator of the Enigma M3.

    Args:
        message (str):
            Message to be enciphered or deciphered.
        recipient (str, optional):
            The intended recipient's code name. Defaults to None.
        sender (str, optional):
            The sender's code name. Defaults to None.
        encipher (bool, optional):
            Enciphers if True, deciphers if False. Defaults to False.
        month (string yyyy-mm, optional):
            Month in which to look for key, this month assumed if None.
            Defaults to None.

    Return: Returns nothing, but prints the result to terminal.
    """
    verbose = False  # For debugging
    if encipher:  # Encipher message
        time = str(datetime.datetime.now().time().strftime("%H%M"))
        date = str(datetime.date.today())
        print(date)
        daykey, _ = get_daykey(date)
        print(daykey)
        key_dayofmonth, key_rotors, key_rings, \
            key_connections, key_kenngruppen = divide_key(daykey)

        # Clean plain
        print(message)
        plaintext = clean_plain(message)
        maxlength = 245
        parts = [plaintext[i: i + maxlength] \
                 for i in range(0, len(plaintext), maxlength)]

        for n in range(len(parts)):
            # choose random message start pos (3 letters)
            msg_start = ''.join(secrets.choice(rotor0) for i in range(3))
            msg_start_list = msg_start.replace("", " ").split()

            # choose random message key (3 letters)
            msg_key = ''.join(secrets.choice(rotor0) for i in range(3))
            msg_key_list = msg_key.replace("", " ").split()

            # encipher message key using message start pos
            key = [key_rotors,
                   [reflB],
                   msg_start_list,
                   key_rings,
                   key_connections]
            enc_msg_key = enigma_M3(key, msg_key)

            # make buchstabenkenngruppen
            letterIDgroup = ''.join(secrets.choice(rotor0) for i in range(2)) \
                            + secrets.choice(key_kenngruppen)

            # Encipher message
            key = [key_rotors,
                   [reflB],
                   msg_key_list,
                   key_rings,
                   key_connections]
            cipher = enigma_M3.encipher(key, parts[n], verbose=verbose)

            # Format output
            # start of message is
            # To: From: Clock: Lettercount: Start pos: Enciphered message key:
            # Fiveletter group containing two random letters
            # and the 3 letter kenngruppe
            lettercount = len(cipher) + len(letterIDgroup)
            precipher = str(recipient) + " " + str(sender) + " " + str(time)\
                + " = " + str(lettercount) + " = " \
                + msg_start + " " + enc_msg_key + "\n" + letterIDgroup + " "

            # # Enciphered message
            cipher = format_in_groups(cipher)
            ciphertext = precipher + cipher
            print(str(date), end="  ")
            print(printable_key(key))
            print(ciphertext)

    elif not encipher:  # Decipher
        # Find recipient
        recipient = re.findall("[A-Z]+ ", message)[0]

        # Find sender
        sender = re.findall("[A-Z]+ ", message)[1]

        # Find time
        time = re.search("[0-9]{4}", message)[0]
        time = time[:2] + ":" + time[-2:]

        # Find message start pos
        # Find enciphered message key
        tla = re.findall("(?=( [A-Z]{3}[\s]))", message)  # ThreeLetterAcronym
        msg_start = tla[0][1:-1]
        enc_msg_key = tla[1][1:-1]
        msg_start_list = msg_start.replace("", " ").split()

        # Find kenngruppen
        kenngruppen = re.search("[A-Z]{5} ", message)[0][2:-1]

        # Look up key in book
        daykey, date = get_daykey(kenngruppen, month=month)
        key_dayofmonth, key_rotors, key_rings, \
            key_connections, key_kenngruppen = divide_key(daykey)

        # Decipher message key
        key = [key_rotors, [reflB], msg_start_list, key_rings, key_connections]
        msg_key = enigma_M3(key, enc_msg_key)
        msg_key_list = msg_key.replace("", " ").split()

        # Get the actual message, i.e. after the 5 letter kenngruppen
        cipher = message.partition(kenngruppen)[-1].replace(" ", "")

        # Decipher message.
        print(message)
        key = [key_rotors, [reflB], msg_key_list, key_rings, key_connections]
        plain = enigma_M3(key, cipher).lower()
        print(str(date), end="  ")
        print(printable_key(key))
        preplain = "Til " + recipient + "fra " + sender \
            + str(date) + " " + time + "\n"
        print(preplain + plain)

def printable_key(key):
    """Return string to print the daykey nicely."""
    return key[0][0][0] + " " + key[0][1][0] + " " + key[0][2][0] + "  "\
         + key[2][0] + " "    + key[2][1] + " "    + key[2][2] + "  "\
     + str(key[3][0]) +" "+ str(key[3][1]) +" "+ str(key[3][2]) + "  "\
         + key[4]

def get_daykey(label, month=None):
    """Return the daykey for the given date or kenngruppen.

    Args:
       label (str):
           One of 3 formats;
           Two digits: dd; day of month, assuming this month.
           Four-two-two digits: yyyy-mm-dd; explicit date.
           3 letters: kenngruppen.
       month (str, optional):
           yyyy-mm: explicit month to use to look for key

    Return:
        (str) daykey matching label
            "| 31 | I II V | 06 22 14 | PO ML IU KJ NH YT GB VF RE DC | EXS TGY IKJ LOP |"
        (str) date on which given key is valid
    """
    # Check label format
    if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", label):
        # Label is a date
        day = datetime.datetime.strptime(label, "%Y-%m-%d").date()
        return get_key_from_date(day), str(day)
    elif re.match("[0-9]{2}", label):
        # Label is a day of month, assuming this month
        if month is None:
            today = datetime.date.today()
            day = datetime.date(today.year, today.month, int(label))
        else:
            day = datetime.date(month[:4], month[-2:], label)
        return get_key_from_date(day), str(day)

    elif re.match("[A-Z]{3}", label):
        # Label is a kenngruppe, assuming from this month
        if month is None:
            day = datetime.date.today()
        else:
            day = datetime.date(month[:4], month[-2:], 1)
        keyfilename = "enigmaSchlussel" + str(day)[:7] + ".txt"
        with open(keyfilename, "r") as infile:
            for line in infile:
                if re.search(str(label), line):
                    # Correct the date to show the date on which
                    # the key was valid.
                    day = datetime.date(int(keyfilename[15:19]),\
                                        int(keyfilename[20:22]),\
                                        int(re.search("[0-9]{2}", line)[0]))
                    return line, str(day)
    else:
        # Program will crash here.
        print(f"Label format not recognised {label}.")

def get_key_from_date(date):
    """Return daykey of given day."""
    keyfilename = "enigmaSchlussel" + str(date)[:7] + ".txt"
    with open(keyfilename, "r") as infile:
        for line in infile:
            if re.search(str(date)[-2:], line[:6]):
                return line

def divide_key(daykey):
    """Split daykey for use in emigma."""
    rotors = {}
    for r in rotorI, rotorII, rotorIII, rotorIV,\
            rotorV, rotorVI, rotorVII, rotorVIII:
        rotors[r[0]] = r

    keyparts = daykey.split("|")

    key_dayofmonth = int(keyparts[1])

    key_rotors = keyparts[2].split()
    for k in range(len(key_rotors)):
        key_rotors[k] = rotors[key_rotors[k]]

    key_rings = keyparts[3].split()
    for k in range(len(key_rings)):
        key_rings[k] = int(key_rings[k])

    key_connections = keyparts[4]
#    print(key_connections)
    key_connections = key_connections.lstrip().rstrip()  # .replace(" ", ".")
#    print(key_connections)

    key_kenngruppen = keyparts[5].split()

    return key_dayofmonth,
    key_rotors,
    key_rings,
    key_connections,
    key_kenngruppen

def clean_plain(s):
    """Clean plain text and prepare it for enciphering."""
# KLAM = Parenthesis
# ZZ = Comma
# X = Full stop (end of sentence)
# YY = Point or dot
# X****X = Inverted commas

# Question mark (Fragezeichen in German) was usually abbreviated to
# FRAGE, FRAGEZ or FRAQ.
# Foreign names, places, etc. are delimited twice by "X", as in
# XPARISXPARISX or XFEUERSTEINX.
# The letters CH were written as Q. ACHT became AQT, RICHTUNG became RIQTUNG.

# Numbers were written out as NULL EINZ ZWO DREI VIER FUNF SEQS SIEBEN AQT NEUN
# It was prohibited to encipher the word "NULL" several times in succession,
# so they used CENTA (00), MILLE (000) and MYRIA (0000).
# Some examples: 200 = ZWO CENTA, 00780 = CENTA SIEBEN AQT NULL.

    s = s.replace("", " ").split()
    for i, letter in enumerate(s):
        # print(i, s[i])
        if letter.upper() in rotor0 or letter in rotor0:
            # Lower case letter or upper case letter
            s[i] = letter.upper()
        elif letter == ".":
            s[i] = "X"
        elif letter == ",":
            _ = s.pop(i)
            s.insert(i, "ZZ")
        elif letter == "?":
            _ = s.pop(i)
            s.insert(i, "FRAGE")
        elif letter == "(" or letter == ")":
            _ = s.pop(i)
            s.insert(i, "KLAM")
        elif letter == "Ä" or letter == "ä":
            _ = s.pop(i)
            s.insert(i, "AE")
        elif letter == "Ü" or letter == "ü":
            _ = s.pop(i)
            s.insert(i, "UE")
        elif letter == "Ö" or letter == "ö":
            _ = s.pop(i)
            s.insert(i, "OE")
        elif letter == "Æ" or letter == "æ":  # Støtte for norsk
            _ = s.pop(i)
            s.insert(i, "AE")
        elif letter == "Ø" or letter == "ø":  # Støtte for norsk
            _ = s.pop(i)
            s.insert(i, "OE")
        elif letter == "Å" or letter == "å":  # Støtte for norsk
            _ = s.pop(i)
            s.insert(i, "AA")
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
            s.insert(i, "SECHS")
        elif letter == "7":
            _ = s.pop(i)
            s.insert(i, "SIEBEN")
        elif letter == "8":
            _ = s.pop(i)
            s.insert(i, "ACHT")
        elif letter == "9":
            _ = s.pop(i)
            s.insert(i, "NEUN")
        elif letter == "0":  # Not convinced this is the most elegant.
            if i + 1 < len(s):
                if s[i + 1] != "0":
                    _ = s.pop(i)
                    s.insert(i, "NULL")
                elif i + 2 < len(s) and s[i + 1] == "0":
                    if s[i + 2] != "0":
                        _ = s.pop(i)
                        _ = s.pop(i)
                        s.insert(i, "CENTA")
                    elif i + 3 < len(s) and s[i + 2] == "0":
                        if s[i + 3] != "0":
                            _ = s.pop(i)
                            _ = s.pop(i)
                            _ = s.pop(i)
                            s.insert(i, "MILLE")
                        elif s[i + 3] == "0":
                            _ = s.pop(i)
                            _ = s.pop(i)
                            _ = s.pop(i)
                            _ = s.pop(i)
                            s.insert(i, "MYRIAD")
                    else:
                        _ = s.pop(i)
                        _ = s.pop(i)
                        _ = s.pop(i)
                        s.insert(i, "MILLE")
                else:
                    _ = s.pop(i)
                    _ = s.pop(i)
                    s.insert(i, "CENTA")
            else:
                _ = s.pop(i)
                s.insert(i, "NULL")
        else:
            # Discard all else
            print(f"Character not allowed. Discarded character: {s[i]}")
            s[i] = ""

    return "".join(s)

def format_in_groups(s, group=5):
    """Format the cipher text in groups for transmission."""
    # Adds a space every five characters or so.
    return " ".join(s[i: i + group] for i in range(0, len(s), group))

class enigma_M3():
    """Emulates the Enigma M3 machine.

    Args:
        key (list):
            key = [[rotorI, rotorII, rotorV],  # Rotors, left to right
            # TODO change to ["I", "II", "V"] format
            [reflB],  # Reflector
            ["J", "S", "G"],  # Starting positions
            [7, 14, 21],  # Ring settings
            "AB CD EF GH IJ KL MN OP QR ST"]  # Plugboard

        text (str):
            Plain text to be enciphered or ciphertext to be solved.
        verbose (bool, optional):
            Gives details on single letter substitutions. Defaults to False.
        silent (bool, optional):
            Suppresses printing the key if True. Defaults to False.

    Return:
        cipher (str):
            The enciphered message.
    """
    # TODO: Implement list of rotors as class attributes
    # TODO: Reshape key and refer to rotors by string of roman number.
    __rotors = [
        # 0 : "ABCDEFGHIJKLMNOPQRSTUVWXYZ".replace("", " ").split(),
        # rotor = ["name", "cipher alpha", [notches]]
        ["0",   "ABCDEFGHIJKLMNOPQRSTUVWXYZ", [""]],
        ["I",   "EKMFLGDQVZNTOWYHXUSPAIBRCJ", ["Q"]],  # Q = 17
        ["II",  "AJDKSIRUXBLHWTMCQGZNPYFVOE", ["E"]],  # E = 05
        ["III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", ["V"]],  # V = 22
        ["IV",  "ESOVPZJAYQUIRHXLNFTGKDCMWB", ["J"]],  # J = 10
        ["V",   "VZBRGITYUPSDNHLXAWMJQOFECK", ["Z"]],  # Z = 26
        # Rotors VI - VIII only on Enigma M3, not on the Enigma I.
        ["VI",  "JPGVOUMFYQBENHZRDKASXLICTW", ["Z", "M"]],  # Z=26, M=13
        ["VII", "NZJHGRCXMYSWBOUFAIVLPEKQDT", ["Z", "M"]],  # Z=26, M=13
        ["VIII","FKQHTLXOCBJSPDZRAMEWNIUYGV", ["Z", "M"]],  # Z=26, M=13
    ]

    def __init__(self, key, text, verbose=False):
        self.plaintext = text  # TODO Move this to method encipher
        self.verbose = verbose
        # TODO for i in range(len(key[0])):
        # Make the number of active rotors adjustable.

        # Setting up the hardware
        self.lft = Rotor(key[0][0], key[2][0], key[3][0])
        self.mid = Rotor(key[0][1], key[2][1], key[3][1])
        self.rgt = Rotor(key[0][2], key[2][2], key[3][2])
        self.ref = Reflector(key[1][0])
        self.plg = Plugboard(key[4])

    def encipher(self, text, verbose=False):
        cipher = ""

        # Print starting position and settings.
        # moved to operator
        #     print_rotors(lft, mid, rgt, end="   ")
        #     print_pos(lft, mid, rgt, end="   ")
        #     print_rings(lft, mid, rgt, end="   ")
        #     print(str(plg))

        _ = self.lft.get_position()
        posM = self.mid.get_position()
        posR = self.rgt.get_position()

        # Turn rotors appropriately
        for ch in text:
            posR = self.rgt.turn()
            if posM + 1 in self.mid.get_notch():
                posM = self.mid.turn()
                _ = self.lft.turn()
            if posR in self.rgt.get_notch():
                posM = self.mid.turn()

            # Print rotor positions
            if verbose:
                self.print_pos(self.lft, self.mid, self.rgt, end="   ")

            # Encipher text
            if verbose:
                print(f"{ch} ", end="")
            ch = self.plg.vor(ch)
            if verbose:
                print(f"-> {ch} ", end="")
            ch = self.rgt.vor(ch)
            if verbose:
                print(f"-> {ch} ", end="")
            ch = self.mid.vor(ch)
            if verbose:
                print(f"-> {ch} ", end="")
            ch = self.lft.vor(ch)
            if verbose:
                print(f"-> {ch} ", end="")
            ch = self.ref.vor(ch)
            if verbose:
                print(f"-> {ch} ", end="")
            ch = self.lft.ruck(ch)
            if verbose:
                print(f"-> {ch} ", end="")
            ch = self.mid.ruck(ch)
            if verbose:
                print(f"-> {ch} ", end="")
            ch = self.rgt.ruck(ch)
            if verbose:
                print(f"-> {ch} ", end="")
            ch = self.plg.ruck(ch)
            if verbose:
                print(f"->  {ch}.")

            cipher += ch
        return cipher

    # def print_rotors(l, m, r, end="\n"):
    #     """Print names of active rotors."""
    #     print(l.get_name() + " " + m.get_name() + " " + r.get_name(), end=end)

    # def print_pos(l, m, r, end="\n"):
    #     """Print current positions of the rotors."""
    #     print(chr(l.get_position() + 65) + " " \
    #             + chr(m.get_position() + 65) + " " \
    #             + chr(r.get_position() + 65), end=end)

    # def print_rings(l, m, r, end="\n"):
    #     """Print ring positions on the rotors."""
    #     print(str(l.ring) + " " + str(m.ring) + " " + str(r.ring), end=end)


class Disk():
    """A parent class for the rotors and reflectors."""

    def __init__(self, name, wires):
        self._name = name
        self._wires = wires
        self._alpha_plain = rotor0[:]
        self._alpha_vor = self._wires.replace("", " ").split()
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
            self._notch.append((self._alpha_plain.index(letter) + 1) \
                               % len(self._alpha_plain))
        self._position = 0
        self.ring = ring
        self._set_ring(ring)
        self._set_start(self._alpha_plain.index(str(start)) + 1)

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
            raise ValueError("Reflector wires not correct. "
                             + "Should be symmetric. "
                             + f"\n{self._alpha_vor}\n{self._alpha_ruck}")


class Plugboard():
    """The plugboard just after the keyboard and just before the lamps."""

    def __init__(self, connections):
        self._alpha_plain = rotor0[:]
        self._alpha_vor = rotor0[:]
        self._sanity_check(connections)
        self.connections = connections.split()  # .replace(".", " ").split()

        # Build the _alpha_vor
        while len(self.connections) > 0:  # Until the list is empty
            r = self.connections.pop()  # Pop out a tuple to swap
            j, k = self._alpha_vor.index(r[0]), self._alpha_vor.index(r[1])
            self._alpha_vor[j], self._alpha_vor[k] = \
                self._alpha_vor[k], self._alpha_vor[j]  # swap
        # Fill self.connections again, so its not empty when __str__ gets it.
        self.connections = connections.split()  # .replace(".", " ").split()

    def _sanity_check(self, connections):
        """Check plugboard input for sanity."""
        self._alpha_sane = self._alpha_vor[:]
        if len(connections.replace(" ", "")) % 2 != 0:
            # Odd number of letters not allowed in plugboard settings.
            raise ValueError(f"Invalid plugboard settings \
                             (odd number): {connections}.")
        for ch in connections:
            try:
                if ch in self._alpha_plain:
                    self._alpha_sane.pop(self._alpha_sane.index(ch))
            except ValueError:
                # Some letter occurs twice.
                raise ValueError(f"Invalid plugboard settings \
                                 (letter twice): {connections}.")

    def __str__(self):
        """Return string representation of plugboard settings."""
        text = ""
        for i, s in enumerate(self.connections):
            text += s + " "
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
