# enigma.py #
Emulating the Enigma cipher machine.

This repository emulates the Enigma cipher machine used by the
Germans from the 1920's to the 1940's. Specificly, the Enigma M3.

## v1.0 ##

This version emulates only the machine itself.

It is intended to
be run from an IDE (e.g. Spyder). Input is given by manually
editing the `key` and `plain` variables near the top of
`enigma.py`. Running the file should write the plaintext, the
cleaned plaintext (no numbers or punctuation, only A-Z), the
setting i.e. the key, and the ciphertext to terminal.

The Enigma is symmetrical, thus giving the ciphertext as
`plain`should return the plaintext, albeit without punctuation
and in groups of 5 letters.

The machine is symmetric, i.e. it does return the plaintext if
the plaintext is enciphered twice. It also agrees with online
emulators [Cryptii](https://cryptii.com/pipes/enigma-machine "https://cryptii.com/pipes/enigma-machine") and
[101 Computing](https://www.101computing.net/enigma-machine-emulator/ "https://www.101computing.net/enigma-machine-emulator/")

## v2.0 ##

This version emulates the machine and its operator. The message
metadata is handled by the operator, and there is a difference
between enciphering and deciphering.

It is intended to
be run from an IDE (e.g. Spyder). Input is given by manually
editing the `recipient`, `sender`, and `message` variables near
the top of
`enigma.py`. Setting `encipher` to `True` or `False` will
determine if the message is enciphered or deciphered. The key is
no longer a required input, as this is read from the file
`enigmaSchlusselYYYY-MM.txt`, where YYYY-MM is the month for
which the keys are valid.

Running the file with `encipher = True` should write the
cleaned plaintext (no numbers or punctuation, only A-Z), the
date, the key, and the ciphertext to terminal.
Running the file with `encipher = False` should write the
ciphertext, the
date, the key, and the plaintext (albeit without punctuation)
to terminal.

If the message to be deciphered was sent this month, the operator
will get the right key from `enigmaSchlusselYYYY-MM.txt`. If the
message is older, the month it was sent must be specified using
the `month` variable `month = YYYY-MM`.

There is also a `verbose` variable which, if True will write
all the steps of the (en/de)ciphering process of each letter
in the (cipher/plain)text.