#py3

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd

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


x1 = []
y1 = []

x2 = []
y2 = []

x3 = []
y3 = []

x4 = []
y4 = []

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
            
    #print(time_str)
    #print(line)
    if "I" in line:  # line anchor
        x1.append(int(time_str))
        y1.append(1) 
        #print("1", int(time_str))
    if "O" in line:  # level 1 logic, every pixel should do once
        x2.append(int(time_str))
        y2.append(1)
        #print("2", int(time_str))
    if "K" in line:  # level 2 logic
        x3.append(int(time_str))
        y3.append(1)
    if "R" in line:
        x4.append(int(time_str))
        y4.append(1)
    
    
    #if int(time_str) > 10000000:
    #    break

# print(y)
#plt.scatter(x1, y1, color="red")
#plt.scatter(x2, y2, color="blue")     

#plt.show()
        
# start processing here
## try to group lines first. target: 200 lines

### Calculate the average distance between points.
distance = 0
for i in range(1, len(x1)):
    distance += x1[i] - x1[i-1]
avg_distance = distance/(len(x1)-1)
#print(avg_distance)

###
'''
line_result = []
element_count = 1
for i in range(1, len(x1)):
    #print(x1[i], x1[i-1])
    if x1[i] - x1[i-1] <avg_distance:
        element_count +=1
    else:
        line_result.append(element_count)
        element_count = 1

print(line_result, len(line_result))
'''
x1_y1 = {"X":x1, "Y":y1}
df = pd.DataFrame(x1_y1)
km = KMeans(n_clusters = 250, random_state=250).fit(df)
'''
#print(km.labels_)
#print(km.cluster_centers_)
centroid_list = [item[0] for item in km.cluster_centers_]
centroid_list.sort()

avg_distance = 0.0
for i in range(1, len(centroid_list)):
    avg_distance += centroid_list[i] - centroid_list[i-1]
    
print(avg_distance/len(centroid_list))
'''

  
       
        
