import re

m = re.compile("std::vector<(.+)>")

j = "std::vector<std::vector<std::vector<string>>>"
n = [[j,j]]
while True:
    try:
        j = m.match(j).group(1)
    except: break
    n.append([j,j])
l = n[-1][0]
unny = lambda k: f"<{k}, std::allocator<{k}>>"
n[-2][1] = n[-2][1].replace(f"<{l}>",unny(l))
for i in range(len(n)-2).__reversed__():
    d = n[i+1][1]
    n[i][1] = n[i][1].replace(f"<{n[i+1][0]}>", unny(d))

print(n[0][1])
