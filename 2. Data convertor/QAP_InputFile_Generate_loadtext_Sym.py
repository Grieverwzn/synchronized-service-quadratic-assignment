import pandas as pd
import numpy as np
import csv
import random
from io import StringIO


n=3
data_dis = np.loadtxt('distance_matrix.txt', usecols=range(n))
data_flow=np.loadtxt('flow_matrix.txt', usecols=range(n))
data_built_1=np.loadtxt('data_built_1.txt', usecols=range(n)) # Symmtric case only need one side building cost
data_built_2=np.random.rand(n,n)*0


# n=200
# data_dis=np.random.rand(n,n)*100
# data_flow=np.random.rand(n,n)*100
# data_built_1=np.random.rand(n,n)*100
# data_built_2=np.random.rand(n,n)*100

#Read Data
nodename_array=['building node1','location node1','location node2','building node2']


node_num_each = n


with open('input_node.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['node_name', 'node_id','x', 'y'])
    for i in  range(0,4):
        for j in range(node_num_each):
            if(i<4):
                nodeid=1000*(i+1)+j+1
                locationx = 100 * i
                locationy = 10 * j
            line = [nodename_array[i],
                    nodeid,
                    locationx,
                    locationy]
            writer.writerow(line)



with open('input_link.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(
        ['link_id','from_node_id', 'to_node_id', 'built_cost','trans_cost','link_type','acting_link_id'])
    count=0
    for i in range(node_num_each):# building1 to location1
        for j in range(node_num_each):
            count+=1
            line1=[count,
                   1000+i+1,
                   2000+j+1,
                   data_built_1[i][j], # built cost
                   0, #trans cost
                   2,#building to location
                   count]
            writer.writerow(line1)
    for i in range(node_num_each):# location 2 to building 2
        for j in range(node_num_each):
            count+=1
            line2=[count,
                   3000+i+1,
                   4000+j+1,
                   data_built_2[i][j], # built cost
                   0,# trans cost
                   3,#location to building
                   count]
            writer.writerow(line2)
            # print('node',node_num_each)
            # print('x',i)
            # print('y',j)
            # print(data_built_2[i][j])
    for i in range(node_num_each): # location 1 to location 2 transportation
        for j in range(node_num_each):
            if(j!=i):
                count += 1
                line3 = [count,
                     2000 + i + 1,
                     3000 + j + 1,
                     0, # built
                     data_dis[i][j],# trans
                     1,#physical transportation link
                     count]
                writer.writerow(line3)
    for i in range(node_num_each):
        count += 1
        line4 = [count,
                 2000 + i + 1,
                 3000+i+1,
                 0,
                 data_dis[i][i],# trans
                 4, #location planning link
                 count]
        writer.writerow(line4)

with open('input_agent.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(
        ['agent_id','origin_node_id','destination_node_id','customized_cost_link_type',
         'customized_cost_link_value','agent_type','set_of_allowed_link_types'])
    count = 0
    # transportation agent
    for i in range(node_num_each):
        for j in range(node_num_each):
            if(i!=j):
                count += 1
                line1 = [count,
                         1000 + i + 1,
                         4000 + j + 1,
                         1,
                         data_flow[i][j],#customized_cost:the flow(i,j)
                         1,
                         '1;2;3']
                writer.writerow(line1)
                #print(data_flow[i][j])
    #builder agent
    for i in range(node_num_each):
        count += 1
        line2 = [count,
                 1000+i+1,
                 4000+i+1,
                 2,
                 data_flow[i][i], #customized_cost
                 2,
                 '2;3;4']
        writer.writerow(line2)

