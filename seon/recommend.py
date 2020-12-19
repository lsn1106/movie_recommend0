#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import datetime as pydatetime
import numpy as np
from scipy.sparse.linalg import svds

class recommend:
    def __init__(self, userID):
        self.uId = userID;
        self.pivot_table = pd.DataFrame();
        
    def add(self, movieTitle, score):
        movies_df = pd.read_csv("./data/movie_cert_test.csv")
        ratings_df = pd.read_csv("./data/rating_cert_test.csv")
        
        #movieTitle이 movie_cert_test.csv에 없다면 에러 출력후 리턴
        temp = movies_df[movies_df['title']==movieTitle]
        if len(temp)<1 or len(temp)>2:
            print("해당 영화가 없거나 에러 존재합니다. 다시 입력하세요")
            return
        
        movieId = temp.iloc[0]['movieId']
        
        #현재 timestamp
        currTime = int(pydatetime.datetime.now().timestamp())
        
        #rating_cert_test 추가 
        toAppend = {"userId" : self.uId, "movieId" : movieId, 
                    "rating": score, "timestamp": currTime}
        
        ratings_df = ratings_df.append(toAppend, ignore_index=True)
        
        ratings_df.to_csv("./data/rating_cert_test.csv", index=False)
        
    def prediction(self, num_recommendations):
        movies_df = pd.read_csv("./data/movie_cert_test.csv")
        ratings_df = pd.read_csv("./data/rating_cert_test.csv")
        
        pivot_df = ratings_df.pivot(index = 'userId', columns = 'movieId', values='rating').fillna(0)
        
        
        #####make_prediction_df 부분####
        R = pivot_df.values
        
        #user_rating_mean은 사용자의 평균 평점
        user_ratings_mean = np.mean(R, axis = 1)
    
        #R_demeaned : 사용자-영화 테이블에 대해 사용자 평균 평점을 뺀 것
        R_demeaned = R - user_ratings_mean.reshape(-1, 1)
        
        #U 행렬, sigma 행렬, V전치행렬을 반환.
        #이때 spicy에 있는 svd를 이용한다.
        U, sigma, Vt = svds(R_demeaned, k = 50)
    
        #sigma는 0이 포함되지 않은 값으로만 구성되어 있다.
        #sigma를 0이 포함된 대칭 행렬로 변환한다.
        sigma = np.diag(sigma)
    
        #SVD가 적용되어 분해된 R_demeaned를 원본 행렬로 복구
        #구한 원본 행렬에 사용자 평균 rating을 더해준다.
        all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1,1)
    
        preds_df = pd.DataFrame(all_user_predicted_ratings, columns = pivot_df.columns)
        
        
        
        #####recommend_movies부분#####
        
        #인덱스로 변환해주어야 해서 -1 
        user_row_number = list(pivot_df.index).index(self.uId)
    
        #앞에서 만든 prediction행렬을 사용자 인덱스에 따라 영화 정렬 -> 영화 평점이 높은 순으로 정렬
        sorted_user_predictions = preds_df.iloc[user_row_number].sort_values(ascending=False)
        
    
        #원본 rating_data에서 user_id에 해당하는 데이터를 뽑아낸다.
        new_data = pivot_df.loc[[self.uId]]
        watched_movies = []
        for c in pivot_df.columns.to_list():
            if new_data.iloc[0][c] != 0:
                watched_movies.append(c)
                
        recommendations = pd.merge(sorted_user_predictions, movies_df, on='movieId')
        
        recommendations = recommendations[~recommendations['movieId'].isin(watched_movies)]
        
        ##user_data와 원본 영화 데이터를 합친다.
        #user_full = (user_data.merge(movies_df, how = 'left', on='movieId').sort_values(['rating'], ascending=False))
        #
        ##원본 영화 데이터에서 사용자가 본 영화를 제외한 데이터 추출
        ##.merge로 sorted_user_predcitions와 user_full데이터를 합친다.
        ##.rename으로 컬럼 이름을 바꾸고 정렬한다
        #recommendations = (movies_df[~movies_df['movieId'].isin(user_full['movieId'])].
        # merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',left_on='movieId',right_on='index').
        # rename(columns = {user_row_number: 'Predictions'}).
        # sort_values('Predictions', ascending = False))
                       
        return recommendations['title'][:num_recommendations].to_list()

