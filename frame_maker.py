#!/usr/bin/env python
# -*- coding: utf-8 -*-
from img_tools import *


class FrameMaker:
    def __init__(self, frame_path=r"frames_temp/{}.png", x_size=512, y_size=256):
        self.colors = {
            "text": 'rgb(255, 255, 255)',
            "text2": 'rgb(200, 200, 190)',
            "note": 'rgb(255, 190, 190)',
            "direct_speech1": 'rgb(255, 0, 0)',
            "direct_speech2": 'rgb(0, 255, 0)',
        }
        self.END_SENTENCE_LIST = [".", '!', "?"]

        self.frame_path = frame_path
        self.x_size = x_size
        self.y_size = y_size

        self.main_color = self.colors["text"]
        self.second_color = self.colors["text2"]

        self.frame_time = []
        self.phrase = self.Phrase()

        self.SHORT_TIMEFRAME = 7
        self.NORMAL_TIMEFRAME = 10
        self.LONG_TIMEFRAME = 13
        self.VERY_LONG_TIMEFRAME = 20

    class Phrase:
        def __init__(self):
            self.cur_phrase = ''
            self.last_phrase = '.'

        def add_word(self, word):
            # Собираем словосочетания
            if len(word) < 3 and len(self.cur_phrase) < 10 and \
                    (word == "" or word[-1] not in [",", ".", "!", "?"]):  # Знаки препинания в конец строки
                if self.cur_phrase != "":
                    self.cur_phrase += " "  # Пробелы между словами
                self.cur_phrase += word
                return None

            if self.cur_phrase != "":
                self.cur_phrase += " "
            result = self.cur_phrase + word
            self.cur_phrase = ""
            return result

    def make_frames_from_string(self, text):
        splited_text = text.split("\n")
        for block in splited_text:
            self.make_fraims_from_block(block)
        return self.frame_time

    def make_frames_from_txt(self, filepath):
        file = open(filepath, 'r', encoding='utf8')
        text = file.read().split('\n')
        for line in text:
            self.make_fraims_from_block(line)
        return self.frame_time

    def make_frames_from_wiki(self, wiki_url):
        pass

    def make_start_frames(self):
        for word in zip(['3', '2', '1', 'Старт', ''], ['start1', 'start2', 'start3', 'start4', 'black']):
            img = word_to_img(word[0], self.x_size, self.y_size)
            img[0].save(self.frame_path.format(word[1]), 'png')  # best_img.save("BEST.png", "png")

    def make_fraims_from_block(self, text_block):
        if text_block == "":
            return

        # self.main_color, self.second_color = self.second_color, self.main_color  # Выделение блоков разным цветом

        splited_sentence = text_block.split()
        for word_num in range(len(splited_sentence)):
            word = splited_sentence[word_num]

            phrase = self.phrase.add_word(word)
            if not phrase:
                continue

            if self.phrase.last_phrase and self.phrase.last_phrase[-1] in [".", '!', "?"]:
                self.main_color, self.second_color = self.second_color, self.main_color  # Выделение блоков разным цветом
            self.phrase.last_phrase = phrase

            color = self.main_color

            # Генерим картинку
            img = word_to_img(phrase, self.x_size, self.y_size, color=color)
            img[0].save(self.frame_path.format("word" + str(self.get_next_frame_num())), 'png')

            # Устанавливаем время показа
            self.add_timeframe(phrase)

    def get_next_frame_num(self):
        return len(self.frame_time)

    def add_timeframe(self, phrase):

        if phrase[-1] in self.END_SENTENCE_LIST:
            self.frame_time.append(self.VERY_LONG_TIMEFRAME)
        elif len(phrase) < 8:
            self.frame_time.append(self.SHORT_TIMEFRAME)
        elif phrase[-1] in [","]:
            self.frame_time.append(self.LONG_TIMEFRAME)
        else:
            self.frame_time.append(self.NORMAL_TIMEFRAME)
