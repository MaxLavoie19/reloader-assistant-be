class InterpolationService:
  def linear_interpolation(self, x1: float, y1: float, x2: float, y2: float, x: float):
    diff_x = x2 - x1
    diff_y = y2 - y1
    desired_x_diff = x - x1
    x_ratio = desired_x_diff / diff_x
    y = y1 + (diff_y * x_ratio)
    return y
