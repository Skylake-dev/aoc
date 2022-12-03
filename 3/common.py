chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

priority = {}
for i in range(len(chars)):
    priority[chars[i]] = i + 1