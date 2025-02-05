#!/usr/bin/env python3

import sys
import os

notes = {
    "A " : "A#",
    "A#" : "B ",
    "B " : "C ",
    "C " : "C#",
    "C#" : "D ",
    "D " : "D#",
    "D#" : "E ",
    "E " : "F ",
    "F " : "F#",
    "F#" : "G ",
    "G " : "G#",
    "G#" : "A ",
}

def fret_separator():
    result = "    ||---------------------------------------------" \
             "--------------|"
    return result

def fret_numbers():
    result = "    || 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |" \
             " 10 | 11 | 12 |"
    return result

def fret_dots():
    result = "    ||           *         *         * " \
             "             *         *  |"
    return result

def notes_per_string(note, count):
    result = " {} |".format(note)
    note = notes[note]
    for i in range(1, count):
        result += "| {} ".format(note)
        note = notes[note]
    result += "|"
    return result

def to_note(candidate):
    candidate = candidate.upper()
    if candidate in notes:
        return candidate
    candidate += " "
    if candidate in notes:
        return candidate
    raise Exception("Unknown note")

def main():
    if len(sys.argv) != 2:
        raise Exception("Unknown or missing parameter")
    sharp = False
    notes = []
    for c in sys.argv[1][::-1]: # read it backwards
        if c == "#":
            sharp = True
            continue
        if sharp:
            c = c + "#"
            sharp = False
        try:
            notes.insert(0, to_note(c))
        except:
            pass

    print(fret_separator())
    print(fret_numbers())
    print(fret_separator())
    for note in notes[::-1]:
        print(notes_per_string(note, 13))
    print(fret_separator())
    print(fret_dots())
    print(fret_separator())

if __name__ == "__main__":
    main()
