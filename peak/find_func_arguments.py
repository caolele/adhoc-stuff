# https://leetcode.com/discuss/interview-question/391709/google-onsite-find-function-arguments


def binary_search_region(f, x, z):
    y = 1
    while f(x, y) < z:
        y *= 2
    return y/2, y

def binary_search_y(f, x, y_begin, y_end, z):
    while y_begin <= y_end:
        mid = (y_begin + y_end) // 2
        if f(x, mid) > z:
            y_end = mid - 1
        elif f(x, mid) < z:
            y_begin = mid + 1
        else:
            return mid
    return None

def solve(f, z):
    result = []
    x, y = 1, 1
    while f(x, 1) <= z:
        y_begin, y_end = binary_search_region(f, x, z)
        _y = binary_search_y(f, x, y_begin, y_end, z)
        if _y is not None:
            result.append((x, int(_y)))
        x += 1
    return result
        

if __name__ == '__main__':
    
    def f1(x, y):
        return x + y
    print(solve(f1, 5))
    
    def f2(x, y):
        return x**2 + y
    print(solve(f2, 50))
    
