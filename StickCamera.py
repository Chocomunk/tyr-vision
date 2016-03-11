import cv2

cap = cv2.VideoCapture(0)

cv2.namedWindow("Tyr-Vision", cv2.cv.CV_WINDOW_NORMAL)

while cap.isOpened():
	print cap.read()[0]
	cv("Tyr-Vision", cap.read()[1])
	cv2.waitKey(1)