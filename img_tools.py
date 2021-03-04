# -*- coding: utf-8 -*-
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def add_text_to_photo(img, draw, alignment_vertical_type, alignment_horizontal_type, margin, drop_text, font_size, font, color=None):
    """
    :param draw: обьект, на котором рисуем
    :param alignment_vertical_type: тип вертикального выравнивания
    :param alignment_horizontal_type: коэффицент горизонтального отступа для каждой строки(число от 0 до 1)
    :param margin: отступы от края картинки(лево, верх, право, низ)
    :param drop_text: разбитый на строки текст
    :param font_size: размер шрифта
    :param font: шрифт
    :return:
    """
    if color is None:
        color = 'rgb(255, 255, 255)'

    location = []
    #try:
    w, h = font.getsize_multiline(drop_text[0])
    #except IndexError:
    #    return None
    if alignment_vertical_type == "uniform":  # вертикальное заполнение - равномерно распределенный текст
        vertical_indent = (img.shape[0] - h * len(drop_text) - margin[1] - margin[3]) / len(
            drop_text) + 1  # Рассчитываем отступ по вертикали
    else:  # вертикальное заполнение - центированный текст
        vertical_indent = (img.shape[0] - h * (2 * len(drop_text) - 1) - margin[1] - margin[
            3]) / 2  # Рассчитываем отступ по вертикали
    current_vert_indent = vertical_indent  # текущий вертикальный отступ
    for i in range(len(drop_text)):
        current_w, current_h = font.getsize_multiline(drop_text[i])  # Получаем размеры текущей строки
        current_horiz_indent = (img.shape[1] - current_w) * alignment_horizontal_type[i] + margin[0]
        while current_vert_indent + current_h < (margin[1]):
            current_vert_indent = current_vert_indent + 1
        while current_vert_indent + current_h > (img.shape[0] - margin[3]):
            current_vert_indent = current_vert_indent - 1
        while current_horiz_indent + current_w > (
                img.shape[1] - margin[2]):  # Если с текущим отступом вылезли за края, уменьшим отступ
            current_horiz_indent = current_horiz_indent - 1
        draw.text((current_horiz_indent, current_vert_indent), drop_text[i], fill=color, font=font)
        pos = (
            current_horiz_indent, current_vert_indent, current_horiz_indent + current_w,
            current_vert_indent - current_h)
        location.append(pos)
        if alignment_vertical_type == "uniform":  # вертикальное заполнение - равномерно распределенный текст
            current_vert_indent += vertical_indent  # Выставим новый вертикальный отступ
        else:  # вертикальное заполнение - центированный текст
            current_vert_indent += 2 * h
    return location


def word_to_img(word, x_size, y_size, font_size=48, color=None):
    img = np.zeros((y_size, x_size, 3), np.uint8)
    img[:, :, :] = 0
    im = Image.fromarray(img)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('times-new-roman.ttf', size=font_size)

    add_text_to_photo(img, draw, [0.5, 0.5], [0.5, 0.5], [0, 0, 0, font_size//2], [word], font_size, font, color=color)
    # cv2.imshow('Result', np.asarray(im))
    # cv2.waitKey()
    return im, np.asarray(im)



