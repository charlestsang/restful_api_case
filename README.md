# Restful_api_case_study
 A a case study of rest api with stackoverflow.com open api data

### 1.Data source: 
sample 3rd party data: api from Stackover 2.3 reslease; running jupyter notebook to extract sample json data.
https://api.stackexchange.com/docs/questions

![image](https://user-images.githubusercontent.com/14142646/147071137-b59f7889-e070-4347-946e-1da56381e1de.png)

### 2.Extract from api and transformed to structured data with python 
![image](https://user-images.githubusercontent.com/14142646/147011323-4a5f001d-a6ad-4e6d-9148-526403813ab6.png)

2.1 Users table:

![image](https://user-images.githubusercontent.com/14142646/147072091-fc55087c-c5f5-45c3-b514-37c3f9377458.png)

2.2 Questions table:

![image](https://user-images.githubusercontent.com/14142646/147072206-67845988-1d13-40c4-a01d-d34b86aba678.png)

2.3 Answers table:

![image](https://user-images.githubusercontent.com/14142646/147072351-a7d2a775-8427-4db9-a0af-692fa03948ba.png)


### 3. Abstract data model
![image](https://user-images.githubusercontent.com/14142646/147070928-74581f03-aa11-496b-a746-146874e8c9e3.png)



## REST API demo from Postman app:

Deploy a restful api with transformed 3rd party data.

![image](https://user-images.githubusercontent.com/14142646/147011161-d66f26d6-4384-4dbd-ae58-b5bf8ea6640c.png)

### GET /users
![image](https://user-images.githubusercontent.com/14142646/147011005-483a729e-832c-4b59-813c-5bbca0cb1d66.png)

### GET /questions
![image](https://user-images.githubusercontent.com/14142646/147011067-ec1dfabd-0361-4aac-a199-7d17ce690661.png)

### GET /answers
![image](https://user-images.githubusercontent.com/14142646/147011114-f4d01e4d-e9b1-4a82-a96b-7af52c484d85.png)

