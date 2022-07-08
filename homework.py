from typing import Dict
from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {training_type};'
        ' Длительность: {duration:.3f} ч.;'
        ' Дистанция: {distance:.3f} км;'
        ' Ср. скорость: {speed:.3f} км/ч;'
        ' Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))

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
        raise NotImplementedError('DataCouldNotBeRetrieved')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 20
    SEC_IN_MIN: int = 60

    def get_spent_calories(self) -> float:
        MEDIUM_SPEED: float = self.get_mean_speed()
        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * MEDIUM_SPEED
                           - self.CALORIES_MEAN_SPEED_SHIFT)
                           * self.weight
                           / self.M_IN_KM
                           * self.duration
                           * self.SEC_IN_MIN)

        return calories


class SportsWalking(Training):
    height: int

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
    CALORIES_MEAN_SPEED_SHIFT: float = 0.029
    SEC_IN_MIN: int = 60

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

        calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                           * self.weight
                           + (MEDIUM_SPEED**2 // self.height)
                           * self.CALORIES_MEAN_SPEED_SHIFT
                           * self.weight)
                           * self.duration
                           * self.SEC_IN_MIN)

        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1
    CALORIES_MEAN_SPEED_SHIFT: int = 2

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

        calories: float = ((MEDIUM_SPEED + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                           * self.CALORIES_MEAN_SPEED_SHIFT
                           * self.weight)

        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_packages: Dict[str, type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type in dict_packages:
        return dict_packages[workout_type](*data)
    raise ValueError('WorkoutNotFound')


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
