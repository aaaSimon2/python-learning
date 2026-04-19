rows=5
current_row=1
while current_row<=rows:
    spaces=rows-current_row
    while spaces>0:
        print('',end="")
        spaces-=1
    stars=current_row
    while stars>0:
        print('*',end="")
        stars-=1
    print()
    current_row+=1
