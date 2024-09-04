class Centrifuge:
    # Centrifuge 클래스를 정의하여 시험관이 채워진 구멍을 가진 원심분리기를 나타내십시오.
    # 새로운 원심분리기(Centrifuge)를 생성할 때 두 개의 인자를 전달해야 합니다:
    # 𝑖) 구멍의 수 𝑛과 𝑖𝑖) 시험관이 채워진 구멍을 설명하는 구성.
    def __init__(self, n, info):
        self.n = n
        self.info = list(info)
        pass

    # 내장 함수 repr에 원심분리기(Centrifuge)가 전달되면, repr 함수에 전달된 원심분리기와 같은 수의 구멍과 같은 시험관이 채워진 구멍 구성을 가진
    # 새로운 원심분리기(Centrifuge)를 생성하는 Python 표현식(str)을 반환해야 하며, 구성은 오름차순으로 정렬된 숫자 리스트로 표현되어야 합니다.
    def __repr__(self):
        return f"Centrifuge({self.n},{self.info})"

    # 시계 방향 또는 반시계 방향으로 회전하는 rotate 메소드(기본값: False). 회전이 시계 방향(True) 또는 반시계 방향(False)인지
    # 나타내는 부울 값(bool)을 가질 수 있는 선택적 매개변수를 가집니다. 이 메소드는 원심분리기 𝑐의 모든 시험관이 시계 방향 또는 반시계 방향으로
    # 한 번의 회전 단계를 진행하도록 설정해야 하며, 원심분리기 𝑐에 대한 참조를 반환해야 합니다.
    # print(f"rotate: {self.test_tube} => ", end='')
    def rotate(self,clockwise = False):
        
        return self


    # mirror 메소드는 인자를 받지 않습니다. 이 메소드는 원심분리기 𝑐의 시험관 배치를 𝑋 축을 기준으로 대칭 시키고, 원심분리기 𝑐에 대한 참조를 반환해야 합니다.
    # 힌트: mirror 연산을 더 잘 이해하기 위해 종이에 예제를 작성해 보는 것이 도움이 될 수 있습니다.
    # print(f"mirror: {self.test_tube} => ",end ='')
    def mirror(self):
        pass

    # 두 원심분리기 𝑐와 𝑑(Centrifuge)가 동일한 경우를 확인하기 위해 == 연산자를 사용할 수 있어야 합니다. 이는 두 원심분리기가 같은 수의 구멍을 가지고,
    # 하나의 원심분리기가 몇 번의 회전 단계를 거쳐 두 원심분리기가 동일한 구멍이 채워진 상태를 갖는 경우, (가능하면 한 원심분리기를 대칭한 후) 성립합니다.
    # == 연산자는 원심분리기 𝑐와 𝑑의 상태를 변경하지 않아야 합니다.
    def __eq__(self, other):
        pass



    # += 연산자를 사용하여 (𝑐 += 𝑑) 원심분리기 𝑐(Centrifuge)에서 원심분리기 𝑑(Centrifuge)에서 채워진 모든 구멍을 채울 수 있어야 합니다.
    # 이는 원심분리기 𝑑의 상태를 변경하지 않아야 합니다. 만약 원심분리기 𝑐와 𝑑가 같은 수의 구멍을 가지고 있지 않거나 원심분리기 𝑑에서 채워진 구멍이 원심분리기 𝑐에서도 채워져 있는 경우,
    # 원심분리기 𝑐의 상태는 변경되지 않아야 하며, AssertionError가 "could not fill holes" 메시지와 함께 발생해야 합니다.

    def __iadd__(self, other):
        pass

    # -= 연산자를 사용하여 (𝑐 -= 𝑑) 원심분리기 𝑐(Centrifuge)에서 원심분리기 𝑑(Centrifuge)에서 채워진 모든 구멍을 비울 수 있어야 합니다.
    # 이는 원심분리기 𝑑의 상태를 변경하지 않아야 합니다. 만약 원심분리기 𝑐와 𝑑가 같은 수의 구멍을 가지고 있지 않거나 원심분리기 𝑑에서 채워진 구멍이 원심분리기 𝑐에서 비어 있는 경우,
    # 원심분리기 𝑐의 상태는 변경되지 않아야 하며, AssertionError가 "could not empty holes" 메시지와 함께 발생해야 합니다.
    def __isub__(self, other):
        pass


if __name__ == "__main__":
    centrifuge = Centrifuge(6, {4, 1, 3, 0})
    print(repr(centrifuge))
    Centrifuge(6, [0, 1, 3, 4])

    print(centrifuge.rotate())
    Centrifuge(6, [1, 2, 4, 5])

    print(centrifuge.rotate(clockwise=True))
    Centrifuge(6, [0, 1, 3, 4])

    print(centrifuge.mirror())
    Centrifuge(6, [0, 2, 3, 5])

    print(centrifuge.mirror())
    Centrifuge(6, [0, 1, 3, 4])


    centrifuge = Centrifuge(6, [2, 0, 5])
    print(centrifuge == Centrifuge(6, [2, 4, 5]))
    True

    print(centrifuge == Centrifuge(6, [3, 4, 5]))
    False

    print(centrifuge)
    Centrifuge(6, [0, 2, 5])

    print(centrifuge.rotate().rotate().mirror())
    Centrifuge(6, [2, 4, 5])

    print(centrifuge.mirror().rotate(True).rotate(True))
    Centrifuge(6, [0, 2, 5])

    centrifuge += Centrifuge(6, {1, 4})
    print(centrifuge)
    Centrifuge(6, [0, 1, 2, 4, 5])

    # centrifuge += Centrifuge(6, [1, 4, 2])
    # Traceback(mostrecentcalllast):
    # AssertionError: couldnot fillholes
    centrifuge -= Centrifuge(6, {1, 4})
    print(centrifuge)
    Centrifuge(6, [0, 2, 5])

    centrifuge -= Centrifuge(6, (1, 5))
    # Traceback(mostrecentcalllast):
    # AssertionError: could not empty holes
