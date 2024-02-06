
"""
Finds the most significant bit of a number, i.e., left-most set bit
"""
def msb_of(num):
    if num == 0: return None
    msb = 0
    while num > 0:
        num = num // 2
        msb += 1
    return msb - 1
