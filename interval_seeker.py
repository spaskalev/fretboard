#!/usr/bin/env python3

candidates = []

crit = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14]

starting = 2
ending = 7
for i in range(starting, ending):
  for j in range(starting, ending):
    for k in range(starting, ending):
      for l in range(starting, ending):
        for m in range(starting, ending):
          distances = [i, j, k, l, m]
          all_distances = set()

          while len(distances) > 0:
            acc = 0
            for dist in distances:
              acc += dist
              all_distances.add(acc)
            del distances[0]
            if acc > 19:
                break

          for check in crit:
              if check not in all_distances:
                  break
          else:
            candidates.append((f"{i, j, k, l, m}", all_distances))

for value in candidates:
    print(value)
