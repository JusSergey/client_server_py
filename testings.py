def revert(inputstr):
    res = ""
    for ch in inputstr:
        res = ch + res

    return res


str1 = "Hello"
str2 = revert(str1)
print("revert %s" % str2)