# Программа: Замена фона с пост-обработкой маски и сглаживанием краёв

import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
import time
import numpy as np

cap = cv2.VideoCapture(0)  # Подключаем веб-камеру
cap.set(3, 640)
cap.set(4, 480)

segmentor = SelfiSegmentation()
fps_start = time.time()

# Загружаем все изображения из папки img
listImg = os.listdir("img")
imgList = [cv2.imread(f"img/{imgPath}") for imgPath in listImg]
indexImg = 0

while True:
    success, img = cap.read()
    if not success:
        break

    # Масштабируем фон
    bgResized = cv2.resize(imgList[indexImg], (img.shape[1], img.shape[0]))

    # Получаем альфа-маску
    mask = segmentor.segment(img, draw=False)  # 0 — фон, 1 — человек
    mask = cv2.GaussianBlur(mask, (15, 15), 0)  # Сглаживаем границу
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # Конвертируем в 3 канала
    mask = mask / 255.0  # Нормализуем в диапазон [0..1]

    # Комбинируем изображение и фон с учётом маски
    foreground = img * mask
    background = bgResized * (1 - mask)
    imgOut = cv2.addWeighted(foreground.astype(np.uint8), 1, background.astype(np.uint8), 1, 0)

    # Расчёт FPS
    fps_end = time.time()
    fps = 1 / (fps_end - fps_start)
    fps_start = fps_end

    # Выводим FPS
    cv2.putText(imgOut, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Отображаем изображение
    cv2.imshow("Image", imgOut)

    # Управление клавишами
    key = cv2.waitKey(1)
    if key == ord("a"):
        indexImg = (indexImg - 1) % len(imgList)
    elif key == ord("d"):
        indexImg = (indexImg + 1) % len(imgList)
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
