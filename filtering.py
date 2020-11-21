import pandas as pd
import numpy as np

"""
parameters : 
    input_data (DataFrame)
        : movie.csv에서 읽은 DataFrame.
          입력된 DataFrame 객체의 원형은 바뀌지 않습니다.
        
    year (integer)
        : year 미만 영화는 거릅니다.
        
    genres (array of string)
        : 분류된 모든 장르가 genres배열에 포함되지 않는 영화는 거릅니다.


return (DataFrame): 
    year 컬럼이 추가되고 조건에 맞게 필터링된 DataFrame
    

*
title이 (year)로 끝나지 않는 15개의 영화는 아예 제외했습니다.
(ex. movield 7789)
       
"""
def movie_filter(input_data, year=0, genres=[]):
    data = input_data.copy() 
    
    data['year'] = data['title'].str[-5:-1]
    data['year'] = pd.to_numeric(data['year'], downcast='integer', errors='coerce')
    data = data.dropna(axis=0)    
    
    data['genres'] = data['genres'].str.split('|')
    
    data = data[data['year']>=year]
    
    mask = []
    for genre_ in data['genres']:
        mask.append(True if np.intersect1d(genre_, genres).size > 0 else False) 
            
    data = data[mask]
    
    return data




"""
parameters : 
    input_data (DataFrame) 
        : rating.csv에서 읽은 DataFrame.
          입력된 DataFrame 객체의 원형은 바뀌지 않습니다.
    
    threshold (integer)
        : 평가횟수가 threshold 미만인 유저는 거릅니다.
        
return :
    필터링된 rating DataFrame

"""
def rating_filter(input_data, threshold = 100):
    data = input_data.copy()
    
    x = data['userId'].value_counts()>=threshold
    y = x[x].index
    data = data[data['userId'].isin(y)]
    
    return data

