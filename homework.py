from typing import ClassVar
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
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
                f'Потрачено ккал: {self.calories:.3f}.'
                )


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65  # Длина шага
    M_IN_KM: ClassVar[float] = 1000  # Постоянная для перевода м. в км.
    action: int
    duration: float
    weight: float

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
        NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: ClassVar[float] = 18  # Коэффициент по бегу №1
    COEFF_CALORIE_2: ClassVar[float] = 20  # Коэффициент по бегу №2

    def get_spent_calories(self) -> float:
        calor_run = ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                      - self.COEFF_CALORIE_2) * self.weight
                     / self.M_IN_KM * self.duration * 60)
        return calor_run


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_1: ClassVar[float] = 0.035  # Коэффициент по ходьбе №1
    COEFF_CALORIE_2: ClassVar[float] = 0.029  # Коэффициент по ходьбе №2
    COEFF_HOUR: ClassVar[float] = 60  # Коэффициент перевода чамы в минуты
    height: float

    def get_spent_calories(self) -> float:
        calor_walk = ((self.COEFF_CALORIE_1 * self.weight
                       + (self.get_mean_speed()**2 // self.height)
                       * self.COEFF_CALORIE_2 * self.weight)
                      * self.duration * self.COEFF_HOUR)
        return calor_walk


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38  # Длина гребка
    COEF_CALORIE_1: ClassVar[float] = 1.1  # Коэффициент по плаванию №1
    COEF_CALORIE_2: ClassVar[float] = 2  # Коэффициент по плаванию №2
    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        speed = (self.length_pool * self.count_pool
                 / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        calor_swim = ((self.get_mean_speed() + self.COEF_CALORIE_1)
                      * self.COEF_CALORIE_2 * self.weight)
        return calor_swim


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in trainings:
        raise ValueError('Неизвестный тип тренировки')
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
