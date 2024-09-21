from typing import Tuple
import cv2


class ImageEditingService:
  def convert_to_gray_scale(self, image: cv2.typing.MatLike):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

  def crop_image(self, image: cv2.typing.MatLike, x1: int, y1: int, x2: int, y2: int):
    croped_image = image[y1:y2, x1:x2]
    return croped_image

  def print(self, image: cv2.typing.MatLike, text: str, text_bottom_left: Tuple[int, int]):
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 2
    font_color = (255,255,255)
    thickness = 2
    line_type = 2

    cv2.putText(
      image, text, text_bottom_left, font, font_scale, font_color, thickness, line_type,
    )


  def get_centered_rectangle(
      self,
      image: cv2.typing.MatLike,
      rectangle_width: int,
      rectangle_height: int,
  ):
    image_height, image_width, _ = image.shape
    half_image_height = int(image_height/ 2.0)
    half_image_width = int(image_width/ 2.0)

    half_rectangle_height = int(rectangle_height / 2.0)
    half_rectangle_width = int(rectangle_width / 2.0)

    x1 = half_image_width - half_rectangle_width
    y1 = half_image_height - half_rectangle_height

    x2 = half_image_width + half_rectangle_width
    y2 = half_image_height + half_rectangle_height
    return x1, y1, x2, y2
