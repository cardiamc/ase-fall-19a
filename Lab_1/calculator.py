def sum(m,n):
    # It performs n increments to the value of m and return the result
    tot_sum = m
    if n < 0:
        for i in range(abs(n)):
            tot_su -= 1
    else: 
        for i in range(0,n):
            tot_sum += 1
    return tot_sum

def divide(m,n):
    result = 0
    negativeResult = m > 0 and n < 0 or m < 0 and n > 0
    n = abs(n)
    m = abs(m)

    while (m-n >= 0):
        m -= n
        result += 1

        result = -result if negativeResult else result
    return result
