x0, y0, w0, h0 = map(int, input().split())
x1, y1, w1, h1 = map(int, input().split())
if (x0 <= x1 + w1 and x0 + w0 >= x1
    and y0 <= y1 + h1 and y0 + h0 >= y1):
    print('YES')
else:
    print('NO')

