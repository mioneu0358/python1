# //정수로 입력받은 수는 한글로, 한글로 입력받은 수는 정수로 변환하려고 한다. 예시는 다음과 같다


class Hangulstudy:
    def __init__(self,num):
        self.num = num

    def __int__(self):
        int_num = 0
        han_number = {'일' :1,'이':2,'삼':3,'사':4,'오':5,'육':6,'칠':7,'팔':8,'구':9}
        point = {'만': 10000, '천': 1000,'백':100, '십':10}
        if self.num[0] in point:
            int_num += point[self.num[0]]
        for i in range(len(self.num)-1):
            if self.num[i+1] in point:
                if self.num[i] in han_number:
                    int_num += han_number[self.num[i]] * point[self.num[i+1]]
                else:
                    int_num += point[self.num[i+1]]
        int_num += han_number[self.num[-1]]

        return int_num



    def __str__(self):
        units =['','십','백','천','만']

        nums = '일이삼사오육칠팔구'
        result = []
        i = 0
        while self.num > 0:
            r =  self.num % 10
            self.num = self.num // 10
            if r > 0:
                result.append(nums[r - 1] + units[i])
            i += 1



        result = ''.join(result[::-1])
        if result[0] == '일':
            result = result[1:]
        return result


a = Hangulstudy("만이천이십이")
print(int(a)) #출력 123
a = Hangulstudy(23456)
print(str(a)) #출력 백이십삼"




#만단위를 넘을떄
class Hangulstudy:
    def __init__(self,num):
        self.num = num

    def __int__(self):

        han_number = {'일': 1, '이': 2, '삼': 3, '사': 4, '오': 5, '육': 6, '칠': 7, '팔': 8, '구': 9}
        point = {'만': 10000, '천': 1000, '백': 100, '십': 10}
        man_point = self.num.find('만')
        print(man_point)
        nums = []
        for i in self.num[:man_point]:
            if i in point:
                nums.append(self.num[:man_point])
                nums.append(self.num[man_point:])
                break
        print(nums)
        part = []
        for num in nums:
            int_num = 0
            if num[0] in point:
                int_num += point[num[0]]
            print(int_num)
            for i in range(len(num)-1):
                if num[i+1] in point:
                    if num[i] in han_number:
                        int_num += han_number[num[i]] * point[num[i+1]]
                    else:
                        int_num += point[num[i+1]]
                print(int_num)
            if len(num) > 1:
                int_num += han_number[num[-1]]
            print(int_num)
            part.append(str(int_num))
        print(part)
        part = ''.join(part)
        return int(part)

num = Hangulstudy("천이백오십만일")
print(int(num))
