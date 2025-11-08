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

intervals = [
    "P1",
    "m2",
    "M2",
    "m3",
    "M3",
    "P4",
    "TT",
    "P5",
    "m6",
    "M6",
    "m7",
    "M7",
    "P8",
    "m9",
    "M9",
    "m10",
    "M10",
    "P11",
    "TT'",
    "P12",
    "m13",
    "M13",
    "m14",
    "M14",
    "P15",
    "m16",
    "M16",
    "m17",
    "M16",
    "P18",
    "TT''",
    "P19",
    "m20",
    "M20",
    "m21",
    "M21",
    "P22",
]

def note_distance(note_tuple):
    index1 = notes.index(note_tuple[0])
    index2 = notes.index(note_tuple[1])
    diff = index2 - index1
    if diff < 0:
        diff = 12 + diff
    return diff

def print_intervals(note_input):
    distances = [x for x in map(note_distance, zip(note_input, note_input[1:]))]
    all_distances = set()
    while len(distances) > 0:
        acc = 0
        for i in distances:
            acc += i
            all_distances.add(acc)
        del distances[0]
    ordered_distances = [x for x in all_distances]
    ordered_distances.sort()
    named_intervals = [intervals[x] for x in ordered_distances]
    # Ignore the perfect unison here, we're not interested that it is missing
    missing_intervals = [x for x in range(1, ordered_distances[-1]) if x not in ordered_distances]
    missing_names = [intervals[x] for x in missing_intervals]
    print(" Available intervals:  " + " ".join(named_intervals) + f" (total: {len(named_intervals)})")
    print(" Missing ones:         " + " ".join(missing_names))

def fret_separator():
    result = "    ||---------------------------------------------" \
             "-----------------------------||"
    return result

def fret_numbers():
    result = "    || 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  |" \
             " 10 | 11 | 12 | 13 | 14 | 15 ||"
    return result

def fret_dots():
    result = "    ||           *         *         *             " \
             " *         **              * ||"
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
    result += "||"
    return result

def degrees_per_string(starting_note, note, count):
    index = note_distance((starting_note, note))
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
    result += "||"
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
        print(notes_per_string(note, 16))
    print(fret_separator())
    print(fret_dots())
    print(fret_separator())

    print()

    starting_note = input[0]
    print(fret_separator())
    print(fret_numbers())
    print(fret_separator())
    for note in input[::-1]:
        print(degrees_per_string(starting_note, note, 16))
    print(fret_separator())
    print(fret_dots())
    print(fret_separator())

    print()

    print_intervals(input)

if __name__ == "__main__":
    main()
