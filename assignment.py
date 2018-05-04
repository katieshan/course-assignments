import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

housing = pd.read_csv("C:/Users/username/Desktop/PEP_2016_PEPANNHU_with_ann.csv", skiprows=0, header=1)
pop = pd.read_excel("C:/Users/username/Desktop/nst-est2017-01.xlsx", sheet_name="NST01", skiprows=1, header=2)
income = pd.read_csv("C:/Users/username/Desktop/MEHOINUSDCA672N.csv")
rent = pd.read_csv("C:/Users/username/Desktop/State_Zri_AllHomesPlusMultifamily.csv")
df_desc=rent.head()
#print(df_desc)

housing_dc = housing.loc[housing['Geography'] == "District of Columbia"].T
housing_dc = housing_dc.drop(housing_dc.index[0:5])
housing_dc.columns=['housing_stock']
housing_dc.index=housing_dc.index.str[-4:].astype('int')
pop_dc = pop.loc[pop['Unnamed: 0'] == ".District of Columbia"].T
pop_dc = pop_dc.drop(pop_dc.index[0:3])
pop_dc.columns=['population']
pop_dc.index.astype('int')
income_dc = income
income_dc.columns=['date', 'income']
income_dc['date'] = pd.to_datetime(income_dc['date'])
income_dc['year']=income_dc['date'].dt.year
income_dc = income_dc.drop(columns=['date'])
income_dc = income_dc.set_index('year').astype('int')
rent_dc = rent.loc[rent['RegionName'] == "District of Columbia"].T
rent_dc = rent_dc.drop(rent_dc.index[0:3])
rent_dc=rent_dc.reset_index()
rent_dc.columns=['date', 'rent']
rent_dc['date'] = pd.to_datetime(rent_dc['date'])
rent_dc['year']=rent_dc['date'].dt.year
rent_dc['rent'] = pd.to_numeric(rent_dc['rent'])
rent_dc = rent_dc.drop(columns=['date'])
rent_dc = rent_dc.groupby('year', as_index=False)['rent'].mean()
rent_dc = rent_dc.set_index(['year']).astype('int')

merge = housing_dc.join(pop_dc, how='inner')
merge = merge.join(income_dc, how='inner')
merge = merge.join(rent_dc, how='inner')
merge['housing_percap'] = (merge['housing_stock']/merge['population'])
base2010 = merge.iloc[0]
merge_base = merge/base2010

plt.figure()
sns.set_style('white')
sns.set_palette(sns.color_palette("bright"))
plt.plot(merge_base.index, merge_base['income'], ':', label="Median Income per Capita")
plt.plot(merge_base.index, merge_base['housing_percap'], label="Housing Stock per Capita")
plt.plot(merge_base.index, merge_base['rent'], label="Rent Index")
plt.plot(merge_base.index, merge_base['population'], label="Population")
plt.plot(merge_base.index, merge_base['housing_stock'], label="Estimated Housing Stock")
plt.legend()
plt.title("Change in Washington, DC Population, Income, and Housing Indicators since 2010")

plt.show()
