

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65  # Длина шага
    M_IN_KM: int = 1000  # Постоянная для перевода м. в км.

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
        dist = (self.action * self.LEN_STEP / self.M_IN_KM)
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
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
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight)
        self.training_type = 'RUN'

    def get_spent_calories(self) -> float:
        calor_run = ((self.coeff_calorie_1 * self.get_mean_speed()
                      - self.coeff_calorie_2) * self.weight
                      / self.M_IN_KM * self.duration * 60)
        return calor_run


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight
                         )
        self.height = height
        self.training_type = 'WLK'

    def get_spent_calories(self) -> float:
        calor_walk = ((self.coeff_calorie_1 * self.weight
                       + (self.get_mean_speed()**2 // self.height)
                       * self.coeff_calorie_2 * self.weight)
                       * self.duration * 60)
        return calor_walk


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38  # Длина гребка
    coef_calorie_1: float = 1.1
    coef_calorie_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action,
                         duration,
                         weight
                         )
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.training_type = 'SWM'

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calor_swim = ((self.get_mean_speed() + self.coef_calorie_1)
                       * self.coef_calorie_2 * self.weight)
        return calor_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings: dict = {'SWM': Swimming,
                       'RUN': Running,
                       'WLK': SportsWalking
                       }
    if workout_type in trainings:
        return trainings[workout_type](*data)


def main(training: Training) -> str:
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
