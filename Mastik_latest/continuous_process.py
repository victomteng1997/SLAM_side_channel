#py3

#py3

import matplotlib.pyplot as plt

f = open('sample_out_house.txt', 'r')
content = f.readlines()
f.close()

print(len(content))


# statistics
I_count = 0
O_count = 0
K_count = 0
R_count = 0

for line in content:
    if "I" in line:
        I_count += 1
    if "O" in line:
        O_count += 1
    if "K" in line:
        K_count += 1
    if "R" in line:
        R_count += 1
print(I_count, O_count, K_count, R_count)


x = []
y = []

previous_time = 0
O_count_list = []
O_count = 0
for line in content:
    #print(line)
    time_str = ''
    start = False
    for char in line:
        if char == ']':
            break
        if start:
            time_str += char
        if char == '[':
            start = True
    
    if int(time_str) - previous_time < 2:
        #print(time_str, previous_time)
        previous_time = int(time_str)
        continue
    previous_time = int(time_str)
            
    #print(time_str)
    #print(line)
    if "I" in line:
        x.append(int(time_str))
        y.append(1) 
        #print("1", int(time_str))
        O_count_list.append(O_count)
        O_count = 0
    if "O" in line:
        x.append(int(time_str))
        y.append(2)
        #print("2", int(time_str))
        O_count += 1
    if "K" in line:
        x.append(int(time_str))
        y.append(3)
    if "R" in line:
        x.append(int(time_str))
        y.append(4)
    
    
    #if int(time_str) > 10000000:
    #    break
    


print(O_count_list)

# print(y)
print(len(x))
#plt.scatter(x, y)      
#plt.show()
        
