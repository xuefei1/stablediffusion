

def lps(p):
    lps_arr = [0] * len(p)
    j, t = 0, -1
    lps_arr[0] = -1
    while j < len(p) - 1:
        if 0 > t or p[j] == p[t]:
            j += 1
            t += 1
            # if p[j] != p[t]: # Check after increment to j and t
            lps_arr[j] = t # Avoid repeated compare of the same items.
            # else:
            #     lps_arr[j] = lps_arr[t]
        else:
            t = lps_arr[t]
    return lps_arr


def kmp(s, p):
    lps_ = lps(p)
    si = 0
    pi = 0
    while si < len(s) and pi < len(p):
        if 0 > pi or s[si] == p[pi]:
            si += 1
            pi += 1
        else:
            pi = lps_[pi]
    return si - pi


if __name__ == "__main__":
    # print(lps("AAACAAAA"))
    # print(kmp("AAAAAAAOOAAAAAAAACAAAABBBBBB", "AAACAAAA"))
    print(lps("issipi"))
    print(kmp("mississippi", "issipi"))
