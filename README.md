# movie_recommend0
20-2 인빅 프로젝트

## 필터링

### movie_filter(input_data, year, genres)
<details>
<summary>details</summary>

#### parameters : 
- input_data (DataFrame): movie.csv에서 읽은 DataFrame. 
        
- year (integer): year 미만 영화는 거릅니다.
        
- genres (array of string): 분류된 모든 장르가 genres배열에 포함되지 않는 영화는 거릅니다.

#### return (DataFrame): 
-    year 컬럼이 추가되고 조건에 맞게 필터링된 DataFrame
    
#### comment
- title이 (year)로 끝나지 않는 15개의 영화는 아예 제외했습니다. (ex. movield 7789)
- year컬럼을 추가했습니다.
- genres를 구분자 '|' 기준으로 파싱하여 문자열의 배열로 변환했습니다.
- input_data로 입력된 DataFrame 객체의 원형은 바뀌지 않습니다.
</details>

