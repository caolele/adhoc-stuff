def chop(target, array_of_int):
    arr_len = len(array_of_int)
    begin_idx = 0
    end_idx = arr_len - 1

    # iterative approach
    while (True):
        _len = end_idx - begin_idx + 1
        if _len <= 0:
            return -1
        mid_idx = begin_idx + int(_len / 2)
        if array_of_int[mid_idx] == target:
            return mid_idx
        elif array_of_int[mid_idx] > target:
            end_idx = mid_idx - 1
        else:
            begin_idx = mid_idx + 1
 


if __name__ == "__main__":

    assert(-1==chop(3, []))
    assert(-1==chop(3, [1]))
    assert(0==chop(1, [1]))
    #
    assert(0==chop(1, [1, 3, 5]))
    assert(1==chop(3, [1, 3, 5]))
    assert(2==chop(5, [1, 3, 5]))
    assert(-1==chop(0, [1, 3, 5]))
    assert(-1==chop(2, [1, 3, 5]))
    assert(-1==chop(4, [1, 3, 5]))
    assert(-1==chop(6, [1, 3, 5]))
    #
    assert(0==chop(1, [1, 3, 5, 7]))
    assert(1==chop(3, [1, 3, 5, 7]))
    assert(2==chop(5, [1, 3, 5, 7]))
    assert(3==chop(7, [1, 3, 5, 7]))
    assert(-1==chop(0, [1, 3, 5, 7]))
    assert(-1==chop(2, [1, 3, 5, 7]))
    assert(-1==chop(4, [1, 3, 5, 7]))
    assert(-1==chop(6, [1, 3, 5, 7]))
    assert(-1==chop(8, [1, 3, 5, 7]))