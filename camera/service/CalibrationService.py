import cv2


class CalibrationService:
  def get_bluriness_level(self, image):
    image_laplacian = cv2.Laplacian(image, 8)
    variance = max(image_laplacian.var(), 0.0000000000000001)
    bluriness = 1.0 / variance
    return bluriness
