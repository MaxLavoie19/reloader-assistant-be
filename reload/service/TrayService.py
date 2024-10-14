
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class TrayService:
  def get_coordinates(self, index: int):
    letter_index = int((index % 100) / 10)
    letter = ALPHABET[letter_index]
    digit = int((index + 1) % 10)
    coordinates = f"{letter}{digit}"
    return coordinates
