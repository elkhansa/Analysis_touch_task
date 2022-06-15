import pandas as pd
import numpy as np
import re
from statistics import mean

# Import and read the log file from the current domain (txt to csv):
# Convert the txt file to csv and name the columns:
read_file = pd.read_csv (r'file path.txt', sep='\t')
read_file.to_csv (r'file path.csv', index=None)
df = pd.read_csv (r'file path.csv', header=None)
df.rename(columns={df.columns[1]: "Var2", df.columns[0]: "Var1"}, inplace=True)

# Touch Ratings:
# A. Stimulation touch ratings:
# 1. A dataframe that contain all the rows containing the string (DrawRatingStimulationTouch):
stim_touch_ratings_rows = df[df['Var2'].str.contains('DrawRatingStimulationTouch')]
# Copy of the data frame to avoid SettingWithCopy error:
strr2=stim_touch_ratings_rows.copy()
# 2. Make a third column containing the differences between the indexes of trr2:
strr2['Diff_indexes'] = strr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 0:
strr2.iat[0,2]= 0
# 3. Make a list of the indexes of the rows that contain the touch ratings:
# Rows are the last ones in each rating blocks:
stim_touch_ratings_idx= strr2.loc[strr2["Diff_indexes"].gt(50).shift(-1, fill_value=False)].index.tolist() + [strr2.index[-2]]
# In case the last row had a value >50 (i.e the participant didn't move the cursor and chose the first rating appeared):
v=strr2.iloc[-1]['Diff_indexes']
y=strr2.index[-1]
if v>50:
	stim_touch_ratings_idx.append(y)
# Get a datframe with rows containing the required touch ratings:
stim_touch_ratings_df=df[df.index.isin(stim_touch_ratings_idx)]

# B. Anticipation Touch Ratings:
# 1. A dataframe that contain all the rows containing the string (DrawRatingAnticipationOnlyTouch):
anti_touch_ratings_rows = df[df['Var2'].str.contains('DrawRatingAnticipationOnlyTouch')]
# Copy of the data frame to avoid SettingWithCopy error:
atrr2=anti_touch_ratings_rows.copy()
# 2. Make a third column containing the differences between the indexes of trr2:
atrr2['Diff_indexes'] = atrr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 0:
atrr2.iat[0,2]= 0
# 3. Make a list of the indexes of the rows that contain the touch ratings:
# Rows are the last ones in each rating blocks:
anti_touch_ratings_idx= atrr2.loc[atrr2["Diff_indexes"].gt(50).shift(-1, fill_value=False)].index.tolist() + [atrr2.index[-2]]
# In case the last row had a value >50 (i.e the participant didn't move the cursor and chose the first rating appeared):
v=atrr2.iloc[-1]['Diff_indexes']
y=atrr2.index[-1]
if v>50:
	anti_touch_ratings_idx.append(y)
# Get a datframe with rows containing the required touch ratings:
anti_touch_ratings_df=df[df.index.isin(anti_touch_ratings_idx)]

# C, D, and E steps are done once per code:
# C. Background Yellow:
# 1. A dataframe that contain all the rows containing the string (DrawBackgroundYellow):
draw_yellow_rows = df[df['Var2'].str.contains('DrawBackgroundYellow')]
# Copy of the data frame to avoid SettingWithCopy error:
dyr2=draw_yellow_rows.copy()
# 2. Make a third column containing the differences between the indexes of dyr2:
dyr2['Diff_indexes'] = dyr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 1000 (to include the first row)!:
dyr2.iat[0,2]= 1000
#3. Make a data frame of all the rows in which the differnce in indexs is more than 20:
specific_yellow_rows_df= dyr2[dyr2['Diff_indexes']>20]

# D. Background Red:
# 1. A dataframe that contain all the rows containing the string (DrawBackgroundRed):
draw_red_rows = df[df['Var2'].str.contains('DrawBackgroundRed')]
# Copy of the data frame to avoid SettingWithCopy error:
drr2=draw_red_rows.copy()
# 2. Make a third column containing the differences between the indexes of dyr2:
drr2['Diff_indexes'] = drr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 1000 (to include the first row)!:
drr2.iat[0,2]= 1000
#3. Make a data frame of all the rows in which the differnce in indexs is more than 20:
specific_red_rows_df= drr2[drr2['Diff_indexes']>20]

# E. General dataframe (Aversive and Pleasant) (Yellow and Red):
# Generate a general dataframe that contain all the wanted aversive and pleasant rows (Yellow and Red) (combined according to their index order):
general_yandr_df = pd.concat([specific_yellow_rows_df, specific_red_rows_df], sort=False).sort_index()
# Rename the column (Var2) to not be mixed with the column from the behavioral measuremnets' dataframes:
general_yandr_df = general_yandr_df.rename(columns={'Var2': 'colour'})
# Reset indexes (to later add the column from one dataframe to the other):
general_yandr_df = general_yandr_df.reset_index(drop=True)

# F, G, and H are done per behavioral measure:
# F. General dataframe (Touch ratings) (both in the anticipation and stimulation state):
# Generate a general dataframe that contain all the stimulation and anticpation rows (for the touch)(combined according to their index order):
general_stimandanti_touch_df= pd.concat([stim_touch_ratings_df, anti_touch_ratings_df], sort=False).sort_index()
# Reset indexes (to later add the column from one dataframe to the other):
general_stimandanti_touch_df = general_stimandanti_touch_df.reset_index(drop=True)
# Add (colour) column from the aversive and pleasant dataframeto the touch ratings dataframe:
general_stimandanti_touch_df[['colour']] = general_yandr_df[['colour']].to_numpy()

# G. Touch ratings for Yellow case:
# A dataframe that contain touch ratings only when the background colour is Yellow:
yel_touch_df=general_stimandanti_touch_df[general_stimandanti_touch_df['colour'].isin(['DrawBackgroundYellow'])]
# 1. A dataframe that contain touch ratings when the background colour is yellow and the anticipation phase:
yel_anti_touch_df = yel_touch_df[yel_touch_df['Var2'].str.contains('DrawRatingAnticipationOnlyTouch')]
# Get a list with the corresponding touch ratings strings:
yel_anti_touch_strings= [r for r in yel_anti_touch_df['Var2']]
# Filter the rating as an integer and separate it from the string:
yel_anti_touch_ratings = []
for b in yel_anti_touch_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	yel_anti_touch_ratings.extend(x)
# get the mean of ratings:
yel_anti_touch_ratings_mean= mean(yel_anti_touch_ratings)
print('yellow.touch.anticipation=', yel_anti_touch_ratings_mean)
# 2. A dataframe that contain touch ratings when the background colour is yellow and the stimulation phase:
yel_stim_touch_df = yel_touch_df[yel_touch_df['Var2'].str.contains('DrawRatingStimulationTouch')]
# Get a list with the corresponding touch ratings strings:
yel_stim_touch_strings= [r for r in yel_stim_touch_df['Var2']]
# Filter the rating as an integer and separate it from the string:
yel_stim_touch_ratings = []
for b in yel_stim_touch_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	yel_stim_touch_ratings.extend(x)
# get the mean of ratings:
yel_stim_touch_ratings_mean= mean(yel_stim_touch_ratings)
print('yellow.touch.stimulation=', yel_stim_touch_ratings_mean)

# H. Touch ratings for Red case:
# A dataframe that contain touch ratings only when the background colour is Red:
red_touch_df=general_stimandanti_touch_df[general_stimandanti_touch_df['colour'].isin(['DrawBackgroundRed'])]
# 1. A dataframe that contain touch ratings when the background colour is Red and the anticipation phase:
red_anti_touch_df = red_touch_df[red_touch_df['Var2'].str.contains('DrawRatingAnticipationOnlyTouch')]
# Get a list with the corresponding touch ratings strings:
red_anti_touch_strings= [r for r in red_anti_touch_df['Var2']]
# Filter the rating as an integer and separate it from the string:
red_anti_touch_ratings = []
for b in red_anti_touch_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	red_anti_touch_ratings.extend(x)
# get the mean of ratings:
red_anti_touch_ratings_mean= mean(red_anti_touch_ratings)
print('red.touch.anticipation=', red_anti_touch_ratings_mean)
# 2. A dataframe that contain touch ratings when the background colour is red and the stimulation phase:
red_stim_touch_df = red_touch_df[red_touch_df['Var2'].str.contains('DrawRatingStimulationTouch')]
# Get a list with the corresponding touch ratings strings:
red_stim_touch_strings= [r for r in red_stim_touch_df['Var2']]
# Filter the rating as an integer and separate it from the string:
red_stim_touch_ratings = []
for b in red_stim_touch_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	red_stim_touch_ratings.extend(x)
# get the mean of ratings:
red_stim_touch_ratings_mean= mean(red_stim_touch_ratings)
print('red.touch.stimulation=', red_stim_touch_ratings_mean)


# Unpleasant Ratings:
# A. Stimulation unpleasant Ratings:
# 1. A dataframe that contain all the rows containing the string (DrawRatingStimulationUnpleasantness):
stim_unpleasant_ratings_rows = df[df['Var2'].str.contains('DrawRatingStimulationUnpleasantness')]
# Copy of the data frame to avoid SettingWithCopy error:
suprr2=stim_unpleasant_ratings_rows.copy()
# 2. Make a third column containing the differences between the indexes of prr2:
suprr2['Diff_indexes'] = suprr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 0:
suprr2.iat[0,2]= 0
# 3. Make a list of the indexes of the rows that contain the pleasant ratings:
# Rows are the last ones in each rating blocks:
stim_unpleasant_ratings_idx= suprr2.loc[suprr2["Diff_indexes"].gt(50).shift(-1, fill_value=False)].index.tolist() + [suprr2.index[-1]]
# In case the last row had a value >50 (i.e the participant didn't move the cursor and chose the first rating appeared):
v=suprr2.iloc[-1]['Diff_indexes']
y=suprr2.index[-1]
if v>50:
	stim_unpleasant_ratings_idx.append(y)
# Get a datframe with rows containing the required pleasant ratings:
stim_unpleasant_ratings_df=df[df.index.isin(stim_unpleasant_ratings_idx)]

# B. Anticipation unpleasant Ratings:
# 1. A dataframe that contain all the rows containing the string (DrawRatingAnticipationOnlyUnpleasantness):
anti_unpleasant_ratings_rows = df[df['Var2'].str.contains('DrawRatingAnticipationOnlyUnpleasantness')]
# Copy of the data frame to avoid SettingWithCopy error:
auprr2=anti_unpleasant_ratings_rows.copy()
# 2. Make a third column containing the differences between the indexes of prr2:
auprr2['Diff_indexes'] = auprr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 0:
auprr2.iat[0,2]= 0
# 3. Make a list of the indexes of the rows that contain the pleasant ratings:
# Rows are the last ones in each rating blocks:
anti_unpleasant_ratings_idx= auprr2.loc[auprr2["Diff_indexes"].gt(50).shift(-1, fill_value=False)].index.tolist() + [auprr2.index[-1]]
# In case the last row had a value >50 (i.e the participant didn't move the cursor and chose the first rating appeared):
v=auprr2.iloc[-1]['Diff_indexes']
y=auprr2.index[-1]
if v>50:
	anti_unpleasant_ratings_idx.append(y)
# Get a datframe with rows containing the required pleasant ratings:
anti_unpleasant_ratings_df=df[df.index.isin(anti_unpleasant_ratings_idx)]

# F. General dataframe (unpleasant ratings) (both in the anticipation and stimulation state):
# Generate a general dataframe that contain all the stimulation and anticpation rows (for the unpleasant)(combined according to their index order):
general_stimandanti_upl_df= pd.concat([stim_unpleasant_ratings_df, anti_unpleasant_ratings_df], sort=False).sort_index()
# Reset indexes (to later add the column from one dataframe to the other):
general_stimandanti_upl_df = general_stimandanti_upl_df.reset_index(drop=True)
# Add (colour) column from the aversive and pleasant dataframeto the unpleasant ratings dataframe:
general_stimandanti_upl_df[['colour']] = general_yandr_df[['colour']].to_numpy()

# G. Unpleasant ratings for Yellow case:
# A dataframe that contain unpleasant ratings only when the background colour is Yellow:
yel_upl_df=general_stimandanti_upl_df[general_stimandanti_upl_df['colour'].isin(['DrawBackgroundYellow'])]
# 1. A dataframe that contain unpleasant ratings when the background colour is yellow and the anticipation phase:
yel_anti_upl_df = yel_upl_df[yel_upl_df['Var2'].str.contains('DrawRatingAnticipationOnlyUnpleasantness')]
# Get a list with the corresponding pleasant ratings strings:
yel_anti_upl_strings= [r for r in yel_anti_upl_df['Var2']]
# Filter the rating as an integer and separate it from the string:
yel_anti_upl_ratings = []
for b in yel_anti_upl_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	yel_anti_upl_ratings.extend(x)
# get the mean of ratings:
yel_anti_upl_ratings_mean= mean(yel_anti_upl_ratings)
print('yellow.unpleasant.anticipation=', yel_anti_upl_ratings_mean)
# 2. A dataframe that contain unpleasant ratings when the background colour is yellow and the stimulation phase:
yel_stim_upl_df = yel_upl_df[yel_upl_df['Var2'].str.contains('DrawRatingStimulationUnpleasantness')]
# Get a list with the corresponding pleasant ratings strings:
yel_stim_upl_strings= [r for r in yel_stim_upl_df['Var2']]
# Filter the rating as an integer and separate it from the string:
yel_stim_upl_ratings = []
for b in yel_stim_upl_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	yel_stim_upl_ratings.extend(x)
# get the mean of ratings:
yel_stim_upl_ratings_mean= mean(yel_stim_upl_ratings)
print('yellow.unpleasant.stimulation=', yel_stim_upl_ratings_mean)

# H. Unpleasant ratings for Red case:
# A dataframe that contain unpleasant ratings only when the background colour is Red:
red_upl_df=general_stimandanti_upl_df[general_stimandanti_upl_df['colour'].isin(['DrawBackgroundRed'])]
# 1. A dataframe that contain unpleasant ratings when the background colour is Red and the anticipation phase:
red_anti_upl_df = red_upl_df[red_upl_df['Var2'].str.contains('DrawRatingAnticipationOnlyUnpleasantness')]
# Get a list with the corresponding pleasant ratings strings:
red_anti_upl_strings= [r for r in red_anti_upl_df['Var2']]
# Filter the rating as an integer and separate it from the string:
red_anti_upl_ratings = []
for b in red_anti_upl_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	red_anti_upl_ratings.extend(x)
# get the mean of ratings:
red_anti_upl_ratings_mean= mean(red_anti_upl_ratings)
print('red.unpleasant.anticipation=', red_anti_upl_ratings_mean)
# 2. A dataframe that contain unpleasant ratings when the background colour is red and the stimulation phase:
red_stim_upl_df = red_upl_df[red_upl_df['Var2'].str.contains('DrawRatingStimulationUnpleasantness')]
# Get a list with the corresponding unpleasant ratings strings:
red_stim_upl_strings= [r for r in red_stim_upl_df['Var2']]
# Filter the rating as an integer and separate it from the string:
red_stim_upl_ratings = []
for b in red_stim_upl_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	red_stim_upl_ratings.extend(x)
# get the mean of ratings:
red_stim_upl_ratings_mean= mean(red_stim_upl_ratings)
print('red.unpleasant.stimulation=', red_stim_upl_ratings_mean)


# PLeasant ratings:
# A. Stimulation pleasant Ratings:
# 1. A dataframe that contain all the rows containing the string (DrawRatingStimulationPleasantness):
stim_pleasant_ratings_rows = df[df['Var2'].str.contains('DrawRatingStimulationPleasantness')]
# Copy of the data frame to avoid SettingWithCopy error:
sprr2=stim_pleasant_ratings_rows.copy()
# 2. Make a third column containing the differences between the indexes of prr2:
sprr2['Diff_indexes'] = sprr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 0:
sprr2.iat[0,2]= 0
# 3. Make a list of the indexes of the rows that contain the pleasant ratings:
# Rows are the last ones in each rating blocks:
stim_pleasant_ratings_idx= sprr2.loc[sprr2["Diff_indexes"].gt(50).shift(-1, fill_value=False)].index.tolist() + [sprr2.index[-1]]
# In case the last row had a value >50 (i.e the participant didn't move the cursor and chose the first rating appeared):
v=sprr2.iloc[-1]['Diff_indexes']
y=sprr2.index[-1]
if v>50:
	stim_pleasant_ratings_idx.append(y)
# Get a datframe with rows containing the required pleasant ratings:
stim_pleasant_ratings_df=df[df.index.isin(stim_pleasant_ratings_idx)]

# B. Anticipation pleasant Ratings:
# 1. A dataframe that contain all the rows containing the string (DrawRatingAnticipationOnlyPleasantness):
anti_pleasant_ratings_rows = df[df['Var2'].str.contains('DrawRatingAnticipationOnlyPleasantness')]
# Copy of the data frame to avoid SettingWithCopy error:
aprr2=anti_pleasant_ratings_rows.copy()
# 2. Make a third column containing the differences between the indexes of prr2:
aprr2['Diff_indexes'] = aprr2.index.to_series().diff()
# Giving the first item of the coloumn a value of 0:
aprr2.iat[0,2]= 0
# 3. Make a list of the indexes of the rows that contain the pleasant ratings:
# Rows are the last ones in each rating blocks:
anti_pleasant_ratings_idx= aprr2.loc[aprr2["Diff_indexes"].gt(50).shift(-1, fill_value=False)].index.tolist() + [aprr2.index[-1]]
# In case the last row had a value >50 (i.e the participant didn't move the cursor and chose the first rating appeared):
v=aprr2.iloc[-1]['Diff_indexes']
y=aprr2.index[-1]
if v>50:
	anti_pleasant_ratings_idx.append(y)
# Get a datframe with rows containing the required pleasant ratings:
anti_pleasant_ratings_df=df[df.index.isin(anti_pleasant_ratings_idx)]

# F. General dataframe (Pleasant ratings) (both in the anticipation and stimulation state):
# Generate a general dataframe that contain all the stimulation and anticpation rows (for the pleasant)(combined according to their index order):
general_stimandanti_pl_df= pd.concat([stim_pleasant_ratings_df, anti_pleasant_ratings_df], sort=False).sort_index()
# Reset indexes (to later add the column from one dataframe to the other):
general_stimandanti_pl_df = general_stimandanti_pl_df.reset_index(drop=True)
# Add (colour) column from the aversive and pleasant dataframeto the pleasant ratings dataframe:
general_stimandanti_pl_df[['colour']] = general_yandr_df[['colour']].to_numpy()

# G. Pleasant ratings for Yellow case:
# A dataframe that contain pleasant ratings only when the background colour is Yellow:
yel_pl_df=general_stimandanti_pl_df[general_stimandanti_pl_df['colour'].isin(['DrawBackgroundYellow'])]
# 1. A dataframe that contain pleasant ratings when the background colour is yellow and the anticipation phase:
yel_anti_pl_df = yel_pl_df[yel_pl_df['Var2'].str.contains('DrawRatingAnticipationOnlyPleasantness')]
# Get a list with the corresponding pleasant ratings strings:
yel_anti_pl_strings= [r for r in yel_anti_pl_df['Var2']]
# Filter the rating as an integer and separate it from the string:
yel_anti_pl_ratings = []
for b in yel_anti_pl_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	yel_anti_pl_ratings.extend(x)
# get the mean of ratings:
yel_anti_pl_ratings_mean= mean(yel_anti_pl_ratings)
print('yellow.pleasant.anticipation=', yel_anti_pl_ratings_mean)
# 2. A dataframe that contain pleasant ratings when the background colour is yellow and the stimulation phase:
yel_stim_pl_df = yel_pl_df[yel_pl_df['Var2'].str.contains('DrawRatingStimulationPleasantness')]
# Get a list with the corresponding pleasant ratings strings:
yel_stim_pl_strings= [r for r in yel_stim_pl_df['Var2']]
# Filter the rating as an integer and separate it from the string:
yel_stim_pl_ratings = []
for b in yel_stim_pl_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	yel_stim_pl_ratings.extend(x)
# get the mean of ratings:
yel_stim_pl_ratings_mean= mean(yel_stim_pl_ratings)
print('yellow.pleasant.stimulation=', yel_stim_pl_ratings_mean)

# H. Pleasant ratings for Red case:
# A dataframe that contain pleasant ratings only when the background colour is Red:
red_pl_df=general_stimandanti_pl_df[general_stimandanti_pl_df['colour'].isin(['DrawBackgroundRed'])]
# 1. A dataframe that contain pleasant ratings when the background colour is Red and the anticipation phase:
red_anti_pl_df = red_pl_df[red_pl_df['Var2'].str.contains('DrawRatingAnticipationOnlyPleasantness')]
# Get a list with the corresponding pleasant ratings strings:
red_anti_pl_strings= [r for r in red_anti_pl_df['Var2']]
# Filter the rating as an integer and separate it from the string:
red_anti_pl_ratings = []
for b in red_anti_pl_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	red_anti_pl_ratings.extend(x)
# get the mean of ratings:
red_anti_pl_ratings_mean= mean(red_anti_pl_ratings)
print('red.pleasant.anticipation=', red_anti_pl_ratings_mean)
# 2. A dataframe that contain pleasant ratings when the background colour is red and the stimulation phase:
red_stim_pl_df = red_pl_df[red_pl_df['Var2'].str.contains('DrawRatingStimulationPleasantness')]
# Get a list with the corresponding pleasant ratings strings:
red_stim_pl_strings= [r for r in red_stim_pl_df['Var2']]
# Filter the rating as an integer and separate it from the string:
red_stim_pl_ratings = []
for b in red_stim_pl_strings:
	ratings=re.findall(r"\d+", b)
	x= [int(i) for i in ratings]
	red_stim_pl_ratings.extend(x)
# get the mean of ratings:
red_stim_pl_ratings_mean= mean(red_stim_pl_ratings)
print('red.pleasant.stimulation=', red_stim_pl_ratings_mean)