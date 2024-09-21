from typing import Tuple

import cv2


class HeadUpDisplayService:

  def draw_rectangle(
      self,
      image: cv2.typing.MatLike,
      x1: int,
      y1: int,
      x2: int,
      y2: int,
      color: Tuple[int, int, int],
      thickness: int,
    ):
    cv2.rectangle(image, (x1, y1), (x2, y2), color=color, thickness=thickness)
