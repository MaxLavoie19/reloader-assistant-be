import cv2 as cv

FILE_TO_ANALYSE = "./output.avi"

cap = cv.VideoCapture(FILE_TO_ANALYSE)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
