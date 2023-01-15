def log_in(input_id,input_pw):
    # log_in.txt파일을 불러와서 입력받은 input_id와 input_pw가 일치하는지
    # 확인후에 일치할 경우 True, 아니면 False를 리턴하시오
    real_id = ""
    real_pw = ""
    file = open('log_in.txt','r',encoding='utf8')
    lines = file.readlines()
    for line in lines:
        key,value = line.split()
        if '\n' in value:
            value = value.replace('\n','')
        if key[:-1] == 'ID':
            real_id = value
        else:
            real_pw = value
            if real_id == input_id and real_pw == input_pw:
                return True
    return False
