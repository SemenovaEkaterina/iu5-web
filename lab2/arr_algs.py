a = [1,2,3,6,2,3,5,2,8,9,0,5,4]
min = a[0]
sum = 0
for i in range(len(a)):
	if a[i] < min:
		min = a[i]
	sum +=a[i]
print(min)
print(sum/len(a))

