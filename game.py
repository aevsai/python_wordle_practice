import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Final, List

import pygame

Color = tuple[int, int, int]
# Определение констант
WIDTH: Final[int] = 600
HEIGHT: Final[int] = 800

WHITE: Final[Color] = (255, 255, 255)
BLACK: Final[Color] = (0, 0, 0)
GREEN: Final[Color] = (51, 255, 87)
YELLOW: Final[Color] = (255, 189, 51)
RED: Final[Color] = (255, 87, 51)
LIGHT_GRAY: Final[Color] = (229, 231, 233)
DARK_GRAY: Final[Color] = (123, 125, 125)

FONT_SIZE: Final[int] = 40
WORD_LIST = ["python"]
WORD_LENGTH = 6
ATTEMPTS_LIMIT = 6

LETTER_BOX_WIDTH = 60
LETTER_BOX_HEIGHT = 80

class LetterStatusWithColor(Enum):
    WRONG_LETTER = DARK_GRAY
    WRONG_POSITION = YELLOW
    CORRECT = GREEN
    DEFAULT = LIGHT_GRAY
    
@dataclass
class Letter:
    value: str
    pos: int
    status: LetterStatusWithColor = LetterStatusWithColor.DEFAULT

class Word(list[Letter]):
    
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
    
    def __str__(self) -> str:
        return ''.join([i.value for i in self])
    
@dataclass
class Attempt:
    word: Word = field(default_factory=Word)
    num: int = 0
    
# Инициализация Pygame
pygame.init()

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")

# Функции
def draw_text(text, font_size, color, x_pos, y_pos):
    font = pygame.font.Font(None, font_size)
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(x_pos, y_pos))
    screen.blit(text, text_rect)


def get_grip_pos(attempt_num: int, letter_num: int):
    init_left = 100
    init_top = 150
    offset_left = 10
    offset_top = 15
    
    return (
        init_left + (LETTER_BOX_WIDTH+offset_left) * letter_num, 
        init_top + (LETTER_BOX_HEIGHT+offset_top) * attempt_num
    )
    
    
def draw_attempt(attempt: Attempt):
    for i in range(WORD_LENGTH):
        pos = get_grip_pos(attempt.num, i)
        pygame.draw.rect(
            surface=screen,
            color=attempt.word[i].status.value if len(attempt.word) > i else LIGHT_GRAY,
            rect=(pos[0], pos[1], LETTER_BOX_WIDTH, LETTER_BOX_HEIGHT)
        )
        draw_text(attempt.word[i].value if len(attempt.word) > i else "", FONT_SIZE, BLACK, pos[0]+LETTER_BOX_WIDTH//2, pos[1]+LETTER_BOX_HEIGHT//2)


def draw_attempts(attempts: List[Attempt]):
    for i in range(6):
        draw_attempt(attempts[i])

def get_random_word(word_list):
    return random.choice(word_list)


def check_guess(letter, pos, word: str) -> LetterStatusWithColor:
    if letter in word:
        if pos == word.find(letter):
            return LetterStatusWithColor.CORRECT
        else:
            return LetterStatusWithColor.WRONG_POSITION
    else:
        return LetterStatusWithColor.WRONG_LETTER

# Игровой цикл
def game_loop():
    alphabet_letters = "abcdefghijklmnopqrstuvwxyz"
    attempts: list[Attempt] = [Attempt(num=i) for i in range(WORD_LENGTH)]
    word = get_random_word(WORD_LIST)
    attempt_cnt = 0
    print(word)  # Для тестирования. Необходимо удалить в конечном варианте.
    is_win = False
    fill_boxes = False
    while attempt_cnt < ATTEMPTS_LIMIT:
        screen.fill(WHITE)
        draw_attempts(attempts)

        # Рисование количества оставшихся попыток
        if is_win:
            draw_text("YOU WIN!!!", FONT_SIZE, GREEN, WIDTH//2, 100)
        else:
            draw_text(f"Attempts left: {ATTEMPTS_LIMIT - attempt_cnt}", FONT_SIZE, DARK_GRAY, WIDTH//2, 100)

        if fill_boxes:
            draw_text("Fill all letters!", FONT_SIZE, BLACK, WIDTH//2, 700)
            
        pygame.display.update()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.unicode in alphabet_letters:
                    fill_boxes = False
                    if len(attempts[attempt_cnt].word) < 6:
                        letter = Letter(
                            value=event.unicode,
                            status=LetterStatusWithColor.DEFAULT,
                            pos=len(attempts[attempt_cnt].word)
                        )
                        attempts[attempt_cnt].word.append(letter)
                elif event.key == pygame.K_BACKSPACE:
                    if len(attempts[attempt_cnt].word):
                        del attempts[attempt_cnt].word[-1]
                elif event.key == pygame.K_RETURN:
                    if len(attempts[attempt_cnt].word) == WORD_LENGTH:
                        is_win = True
                        for i in attempts[attempt_cnt].word:
                            i.status = check_guess(i.value, i.pos, word)
                            if i.status != LetterStatusWithColor.CORRECT:
                                is_win = False
                        attempt_cnt += 1
                    else:
                        fill_boxes = True

# Запуск игрового цикла

if __name__ == '__main__':
    game_loop()
