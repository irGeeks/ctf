hardcode = 'c61b68366edeb7bdce3c6820314b7498'
add_byte = [-1, 1]
flag = [chr(ord(char) + add_byte[(index & 1)]) for index, char in enumerate(hardcode)]
print "SharifCTF{%s}" % ''.join(flag)