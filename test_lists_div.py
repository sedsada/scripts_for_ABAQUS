def split_list(alist, wanted_parts=1):
   length = len(alist)
   return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
           for i in range(wanted_parts)]


A = [i for i in range(12)]

print split_list(A, wanted_parts=1)
print split_list(A, wanted_parts=3)
print split_list(A, wanted_parts=4)
print split_list(A, wanted_parts=4)[1]

