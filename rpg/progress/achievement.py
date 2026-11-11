from enum import Enum

class Achievement(Enum):
    FIRST_BLOOD = ("first-blood", "Первая кровь", "одержать первую победу")
    LUCKY = ("lucky", "Счастливчик", "найти зачарованный лут")
    VETERAN = ("veteran", "Ветеран", "достичь 5 уровня")
    DRAGON_SLAYER = ("dragon-slayer", "Драконоборец", "победить дракона")

    def __init__(self, code: str, display_name: str, description: str):
        self.code = code
        self.display_name = display_name
        self.description = description