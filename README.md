## API Documentation
https://documenter.getpostman.com/view/32946570/2sA2r82Pmq
## Steps
### Launch services via docker compose
```
docker compose up -d --build
```
The application is running on localhost:8000
### Run the migrations
```
docker exec -it word_search-web-1 bash
python manage.py migrate
```
### POST Register user
```
http://localhost:8000/users/
```
#### Body
```
{
    "name": "John Doe",
    "email": "johndo@eabc.com",
    "dob": "2000-01-01",
    "password1": "johndoe123",
    "password2": "johndoe123"
}
```
#### Response (201-created)
```
{}
```
### POST Login user
```
http://localhost:8000/users/login/
```
#### Body
```
{
    "email": "johndo@eabc.com",
    "password": "johndoe123"
}
```
#### Response (200-ok)
```
{
    "auth_token": "38d798a7f851d95e113bbede6fddcef27119f943"
}
```
### POST Add paragraphs
```
http://localhost:8000/search/paragraphs/
```
#### Request Headers
-------------
Authorization&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  Token 38d798a7f851d95e113bbede6fddcef27119f943
#### Body
```
{
    "text": "In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before the final copy is available. It is also used to temporarily replace text in a process called greeking, which allows designers to consider the form of a webpage or publication, without the meaning of the text influencing the design.\n\nLorem ipsum is typically a corrupted version of De finibus bonorum et malorum, a 1st-century BC text by the Roman statesman and philosopher Cicero, with words altered, added, and removed to make it nonsensical and improper Latin. The first two words themselves are a truncation of dolorem ipsum ('pain itself').\n\nVersions of the Lorem ipsum text have been used in typesetting at least since the 1960s, when it was popularized by advertisements for Letraset transfer sheets.[1] Lorem ipsum was introduced to the digital world in the mid-1980s, when Aldus employed it in graphic and word-processing templates for its desktop publishing program PageMaker. Other popular word processors, including Pages and Microsoft Word, have since adopted Lorem ipsum,[2] as have many LaTeX packages,[3][4][5] web content managers such as Joomla! and WordPress, and CSS libraries such as Semantic UI."
}
```
#### Response (201-created)
```
{}
```
### List Top paragraphs
In the URL below, enter the word to be searched and set top_n = 10 to get the top 10 paragraphs.
```
http://localhost:8000/search/paragraphs/?word=is&top_n=10
```
#### Response
```
[
    "In publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before the final copy is available. It is also used to temporarily replace text in a process called greeking, which allows designers to consider the form of a webpage or publication, without the meaning of the text influencing the design.",
    "Lorem ipsum is typically a corrupted version of De finibus bonorum et malorum, a 1st-century BC text by the Roman statesman and philosopher Cicero, with words altered, added, and removed to make it nonsensical and improper Latin. The first two words themselves are a truncation of dolorem ipsum ('pain itself')."
]
```