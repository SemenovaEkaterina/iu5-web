ivan = {
	"name":"ivan",
	"age":34,
	"children": [{
		"name":"vasya",
		"age": 12,
	}, {
		"name":"petya",
		"age": 10,
	}]
}

emps = [ivan,]

for i in emps:
	for j in i["children"]:
		if j["age"] > 9:
			print(i["name"])
			break

