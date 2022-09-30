# # -*- coding: utf-8 -*-
# """
# Created on Thu Aug 11 06:31:29 2022

# @author: onais

import pandas as pd
from thefuzz import process
df1 = pd.DataFrame({'col_a':[ 'Owais Khan Mohammed', 'King Khan Mohammed', 'Saleem Khan Mohammed K'],'col_b':[1001,1002,1003]})
df2 = pd.DataFrame({'col_a':['Onais Mohammed', 'Owais Mohammed', 'King Khan Mohamed', 'Saleem Khan Mohad'],'col_b':[2001,2002,2003,2004]})

def fuzzy_match(
    df_left, df_right, column_left, column_right, threshold=90, limit=1):
    # Create a series
    series_matches = df_left[column_left].apply(
        lambda x: process.extract(x, df_right[column_right], limit=limit) )           # Creates a series with id from df_left and column name _column_left_, with _limit_ matches per item)

    # Convert matches to a tidy dataframe
    df_matches = series_matches.to_frame()
    df_matches = df_matches.explode(column_left)     # Convert list of matches to rows
    df_matches[['match_string', 'match_score', 'df_right_id']] = pd.DataFrame(df_matches[column_left].tolist(), index=df_matches.index)       # Convert match tuple to columns
    df_matches.drop(column_left, axis=1, inplace=True)      # Drop column of match tuples

    # Reset index, as in creating a tidy dataframe we've introduced multiple rows per id, so that no longer functions well as the index
    if df_matches.index.name:
        index_name = df_matches.index.name     # Stash index name
    else:
        index_name = 'index'        # Default used by pandas
    df_matches.reset_index(inplace=True)
    df_matches.rename(columns={index_name: 'df_left_id'}, inplace=True)       # The previous index has now become a column: rename for ease of reference

    # Drop matches below threshold
    df_matches.drop(
        df_matches.loc[df_matches['match_score'] < threshold].index,
        inplace=True)

    return df_matches



df_matches = fuzzy_match(
    df1,
    df2,
    'col_a',
    'col_a',
    threshold=60,
    limit=1
)

df_output = df1.merge(
    df_matches,
    how='left',
    left_index=True,
    right_on='df_left_id'
).merge(
    df2,
    how='left',
    left_on='df_right_id',
    right_index=True,
    suffixes=['_df1', '_df2']
)

df_output.set_index('df_left_id', inplace=True)       # For some reason the first merge operation wrecks the dataframe's index. Recreated from the value we have in the matches lookup table

df_output = df_output[['col_a_df1', 'col_b_df1', 'col_b_df2']]      # Drop columns used in the matching
df_output.index.name = 'id'
print(df_output)

