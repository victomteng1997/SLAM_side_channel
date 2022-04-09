#py3
import matplotlib.pyplot as plt
with open("sample_baseline_house.txt",'r') as f:
    content = f.readlines()

a=0
b=0
c=0
d=0
line_count = 0
for line in content:

    if "Time difference" in line: # anchor
        line_count += 1
        
    if "2" in line:
        b+=1
    if "3" in line:
        c+=1
    if "4" in line:
        d+=1
    
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
    '''
    if "2" in line:
        x2.append(i)
        y2.append(1)
        #print("2", int(time_str))
    if "3" in line:
        x3.append(i)
        y3.append(1)
    if "4" in line:
        x4.append(i)
        y4.append(4)
    '''
    if "Time" in line:
        time = int(line.split()[-1][0:-4])
        line_x.append(time)
        line_y.append(5)
        

        
print(len(line_x))
    
plt.scatter(line_x, line_y, color="red")
#plt.scatter(x2, y2, color="blue")     
#plt.scatter(x3, y3, color="yellow")    

plt.show()
        
