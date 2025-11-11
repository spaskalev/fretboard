#!/usr/bin/env python3

candidates = {}

for i in range(1, 7):
  for j in range(1, 7):
    for k in range(1, 7):
      for l in range(1, 7):
          distances = [i, j, k, l]
          all_distances = set()

          while len(distances) > 0:
            acc = 0
            for dist in distances:
              acc += dist
              all_distances.add(acc)
            del distances[0]
            if acc > 19:
                break

          if len(all_distances) >= 10:
            candidates[f"{i, j, k, l}"] = all_distances

for key, value in candidates.items():
    if 1 in value:
        continue
    print(key, value)
