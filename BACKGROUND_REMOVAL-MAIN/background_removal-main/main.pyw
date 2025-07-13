# Программа: Замена фона в реальном времени с веб-камеры с помощью OpenCV и cvzone

import cv2  # Импорт OpenCV для работы с изображениями
import cvzone  # Импорт cvzone — надстройки над OpenCV
from cvzone.SelfiSegmentationModule import SelfiSegmentation  # Модуль для отделения человека от фона
import os  # Для работы с файлами и папками
import time  # Для расчёта FPS

# === Настройка камеры ===
cap = cv2.VideoCapture(0)  # Включаем веб-камеру
cap.set(3, 640)  # Устанавливаем ширину кадра
cap.set(4, 480)  # Устанавливаем высоту кадра

segmentor = SelfiSegmentation()  # Создаём сегментатор для удаления фона
fps_start = time.time()  # Засекаем начальное время для FPS

# === Загрузка всех фонов из папки img ===
listImg = os.listdir("img")  # Получаем список файлов
imgList = [cv2.imread(f"img/{imgPath}") for imgPath in listImg]  # Загружаем все изображения

indexImg = 0  # Индекс текущего фона

# === Основной цикл программы ===
while True:
    success, img = cap.read()  # Получаем кадр с камеры
    if not success:
        break  # Если не удалось — выходим

    # Подгоняем фоновое изображение под размер кадра с камеры
    bgResized = cv2.resize(imgList[indexImg], (img.shape[1], img.shape[0]))

    # Заменяем фон
    imgOut = segmentor.removeBG(img, bgResized)

    # Расчёт FPS
    fps_end = time.time()
    fps = 1 / (fps_end - fps_start)
    fps_start = fps_end

    # Отображаем FPS на изображении
    cv2.putText(imgOut, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Показываем результат
    cv2.imshow("Image", imgOut)

    # Управление клавишами
    key = cv2.waitKey(1)

    if key == ord("a"):  # Предыдущий фон
        indexImg = (indexImg - 1) % len(imgList)
    elif key == ord("d"):  # Следующий фон
        indexImg = (indexImg + 1) % len(imgList)
    elif key == ord("q"):  # Выход
        break

# === Завершение работы ===
cap.release()
cv2.destroyAllWindows()
