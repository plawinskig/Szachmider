from abc import ABC, abstractmethod
from math import sqrt


class MovementIter(ABC):

    SQRT_OF_2 = sqrt(2)

    def __init__(self):
        self._location: tuple[int, int]
        self._finite: bool


    def __iter__(self):
        return self

    def __call__(self, startX: int, startY: int):
        self._location = (startX, startY)
        return self

    # returns coordinates of next square and if the move is a jump
    @abstractmethod
    def __next__(self):
        return (0, 0), False

    def is_finite(self):
        return self._finite

    def vector_dist(self, vec1: tuple[int, int], vec2: tuple[int, int]):
        return sqrt((vec1[0] - vec2[0]) ** 2 + (vec1[1] - vec2[1]) ** 2)


# outpus consecutive moves in one direction
class MoveVectorDir(MovementIter):
    def __init__(self, vector: tuple[int, int]):
        self.__vector = vector
        self.__jump = self.vector_dist((0, 0), self._location) > MovementIter.SQRT_OF_2
        self._finite = False

    def __next__(self):
        old = self._location
        self._location = (self._location[0] + self.__vector[0], self._location[1] + self.__vector[1])

        return self._location, self.__jump


class MoveVectorList(MovementIter):
    def __init__(self, vectors: list[tuple[int, int]]):
        self._finite = True

        self.__vectors = vectors
        self.__moves = 0

    def __next__(self):
        if self.__moves == len(self.__vectors):
            raise StopIteration

        move = self





if __name__ == '__main__':
    move = MoveVectorInf((2, 1))
    newMOve = move(2, 3)
    for i in range(5):
        print(next(newMOve))
