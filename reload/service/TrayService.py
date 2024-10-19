from typing import List
import numpy as np


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class TrayService:
  def get_coordinates(self, index: int):
    letter_index = int((index % 100) / 10)
    letter = ALPHABET[letter_index]
    digit = int((index + 1) % 10)
    coordinates = f"{letter}{digit}"
    return coordinates

  def print_bin(self, prefix: str, bin: List):
    index_arrays, values_arrays = np.split(np.array(bin), 2, axis=1)
    indexes = index_arrays.flatten()
    values = values_arrays.flatten()
    coordinates = list(map(lambda x: self.get_coordinates(x), indexes))
    min_value = min(values)
    max_value = max(values)
    value_std = np.std(values)

    print(
      f"{prefix}: {min_value:{'>'}{0}0.3f}-{max_value:{' '}{'<'}{1}0.3f}{'±':{' '}{'<'}{0}}{value_std:{'<'}{0}0.3f} : {', '.join(coordinates)}"
    )
