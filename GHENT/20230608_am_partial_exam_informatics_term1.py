# Programming assignment 1: The Feynman ciphers (4 points)------------------------------------------------------------------------------------------------------------------------------------

s = int(input())    # 입력받은 문자열을 끊어 읽을 수
t = int(input())    # 입력받은 문자열의 수

sentence = ''
for _ in range(t):
    sentence += input()

sentence = sentence[::-1]

for i in range(s):
    for j in range(i,len(sentence),s):
        print(sentence[j],end = '')

# THEREISNOAUTHORITYWHODECIDESWHATISAGOODIDEA

# Programming assignment 2: Platypus (5 points)------------------------------------------------------------------------------------------------------------------------------------
from fractions import Fraction

def word_fraction(word,frac):
    result = ""
    a, b = frac.numerator, frac.denominator
    a *= len(word) // b
    if a < 0:
        result += word[a:]
    else:
        result += word[:a]
    return result

def combine(words, fracs):
    result = ""
    for i in range(len(words)):
        result += word_fraction(words[i], fracs[i])
    return result

def decompose(query):
    parse = query.replace('What is ','').replace(',','').replace('and ','').replace('?','')
    parse = parse.split()
    result1 = []
    result2 = []
    for i in range(0,len(parse),2):
        frac_a,frac_b = map(int,parse[i].split('/'))
        result2.append(Fraction(frac_a,frac_b))
        result1.append(parse[i+1])
    return result1,result2
def answer(query):
    words, fracs = decompose(query)
    return combine(words,fracs)
if __name__ == "__main__":
    print(word_fraction("wallaby", Fraction(4,7)))
    print(combine(['wallaby', 'parakeet', 'perch'], [Fraction(4, 7), Fraction(1, 4), Fraction(3, 5)]))
    'wallpaper'

    print(combine(['ALPACA', 'PARTRIDGE'], [Fraction(-1, 3), Fraction(-7, 9)]))
    'CARTRIDGE'

    print(combine(['Manatee', 'cheetah', 'hamster'], [Fraction(3, 7), Fraction(3, 7), Fraction(-4, 7)]))
    'Manchester'
    #
    print(decompose('What is 4/7 wallaby, 1/4 parakeet and 3/5 perch?'))
    (['wallaby', 'parakeet', 'perch'], [Fraction(4, 7), Fraction(1, 4), Fraction(3, 5)])

    print(decompose('What is -1/3 ALPACA and -7/9 PARTRIDGE?'))
    (['ALPACA', 'PARTRIDGE'], [Fraction(-1, 3), Fraction(-7, 9)])

    print(decompose('What is 3/7 Manatee, 3/7 cheetah and -4/7 hamster?'))
    (['Manatee', 'cheetah', 'hamster'], [Fraction(3, 7), Fraction(3, 7), Fraction(-4, 7)])

    print(answer('What is 4/7 wallaby, 1/4 parakeet and 3/5 perch?'))
    'wallpaper'

    print(answer('What is -1/3 ALPACA and -7/9 PARTRIDGE?'))
    'CARTRIDGE'

    print(answer('What is 3/7 Manatee, 3/7 cheetah and -4/7 hamster?'))
    'Manchester'


# Programming assignment 3: Color nonogram (6 points) -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def hint(string):
    # 함수 hint를 작성하여 ASCII 그림의 행/열(str)을 입력으로 받습니다. 이 함수는 주어진 행/열에 대한 힌트를 반환해야 합니다.
    #
    result = []
    i = 0
    while i < len(string):
        j = i+1
        while j < len(string) and string[i] == string[j]:
            j += 1
        if string[i] != ' ':
            result.append(str(j-i)+string[i])
        i = j
    return result

def row_hints(str_list:list):
    # 함수 row_hints를 작성하여 ASCII 그림을 나타내는 문자열 목록(list)을 입력으로 받습니다.
    # 이 함수는 ASCII 그림의 모든 행에 대한 힌트(위에서 아래로 나열)를 포함한 리스트(list)를 반환해야 합니다.
    result = []
    for i in range(len(str_list)):
        result.append(hint(str_list[i]))
    return result

def column_hints(str_list):
    # 함수 column_hints를 작성하여 ASCII 그림을 나타내는 문자열 목록(list)을 입력으로 받습니다.
    # 이 함수는 ASCII 그림의 모든 열에 대한 힌트(왼쪽에서 오른쪽으로 나열)를 포함한 리스트(list)를 반환해야 합니다.
    result = []
    for i in range(len(str_list[0])):
        new_str = ""
        for j in range(len(str_list)):
            new_str += str_list[j][i]
        result.append(hint(new_str))
    return result
    # pass



def issolution():
    # 함수 issolution을 작성하여 세 가지 인수를 입력으로 받습니다: 𝑖) ASCII 그림을 나타내는 문자열 목록(list), 𝑖𝑖)
    # 노노그램의 모든 행에 대한 힌트 목록(list)(위에서 아래로 나열) 및 𝑖𝑖𝑖) 노노그램의 모든 열에 대한 힌트 목록(list)(왼쪽에서 오른쪽으로 나열).
    # 이 함수는 주어진 ASCII 그림이 주어진 힌트를 가진 노노그램의 솔루션인지 여부를 나타내는 부울 값(bool)을 반환해야 합니다.

    pass

def compare(result,answer):
    print(f"결과값의 길이: {len(result)}, 정답의 길이: {len(answer)}")
    if len(result) != len(answer): return
    for i in range(len(result)):
        if len(result[i]) != len(answer[i]):
            print(f"result[{i}]: {result[i]}, len: {len(result[i])}")
            print(f"answer[{i}]: {answer[i]}, len: {len(answer[i])}")
        for j in range(min(len(result[i]), len(answer[i]))):
            if result[i][j] != answer[i][j]:
                print(f"result[{i}]: {result[i]}")
                print(f"answer[{i}]: {answer[i]}")
                print(f"result[{i}][{j}]: {result[i][j]}, answer[{i}][{j}]: {answer[i][j]}\n")




if __name__ == "__main__":
    print(hint('ABBCCCDDDDEEEFFG'))
    ['1A', '2B', '3C', '4D', '3E', '2F', '1G']

    print(hint(' A  BB   CCC    DDDD    EEE   FF  G '))
    ['1A', '2B', '3C', '4D', '3E', '2F', '1G']

    print(hint('''          .      . "####"###"####"  .                       '''))
    ['1.', '1.', '1"', '4#', '1"', '3#', '1"', '4#', '1"', '1.']

    print(hint('.. .. ..................O000O........................ ......'))
    ['2.', '2.', '18.', '1O', '30', '1O', '24.', '6.']

    nonogram = ['          .     .  .      +     .      .          .         ',
                '     .       .      .     #       .           .             ',
                '        .      .         ###            .      .      .     ',
                '      .      .   "#:. .:##"##:. .:#"  .      .              ',
                '          .      . "####"###"####"  .                       ',
                '       .     "#:.    .:#"###"#:.    .:#"  .        .       .',
                '  .             "#########"#########"        .        .     ',
                '        .    "#:.  "####"###"####"  .:#"   .       .        ',
                '     .     .  "#######""##"##""#######"                  .  ',
                '                ."##"#####"#####"##"           .      .     ',
                '    .   "#:. ...  .:##"###"###"##:.  ... .:#"     .        .',
                '      .     "#######"##"#####"##"#######"      .     .      ',
                '    .    .     "#####""#######""#####"    .      .          ',
                '            .     "      000      "    .     .              ',
                '       .         .   .   000     .        .       .         ',
                '.. .. ..................O000O........................ ......']
    rows = row_hints(nonogram)
    # print(rows)
    answer_rows=[['1.', '1.', '1.', '1+', '1.', '1.', '1.'], ['1.', '1.', '1.', '1#', '1.', '1.'], ['1.', '1.', '3#', '1.', '1.', '1.'], ['1.', '1.', '1"', '1#', '1:', '1.', '1.', '1:', '2#','1"', '2#', '1:', '1.', '1.', '1:', '1#', '1"', '1.', '1.'], ['1.', '1.', '1"', '4#', '1"', '3#', '1"', '4#', '1"', '1.'], ['1.', '1"', '1#', '1:', '1.', '1.', '1:', '1#', '1"', '3#', '1"', '1#', '1:', '1.', '1.', '1:', '1#', '1"', '1.', '1.', '1.'], ['1.', '1"','9#', '1"', '9#', '1"', '1.', '1.'], ['1.', '1"', '1#', '1:', '1.', '1"', '4#', '1"', '3#', '1"', '4#', '1"', '1.', '1:', '1#', '1"', '1.', '1.'], ['1.', '1.', '1"', '7#', '2"', '2#', '1"', '2#', '2"', '7#', '1"', '1.'], ['1.', '1"', '2#', '1"', '5#', '1"', '5#','1"', '2#', '1"', '1.', '1.'], ['1.', '1"', '1#', '1:', '1.', '3.', '1.', '1:', '2#', '1"', '3#', '1"', '3#', '1"', '2#', '1:', '1.', '3.', '1.', '1:', '1#', '1"', '1.'], ['1.', '1"', '7#', '1"', '2#', '1"', '5#', '1"', '2#', '1"', '7#', '1"', '1.', '1.'], ['1.','1.', '1"', '5#', '2"', '7#', '2"', '5#', '1"', '1.', '1.'], ['1.', '1"', '30', '1"', '1.', '1.'], ['1.', '1.', '1.', '30', '1.', '1.', '1.'], ['2.', '2.', '18.', '1O', '30', '1O', '24.', '6.']]

    # compare(rows,answer_rows)
    cols = column_hints(nonogram)
    print(cols)
    answer_cols =
    compare(cols,answer_cols)
    # print(issolution(nonogram, rows, cols))
    # True
