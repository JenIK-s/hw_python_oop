class InfoMessage:
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        time: int = 60
        medium_speed = self.get_mean_speed()

        calories: float = ((coeff_calorie_1 * medium_speed - coeff_calorie_2)
                           * self.weight
                           / self.M_IN_KM
                           * self.duration
                           * time)

        return calories


class SportsWalking(Training):
    height: int

    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_1: float = 0.035
        coeff_2: float = 0.029
        time: int = 60
        medium_speed = self.get_mean_speed()

        calories: float = ((coeff_1
                           * self.weight
                           + (medium_speed**2 // self.height)
                           * coeff_2
                           * self.weight)
                           * self.duration
                           * time)

        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
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
        coeff_1: float = 1.1
        coeff_2: int = 2
        medium_speed: float = self.get_mean_speed()

        calories: float = ((medium_speed + coeff_1)
                           * coeff_2
                           * self.weight)

        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_packages: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    for key, values in dict_packages.items():
        if key == workout_type:
            return values(*data)


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
