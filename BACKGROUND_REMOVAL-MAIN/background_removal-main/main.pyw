# Программа: Замена фона в реальном времени с веб-камеры
import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import time

# Захватываем видео с камеры
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # ширина
cap.set(4, 480)  # высота

segmentor = SelfiSegmentation()  # сегментатор из cvzone
fps_start = time.time()

# Загружаем все фоны из папки img/
listImg = os.listdir("img")
imgList = [cv2.imread(f"img/{imgPath}") for imgPath in listImg]

indexImg = 0  # текущий индекс фона

while True:
    success, img = cap.read()  # читаем кадр
    if not success:
        break

    imgOut = segmentor.removeBG(img, imgList[indexImg], threshold=0.8)

    # Расчёт FPS вручную
    fps_end = time.time()
    fps = 1 / (fps_end - fps_start)
    fps_start = fps_end

    # Отображаем FPS на изображении
    cv2.putText(imgOut, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Image", imgOut)

    key = cv2.waitKey(1)

    if key == ord("a"):
        indexImg = (indexImg - 1) % len(imgList)
    elif key == ord("d"):
        indexImg = (indexImg + 1) % len(imgList)
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
