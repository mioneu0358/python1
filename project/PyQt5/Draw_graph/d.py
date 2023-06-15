ent = input().replace(' ','')
X = ['x**3','x**2','x']
op = ['+','-']
nums = []
for x in X:
    idx = ent.find(x)
    print(ent)
    if idx >= 0:
        num = ent[:idx]
        nums.append(1 if num in ['','+','-'] else int(num))
        ent = ent[idx + len(x):]
    else:
        nums.append(0)
if ent[-1].isdigit():
    nums.append(int(ent))
print(nums)
# 3x**3 + 2x**2 + 1x + 0
# x**3 + x**2 + x + 0
# 3x**3 + 16x
# 2x**2 + 16