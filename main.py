#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
from frame_maker import FrameMaker
import numpy as np
MAX_CROPE_SIZE = 7


def imgs_to_video(img_path, black_path, out_path, x_size, y_size, w_list, black_time, out=None, save=False):
    n = 2
    if out is None:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(out_path, fourcc, 60, (x_size, y_size))  # создаем видео

    for i in range(len(w_list)):
        for j in range(w_list[i]):  # Запись слова
            img = cv2.imread(img_path.format(str(i)))
            if img is not None:
                crope_time = j
                if crope_time >= MAX_CROPE_SIZE:
                    crope_time = MAX_CROPE_SIZE
                img = img[crope_time * n:y_size - crope_time * n, crope_time * n * 2:x_size - crope_time * n * 2, :]
                if img.size > 0:
                    img = cv2.resize(img, (x_size, y_size), interpolation=cv2.INTER_AREA)  # Плавное приближение
            out.write(img)
            # print(img)
            # if img is not None:
            #     img = img[3:y_size-3, 3:x_size-3]
            #     img = cv2.resize(img, (y_size, x_size))  # Плавное приближение

        for j in range(black_time):  # Запись черной паузы
            out.write(cv2.imread(black_path))

    if save:
        cv2.destroyAllWindows()  # завершаем
        out and out.release()
    return out


# img = cv2.imread(r"frames_temp/start4.png")
# cv2.imshow('Result', np.asarray(img))
# cv2.waitKey()
# n = 20
# img = img[n:256-n, n*2:512-n*2, :]
# img = cv2.resize(img, (512, 256))
# cv2.imshow('Result', np.asarray(img))
# cv2.waitKey()
# exit()

frame_maker_e = FrameMaker(x_size=512, y_size=256)
# frame_maker_e.NORMAL_TIMEFRAME = 12
# frame_maker_e.LONG_TIMEFRAME = 15

frame_maker_e.SHORT_TIMEFRAME = 4
frame_maker_e.NORMAL_TIMEFRAME = 8
frame_maker_e.LONG_TIMEFRAME = 9
frame_maker_e.VERY_LONG_TIMEFRAME = 12

frame_maker_e.make_start_frames()

w_list = [50, 50, 50, 50]
out2 = imgs_to_video(r"frames_temp/start{}.png", r"frames_temp/black.png", r"page.mp4", 512, 256, w_list, 1)

frame_time_list = frame_maker_e.make_frames_from_txt(r'text.txt')
imgs_to_video(r"frames_temp/word{}.png", r"frames_temp/black.png", r"page.mp4", 512, 256, frame_time_list, 3, out=out2, save=True)

