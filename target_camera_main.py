from pathlib import Path

import cv2 as cv


def get_filename(size):
    counter_file_path = Path("counter.txt")
    if counter_file_path.is_file():
        counter = int(counter_file_path.read_text('utf-8'))
    else:
        counter = 0

    filename = format_file_name(counter, size)
    file_path = Path(filename)
    while file_path.is_file():
        counter += 1
        filename = format_file_name(counter, size)
        file_path = Path(filename)

    counter_file_path.write_text(f"{counter + 1}")
    return filename


def format_file_name(counter, size):
    filename = f'output_{counter}_{"x".join(map(lambda x: x.__str__(), size))}.avi'
    return filename


WINDOW_NAME = "frame"
DESIRED_RESOLUTION = (1280, 960)


cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, DESIRED_RESOLUTION[0])
cap.set(cv.CAP_PROP_FRAME_HEIGHT, DESIRED_RESOLUTION[1])
frame_shape = cap.read()[1].shape
size = (frame_shape[1], frame_shape[0])
print(size)

fourcc = cv.VideoWriter_fourcc(*'XVID')
cv.namedWindow(WINDOW_NAME, cv.WINDOW_NORMAL)
cv.setWindowProperty(WINDOW_NAME, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

video_filename = get_filename(size)
out = cv.VideoWriter(video_filename, fourcc, 20.0, size)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    out.write(frame)
    cv.imshow(WINDOW_NAME, frame)
    if cv.waitKey(1) == ord('q'):
        break

out.release()
cap.release()
cv.destroyAllWindows()
