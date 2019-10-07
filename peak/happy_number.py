def isHappy(n: int) -> bool:
    dp_arr = {}
    _n = str(n)
    last_n = n
    history = {last_n}
    while True:
        curr_n = 0
        for digit in str(last_n):
            _d = int(digit)
            if _d in dp_arr:
                curr_n += dp_arr[_d]
            else:
                dp_arr[_d] = _d ** 2
                curr_n += dp_arr[_d]
        print(last_n, curr_n)
        if curr_n == 1:
            return True
        if curr_n in history:
            return False
        last_n = curr_n
        history.add(last_n)
        
print(isHappy(19))
print(isHappy(2))