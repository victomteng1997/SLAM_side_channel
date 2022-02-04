#py3
import matplotlib.pyplot as plt
with open("baseline.txt",'r') as f:
    content = f.readlines()

a=0
b=0
c=0
d=0
line_count = 0
for line in content:

    if "1" in line:
        a+=1 
    if "2" in line:
        b+=1
    if "3" in line:
        c+=1
    if "4" in line:
        d+=1
    if "Time difference" in line: # anchor
        line_count += 1
        
print(a,b,c,d,line_count)


x1 = []
y1 = []

x2 = []
y2 = []

x3 = []
y3 = []

x4 = []
y4 = []

line_x = []
line_y = []

for i in range(0, len(content)):
    line = content[i]  
    #print(time_str)
    #print(line)
    if "1" in line:
        x1.append(i)
        y1.append(1) 
        #print("1", int(time_str))
    if "2" in line:
        x2.append(i)
        y2.append(2)
        #print("2", int(time_str))
    if "3" in line:
        x3.append(i)
        y3.append(3)
    if "4" in line:
        x4.append(i)
        y4.append(4)
    if "Time" in line:
        line_x.append(i)
        line_y.append(5)
        
        
        
# debug first level 

result_x1 = [] 
counter = 0
current_count = 0
for i in range(1, len(x1)):
    if x1[i] <= line_x[counter]:
        current_count += 1
    else:
        counter += 1
        result_x1.append(current_count)
        current_count = 0
    
    if counter >= len(line_x):
        result_x1.append(len(x1)-i)
        break
print(result_x1, len(result_x1))

    

result_x2 = [] 
counter = 0
current_count = 0
for i in range(1, len(x1)):
    if x2[i] <= line_x[counter]:
        current_count += 1
    else:
        counter += 1
        result_x2.append(current_count)
        current_count = 0
    
    if counter >= len(line_x):
        result_x2.append(len(x2)-i)
        break
print(result_x2, len(result_x2))

    

# print(y)
#plt.scatter(x, y)      
#plt.show()
        
        
