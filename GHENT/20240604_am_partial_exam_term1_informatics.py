# Programming assignment 1: Palindromic numbers (4 points) -----------------------------------------------------------------------------------------------

nums = input().replace(',','').split()  # 안에 ','외에도 공백이 있기 때문에 먼저 ','를 없애고 공백으로 분리 합니다.
print(nums)
result = ""
for i in range(len(nums)):        # 그 다음 원소값들을 하나씩 불러와서 확인하는 작업을 가집니다.
    if nums[i].isdigit():         # 우선 숫자로만 이루어진 값인지 아닌지를 판단합니다. 그래야 int()를 사용할 수 있으니까요.
        binary = bin(int(nums[i]))[2:]
        print(nums[i],binary)
        if nums[i] == nums[i][::-1] and binary == binary[::-1]:# 정수로 변경한 값이 짝수라면 False를
            result += "True"
        else:
            result += 'False'        # 정수로 변경한 값이 홀수면 True
    else:
        result += 'None'            # 문자열이라면 None
    if i != len(nums)-1:         # 맨 마지막을 제외하고는 콤마 붙여줍니다.
        result += ', '
print(result)


# Programming assignment 2: Roof rambles (5 points) -----------------------------------------------------------------------------------------------------------

# 다음과 같은 조건을 가진 건물을 고려해 보세요. 건물의 평평한 정사각형 지붕은 크기가 3^k * 3^k미터입니다. (k∈N0) .
# 지붕의 면은 북-남 및 동-서 방향과 평행합니다. 지붕은 각각 길이가 1 미터인 정사각형 타일로 덮여 있습니다.
# 하나의 타일이 제거되어 지붕에 큰 구멍이 생겼습니다. 타일들은 지붕 위에 직사각형 그리드를 형성하며, 이들의 위치는 (x,y) 좌표로 지정할 수 있습니다.
# 남서쪽 모서리에 위치한 타일의 좌표는 (1,1)입니다. 첫 번째 좌표는 동쪽으로 증가하고, 두 번째 좌표는 북쪽으로 증가합니다.
# 잠자는 방랑자는 지붕 위를 돌아다니며, 현재 서 있는 타일에서 동쪽(E), 서쪽(W), 남쪽(S), 또는 북쪽(N)으로 이동합니다. 방랑자의 경로,
# 즉 "지붕 위의 방랑"은 남서쪽 모서리 타일에서 시작합니다. 그의 경로를 설명하는 문자열 dk 는 N, S, E, W 문자로 구성되며, 각각 북쪽, 남쪽, 동쪽, 서쪽으로의 이동을 나타냅니다.
# k = 1인경우 방랑자의 경로를 설명하는 문자열은 다음과 같습니다.
# d1 = EENNWSWN
# k = 2인경우 방랑자의 경로를 설명하는 문자열은 다음과 같습니다.
# d2 = 𝑁𝑁𝐸𝐸𝑆𝑊𝑆𝐸𝐸𝑁𝑁𝐸𝐸𝑆𝑊𝑆𝐸𝐸𝐸𝐸𝑁𝑁𝑊𝑆𝑊𝑁𝑁𝐸𝐸𝑁𝑁𝑊𝑆𝑊𝑁𝑁𝐸𝐸𝑁𝑁𝑊𝑆𝑊𝑁𝑊𝑊𝑊𝑆𝑆𝐸𝑁𝐸𝑆𝑆𝑆𝑆𝑊𝑊𝑁𝐸𝑁𝑊𝑊𝑆𝑆𝑊𝑊𝑁𝐸𝑁𝑊𝑁𝐸𝐸𝑁𝑁𝑊𝑆𝑊�
# 다음 그림은 방랑자가 3 × 3 크기의 지붕과 9 × 9 크기의 지붕을 어떻게 이동하는지를 보여줍니다. 오른쪽 그림에는 관찰이 시작되는 타일과 제거된 타일이 표시되어 있습니다.
# 방랑자는 관찰이 시작된 시점부터 20걸음 만에 구멍에 빠집니다.
# 일반적으로, k >= 1인경우,  3^(𝑘+1) × 3^(𝑘+1)인 지붕에서 방랑자의 경로는 다음과 같은 문자열로 설명됩니다 (읽기 편하도록 개별 방향이 빨간색으로 표시되었습니다):
# 𝑑𝑘+1 = 𝑝𝑎(𝑑𝑘)𝑬𝑝𝑎(𝑑𝑘)𝑬𝑑𝑘𝑵𝑑𝑘𝑵𝑑𝑘𝑾𝑝𝑐(𝑑𝑘)𝑺𝑝𝑏(𝑑𝑘)𝑾𝑝𝑏(𝑑𝑘)𝑵𝑑𝑘
#
# 여기서 함수 𝑝𝑎, 𝑝𝑏, 및 𝑝𝑐는 방향의 당므과 같은 순열(재배열)을 나타냅니다.
#   | 𝑬 | 𝑾 | 𝑵 | 𝑺 |
# 𝒑𝒂| 𝑁 | 𝑆 | 𝐸 | 𝑊 |
# 𝒑𝒃| 𝑆 | 𝑁 | 𝑊 | 𝐸 |
# 𝒑𝒄| 𝑊 | 𝐸 | 𝑆 | 𝑁 |

# 예를 들어, 𝑝𝑎(𝑆𝐸𝑁) = 𝑊𝑁𝐸, 𝑝𝑏(𝑆𝐸𝑁) = 𝐸𝑆𝑊, and 𝑝𝑐(𝑆𝐸𝑁) = 𝑁𝑊𝑆 입니다.
#
# 우리는 방랑자가 (sx,sy) 좌표에 있는 타일에 서 있는 순간부터 관찰을 시작합니다. 방랑자가 (gx,gy) 좌표에 있는 구멍에 빠지기까지 몇 걸음이 필요한지 계산해야 합니다.
# 이 질문에 답하기 위해 다음 절차를 따릅니다:
def permutation(dir_str, abc):
    # permutation 함수 작성: 이 함수는 두 개의 문자열 인수를 입력으로 받습니다. 첫 번째 인수는 방향을 포함하는 문자열입니다 (N, S, E, W만 포함).
    convert_dir = {'a': {'E':'N','W':'S','N':'E','S':'W'},
                   'b': {'E':'S','W':'N','N':'W','S':'E'},
                   'c': {'E':'W','W':'E','N':'S','S':'N'}}
    # 두 번째 인수는 문자 a, b 또는 c 중 하나여야 하며, 이 문자는 함수가 각각 𝑝𝑎, 𝑝𝑏 또는 𝑝𝑐의 결과를 반환하도록 합니다.
    result = ""
    for d in dir_str:
        result += convert_dir[abc][d]
    return result

def path(k):
    # path 함수 작성: 이 함수는 정수 k∈N0 를 입력으로 받습니다. 함수는 크기가 3^k * 3^k 인 지붕에서 방랑자가 따르는 방향 문자열을 반환해야 합니다.
    # 𝑑𝑘+1 = 𝑝𝑎(𝑑𝑘) 𝑬 𝑝𝑎(𝑑𝑘) 𝑬 𝑑𝑘 𝑵 𝑑𝑘 𝑵 𝑑𝑘 𝑾 𝑝𝑐(𝑑𝑘) 𝑺 𝑝𝑏(𝑑𝑘) 𝑾 𝑝𝑏(𝑑𝑘) 𝑵 𝑑𝑘
    if k == 0:
        return ""
    if k == 1:
        return "EENNWSWN"

    dk = path(k - 1)
    pa_dk = permutation(dk, 'a')
    pb_dk = permutation(dk, 'b')
    pc_dk = permutation(dk, 'c')

    return pa_dk + 'E' + pa_dk + 'E' +  dk + 'N' + dk + 'N' +  dk + 'W' + pc_dk + 'S' + pb_dk + 'W' + pb_dk + 'N' +  dk

def sleepwalker(k, sx, sy, gx, gy):
    # sleepwalker 함수 작성: 이 함수는 방랑자가 구멍에 빠지기까지 몇 걸음이 필요한지를 계산합니다. 이 함수는 다섯 개의 인수를 받습니다.
    # 첫 번째 인수는 지붕의 크기 3^k * 3^k 를 결정하는 정수 k∈N0  입니다. 다음 두 인수는 관찰이 시작되는 타일의 좌표 (sx,sy)입니다. 마지막 두 인수는 제거된 타일의 좌표 (gx,gy)입니다
    walker_path = path(k)
    x,y = 1,1
    cnt = 0
    flag = False
    offset = {'E': (1,0), 'W': (-1,0), 'N': (0,1), 'S': (0,-1)}
    for p in walker_path:
        if (x,y) == (sx,sy):
            flag = True
        x += offset[p][0]
        y += offset[p][1]
        if flag:
            cnt += 1
        if (x,y) == (gx,gy):
            return cnt



if __name__ == "__main__":
    print(permutation('SEN', 'a'))
    'WNE'
    print(permutation('SEN', 'b'))
    'ESW'
    print(permutation('SEN', 'c'))
    'NWS'

    print(path(1))
    'EENNWSWN'
    print(path(2))
    print(path(2) == "NNEESWSEENNEESWSEEEENNWSWNNEENNWSWNNEENNWSWNWWWSSENESSSSWWNENWWSSWWNENWNEENNWSWN")
    'NNEESWSEENNEESWSEEEENNWSWNNEENNWSWNNEENNWSWNWWWSSENESSSSWWNENWWSSWWNENWNEENNWSWN'
    print()

    route = path(3)
    print(route)
    r1 = '\\n'.join(route[x:x + 80] for x in range(0, len(route), 80))

    # EENNWSWNNEENNWSWNNNNEESWSEENNEESWSEENNEESWSESSSWWNENWWWWSSENESSWWSSENESENNEESWSE
    # EEENNWSWNNEENNWSWNNNNEESWSEENNEESWSEENNEESWSESSSWWNENWWWWSSENESSWWSSENESENNEESWS
    # EENNEESWSEENNEESWSEEEENNWSWNNEENNWSWNNEENNWSWNWWWSSENESSSSWWNENWWSSWWNENWNEENNWS
    # WNNNNEESWSEENNEESWSEEEENNWSWNNEENNWSWNNEENNWSWNWWWSSENESSSSWWNENWWSSWWNENWNEENNW
    # SWNNNNEESWSEENNEESWSEEEENNWSWNNEENNWSWNNEENNWSWNWWWSSENESSSSWWNENWWSSWWNENWNEENN
    # WSWNWSSWWNENWWSSWWNENWWWWSSENESSWWSSENESSWWSSENESEEENNWSWNNNNEESWSEENNEESWSESWWS
    # SENESSWWSSENESSWWSSENESSSSWWNENWWSSWWNENWWSSWWNENWNNNEESWSEEEENNWSWNNEENNWSWNWSS
    # WWNENWWWWSSENESSWWSSENESSSSWWNENWWSSWWNENWWSSWWNENWNNNEESWSEEEENNWSWNNEENNWSWNWS
    # SWWNENWNNNEESWSEENNEESWSEEEENNWSWNNEENNWSWNNEENNWSWNWWWSSENESSSSWWNENWWSSWWNENWN
    # EENNWSWN
    print(sleepwalker(2, 3, 2, 7, 2))
    20
    print(sleepwalker(2, 9, 6, 3, 7))
    43
    print(sleepwalker(3, 1, 1, 1, 27))
    728


# 프로그래밍 과제 3: 바이킹 암호 (6점)
# 발크누트(Valknut, 발음: 발크누트)는 각 기호(문자, 숫자, 구두점 또는 공백)가 두 개의 숫자(1-9) 조합으로 표현되는 암호입니다. 반대로 각 숫자 쌍(1-9)은 고유한 기호에 해당합니다. 숫자 0은 사용되지 않으므로 총 81개의 숫자 쌍이 있으며, 따라서 81개의 고유한 기호도 있습니다.
# 발크누트 암호의 키는 각 기호 α(문자, 숫자, 구두점 또는 공백)에 대응하는 숫자 쌍 𝑖𝑗(1 ≤ 𝑖,𝑗 ≤ 9)을 지정합니다. 이는 81개의 문자열 항목을 포함하는 목록을 통해 이루어질 수 있습니다. 각 문자열 항목에는 하나의 기호 α, 해당 숫자 𝑖, 그리고 숫자 𝑗가 탭으로 구분되어 포함됩니다.
# 발크누트 암호에서 탭은 절대 기호로 사용되지 않습니다. 예를 들어, 이러한 문자열 항목 리스트는 다음과 같을 수 있습니다:
# 위 키에 따르면 대문자 W는 숫자 쌍 26으로 표현되며, 소문자 e는 숫자 쌍 63, 숫자 4는 숫자 쌍 86, 공백은 숫자 쌍 68, 점(.)은 숫자 쌍 27로 표현됩니다.
# 숫자 쌍 𝑖𝑗(1 ≤ 𝑖,𝑗 ≤ 9)에 해당하는 기호 α를 빠르게 찾기 위해 발크누트 키의 81개 기호는 9 × 9 격자에 배치되며, 9개의 행과 9개의 열로 구성됩니다. 이 격자의 행은 위에서 아래로, 열은 왼쪽에서 오른쪽으로 각각 1부터 시작하여 번호가 매겨집니다. 그러면 숫자 쌍 𝑖𝑗은 해당 기호 α가 위치한 격자의 행 번호 𝑖와 열 번호 𝑗입니다. 예를 들어, 숫자 쌍 26은 두 번째 행, 여섯 번째 열에서 대문자 W를 찾을 수 있습니다. 마찬가지로, 숫자 쌍 63은 소문자 e에 해당하고, 숫자 쌍 86은 숫자 4에, 숫자 쌍 68은 공백(6행 8열의 빈 칸), 숫자 쌍 27은 점(.)에 해당합니다.
# 암호화 및 복호화
# 바이킹은 강한 전사로 잘 알려져 있지만, 매우 지적이며 영적 성향도 강했습니다. 그들의 중요한 교훈 중 하나는 다음과 같습니다:
# "늑대의 귀가 있는 곳에, 늑대의 이빨이 가까이 있다."
# 이 예제를 사용해 평문을 발크누트 암호로 인코딩하는 과정을 설명하겠습니다. 먼저 평문의 각 기호를 해당하는 숫자 쌍으로 변환합니다(W → 26, h → 38, e → 63, …, . → 27).
# 모든 숫자 쌍을 연결하면 다음과 같은 숫자열이 됩니다: 263863356368227752646124686325352468253563876822775264612468326363323868253563689463253527
# 이 숫자열의 각 숫자 쌍을 다시 기호로 변환하면 원래 평문으로 돌아갈 수 있습니다. 하지만 먼저 각 숫자 쌍의 두 숫자의 순서를 바꿉니다.
# 이렇게 하면 다음과 같은 숫자열이 됩니다: 628336533686227725461642863652534286525336788622772546164286233636238386525336864936525372
# 이 숫자열을 다시 기호로 변환하면 다음과 같은 암호문이 됩니다: -;7X74woa#pG47lXG4lX7:4woa#pG4R77R;4lX74&7lXS
# 복호화는 인코딩과 동일한 방법으로 매우 쉽게 수행할 수 있습니다.

# 함수 read_key를 작성하여 발크누트 키 𝓥를 나타내는 문자열 리스트를 입력으로 받습니다. 이 함수는 발크누트 키 𝓥의 사전(dictionary) 표현을 반환해야 합니다.
# 즉, 각 기호 α(str)를 숫자 쌍(𝑖,𝑗)과 연결하는 사전을 반환해야 합니다. 여기서 𝑖와 𝑗는 해당 기호 α에 대응하는 숫자 쌍(1 ≤ 𝑖,𝑗 ≤ 9)을 나타냅니다.
def read_key(V):
    result = {}
    for v in V:
        k,x,y = v.split(' ')
        k = k or ' '
        result[k] = (int(x),int(y))
    return result

# 함수 symbols2digits를 작성하여 두 가지 인수를 입력으로 받습니다: i) 기호의 시퀀스 𝑠(str)와 ii) 발크누트 키 𝒱의 사전 표현(dict).
# 이 함수는 시퀀스 𝑠에 있는 각 기호에 대응하는 숫자열 𝑐(str)을 반환해야 합니다. 함수에는 세 번째 선택적 매개변수 swap이 있으며,
# 이는 불리언 값(bool)을 받을 수 있습니다(기본값: False). 이 매개변수가 True 값을 받으면 반환되는 숫자열 𝑐에서 각 숫자 쌍의 순서를 바꾸어야 합니다.
def symbols2digits(sequence, key, swap = False):
    result = ""
    for s in sequence:
        r = ''.join(map(str,key[s]))
        if swap: r = r[::-1]
        result += r
    return result

# 함수 make_grid를 작성하여 발크누트 키 𝒱의 사전 표현(dict)을 입력으로 받습니다. 이 함수는 발크누트 키 𝒱의 그리드 표현을 반환해야 합니다.
# 즉, 각 숫자 1-9(int)를 해당 행에 있는 기호를 포함하는 문자열(str)로 연결하는 새로운 사전(dict)을 반환해야 합니다.
def make_grid(key):
    result = {}
    items = sorted(key.items(),key = lambda x: x[1])

    for i in range(9):
        val = ""
        for j in range(9):
            val += items[i*9+j][0]
        result[i+1] = val

    return result

# 함수 digits2symbols를 작성하여 두 가지 인수를 입력으로 받습니다: i) 숫자열 𝑐(str)과 ii) 발크누트 키 𝒱의 그리드 표현(dict).
# 이 함수는 숫자열 𝑐에 대응하는 기호의 시퀀스 𝑠(str)을 반환해야 합니다. 함수에는 세 번째 선택적 매개변수 swap이 있으며,
# 이는 불리언 값(bool)을 받을 수 있습니다(기본값: False). 이 매개변수가 True 값을 받으면, 숫자열 𝑐의 각 숫자 쌍의 순서를 바꾼 후에
# 기호의 시퀀스 𝑠을 반환해야 합니다.
def digits2symbols(numstr, grid, swap = False):
    result = ""
    for i in range(0,len(numstr),2):
        x,y = numstr[i:i+2]
        if swap: x,y = y,x
        r = grid[int(x)][int(y)-1]
        result +=  r
    return result

# 함수 encode를 작성하여 두 가지 인수를 입력으로 받습니다: i) 평문 𝑡(str)과 ii) 발크누트 키 𝒱의 사전 표현(dict).
# 이 함수는 발크누트 암호로 평문 𝑡을 인코딩한 후 얻은 암호문(str)을 반환해야 합니다.
def encode(string,key):
    r1 = symbols2digits(string,key)
    grid = make_grid(key)
    r2 = digits2symbols(r1,grid,True)
    return r2

# 함수 decode를 작성하여 두 가지 인수를 입력으로 받습니다: i) 암호문 𝑐(str)과 ii) 인코딩에 사용된 발크누트 키 𝒱의 사전 표현(dict).
# 이 함수는 평문 𝑡을 반환해야 합니다.
def decode(string,key):
    r1 = symbols2digits(string,key)
    grid = make_grid(key)
    r2 = digits2symbols(r1,grid,True)
    return r2

if __name__ == "__main__":
    V = ['W 2 6', '? 9 5', ' 6 8', 'h 3 8', '( 4 8', 'e 6 3', '4 8 6', 'z 7 6', '. 2 7', 'P 5 8', '! 9 9', 'd 8 9','c 5 6', '5 8 5', '@ 7 5',
         '% 4 3', "' 6 1", 'V 3 3', 'm 1 1', 'C 3 4', 'Q 2 9', 'L 4 7', '" 3 9', 'H 5 4', 'M 1 7', 'O 5 7', 'o 7 7','E 1 9', 'k 1 3', '& 4 9',
         'S 7 2', 'v 9 7', 'U 1 5', '2 6 9', '3 5 1', 'i 5 9', 'K 1 8', 'u 4 5', 'y 4 1', 'T 3 7', 't 3 2', '8 7 3','Y 6 5', 'F 9 3', 'N 8 4',
         'b 7 9', 'r 3 5', ', 8 7', 'g 8 2', 'j 7 1', 'f 6 4', '7 3 6', 'R 2 3', '9 6 6', '# 4 6', 'J 9 1', '| 3 1','A 9 6', '; 8 3', '1 9 2',
         'a 2 5', 's 2 4', 'n 9 4', 'X 5 3', '0 7 4', 'D 2 8', 'Z 1 2', 'B 2 1', 'w 2 2', '$ 6 7', ': 7 8', ') 8 1','x 8 8', '_ 4 4', 'p 1 6',
         'q 1 4', 'I 5 5', '- 6 2', '6 9 8', 'G 4 2', 'l 5 2']

    key = read_key(V)
    print(key['W'])
    (2, 6)
    print(key['h'])
    (3, 8)
    print(key[' '])
    (6, 8)
    print(key['.'])
    (2, 7)
    r1 = symbols2digits("Where wolf's ears are, wolf's teeth are near.", key)
    print(r1 == '263863356368227752646124686325352468253563876822775264612468326363323868253563689463253527')
    r2 = symbols2digits("Where wolf's ears are, wolf's teeth are near.", key, swap=True)
    print(r2 == '628336533686227725461642863652534286525336788622772546164286233636238386525336864936525372')
    grid = make_grid(key)
    print(grid)
    {1: 'mZkqUpMKE', 2: 'BwRsaW.DQ', 3: '|tVCr7Th"', 4: 'yG%_u#L(&', 5: '3lXHIcOPi', 6: "'-efY9$ 2", 7: 'jS80@zo:b', 8: ')g;N54,xd', 9: 'J1Fn?Av6!'}
    print(digits2symbols('263863356368227752646124686325352468253563876822775264612468326363323868253563689463253527', grid))
    "Where wolf's ears are, wolf's teeth are near."
    print(digits2symbols('628336533686227725461642863652534286525336788622772546164286233636238386525336864936525372', grid, swap=True))
    "Where wolf's ears are, wolf's teeth are near."
    print(encode("Where wolf's ears are, wolf's teeth are near.", key))
    '-;7X74woa#pG47lXG4lX7:4woa#pG4R77R;4lX74&7lXS'
    print(decode('-;7X74woa#pG47lXG4lX7:4woa#pG4R77R;4lX74&7lXS', key))
    "Where wolf's ears are, wolf's teeth are near."

