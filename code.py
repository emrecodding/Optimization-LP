from pyomo.environ import *
import pandas as pd

product = ['X','X','X','Y','Y']
plant = ['F1','F2','F3','F1','F2']
hours = [3,2,2,2,1] # product time for 100 kg

# Dataframe 
df = pd.DataFrame(list(zip(product,plant,hours)),columns=['product','plant','hours'])

# whole hours in a month
monthly_hours = 31*24

# calculating monthly capacity from hours / 100 kg
df['monthly_hours'] = monthly_hours*100/df['hours']  
model = ConcreteModel()

n_df =len(df)

model.x = Var(range(n_df),bounds=(0,None))
Lp = model.x

obj = sum(Lp[i] * df['hours'][i] for i in df.index)
model.obj = Objective(expr= obj, sense= minimize)

F1 = df[df['plant'] == 'F1']
F2 = df[df['plant'] == 'F2']
F3 = df[df['plant'] == 'F3']

model.cons = ConstraintList()

# The capacity of products that can be produced in a plant have to be less or equal to the capacity of monthly hours.
model.cons.add(expr= sum(Lp[i]* df['hours'][i]/100 for i in F1.index) <= 744 )
model.cons.add(expr= sum(Lp[i]* df['hours'][i]/100 for i in F2.index) <= 744 )
model.cons.add(expr= sum(Lp[i]* df['hours'][i]/100 for i in F3.index) <= 744 )

X_demand = 50000
Y_demand = 71000

X = df[df['product'] == 'X']
Y = df[df['product'] == 'Y']

model.cons.add(expr= sum(Lp[i] for i in X.index) == X_demand)
model.cons.add(expr= sum(Lp[i] for i in Y.index) == Y_demand)

opt = SolverFactory('gurobi')
solver = opt.solve(model)

model.pprint()


