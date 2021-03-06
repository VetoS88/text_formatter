"""
 Программа создает из произвольного тектового файла отформатированный, 
 удовлетворяющий следующим условиям: 
    -абзацы текста разделяются одним из символов \n, \r;
    -каждая строка кроме последней строки абзаца состоит ровно из заданного количества символов;
    -каждая строка абзаца кроме последней заканчивается не пробельным символом;
    -ни на одну строку невозможно перенести первое слово следующей строки;
    -необходимые для форматирования строки пробелы распределены между словами равномерно. 

 Пример выходного файла при заданной длине строки 10 символов.
    
    1 задание.
         Дано:
    произвольн
            ый
     текстовый
    файл     и
    ограничени
    е       по
        ширине
      страницы
      (указано
        кол-во
    символов).
    Требуется:
    создать
    
"""

import re


class Formatter(object):
    """
    Класс Formatter. Выполняет функции:
        загрузка файла,
        считывание и обработка текстовых данных,
        запись отформатированных данных в новый файл.
    Принимает обязательный входной параметр:
        str_len - требуемая длинна строки в выходном файле.
    И два необязательных:
        input_file_name - имя входного файла.
        output_file_name - имя выходного файла.
    Если параметр входного фала не указан, то текстовый файл для форматирования должен находиться
    по относительному пути 'data/input' и быть доступен для чтения.
    Если параметр выходного фала не указан, то для записи должен быть доступен каталог
    по относительному пути 'data/. В нем будет создан выходной файл output.
    
    """

    def __init__(self, str_len, input_file_name='data/input', output_file_name='data/output'):
        self.str_len = str_len
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name

    def _white_space_extend(self, out_string_words):
        """
        Форматирует, равномерно заполняет строку, недостающими до заданной длинны, пробелами.
        :return: out_string - Строка равная длинне требуемой строки.
        """
        if len(out_string_words) == 1:
            word = out_string_words[0]
            out_string = ' ' * (self.str_len - len(word)) + word
            return out_string
        white_space_expected = self.str_len - len(''.join(out_string_words))
        white_space_for_word = divmod(white_space_expected, (len(out_string_words) - 1))
        for i in range(len(out_string_words) - 1):
            out_string_words[i] += (' ' * white_space_for_word[0])
        for i in range(white_space_for_word[1]):
            out_string_words[i] += ' '
        out_string = ''.join(out_string_words)
        return out_string

    @staticmethod
    def _count_expected_space(out_string_words, exp_word):
        """
        Вычисляет длинну строки при добавлении очередного слова.
        :return: expected_string_length - ожидаемая длинна строки при добавлении слова.
        """
        expected_string_length = 0
        for word in out_string_words:
            expected_string_length += len(word)
        expected_string_length += len(exp_word)
        expected_string_length += len(out_string_words)
        return expected_string_length

    def _word_cutter(self, word):
        """
        'Разрезает' слова, длинна которых более требуемой длинны строки. 
        :return: sliced_word - разрезанное слово в виде списка.
        """
        sliced_word = []
        while len(word) > self.str_len:
            sliced_word.append(word[:self.str_len])
            word = word[self.str_len:]
        sliced_word.append(word)
        return sliced_word

    def format_text(self):
        """
        Основной метод, доступный 'снаружи'. Выполняет считывание входного файла 
        и запись отформатированной строки в выходной файл. 
        """
        is_open = self._open_files()
        if not is_open:
            print('Не удалось открыть файлы!')
            return
        raw_line = self.in_file.read()
        raw_line = re.sub('\s+', ' ', raw_line)
        words = raw_line.split()
        out_string_words = []
        for raw_word in words:
            word_len = len(raw_word)
            if word_len > self.str_len:
                sliced_word = self._word_cutter(raw_word)
            else:
                sliced_word = [raw_word]
            for word in sliced_word:
                if out_string_words:
                    expected_string_length = self._count_expected_space(out_string_words, word)
                    if expected_string_length > self.str_len:
                        out_string = self._white_space_extend(out_string_words)
                        out_string += '\n'
                        self.out_file.write(out_string)
                        out_string_words = [word]
                    else:
                        out_string_words.append(word)
                else:
                    out_string_words = [word]
        if len(out_string_words) > 1:
            out_string = self._white_space_extend(out_string_words)
            self.out_file.write(out_string)
        elif len(out_string_words) == 1:
            out_string = out_string_words[0]
            self.out_file.write(out_string)
        self.out_file.flush()
        self._close_files()

    def _close_files(self):
        """
        Закрывает файлы.
        """
        self.in_file.close()
        self.out_file.close()

    def _open_files(self):
        """
        Открывает файлы на чтение и запись.
        :return: True - если  файлы успешно открыты.
        """
        try:
            self.in_file = open(self.input_file_name, 'r')
        except FileNotFoundError:
            print('Входной файл "{}" не найден'.format(self.input_file_name))
            return False
        try:
            self.out_file = open(self.output_file_name, 'w')
        except FileNotFoundError:
            print('Выходной файл "{}" не найден'.format(self.output_file_name))
            return False
        return True


if __name__ == '__main__':
    # s_len = 24
    s_len = int(input('Введите размер строки: '))
    formatter = Formatter(s_len)
    formatter.format_text()
