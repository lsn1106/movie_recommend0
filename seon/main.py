#!/usr/bin/env python
# coding: utf-8

import recommend as myRecommend

print("**************영화 추천 프로그램***************")
while True:
    userID = int(input("로그인 (-1 to end program): "))
    if userID == -1 : break;
    print()
    
    #객체 생성
    rec = myRecommend.recommend(userID)
    
    while True:
        movieTitle = str(input("영화 제목: "))
        if movieTitle == "": #엔터 한 번 더 누르면 입력 종료
            print("---------------------") 
            break
        score = float(input(movieTitle+" 의 평점: "))
        rec.add(movieTitle, score)
        print();
    
    recommended = rec.prediction(10) #두번째 인자는 추천받을 영화 개수
    print("< ( user",userID,") 님께 추천드리는 영화목록 >")
    for movie in recommended:
        print(movie)
    
    print("\n")