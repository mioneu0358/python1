# 과제
# 퀼트의 패턴을 표현할 수 있는 Quilt 클래스를 정의하십시오. 각 퀼트는 그리드 형식의 여러 문자로 구성된 표현에 해당합니다.
# 예를 들어, 퀼트는 다음과 같이 보일 수 있습니다:
#  //-\
#  ++||
# 이 클래스는 다음 메서드를 구현해야 합니다:
# 초기화 메서드 __init__은 세 개의 인수를 받아야 합니다: i) 행의 수, ii) 열의 수, iii) 문자열.
# 퀼트는 주어진 문자열의 연속적인 문자로 왼쪽에서 오른쪽, 위에서 아래로 채워집니다. 이 문자열은 퀼트가 구성하는 행의 수와 열의 수의 곱과 동일한 문자를 가져야 합니다.
# 이러한 조건이 충족되지 않으면 invalid configuration 텍스트와 함께 AssertionError를 발생시켜야 합니다.
# 퀼트는 유효한 문자만으로 구성될 수 있으며, 초기화 메서드는 이러한 경우에도 invalid configuration 텍스트와 함께 AssertionError를 발생시켜야 합니다.
# 유효한 문자란 90도 회전시킬 때 ASCII 문자 집합으로 표현할 수 있는 기호를 의미합니다: \,/,+,*,-,|,o,x.

# 메서드 __str__는 퀼트의 문자열 표현을 출력합니다. 이 문자열 표현은 각 줄이 행의 수만큼 존재하며, 각 줄은 열의 수만큼의 문자를 가집니다.
# 문자열 표현 자체는 개행 문자로 끝나지 않습니다.

# 메서드 __repr__는 퀼트의 문자열 표현을 출력합니다. 이 문자열 표현은 동일한 상태를 가진 Quilt 클래스의 새 객체를 만드는 Python 표현식처럼 읽힙니다.

# 메서드 rotate는 호출된 객체의 패턴에 대해 시계 방향으로 90도 회전한 패턴을 가진 새로운 Quilt 객체를 반환합니다.

# 메서드 __add__는 두 퀼트를 "봉합"할 수 있도록 합니다. 높이가 동일한 퀼트만 봉합할 수 있습니다. 두 퀼트의 높이가 동일하지 않으면
# quilts do not have equal height 텍스트와 함께 AssertionError를 발생시켜야 합니다. 그렇지 않으면, 두 객체의 패턴을 봉합한 패턴으로 구성된
# 새로운 Quilt 객체를 출력해야 합니다.

# Quilt 클래스의 객체는 변경 불가능(immutable)해야 합니다. 다른 메서드는 Quilt 클래스 객체의 내부 상태를 조정할 수 없습니다.
# 즉, 초기화된 후 객체의 내부 상태는 변경될 수 없으며, 새로운 객체만 만들 수 있습니다.
class Quilt:
    def __init__(self,row,col,string):
        if row * col != len(string):    # 주어진 행의길이 x 열의길이가 문자열의길이와 다르면 에러발생
            raise AssertionError("invalid configuration")
        test_string = string    # 'a'
        valid_string = "\/+*-|ox"

        for va in valid_string:
            test_string = test_string.replace(va,'')
        if test_string:
            raise AssertionError("invalid configuration")

        self.row = row
        self.col = col
        self.string = string

        self.data = [[''] * self.col for _ in range(self.row)]  # 2차원리스트를 만들어서 표현형태로 저장
        for i in range(self.row):
            for j in range(self.col):
                self.data[i][j] = self.string[i*self.col + j]


    def __repr__(self):
        return f"Quilt({self.row}, {self.col}, '{self.string}')"

    def __str__(self):
        result = ""
        # self.data를 이미 표현식대로 저장해놨으니 한 행씩 가져와 문자열로 만든후 줄바꿈문자와 함께 이어주면 됩니다.
        for i in range(self.row):
            result += ''.join(self.data[i]) + '\n'
        return result[:-1]

    def __add__(self, other):
        if self.row != other.row:   # 행의 길이가 다르면 에러발생
            raise AssertionError("quilts do not have equal height")
        new_r = self.row
        new_c = self.col + other.col

        new_data = ""
        for i in range(new_r):
            new_data += ''.join(self.data[i])   # __add__와 같은 방식
            new_data += ''.join(other.data[i])

        result = Quilt(new_r ,new_c ,new_data)
        return result

    def rotate(self):
        new_data = ""
        change = {'/':'\\','-':'|', '\\':'/','|':'-','+':'+'}   # 돌렸을 때 치환될 문자

        # 시계방향으로 90도 회전이기 때문에 불러오는 인덱스의 순서가 바뀝니다.
        for j in range(self.col):
            for i in range(self.row-1,-1,-1):
                new_data += change[self.data[i][j]]
        result = Quilt(self.col,self.row, new_data)
        return result

if __name__ == "__main__":
    quilt = Quilt(2, 2, '//++')
    print(quilt)
    # //
    # ++
    quilt += Quilt(2, 2, '-\\||')
    print(quilt)
    # // - \
    # ++ | |
    print(repr(quilt))
    Quilt(2, 4, '//-\\++||')
    quilt = quilt.rotate()
    print(quilt)
    # + \
    # + \
    # - |
    # - /
    print(repr(quilt))
    Quilt(4, 2, '+\\+\\-|-/')
    # quilt += Quilt(2, 2, '-\\||')
    # Traceback(most recent call last):
    # AssertionError: quilts do not have an equal height
    quilt = quilt.rotate()
    print(quilt)
    # | | ++
    # \- //
    # Quilt(2, 3, '++++')
    # # Traceback(most recent call last):
    # # AssertionError: invalid configuration
    # Quilt(2, 3, 'oxooXo')
    # # Traceback(most recent call last):
    # # AssertionError: invalid configuration
