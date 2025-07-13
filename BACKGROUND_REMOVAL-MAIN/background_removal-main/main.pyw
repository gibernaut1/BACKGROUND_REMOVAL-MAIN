# Программа: Замена фона с помощью cvzone с улучшенной визуализацией

import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import time

# Инициализация камеры
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Сегментатор
segmentor = SelfiSegmentation()
fps_start = time.time()

# Загрузка фоновых изображений
listImg = os.listdir("img")
imgList = [cv2.imread(f"img/{imgPath}") for imgPath in listImg]
indexImg = 0

while True:
    success, img = cap.read()
    if not success:
        break

    # Масштабирование текущего фона
    bgResized = cv2.resize(imgList[indexImg], (img.shape[1], img.shape[0]))

    # Замена фона (метод возвращает итоговое изображение)
    imgOut = segmentor.removeBG(img, bgResized)

    # Применим размытие краёв результата, чтобы сгладить переходы
    imgOut = cv2.bilateralFilter(imgOut, d=9, sigmaColor=75, sigmaSpace=75)

    # Расчёт и вывод FPS
    fps_end = time.time()
    fps = 1 / (fps_end - fps_start)
    fps_start = fps_end
    cv2.putText(imgOut, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Отображение результата
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
