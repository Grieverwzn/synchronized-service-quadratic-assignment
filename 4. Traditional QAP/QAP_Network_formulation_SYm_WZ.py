from gurobipy import *
import numpy as np
import pandas as pd

# Generate distance and flow
link_df=pd.read_csv('input_link.csv')
agent_df=pd.read_csv('input_agent.csv')
node_df=pd.read_csv('input_node.csv')

agent_df['od_pair']=agent_df.apply(lambda x: (x.origin_node_id,x.destination_node_id),axis=1)
flow=agent_df[['od_pair','customized_cost_link_value']].set_index('od_pair').to_dict()['customized_cost_link_value']
link_df['od_pair']=link_df.apply(lambda x: (x.from_node_id,x.to_node_id),axis=1)
distance=link_df[['od_pair','trans_cost']].set_index('od_pair').to_dict()['trans_cost']
built_cost=link_df[['od_pair','built_cost']].set_index('od_pair').to_dict()['built_cost']
# Build up the set of building and locations
building_set_1=[]
building_set_2=[]
location_set_1=[]
location_set_2=[]
building_set=[]
location_set=[]
building_set_map=[]
location_set_map=[]

for i in range(len(node_df)):
    if node_df.iloc[i].node_name == 'building node1':
        building_set_1.append(node_df.iloc[i].node_id)
    if node_df.iloc[i].node_name == 'building node2':
        building_set_2.append(node_df.iloc[i].node_id)
    if node_df.iloc[i].node_name == 'location node1':
        location_set_1.append(node_df.iloc[i].node_id)
    if node_df.iloc[i].node_name == 'location node2':
        location_set_2.append(node_df.iloc[i].node_id) 


location_set.extend(location_set_1)
location_set.extend(location_set_2)
location_set_map.extend(location_set_2)
location_set_map.extend(location_set_1)

building_set.extend(building_set_1)
building_set.extend(building_set_2)
building_set_map.extend(building_set_2)
building_set_map.extend(building_set_1)

# F
location_dict=dict(zip(location_set,location_set_map))
building_dict=dict(zip(building_set,building_set_map))
nb_building=len(building_set_1)
nb_location=len(location_set_1)

# Create optimization model
enviroment = gurobipy.Env()
enviroment.setParam('TimeLimit', 300)
model=Model("quadratic_assignment",env=enviroment)

# Create variables
#path=model.addVars(building_set_1,location_set_1,location_set_2,building_set_2,name='path',lb=0,ub=1)
path=model.addVars(building_set_1,location_set_1,location_set_2,building_set_2,name='path',vtype=GRB.BINARY)

assignment_1=model.addVars(building_set_1,location_set_1,name='assignment_1',vtype=GRB.BINARY)
assignment_2=model.addVars(building_set_2,location_set_2,name='assignment_2',vtype=GRB.BINARY)
# assignment_1=model.addVars(building_set_1,location_set_1,name='assignment_1',lb=0,ub=1)
# assignment_2=model.addVars(building_set_2,location_set_2,name='assignment_2',lb=0,ub=1)

# # Assignment constraints
# for k in location_set_1:
#     model.addConstr(quicksum(assignment_1[i,k] for i in building_set_1)==1,
#                    "building assignment constraint[%s]%k")
# for i in building_set_1:
#     model.addConstr(quicksum(assignment_1[i,k] for k in location_set_1)==1,
#                    "location assignment constraint[%s]%i")

# #Resource allocation constraints (if we relax one of them we will obtain GLB)
for l in location_set_2:
    for j in building_set_2:
        model.addConstr(quicksum(path[i,k,l,j] for i in building_set_1 for k in location_set_1)==nb_building*assignment_2[j,l],
                   "cap[%s,%s]%(l,j)")

for i in building_set_1:
    for k in location_set_1:
        model.addConstr(quicksum(path[i,k,l,j] for l in location_set_2 for j in building_set_2 )==nb_location*assignment_1[i,k],
                   "cap[%s,%s]%(i,k)")

# Shortest path
for i in building_set_1:
    for j in building_set_2:
        if j==building_dict[i]:
            model.addConstr(quicksum(path[i,k,location_dict[k],j] for k in location_set_1)==1,
                   "builder_agent_sp[%s,%s]%(i,j)")
        if j!=building_dict[i]:
            model.addConstr(quicksum(path[i,k,l,j] for k in location_set_1 for l in location_set_2 if l!=location_dict[k])==1,
                   "transport_agent_sp[%s,%s]%(i,j)")

# # Transportation capacity constraint 
for k in location_set_1:
    for l in location_set_2:
            model.addConstr(quicksum(path[i,k,l,j] for i in building_set_1 for j in building_set_2)==1,
                   "trans_cap[%s,%s]%(k,l)")

model.setObjective(quicksum(path[i,k,l,j]*distance[k,l]*flow[i,j]
                            for i in building_set_1 for j in building_set_2 for k in location_set_1 for l in location_set_2)+\
                                quicksum(assignment_1[i,k]*built_cost[i,k] for i in building_set_1 for k in location_set_1))

model.optimize()
print(1)