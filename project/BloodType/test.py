from main import Human
#
# 아버지(A), 어머니(B)
dad = Human("Dad", "A")
mom = Human("Mom", "O")
child = Human("Child")
ABO_bloodType = {
    'A': {'AA', 'AO'},
    'B': {'BB', 'BO'},
    'O': {'OO'},
    'AB': {'AB'},
}
child.set_parent(dad=dad, mom=mom)
result = child.get_my_bloodType()
print(f"Child의 가능한 혈액형: {child.get_my_bloodType()} ")
guess = "AB"
print(f"result: {result}")
for ABO in ABO_bloodType[guess]:
    if ABO in result:
        print(f"{ABO}는 가능합니다. 정답")
        break
else:
    print("잘못된 결과")
#
# # 부모 모두 O형
# dad = Human("Dad", "O")
# mom = Human("Mom", "O")
# child = Human("Child")
#
# child.set_parent(dad=dad, mom=mom)
# print(f"Child의 가능한 혈액형: {child.get_my_bloodType()}")




# # 아버지 혈액형이 없는 경우
# grandfather = Human("Grandfather", "A")
# grandmother = Human("Grandmother", "B")
# dad = Human("Dad")  # 아버지 혈액형 없음
# dad.set_parent(dad=grandfather, mom=grandmother)
#
# mom = Human("Mom", "O")
# child = Human("Child")
#
# child.set_parent(dad=dad, mom=mom)
# print(f"Child의 가능한 혈액형: {child.get_my_bloodType()}")


#
#
# # # 어머니 혈액형이 없는 경우
# maternal_grandfather = Human("Maternal Grandfather", "A")
# maternal_grandmother = Human("Maternal Grandmother", "O")
# mom = Human("Mom")  # 어머니 혈액형 없음
# mom.set_parent(dad=maternal_grandfather, mom=maternal_grandmother)
#
# dad = Human("Dad", "B")
# child = Human("Child")
#
# child.set_parent(dad=dad, mom=mom)
# print(f"Child의 가능한 혈액형: {child.get_my_bloodType()}")
# #
#
#
#
# 부모님 혈액형을 모르는 경우
# grandfather = Human("Grandfather", "A")
# grandmother = Human("Grandmother", "O")
# maternal_grandfather = Human("Maternal Grandfather", "B")
# maternal_grandmother = Human("Maternal Grandmother", "O")
#
# dad = Human("Dad")  # 아버지 혈액형 없음
# dad.set_parent(dad=grandfather, mom=grandmother)
#
# mom = Human("Mom")  # 어머니 혈액형 없음
# mom.set_parent(dad=maternal_grandfather, mom=maternal_grandmother)
#
# child = Human("Child")
#
# child.set_parent(dad=dad, mom=mom)
# print(f"Child의 가능한 혈액형: {child.get_my_bloodType()}")

#
