for i in range(1,10):
    x = i * 0.1
    print(f"x = {x}")
    print(".1f (x) = %.1f" %(x))
    print(":.1f (x) = {:.1f}".format(x))
    print(f"x:.1f = {x:.1f}")
    print(f"round(x,1) = {round(x,1)}")
    print()
