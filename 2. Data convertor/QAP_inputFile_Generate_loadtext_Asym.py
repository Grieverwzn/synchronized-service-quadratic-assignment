import pandas as pd
import numpy as np
import csv
import random
from io import StringIO
inputtype='traditional_QAP'
#inputtype='timetable'

if inputtype == 'traditional_QAP':
    data_dis =  np.loadtxt('distance_matrix.txt')
    data_flow = np.loadtxt('flow_matrix.txt')
    #data_built_1 = np.loadtxt('data_built_1.txt')
    #data_built_2= np.loadtxt('data_built_2.txt')
    data_built_1 = np.zeros([9,9]) # if do not have data_built_1.txt, pls input the number according to the dimension of matrix 
    data_built_2= np.zeros([9,9])# if do not have data_built_2.txt, pls input the number according to the dimension of matrix 
if inputtype =='timetable':
    # basic input
    timetable_o = np.loadtxt('timetable_1.txt') # origin-side timetable
    timetable_d = np.loadtxt('timetable_2.txt') # destination-side timetable
    data_flow = np.loadtxt('t_flow_matrix.txt')
    #data_flow =np.round(np.random.rand(18,18)*10)
    travel_time_o = np.loadtxt('travel_time_1.txt') # origin-side travel_time
    travel_time_d= np.loadtxt('travel_time_2.txt') # destination-side travel_time
    period_time=24
    timewindow=24
    q,n= timetable_o.shape
    q,m= timetable_d.shape
    data_built_1=np.zeros([n,n])
    data_built_2=np.zeros([m,m])
    data_dis=np.zeros([n,m])
    for i in range(n):
        for k in range(n):
            tmp=np.mod(timetable_o[1][i]+travel_time_o[i][k],period_time)
            if timetable_o[0][k]<tmp:
                data_built_1[i][k]=period_time-timetable_o[1][i]+timetable_o[0][k]
            if timetable_o[0][k]>=tmp:
               data_built_1[i][k]=timetable_o[0][k]-timetable_o[1][i]

              
    for l in range(m):
        for j in range(m):
            tmp=np.mod(timetable_d[0][j]-travel_time_d[l][j],period_time)
            if timetable_d[1][l]>tmp:
               data_built_2[l][j]=period_time-timetable_d[1][l]+timetable_d[0][j]
            if timetable_d[1][l]<=tmp:
               data_built_2[l][j]=timetable_d[0][j]-timetable_d[1][l]
    
    for k in range(n):
        for l in range(m):
            if timetable_o[0][k]<timetable_d[1][l]:
               data_dis[k][l] = timetable_d[1][l]-timetable_o[0][k]
            if timetable_o[0][k]>=timetable_d[1][l]:
                data_dis[k][l]=period_time-timetable_o[0][k]+timetable_d[1][l]      
    for i in range(n):
        for k in range(n):
            if (travel_time_o[i][k]+timewindow<data_built_1[i][k]):
                data_built_1[i][k]=100000

    for l in range(m):
        for j in range(m):
            if (travel_time_d[l][j]+timewindow<data_built_2[l][j]):
                data_built_2[l][j]=100000


# usecols=range(m)


n,m=data_flow.shape
node_num_each = [n,n,m,m]
#Read Data
nodename_array=['building node1','location node1','location node2','building node2']





with open('input_node.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['node_name', 'node_id','x', 'y'])
    for i in  range(0,4):
        for j in range(node_num_each[i]):
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
    for i in range(node_num_each[0]):# building1 to location1
        for j in range(node_num_each[1]):
            count+=1
            line1=[count,
                   1000+i+1,
                   2000+j+1,
                   data_built_1[i][j], # built cost
                   0, #trans cost
                   2,#building to location
                   count]
            writer.writerow(line1)
    for i in range(node_num_each[2]):# location 2 to building 2
        for j in range(node_num_each[3]):
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
    for i in range(node_num_each[1]): # location 1 to location 2 transportation
        for j in range(node_num_each[2]):
            #if(j!=i):
            count += 1
            line3 = [count,
                2000 + i + 1,
                3000 + j + 1,
                0, # built
                data_dis[i][j],# trans
                1,#physical transportation link
                count]
            writer.writerow(line3)


with open('input_agent.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(
        ['agent_id','origin_node_id','destination_node_id','customized_cost_link_type',
         'customized_cost_link_value','agent_type','set_of_allowed_link_types'])
    count = 0
    # transportation agent
    for i in range(node_num_each[0]):
        for j in range(node_num_each[3]):
            count += 1
            line1 = [count,
                    1000 + i + 1,
                    4000 + j + 1,
                    1,
                    data_flow[i][j],#customized_cost:the flow(i,j)
                    1,
                    '1;2;3;4']
            writer.writerow(line1)
                #print(data_flow[i][j])

