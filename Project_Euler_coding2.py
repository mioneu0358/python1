def get_kor_num(int_num:str):
    int_num = int(int_num.rstrip('원\n').replace(',',''))
    # 숫자
    digit_list = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
    # 십 ~ 천 단위
    low_part_list = {1: "", 10: "십", 100: "백", 1000: "천", }
    # 억 ~ 조 단위
    high_part_list = {1: "", 10000: "만", 100000000: "억", 1000000000000: "조"}
    # 최대 읽을 수 있는 단위 "조"
    high_part_div = 1000000000000

    ret_str = ""
    while int_num:
        part = int_num // high_part_div
        low_part_div = 1000
        low_str = ""
        if not part:
            high_part_div //= 10000
            continue
        while part:
            num = part // low_part_div
            n = digit_list[num]
            p = low_part_list[low_part_div]
            if num > 1 or num == 1 and low_part_div == 1:
                low_str += n
            if num:
                low_str += p
            part %= low_part_div
            low_part_div //= 10
        hp = high_part_list[high_part_div]

        if hp == "만" and low_str == "일":
            ret_str += hp+' '
        else:
            ret_str += low_str + hp+' '
        int_num %= high_part_div
        high_part_div //= 10000

    return ret_str.rstrip()+'원'



with open('text.txt','r',encoding='utf8') as file:
    lines = file.readlines()
    answer = 0
    for line in lines:
        result = get_kor_num(line)

        a = len(result.split())
        b = len(result.replace(' ',''))
        answer += a * b
        print(f"input: {line[:-1]}, output:{result}\n어절: {a}, 한글개수: {b}, 곱: {a*b}, 정답: {answer}")
        print()
    print(answer)
