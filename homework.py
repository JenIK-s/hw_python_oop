from typing import Dict
from dataclasses import dataclass


@dataclass(init=True)
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

    def print_message(self) -> None:
        """Информационное сообщение о тренировке."""

        print(self.get_message())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        MEDIUM_SPEED: float = self.get_mean_speed()
        calories: float = ((self.COEFF_CALORIE_1
                           * MEDIUM_SPEED
                           - self.COEFF_CALORIE_2)
                           * self.weight
                           / self.M_IN_KM
                           * self.duration
                           * 60)

        return calories


class SportsWalking(Training):
    height: int

    COEFF_1: float = 0.035
    COEFF_2: float = 0.029

    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        MEDIUM_SPEED: float = self.get_mean_speed()

        calories: float = ((self.COEFF_1
                           * self.weight
                           + (MEDIUM_SPEED**2 // self.height)
                           * self.COEFF_2
                           * self.weight)
                           * self.duration
                           * 60)

        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEFF_1: float = 1.1
    COEFF_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        speed: float = (self.length_pool
                        * self.count_pool
                        / self.M_IN_KM
                        / self.duration)

        return speed

    def get_spent_calories(self) -> float:
        MEDIUM_SPEED: float = self.get_mean_speed()

        calories: float = ((MEDIUM_SPEED + self.COEFF_1)
                           * self.COEFF_2
                           * self.weight)

        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_packages: Dict[str, str] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in dict_packages:
        return dict_packages[workout_type](*data)
    else:
        raise ValueError('Такой тренировки не существует')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
