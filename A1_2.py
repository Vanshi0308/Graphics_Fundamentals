import pandas as pd
import altair as alt

df = pd.read_excel('minard-data.xlsx')
projection="mercator"

# Removing blank values from first part of table
df_cities = df.loc[:,['LONC','LATC','CITY']]
df_cities = df_cities.dropna(how='all')

# Creating labels for temperature and removing invalid values
df_temp = df.loc[:,['LONT','TEMP','DAYS','MON','DAY']]
df_temp = df_temp.dropna(how='all')
df_temp = df_temp.fillna("")

num_days = len(df_temp.index)

for i in range(num_days):
  if (df_temp['DAY'][i]!=""):
    df_temp.loc[i,'DAY']=int(df_temp['DAY'][i])
    df_temp.loc[i,'TEMP LABELS'] = str(int(df_temp['TEMP'][i]))+"C - "+str(df_temp['DAY'][i])+' '+str(df_temp['MON'][i])
  else:
    df_temp.loc[i,'TEMP LABELS'] = str(int(df_temp['TEMP'][i]))+"C"

df_army = df.loc[:,['LONP','LATP','SURV','DIR','DIV']]

# Adding points to make the trail connected
pd.DataFrame([['a', 1], ['b', 2]],
                   columns=['letter', 'number'])
df_miss = pd.DataFrame([[37.6,55.8,100000,'A',1], [28.7,55.5,30000,'A',2], [24.6,55.8,6000,'A',3]], columns=['LONP','LATP','SURV','DIR','DIV'])
df_army = pd.concat([df_army, df_miss])

# Making the graphs for the 3 parts of the table
city_graph = alt.Chart(df_cities).mark_text(font='Sans-Serif', 
    fontSize=14, dx=-5 
).encode(longitude='LONC',latitude='LATC',text='CITY', 
).properties(title="Minard's Chart").project(type=projection) 

army_graph = alt.Chart(df_army).mark_trail().encode(
    longitude='LONP',latitude='LATP',
    size=alt.Size('SURV',
        scale=alt.Scale(range=[1,60]),
        legend=None),
    detail='DIV',
    color=alt.Color(
        'DIR', 
        scale=alt.Scale(
            domain=['A', 'R'], 
            range=['red', 'steelblue'] 
        )),
).project(type=projection)

x_range = [df_cities["LONC"].min(), df_cities["LONC"].max()]
x_values = alt.X('LONT',scale=alt.Scale(domain=x_range),axis=None)
y_values = alt.Y('TEMP',axis=alt.Axis(title="Temperature",grid=True, orient='right')) 

temperature_graph = alt.Chart(df_temp).mark_line(color='brown').encode(
    x=x_values,
    y=y_values
    )+ alt.Chart(df_temp).mark_text(dx=-6,dy=16,font='Sans-Serif',fontSize=14
).encode(x=x_values,y=y_values,text='TEMP LABELS')
temperature_graph = temperature_graph.properties(height=100, title='Temperature variation on return journey')

# Adding the graphs to a single chart
fc = alt.vconcat(army_graph + city_graph, temperature_graph, spacing=10).configure_view(width=1000,height=540,strokeWidth=0
).configure_axis(grid=False,labelFont="Sans-Serif")
fc.display()
fc.save("minard_vis.html")