# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 21:38:41 2020

@author: jsg
"""
import datetime
import re
import secrets



def main():
    """Execute enigma program."""
    recipient = "ABC"
    sender = "QRSTU"
    # message = "Skal vi se da funker det Jeg vil ha mer"#.upper()
    message = "ABC QRSTU 1536 = 35 = ]16 v9o ['EKN -YSR; 1D8@s g'>{b a\ZcK Za9O[ Oj@Vm"
    # encipher = True
    encipher = False
    date = None
    month = None
    verbose = True  # For debugging

    op = Operator()
    if encipher:  # Encipher message
        message, date, key, ciphertext = op.encipher(message,
                                                     recipient=recipient,
                                                     sender=sender,
                                                     date=date,
                                                     verbose=verbose)
        print(message)
        print(date, end="  ")
        print(key)
        print(ciphertext)
        # Debug prints
        # print(type(key.rotors))
    elif not encipher:  # Decipher
        message, date, key, plaintext = op.decipher(message,
                                                    month=month,
                                                    verbose=verbose)
        print(message)
        print(date, end="  ")
        print(key)
        print(plaintext)


class Operator():
    """Emulates the operator of the Enigma M3."""

    def __init__(self):
        self._alphabet = list(alphabet)

    def encipher(self, message, recipient="ABC", sender="QRS",
                 date=None, verbose=False):
        """
        Encipher message using the enigma.

        During World War II, codebooks were only used each day to set up
        the rotors, their ring settings and the plugboard. For each message,
        the operator selected a random start position, let's say WZA, and a
        random message key, perhaps SXT. He moved the rotors to the WZA start
        position and encoded the message key SXT. Assume the result was UHL.
        He then set up the message key, SXT, as the start position and
        encrypted the message. Next, he transmitted the start position, WZA,
        the encoded message key, UHL, and then the ciphertext. The receiver
        set up the start position according to the first trigram, WZA, and
        decoded the second trigram, UHL, to obtain the SXT message setting.
        Next, he used this SXT message setting as the start position to
        decrypt the message. This way, each ground setting was different
        and the new procedure avoided the security flaw of double encoded
        message settings.
        https://en.wikipedia.org/wiki/Enigma_machine#Indicator

        Parameters
        ----------
        message : str
            Message to be enciphered.
        recipient : str, optional
            The intended recipient's code name. The default is ABC.
        sender : str, optional
            The sender's code name. The default is QRS.
        date : string yyyy-mm-dd, optional
            Day from which to get key. Today is assumed if None.
            The default is None.
        verbose : bool, optional
            Give more output to terminal. The default is False.

        Returns
        -------
        str
            The enciphered text.

        """
        # Time of day is part of the message metadata.
        time = str(datetime.datetime.now().time().strftime("%H%M"))

        # Date to know which key to use.
        if date is None:
            date = str(datetime.date.today())
        # print(date)
        key, _ = self.get_daykey(date)
        # print(f"{key=}")
        number_of_rotors = len(key.rotors)
        # print(number_of_rotors)
        # Clean plain
        plaintext = self.clean_plain(message)

        # Maximum lenght is 250 characters, but this includes the five-letter
        # group containing two random letters and the three-letter kenngruppen.
        maxlength = 245
        parts = [plaintext[i: i + maxlength]
                 for i in range(0, len(plaintext), maxlength)]

        for part in parts:
            # choose random message start pos (3 letters)
            msg_start = ''.join(secrets.choice(self._alphabet)
                                for i in range(number_of_rotors))
            # print(msg_start)
            # msg_start_list = msg_start.replace("", " ").split()
            msg_start_list = list(msg_start)#.replace("", " ").split()
            # print(f"{msg_start_list=}.")

            key.starts = msg_start_list
            # encipher message key using message start pos
            enigma = Enigma_M3(key)

            # choose random message key (3 letters)
            msg_key = ''.join(secrets.choice(self._alphabet)
                              for i in range(number_of_rotors))
            # msg_key_list = msg_key.replace("", " ").split()
            msg_key_list = list(msg_key)#.replace("", " ").split()
            enc_msg_key = enigma.process(msg_key, verbose=verbose)
            # print(f"{enc_msg_key=}.")
            key.starts = msg_key_list

            # make buchstabenkenngruppen
            letterIDgroup = ''.join(secrets.choice(self._alphabet)
                                    for i in range(2)) \
                            + secrets.choice(key.kenns)
            # Encipher message
            enigma = Enigma_M3(key)
            cipher = enigma.process(part, verbose=verbose)
            lettercount = len(cipher) + len(letterIDgroup)
            cipher = self.format_in_groups(cipher)

            # Format metadata for output
            # start of message is
            # To: From: Clock: Lettercount: Start pos: Enciphered message key:
            # Fiveletter group containing two random letters
            # and the 3 letter kenngruppe
            precipher = str(recipient) + " " + str(sender) + " " + str(time)\
                + " = " + str(lettercount) + " = " \
                + msg_start + " " + enc_msg_key + " " + letterIDgroup + " "

            # Enciphered message
            ciphertext = precipher + cipher

            return message, date, key, ciphertext

    def decipher(self, message, month=None, verbose=False):
        """
        Decipher message.

        Parameters
        ----------
        message : str
            Message to be decipered including encrypted premessage metadata.
        month : string yyyy-mm, optional
            Month in which to look for key, current month assumed if None.
            This is useful for deciphering old messages.
            The default is None.
        verbose : bool, optional
            Give extra output to terminal. The default is False.

        Returns
        -------
        str
            The decipered text.

        """
        # print(message)

        # Find recipient
        recipient = re.findall("[A-Za-z]+ ", message)[0]
        message = message[len(recipient):]
        recipient = recipient.strip()
        # print(recipient, message)
        # Find sender
        sender = re.findall("[A-Za-z]+ ", message)[0]
        message = message[len(sender):]
        sender = sender.strip()
        # print(sender, message)
        # Find time
        time = re.search("[0-9]{4}", message)[0]
        time = time[:2] + ":" + time[-2:]
        message = message[len(time):]
        # print(time, message)
        # Find message length
        # Message length should be a number between two equal signs.
        # The message length is not allowed to exceed 245.

        length = re.search("= [0-9]+ =", message)[0]
        messagelength = int(length[1:-1])
        message = message[len(length):]
        # print(length, message)
        # Find message start pos
        # Find enciphered message key
        msg_start = re.findall("[\S]+ ", message)[0]
        message = message[len(msg_start):]
        msg_start = msg_start.strip()
        # print(msg_start, message)

        enc_msg_key = re.findall("[\S]+ ", message)[0]
        message = message[len(enc_msg_key) + 1:]
        enc_msg_key = enc_msg_key.strip()
        # msg_start_list = msg_start.replace("", " ").split()
        # print(enc_msg_key, message)

        # What is left of the message is what is counted in the message lenght
        actual_message_length = len(message.replace(" ", ""))
        if actual_message_length == messagelength:
            # Message has correct length
            # print(f"Message length is correct: {messagelength}.")
            pass
        else:
            print("Message length is not correctly reported.\n"
                  + f"Should be {messagelength}, but is "
                  + f"{actual_message_length}!")

        # Find kenngruppen
        # Kenngruppen is the last three letters in the first five-letter group.
        kenngruppen = re.search("[\S]{5} ", message)[0][2:-1]

        # Look up key in book
        key, date = self.get_daykey(kenngruppen, month=month)
        key.starts = msg_start

        # Decipher message key
        # print(f"Decipher message key using key {str(key)}.")
        enigma = Enigma_M3(key)
        msg_key = enigma.process(enc_msg_key, verbose=verbose)
        # msg_key_list = msg_key.replace("", " ").split()

        # Get the actual message, i.e. after the 5 letter kenngruppen
        cipher = message.partition(kenngruppen)[-1].replace(" ", "")
        # print(f"{cipher=}")

        # Decipher message.
        # print(message)
        key.starts = msg_key
        # print(f"Decipher message using key {str(key)}.")
        enigma = Enigma_M3(key)
        plain = enigma.process(cipher, verbose=verbose)
        plain.lower()
        preplain = "Til " + recipient + " fra " + sender \
            + " " + str(date) + " " + time + "\n"
        return message, date, key, preplain + plain

    def get_daykey(self, label, month=None):
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
            (Key)
                daykey.
            (str)
                Date on which given key is valid.
        """
        # Check label format
        if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", label):
            # Label is a date
            day = datetime.datetime.strptime(label, "%Y-%m-%d").date()
            return self.get_key_from_date(day), str(day)
        elif re.match("[0-9]{2}", label):
            # Label is a day of month
            if month is None:
                # Assuming current month
                today = datetime.date.today()
                day = datetime.date(today.year, today.month, int(label))
            else:
                # Using specified month
                day = datetime.date(month[:4], month[-2:], label)
            # keyfilename = "enigmaSchlussel" + str(day)[:7] + ".txt"
            return self.get_key_from_date(day), str(day)

        elif re.match("[A-Z]{3}", label):
            # Label is a kenngruppe.
            if month is None:
                # Assuming current month
                day = datetime.date.today()
            else:
                # Using specified month
                day = datetime.date(month[:4], month[-2:], 1)
            key, day = self.get_key_from_kenngruppe(day, label)
            return key, day
        else:
            # Program will crash here.
            raise ValueError(f"Invalid input {label=}.")

    def get_key_from_date(self, date):
        """Return daykey of given day."""
        keyfilename = "enigmaSchlussel" + str(date)[:7] + ".txt"
        with open(keyfilename, "r") as infile:
            for line in infile:
                if re.search(str(date)[-2:], line[:6]):
                    return Key(line)

    def get_key_from_kenngruppe(self, day, kenn):
        """Return daykey of given kenngruppe."""
        keyfilename = "enigmaSchlussel" + str(day)[:7] + ".txt"
        with open(keyfilename, "r") as infile:
            for line in infile:
                if re.search(str(kenn), line):
                    # Correct the date to show the date on which
                    # the key was valid.
                    day = datetime.date(int(keyfilename[15:19]),
                                        int(keyfilename[20:22]),
                                        int(re.search("[0-9]{2}",
                                                      line)[0]))
                    return Key(line), day

    def clean_plain(self, s):
        """
        Clean plain text and prepare it for enciphering.

        Parameters
        ----------
        s : str
            The "raw" text to be cleaned.

        Returns
        -------
        str
            The clean text, containing only characters present
            in the Enigma keyboard.
        """
        # KLAM = Parenthesis
        # ZZ = Comma
        # X = Full stop (end of sentence)
        # YY = Point or dot
        # X****X = Inverted commas

        # Question mark (Fragezeichen in German) was usually abbreviated to
        # FRAGE, FRAGEZ or FRAQ.
        # Foreign names, places, etc. are delimited twice by "X", as in
        # XPARISXPARISX or XFEUERSTEINX.
        # The letters CH were written as Q. ACHT became AQT, RICHTUNG
        # became RIQTUNG.

        # Numbers were written as NULL EINZ ZWO DREI VIER FUNF
        # SEQS SIEBEN AQT NEUN
        # It was prohibited to encipher the word "NULL" several times in a row,
        # so they used CENTA (00), MILLE (000) and MYRIA (0000).
        # Some examples: 200 = ZWO CENTA, 00780 = CENTA SIEBEN AQT NULL.
        # print(s)
        # s = s.replace("", " ").split()
        s = list(s)
        # print(s)
        for i, letter in enumerate(s):
            # print(i, s[i])
            if letter in self._alphabet:
                # Lower case letter or upper case letter
                s[i] = letter
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
                s.insert(i, "SEQS")
            elif letter == "7":
                _ = s.pop(i)
                s.insert(i, "SIEBEN")
            elif letter == "8":
                _ = s.pop(i)
                s.insert(i, "AQT")
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
                print(f"Character not allowed. Discarded character: '{s[i]}'")
                s[i] = ""

        return "".join(s)

    def format_in_groups(self, s, group=5):
        """Format the cipher text in groups for transmission."""
        # Adds a space every five characters or so.
        return " ".join(s[i: i + group] for i in range(0, len(s), group))


class Key():
    """Represents the key."""

    def __init__(self, keytext):
        """
        Initialize key object from code book string (daykey).

        keytext : str
            Line from code book containing daykey.
        """

        keyparts = keytext.split("|")

        self.dayofmonth = int(keyparts[1])
        self.rotors = keyparts[2].split()
        self.rings = keyparts[3].split()
        # print(f"{self.rings=}")
        for k in range(len(self.rings)):
            self.rings[k] = int(self.rings[k])
        # print(f"{self.rings=}")

        self.plugs = keyparts[4]
        self.plugs = self.plugs.lstrip().rstrip()
        self.kenns = keyparts[5].split()
        self.refl = "B"  # Hardcoding reflector B.
        self.starts = ""  # Start position is not read from codebook/file.

    def __str__(self):
        """Return string to print the daykey nicely."""
        s = ""
        for rotor in self.rotors:
            s = s + rotor + " "
        # print(s)
        if self.starts:
            # print("start True.")
            for start in self.starts:
                s = s + start
            s = s + " "
        # print(s)
        for ring in self.rings:
            s = s + str(ring) + " "
        # print(s)
        s = s + self.plugs
        return s


class Enigma_M3():
    """Emulates the Enigma M3 machine."""
    _rotors = {
        # rotor = ["name", "cipher alpha", [notches]]
        # "0": ["0", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", [""]],
        "I": ["I", "EKMFLGDQVZNTOWYHXUSPAIBRCJ", ["Q"]],  # Q = 17
        "II": ["II", "AJDKSIRUXBLHWTMCQGZNPYFVOE", ["E"]],  # E = 05
        "III": ["III", "BDFHJLCPRTXVZNYEIWGAKMUSQO", ["V"]],  # V = 22
        # "I": ['I', 'Ζ<хВгχR=|йÏqdmAφ[Τ&νЖ"ρåпÖАᛦVᛯᚱaδ+,лМᚾοᛒLíMElZΜfΦᛗgeСxᛊБtsTDЗᛏᚦя\\YiυУΧЁvу>ᛜGРᚴФ]äÄЪ6НUИ_ÅbÉᚠΚΑτᛮᚬNΔᛇïΞλΠΟᛉ(ΙЭÞι`KΣ\'ΓЫоSη:)здЧиPᛅQn#μJáᚲκквюышcᛁ0CαЮГþθzo9r2jᛈyξмᛰΘёчᚺХ4O$σКζэóбhΝÓHᛃ53ÐфωрᚢIγЦᛖ@FЙ;Ηц/*аᛚΩð7ъЕО~1ΛЛᛘpтψ{Д.ᛋBᛞWн}ÁuÆᚹæΒ8еᚨᛟΡТж%π-Ε?ЬØøьЩᚼщΨᚷсöÍ!ΥXβШεПékw^Я', ['!', '#', '%', ',', '/', '1', '2', '6', '9', 'A', 'F', 'L', 'M', 'N', 'U', 'Y', '[', '^', '`', 'a', 'e', 'w', 'É', 'Ó', 'Þ', 'Æ', 'Å', 'í', 'ï', 'æ', 'ø', 'ö', 'Α', 'Ζ', 'Η', 'Θ', 'Λ', 'Σ', 'Χ', 'Ψ', 'ι', 'κ', 'λ', 'μ', 'ξ', 'ο', 'ρ', 'υ', 'А', 'Г', 'Е', 'К', 'М', 'Н', 'Ф', 'Ц', 'Ь', 'Ю', 'Я', 'в', 'г', 'д', 'з', 'й', 'н', 'с', 'у', 'х', 'ч', 'ш', 'ъ', 'я', 'ᚠ', 'ᚢ', 'ᚦ', 'ᚨ', 'ᚲ', 'ᚺ', 'ᛁ', 'ᛃ', 'ᛅ', 'ᛈ', 'ᛊ', 'ᛏ', 'ᛒ', 'ᛗ', 'ᛘ', 'ᛟ', 'ᛦ']],
        # "II": ['II', 'Pцо1rsЧÍΝUуGΓ/cσ"ᛞþᛋmψðεV2ᛜC$n0ΤLΦNъыЙкυÉФÁΥγxwf&åR{u(иαЮIÅΩeκМЬᚲØθс-d6ᛦ#.яAiFСΛᚹDᛯК3Щюοх5ζX+7WΠᛇеᛖЫδφΣᚠ]УмqᚼΧ9ÄHZчшτΞhᛘΡïᛉgᛰ)В^ᛮЭΔЖlχщфΖj<ÞᚨЗπ_%ЯНИрΘ*эᚺΚΟY~Рёpᛈ[νᚦ}ᚷztωжтпΑᛃΨбЪᛚBБÆ\'лμГ!ᚾ=æJ\\ιákTᚢéгᛗEΒᛏξзᚴЁДÓвОλÏ>KдρbХПΜ`ÖvηóᛟΙаOayᛒ4ᛅ8ШM,;нβЕьΗА@ЦᛊQᚬÐ|:SΕøoäöᚱйᛁЛ?íТ', ['"', '$', '&', '0', '4', '6', '9', '=', '@', 'B', 'D', 'E', 'F', 'J', 'L', 'P', 'Q', 'S', 'U', 'W', 'Z', '^', 'p', 'q', 's', 'w', '|', 'Í', 'Ï', 'Þ', 'Ø', 'ö', 'å', 'Α', 'Γ', 'Ι', 'Ξ', 'Ο', 'Ρ', 'Ω', 'γ', 'ι', 'ο', 'π', 'Д', 'Е', 'Н', 'С', 'Ф', 'Ч', 'Ш', 'Ы', 'Э', 'Ю', 'д', 'ё', 'ф', 'х', 'ы', 'ᚢ', 'ᚦ', 'ᚱ', 'ᚲ', 'ᛇ', 'ᛈ', 'ᛖ', 'ᛗ', 'ᛘ', 'ᛜ', 'ᛯ', 'ᛰ']],
        # "III": ['III', ':ᚺYhᚾLЬвRεðкΗᛉχЕAτбEЖΚΣ6чᛜαΧиÓᚨзᛁᛖ<ïΥXпνᛊøъС^ᛞξЧ9ΓÄ;ГТΟΦ7ЮIᚦШΔ>οΕδᚼΤᛚЭПPB`ᛮ!тÅβеyΩJtдpЪWш]ЗiЩ_í|wРрΠäИхᛇσ=УujаVéΘÐqψ(ΞᛋᚬáGγÁÍl#DМsНщócоΙeæцþВöмåKÖᛦιzфйÆμ0АΒЛᚢКᚠυэoжᛒᚴО"{πθ~ХΜᚲДΑ*5Фη}\\ᚷgÞᚹCЫρЙQᛘЯ3\'&Ρ-Z.8SлᛏU2сᚱЦг/нᛯr$ΝьёOζЁΛᛃΖb[Éωᛈx)%ΨκÏT1FюvMHБ+Nу@?dmыaᛅ4nf,λφkᛰᛗᛟяØ', ['"', '#', '&', '(', '*', '+', '-', '/', '2', '@', 'A', 'C', 'D', 'E', 'K', 'L', 'P', 'R', 'S', 'T', 'V', '\\', 'd', 'j', 's', '{', 'Ï', 'Ð', 'Å', 'í', 'ï', 'ä', 'Δ', 'Ι', 'Κ', 'Ν', 'Ξ', 'Ο', 'Ρ', 'Τ', 'Φ', 'Χ', 'Ψ', 'γ', 'ε', 'χ', 'Г', 'И', 'Й', 'П', 'Р', 'Ф', 'Ш', 'Ъ', 'Ю', 'Я', 'в', 'е', 'ж', 'и', 'л', 'о', 'у', 'ф', 'ш', 'ю', 'я', 'ᚢ', 'ᚲ', 'ᚷ', 'ᚹ', 'ᚺ', 'ᚼ', 'ᚾ', 'ᛁ', 'ᛃ', 'ᛋ', 'ᛏ', 'ᛒ', 'ᛘ', 'ᛦ', 'ᛯ']],
        "IV": ["IV", "ESOVPZJAYQUIRHXLNFTGKDCMWB", ["J"]],  # J = 10
        "V": ["V", "VZBRGITYUPSDNHLXAWMJQOFECK", ["Z"]],  # Z = 26
        # Rotors VI - VIII only on Enigma M3, not on the Enigma I.
        "VI": ["VI", "JPGVOUMFYQBENHZRDKASXLICTW", ["Z", "M"]],  # Z=26, M=13
        "VII": ["VII", "NZJHGRCXMYSWBOUFAIVLPEKQDT", ["Z", "M"]],
        "VIII": ["VIII", "FKQHTLXOCBJSPDZRAMEWNIUYGV", ["Z", "M"]],
        'X': ['X', 'ZLC\\7dqQ{0,-Spo]K`c+9<8[:?~!"li}*3bts4>6z1XB&#Vw(hOu/Y;rHReAD@\'E)JGfIv|mnN$.5%W_UkMajT^=Fy2xgP', ['"', '&', "'", '/', '7', '9', ';', '>', 'E', 'M', 'S', 'T', 'W', 'X', '\\', 'a', 'b', 'c', 'f', 'k', 'n', 'q', 'v', 'z', '{', '|']],
        'XI': ['XI', 'fk0B75At}-;M\\4/ZJN3?WXTUbR(oDE~^|\'Vs`PF_ezrvG]Sadh[lIKgYO@$i+<L1,8#{!p"jwCn=:6q%u2).m>*c9yxQ&H', ['!', '*', '1', '3', '4', '6', ':', ';', 'A', 'E', 'I', 'J', 'M', 'N', 'O', 'P', 'Q', 'S', 'U', '[', ']', '_', '`', 'a', 'c', 'f', 'h', 'n', 'p', 'q', 'r', 'v', '}']],
        'XII': ['XII', 'z9~2Rt|;]n/S<V}E64j1{uU*5=,M![iA:y.hPD7kaGZe$H^r#_`N@vfmo(ObFW8\'cTl"LI\\0p?qC-xY+>s3dQ%wKgBJX&)', ['+', '/', '3', '5', '8', '9', ':', ';', '<', '>', 'A', 'B', 'R', 'T', 'V', 'Y', 'Z', 'e', 'g', 'r', 'v', 'w', '~']],
        'XIII': ['XIII', 'VKMqv!l7AwU#T`"->}JX2F3%8Nygf{sIDhH\\;=:LWm.r\'Qt9~Gneb(Bu*4<PRdOk$Za,ESj+c6Y^@x&o|/_[51?)p0]zCi', ['$', "'", '(', ')', '.', '1', '2', '6', '7', '8', '?', 'A', 'E', 'J', 'O', 'V', '^', 'a', 'e', 'g', 'h', 'j', 't', 'u', 'w', '{']],
        'XIV': ['XIV', 'IaUN)9SR"?c/0+|w5\'7ust:~^vZ\\W%Km_yf{MjV6d8H`JOk]X*e(1r2il>p!Ph$3YLDC#=gboF<,G@[BzQAEqTx-.4;n}&', ['$', '%', '(', '*', ',', '2', '5', '8', '=', '?', '@', 'A', 'B', 'H', 'I', 'K', 'N', 'P', 'R', 'W', 'c', 'j', 'k', 'm', 'r', 'u', '}', '~']]
    }

    _reflectors = {
        "A": ["A", "EJMZALYXVBWFCRQUONTSPIKHGD"],\
        # reflB is standard on Enigma I.
        "B": ["B", "YRUHQSLDPXNGOKMIEBFZCWVJAT"],\
        "B": ["B", "~}|{zyxwvutsrqponmlkjihgfedcba`_^]\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)('&%$#\"!"],
        # "B": ["B", "ᛰᛯᛮᛦᛟᛞᛜᛚᛘᛗᛖᛒᛏᛋᛊᛉᛈᛇᛅᛃᛁᚾᚼᚺᚹᚷᚴᚲᚱᚬᚨᚦᚢᚠяюэьыъщшчцхфутсрпонмлкйизжёедгвбаЯЮЭЬЫЪЩШЧЦХФУТСРПОНМЛКЙИЗЖЁЕДГВБАωψχφυτσρποξνμλκιθηζεδγβαΩΨΧΦΥΤΣΡΠΟΞΝΜΛΚΙΘΗΖΕΔΓΒΑåöøäæþóðïíéáÅÖØÄÆÞÓÐÏÍÉÁ~}|{zyxwvutsrqponmlkjihgfedcba`_^]\[ZYXWVUTSRQPONMLKJIHGFEDCBA@?>=<;:9876543210/.-,+*)('&%$#\"!"],
        # B is a simple atbash for now.
        "C": ["C", "FVPJIAOYEDRZXWGCTKUQSBNMHL"],\
    }

    def __init__(self, key):  # , verbose=False):
        """
        Sets up the Enigma according to given key.

        Parameters
        ----------
        key : Key
            Key object containing, well, key information.

        """
        # Setting up the hardware
        self.rotorlist = []
        # print(key)
        # print(key.rotors)
        for n in range(len(key.rotors)):
            # print(f"Rotor {n}")
            rot = Rotor(self._rotors[key.rotors[n]],
                        key.starts[n],
                        key.rings[n])
            self.rotorlist.append(rot)
        # print(self.rotorlist)
        # Reflector
        self.ref = Reflector(self._reflectors[key.refl])
        # Plugbord
        self.plg = Plugboard(key.plugs)

    def process(self, text, verbose=False):
        """
        Encipher or decipher text.

        The text is enciphered (or if it is already enciphered, deciphered).
        This method probably needs a better neam than "process".
        This is the heart of the machine.

        Parameters
        ----------
        text : str
            The text to encipher.
        verbose : bool, optional
            Print all the steps in the enciphering process to terminal.
            The default is False.

        Returns
        -------
        cipher : str
            The enciphered (or deciphered) text.

        """
        self.plaintext = text
        cipher = ""

        pos = []
        for n in range(len(self.rotorlist)):
            pos.append(self.rotorlist[n].get_position())

        # Turn rotors appropriately
        for ch in text:
            # print(self.rotorlist)
            pos[-1] = self.rotorlist[-1].turn()
            # print(self.rotorlist[-1]._name,
            #       # self.rotorlist[-1].get_letter(self.rotorlist[-1].get_position()))
            # if pos[-1] in self.rotorlist[-1].get_notch():
            #     # Treating the rightmost rotor separately
            #     # because it steps for every character.
            #     print("Step pos[-2]")
            #     pos[-2] = self.rotorlist[-2].turn()

            # # for n in range(len(self.rotorlist)):
            # #     print(self.rotorlist[n]._name, pos[n], end="   ")
            # # print()

            # for n in range(len(self.rotorlist) - 1):
            #     # traversing the list backwards skipping the  #no
            #     # first and last items.  #no
            #     if (pos[n] +1) in self.rotorlist[n].get_notch():
            #         # Double stepping (I think).
            #         print("Double stepping")
            #         print(self.rotorlist[n]._name)
            #         pos[n] = self.rotorlist[n].turn()
            #         pos[n - 1] = self.rotorlist[n - 1].turn()

            for n in range(1, len(self.rotorlist) - 1):
                # print(n)
                # For all rotors, exept the first and last
                if pos[n] + 1 in self.rotorlist[n].get_notch():
                    # Rotor is in notch position
                    # Turn rotor
                    pos[n] = self.rotorlist[n].turn()
                    # Turn rotor to the left
                    pos[n - 1] = self.rotorlist[n -1].turn()
            # Treat right rotor separately
            if pos[len(self.rotorlist) - 1] in self.rotorlist[len(self.rotorlist) - 1].get_notch():
                    pos[len(self.rotorlist) - 2] = self.rotorlist[len(self.rotorlist) - 2].turn()

            # Print rotor positions
            if verbose:
                for rotor in self.rotorlist:
                    # print(chr(rotor.get_position()+65), end =" ")
                    print(rotor.get_letter(rotor.get_position()), end =" ")

            # Encipher text
            if verbose:
                print(f"  {ch}  ", end="")
            ch = self.plg.vor(ch)
            if verbose:
                print(f"> {ch} ", end="")
            for i in range(len(self.rotorlist) - 1, -1, -1):
                ch = self.rotorlist[i].vor(ch)
                if verbose:
                    print(f"> {ch} ", end="")
            ch = self.ref.vor(ch)
            if verbose:
                print(f">R> {ch} ", end="")
            for i in range(len(self.rotorlist)):
                # print(i, end="")
                ch = self.rotorlist[i].ruck(ch)
                if verbose:
                    print(f"> {ch} ", end="")
            ch = self.plg.ruck(ch)
            if verbose:
                print(f">  {ch}")

            cipher += ch
        return cipher


class Disk():
    """A parent class for the rotors and reflectors."""

    def __init__(self, name, wires):
        self._alphabet = list(alphabet)
        self._name = name
        self._wires = wires
        self._alpha_plain = self._alphabet[:]
        # self._alpha_vor = self._wires.replace("", " ").split()
        self._alpha_vor = list(self._wires)  # .replace("", " ").split()
        # print(f"Disk.__init__ {type(self._alpha_vor)}")
        self._alpha_ruck = self._alphabet[:]
        self.set_ruck()

    def __str__(self):
        """Return string representation of Disk object."""
        return f"Disk, wires {self._wires}."

    def vor(self, ch):
        """Substitute letter, according to disk wiring.

        This function substitutes while the signal moves "forward" thru
        the disk, i.e. towards the reflector.

        Args:
            ch, single character
                Character to be enciphered.
        Returns:
            str
            The enciphered character.

        """
        i = self._alpha_plain.index(ch)
        ch = self._alpha_vor[i]
        return ch

    def set_ruck(self):
        """Build the backward substitution alphabet."""
        for i, l in enumerate(self._alpha_plain):
            self._alpha_ruck[i] = \
                self._alpha_plain[self._alpha_vor.index(l)]


class Rotor(Disk):
    """The rotors in the core of the machine."""

    def __init__(self, hardware, start, ring):
        super(Rotor, self).__init__(hardware[0], hardware[1])
        self._notch = []
        for i, letter in enumerate(hardware[2]):
            self._notch.append((self._alpha_plain.index(letter) + 1)
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

    def get_letter(self, position):
        """Return the letter a a certain position:"""
        return self._alphabet[position]

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

        Args:
            ch, single character
                Character to be enciphered.
        Returns:
            str
            The enciphered character.
        """
        ch = Disk.vor(self, ch)
        i = self._alpha_plain.index(ch) - self._position
        ch = self._alpha_plain[i]
        return ch

    def ruck(self, ch):
        """Substitute letter, according to disk setting.

        This function substitutes while the signal moves "back" thru
        the disk, i.e. from the reflector.

        Args:
            ch, single character
                Character to be enciphered.
        Returns:
            str
            The enciphered character.
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
        self._alphabet = list(alphabet)
        self._alpha_plain = self._alphabet[:]
        self._alpha_vor = self._alphabet[:]
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


def choose_letters():
    a0 = "!\"#$%&'()*+,-./0123456789:;<=>?"
    a3 = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_"
    a5 = "`abcdefghijklmnopqrstuvwxyz{|}~"

    a7 = "\u00c1\u00c9\u00cd\u00cf\u00d0\u00d3\u00deÆÄØÖÅ\u00e1\u00e9\u00ed\u00ef\u00f0\u00f3\u00feæäøöå"

    a8 = "\u00df"

    a9 = "\u0391\u0392\u0393\u0394\u0395\u0396\u0397\u0398\u0399\u039a\u039b\u039c\u039d\u039e\u039f\u03a0\u03a1\u03a3\u03a4\u03a5\u03a6\u03a7\u03a8\u03a9"
    a10 = "\u03b1\u03b2\u03b3\u03b4\u03b5\u03b6\u03b7\u03b8\u03b9\u03ba\u03bb\u03bc\u03bd\u03be\u03bf\u03c0\u03c1\u03c3\u03c4\u03c5\u03c6\u03c7\u03c8\u03c9"

    a11 = "\u0410\u0411\u0412\u0413\u0414\u0415\u0401\u0416\u0417\u0418\u0419\u041a\u041b\u041c\u041d\u041e\u041f\u0420\u0421\u0422\u0423\u0424\u0425\u0426\u0427\u0428\u0429\u042a\u042b\u042c\u042d\u042e\u042f"
    a13 = "\u0430\u0431\u0432\u0433\u0434\u0435\u0451\u0436\u0437\u0438\u0439\u043a\u043b\u043c\u043d\u043e\u043f\u0440\u0441\u0442\u0443\u0444\u0445\u0446\u0447\u0448\u0449\u044a\u044b\u044c\u044d\u044e\u044f"

    a14 = "\u16a0\u16a2\u16a6\u16a8\u16ac\u16b1\u16b2\u16b4\u16b7\u16b9\u16ba\u16bc\u16be\u16c1\u16c3\u16c5\u16c7\u16c8\u16c9\u16ca\u16cb\u16cf\u16d2\u16d6\u16d7\u16d8\u16da\u16dc\u16de\u16df\u16e6\u16ee\u16ef\u16f0"

    asciiChars = a0 + a3 + a5
    nordic = a7  # + a8
    greek = a9 + a10
    russian = a11 + a13
    runes = a14
    return asciiChars  # + nordic + greek + russian + runes


alphabet = choose_letters()
# alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

if __name__ == "__main__":
    main()
