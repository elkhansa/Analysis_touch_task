import pandas as pd
import numpy as np
import re

# Import and read the log file from the current domain (txt to csv to excel):
# Convert the txt file to csv and name the columns:
read_file = pd.read_csv (r'file path.txt', sep='\t')
read_file.to_csv (r'file path.csv', index=None)
df = pd.read_csv (r'file path.csv', header=None)
df.rename(columns={df.columns[1]: "Var2", df.columns[0]: "Var1"}, inplace=True)

#A. Pleasant Ratings:
# 1. A dataframe that contain all the rows containing the string (DrawRatingStimulationPLeasantness):
pleasant_ratings_rows = df[df['Var2'].str.contains('DrawRatingStimulationPleasantness')]
# Copy of the data frame to avoid SettingWithCopy error:
prr2=pleasant_ratings_rows.copy()
# 2. Make a third column containing the differences between the indexes of prr2:
prr2['Diff_indexes'] = prr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 0:
prr2.iat[0,2]= 0
# 3. Make a list of the indexes of the rows that contain the pleasant ratings:
# Rows are the last ones in each rating blocks:
pleasant_ratings_idx= prr2.loc[prr2["Diff_indexes"].gt(100).shift(-1, fill_value=False)].index.tolist() + [prr2.index[-2]]
# In case the last row had a value >100 (i.e the participant didn't move the cursor and chose the first rating appeared):
v=prr2.iloc[-1]['Diff_indexes']
y=prr2.index[-1]
if v>100:
	pleasant_ratings_idx.append(y)
# Get a datframe with rows containing the required pleasant ratings:
pleasant_ratings_df=df[df.index.isin(pleasant_ratings_idx)]
# 4. Get a list with the corresponding pleasant ratings strings:
pleasant_ratings_strings= [r for r in pleasant_ratings_df['Var2']]
# Filter the rating as an integer and separate it from the string:  
pleasant = []
for b in pleasant_ratings_strings: 
	pleasant_ratings=re.findall(r"\d+", b)
	x= [int(i) for i in pleasant_ratings]
	pleasant.extend(x)

#A. Unpleasant Ratings:
# 1. A dataframe that contain all the rows containing the string (DrawRatingStimulationUnpLeasantness):
unpleasant_ratings_rows = df[df['Var2'].str.contains('DrawRatingStimulationUnpleasantness')]
# Copy of the data frame to avoid SettingWithCopy error:
uprr2=unpleasant_ratings_rows.copy()
# 2. Make a third column containing the differences between the indexes of uprr2:
uprr2['Diff_indexes'] = uprr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 0:
uprr2.iat[0,2]= 0
# 3. Make a list of the indexes of the rows that contain the unpleasant ratings:
# Rows are the last ones in each rating blocks:
unpleasant_ratings_idx= uprr2.loc[uprr2["Diff_indexes"].gt(100).shift(-1, fill_value=False)].index.tolist() + [uprr2.index[-2]]
# In case the last row had a value >100 (i.e the participant didn't move the cursor and chose the first rating appeared):
v=uprr2.iloc[-1]['Diff_indexes']
y=uprr2.index[-1]
if v>100:
	unpleasant_ratings_idx.append(y)
# Get a datframe with rows containing the required unpleasant ratings:
unpleasant_ratings_df=df[df.index.isin(unpleasant_ratings_idx)]
# 4. Get a list with the corresponding unpleasant ratings strings:
unpleasant_ratings_strings= [r for r in unpleasant_ratings_df['Var2']]
# Filter the rating as an integer and separate it from the string:  
unpleasant = []
for b in unpleasant_ratings_strings: 
	unpleasant_ratings=re.findall(r"\d+", b)
	x= [int(i) for i in unpleasant_ratings]
	unpleasant.extend(x)

#A. Touch Ratings:
# 1. A dataframe that contain all the rows containing the string (DrawRatingStimulationTouch):
touch_ratings_rows = df[df['Var2'].str.contains('DrawRatingStimulationTouch')]
# Copy of the data frame to avoid SettingWithCopy error:
trr2=touch_ratings_rows.copy()
# 2. Make a third column containing the differences between the indexes of trr2:
trr2['Diff_indexes'] = trr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 0:
trr2.iat[0,2]= 0
# 3. Make a list of the indexes of the rows that contain the touch ratings:
# Rows are the last ones in each rating blocks:
touch_ratings_idx= trr2.loc[trr2["Diff_indexes"].gt(100).shift(-1, fill_value=False)].index.tolist() + [trr2.index[-2]]
# In case the last row had a value >100 (i.e the participant didn't move the cursor and chose the first rating appeared):
v=trr2.iloc[-1]['Diff_indexes']
y=trr2.index[-1]
if v>100:
	touch_ratings_idx.append(y)
# Get a datframe with rows containing the required touch ratings:
touch_ratings_df=df[df.index.isin(touch_ratings_idx)]
# 4. Get a list with the corresponding touch ratings strings:
touch_ratings_strings= [r for r in touch_ratings_df['Var2']]
# Filter the rating as an integer and separate it from the string:  
touch = []
for b in touch_ratings_strings: 
	touch_ratings=re.findall(r"\d+", b)
	x= [int(i) for i in touch_ratings]
	touch.extend(x)

# Pictures:
# 1. A dataframe that contain all the rows containing the string (DrawPicture):
draw_pictures_rows = df[df['Var2'].str.contains('DrawPicture')]
# Copy ofthe data frame to avoid SettingWithCopy error:
dpr2=draw_pictures_rows.copy()
# 2. Make a third column containing the differences between the indexes of dpr2:
dpr2['Diff_indexes'] = dpr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 1000 (to include the first row)!:
dpr2.iat[0,2]= 1000
#3. Make a data frame of all the rows in which the differnce in indexs is more than 70:
pictures_ratings_df= dpr2[dpr2['Diff_indexes']>70]
# 4. Get a list with the corresponding picture:
pictures_strings= [r for r in pictures_ratings_df['Var2']]
pictures = [x[11:] for x in pictures_strings]

#Final Results:
# Make a data frame of the pictures and their corresponding ratings:
data_dictionary={'picture':pictures, 'pleasant': pleasant, 'unpleasant': unpleasant, 'touch_sensation':touch}
whole_ratings_df=pd.DataFrame(data_dictionary)
# Show the pictures with the highest ratings (pleasant):
whole_pleasant_ratings_df=whole_ratings_df[whole_ratings_df['picture'].isin(['Silk','Brush2','Cat','Chick1'])]
pleasant_results= whole_pleasant_ratings_df.groupby('picture').agg({'pleasant':['mean']})
pleasant_results2=whole_pleasant_ratings_df.groupby('picture').agg({'touch_sensation':['mean']})
print(pleasant_results)
print(pleasant_results2)
# Show the pictures with the highest ratings (aversive) :
whole_aversive_ratings_df=whole_ratings_df[whole_ratings_df['picture'].isin(['Oyster1','Spider','Tongue','Worms'])]
aversive_results= whole_aversive_ratings_df.groupby('picture').agg({'unpleasant':['mean']})
aversive_results2= whole_aversive_ratings_df.groupby('picture').agg({'touch_sensation':['mean']})
print(aversive_results)
print(aversive_results2)