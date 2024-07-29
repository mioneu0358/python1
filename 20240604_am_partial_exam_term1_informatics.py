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
