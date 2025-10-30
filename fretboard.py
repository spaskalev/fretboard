	#!/usr/bin/env python3

import itertools
import sys
import os

notes = [
    "A ",
    "A#",
    "B ",
    "C ",
    "C#",
    "D ",
    "D#",
    "E ",
    "F ",
    "F#",
    "G ",
    "G#",
]

degrees = [
    "1 ",
    "b2",
    "2 ",
    "b3",
    "3 ",
    "4 ",
    "b5",
    "5 ",
    "b6",
    "6 ",
    "b7",
    "7 ",
]

use_degrees = False
starting_note = ''

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
    cnotes = itertools.cycle(notes)
    while note != next(cnotes):
        pass
    note = next(cnotes)
    for i in range(1, count):
        result += "| {} ".format(note)
        note = next(cnotes)
    result += "|"
    return result

def degrees_per_string(starting_note, note, count):
    sindex = notes.index(starting_note)
    cindex = notes.index(note)

    index = 0
    if sindex > cindex:
        index = 12 - (sindex - cindex)
    if cindex > sindex:
        index = cindex - sindex

    degree = ''
    cdegrees = itertools.cycle(degrees)
    for i in range(1, index+1):
        degree = next(cdegrees)
        pass

    degree = next(cdegrees)
    result = " {} |".format(degree)
    for i in range(1, count):
        degree = next(cdegrees)
        result += "| {} ".format(degree)
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
    if sys.argv[1] == "-d":
        use_degrees = True
        sys.argv[1] = sys.argv[2]
 
    sharp = False
    input = []
    for c in sys.argv[1][::-1]: # read it backwards
        if c == "#":
            sharp = True
            continue
        if sharp:
            c = c + "#"
            sharp = False
        try:
            input.insert(0, to_note(c))
        except:
            pass

    print(fret_separator())
    print(fret_numbers())
    print(fret_separator())
    for note in input[::-1]:
        print(notes_per_string(note, 13))
    print(fret_separator())
    print(fret_dots())
    print(fret_separator())

    if use_degrees:
        print()
        starting_note = input[0]
        print(fret_separator())
        print(fret_numbers())
        print(fret_separator())
        for note in input[::-1]:
            print(degrees_per_string(starting_note, note, 13))
        print(fret_separator())
        print(fret_dots())
        print(fret_separator())

if __name__ == "__main__":
    main()
