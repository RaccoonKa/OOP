from typing import Union, Iterable
import math


class Point2d:
    WIDTH = 1920
    HEIGHT = 1080

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: int) -> None:
        if not 0 <= value <= self.WIDTH:
            raise ValueError(f"x must be between 0 and {self.WIDTH}")
        self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: int) -> None:
        if not 0 <= value <= self.HEIGHT:
            raise ValueError(f"y must be between 0 and {self.HEIGHT}")
        self._y = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point2d):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"Point2d(x={self.x}, y={self.y})"

    def __repr__(self) -> str:
        return f"Point2d(x={self.x}, y={self.y})"


class Vector2d:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @classmethod
    def from_points(cls, start: Point2d, end: Point2d) -> 'Vector2d':
        return cls(end.x - start.x, end.y - start.y)

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value: Union[int, float]) -> None:
        self._x = int(round(value)) if isinstance(value, float) else int(value)

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value: Union[int, float]) -> None:
        self._y = int(round(value)) if isinstance(value, float) else int(value)

    def __getitem__(self, index: int) -> int:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("Vector2d index out of range")

    def __setitem__(self, index: int, value: int) -> None:
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Vector2d index out of range")

    def __iter__(self) -> Iterable[int]:
        yield self.x
        yield self.y

    def __len__(self) -> int:
        return 2

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2d):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return f"Vector2d(x={self.x}, y={self.y})"

    def __repr__(self) -> str:
        return f"Vector2d(x={self.x}, y={self.y})"

    def __abs__(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other: 'Vector2d') -> 'Vector2d':
        if not isinstance(other, Vector2d):
            raise TypeError("Can only add Vector2d to Vector2d")
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector2d') -> 'Vector2d':
        if not isinstance(other, Vector2d):
            raise TypeError("Can only subtract Vector2d from Vector2d")
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: Union[int, float]) -> 'Vector2d':
        if not isinstance(scalar, (int, float)):
            raise TypeError("Can only multiply Vector2d by scalar")
        return Vector2d(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: Union[int, float]) -> 'Vector2d':
        return self.__mul__(scalar)

    def __truediv__(self, scalar: Union[int, float]) -> 'Vector2d':
        if not isinstance(scalar, (int, float)):
            raise TypeError("Can only divide Vector2d by scalar")
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide Vector2d by zero")
        return Vector2d(self.x / scalar, self.y / scalar)

    def dot(self, other: 'Vector2d') -> Union[int, float]:
        if not isinstance(other, Vector2d):
            raise TypeError("Dot product can only be calculated for Vector2d")
        return self.x * other.x + self.y * other.y

    @staticmethod
    def dot_product(v1: 'Vector2d', v2: 'Vector2d') -> Union[int, float]:
        if not isinstance(v1, Vector2d) or not isinstance(v2, Vector2d):
            raise TypeError("Dot product can only be calculated for Vector2d")
        return v1.x * v2.x + v1.y * v2.y

    def cross(self, other: 'Vector2d') -> Union[int, float]:
        if not isinstance(other, Vector2d):
            raise TypeError("Cross product can only be calculated for Vector2d")
        return self.x * other.y - self.y * other.x

    @staticmethod
    def cross_product(v1: 'Vector2d', v2: 'Vector2d') -> Union[int, float]:
        if not isinstance(v1, Vector2d) or not isinstance(v2, Vector2d):
            raise TypeError("Cross product can only be calculated for Vector2d")
        return v1.x * v2.y - v1.y * v2.x

    @staticmethod
    def triple_product(v1: 'Vector2d', v2: 'Vector2d', v3: 'Vector2d') -> Union[int, float]:
        if not all(isinstance(v, Vector2d) for v in (v1, v2, v3)):
            raise TypeError("Triple product can only be calculated for Vector2d")
        return v1.dot(Vector2d.cross_product(v2, v3))


def demonstrate_functionality():
    print("=== Демонстрация работы Point2d ===")
    try:
        p1 = Point2d(100, 200)
        p2 = Point2d(300, 400)
        p3 = Point2d(100, 200)

        print(f"p1: {p1}")
        print(f"p2: {p2}")
        print(f"p3: {p3}")
        print(f"p1 == p2: {p1 == p2}")
        print(f"p1 == p3: {p1 == p3}")

        # Демонстрация проверки границ
        try:
            bad_point = Point2d(-10, 100)
        except ValueError as e:
            print(f"Ошибка создания точки: {e}")

        try:
            bad_point = Point2d(100, Point2d.HEIGHT + 1)
        except ValueError as e:
            print(f"Ошибка создания точки: {e}")

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

    print("\n=== Демонстрация работы Vector2d ===")
    try:
        v1 = Vector2d(10, 20)
        v2 = Vector2d(30, 40)
        v3 = Vector2d.from_points(p1, p2)

        print(f"v1: {v1}")
        print(f"v2: {v2}")
        print(f"v3 (из p1 и p2): {v3}")

        # Доступ по индексу
        print(f"\nДоступ по индексу:")
        print(f"v1[0]: {v1[0]}, v1[1]: {v1[1]}")
        v1[0] = 15
        print(f"После изменения: v1[0] = {v1[0]}")

        # Итерация
        print("\nИтерация по компонентам:")
        print("Компоненты v2:", end=" ")
        for component in v2:
            print(component, end=" ")
        print()

        # Математические операции
        print("\nМатематические операции:")
        print(f"v1 + v2: {v1 + v2}")
        print(f"v2 - v1: {v2 - v1}")
        print(f"v1 * 3: {v1 * 3}")
        print(f"2.5 * v1: {2.5 * v1}")
        print(f"v2 / 2: {v2 / 2}")
        print(f"Модуль v1: {abs(v1):.2f}")

        # Векторные произведения
        print("\nВекторные произведения:")
        print(f"Скалярное (v1·v2): {v1.dot(v2)}")
        print(f"Скалярное (статический метод): {Vector2d.dot_product(v1, v2)}")
        print(f"Векторное (v1×v2): {v1.cross(v2)}")
        print(f"Векторное (статический метод): {Vector2d.cross_product(v1, v2)}")
        print(f"Смешанное произведение (v1·(v2×v3)): {Vector2d.triple_product(v1, v2, v3)}")

    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    demonstrate_functionality()
