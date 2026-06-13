import copy
from abc import ABC, abstractmethod
from math import sqrt


class MovementIter(ABC):

    SQRT_OF_2 = sqrt(2)

    def __init__(self):
        self._location: tuple[int, int]
        self._finite: bool


    def __iter__(self):
        return copy.deepcopy(self)

    def __call__(self, startX: int, startY: int):
        self._location = (startX, startY)
        return self

    # returns coordinates of next square
    @abstractmethod
    def __next__(self):
        return (0, 0)

    def is_finite(self):
        return self._finite

    def jumps_over(self):
        return True

    def _vector_dist(self, vec1: tuple[int, int], vec2: tuple[int, int]):
        return sqrt((vec1[0] - vec2[0]) ** 2 + (vec1[1] - vec2[1]) ** 2)




# outputs consecutive moves in the direction of vector
class MoveVectorDir(MovementIter):
    def __init__(self, vector: tuple[int, int], jumps: bool = False):
        self.__vector = vector
        self.__jumps = jumps

        self._finite = False

    def __next__(self):
        old = self._location
        self._location = (self._location[0] + self.__vector[0], self._location[1] + self.__vector[1])

        return self._location

    def jumps_over(self):
        return self.__jumps




# outputs moves in the direction of each vector in vectors
class MoveVectorList(MovementIter):
    def __init__(self, vectors: list[tuple[int, int]]):
        self._finite = True

        self.__vectors = vectors
        self.__moves = 0

    def __next__(self):
        if self.__moves == len(self.__vectors):
            raise StopIteration

        move = self.__vectors[self.__moves]
        newLocation = (self._location[0] + move[0], self._location[1] + move[1])
        self.__moves += 1

        return newLocation

# outputs moves in every transformation of  vector
# just horsin' around
class MoveVectorSymmetrical(MovementIter):
    def __init__(self, vector: tuple[int, int]):
        x = vector[0]
        y = vector[1]

        moves = [
            (x, y),
            (-x, y),
            (x, -y),
            (-x, -y),
            (y, x),
            (y, -x),
            (-y, x),
            (-y, -x)
        ]
        moves = list(set(moves))

        self.__insideIter = MoveVectorList(moves)

        self._finite = True


    def __iter__(self):
        return iter(self.__insideIter)

    def __call__(self, startX: int, startY: int):
        self._location = (startX, startY)
        self.__insideIter(startX, startY)
        return self


    def __next__(self):
        try:
            return next(self.__insideIter)
        except StopIteration:
            raise StopIteration







if __name__ == '__main__':
    horsie = MoveVectorSymmetrical((3, 1))
    it = iter(horsie)(4, 4)

    for i in it:
        print(i)