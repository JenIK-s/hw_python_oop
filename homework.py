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
        return (f'''Тип тренировки: {self.training_type};
                    Длительность: {self.duration} ч.;
                    Дистанция: {self.distance:.3f} км;
                    Ср. скорость: {self.speed:.3f} км/ч;
                    Потрачено ккал: {self.calories:.3f}.''')

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

    def show_training_info(self, workout_type) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        duration = self.duration
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()

        return InfoMessage(workout_type,
                           duration, distance,
                           speed, calories)


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        medium_speed = self.get_mean_speed()

        calories: float = (
                           (coeff_calorie_1 * medium_speed -
                           coeff_calorie_2) * self.weight /
                           self.M_IN_KM * self.duration * 60
                           )

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
        medium_speed = self.get_mean_speed()

        calories: float = (
                           (coeff_1 * self.weight +
                           (medium_speed**2 //
                            self.height) * coeff_2 *
                            self.weight) * self.duration * 60
                            )

        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool
        self.LEN_STEP = 1.38

    def get_mean_speed(self) -> float:
        speed: float = (
                        self.lenght_pool * self.count_pool /
                        self.M_IN_KM / self.duration
                        )

        return speed

    def get_spent_calories(self) -> float:
        coeff_1: float = 1.1
        coeff_2: int = 2
        medium_speed: float = self.get_mean_speed()

        calories: float = (
                           (medium_speed + coeff_1) *
                            coeff_2 * self.weight
                            )

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
    info = training.show_training_info(workout_type)
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