# EDEZE

An E-Classroom platform named EDEZE : Education with Ease.

Below are some of the features offered:

- Three user level : Admin, Teacher, Student with class and course based approach.
- Supports proctored exams.
- Malpractices can be tracked leading to termination of exam.
- Exam supports multiple types of questions (objective and subjective with rich editor).
- Automatic grading of submitted answers based on NLP.
- Personalized feedbacks and analytics after exams.
- Assignment facility available for pratice.
- Mock exam also available for pratice.
- Google enhanced search also available within for learning purposes.

## Setup

1. Created a virtual environment `python -m venv venv`
2. Activate the virtual environment `.\venv\Scripts\activate`
3. Install dependencies `pip install -r requirements.txt`
4. Install language check using `pip install git+https://github.com/MCFreddie777/language-check.git` , as normal installation not supported.
5. Launch the application `python manage.py runserver`

## ENV Location

Store the env in the path `utility_functions/.env` . The format of env should be :

```
SQL_HOST= HOSTIP
SQL_USER= USERNAME
SQL_PASSWORD= PASSWORD
SQL_DB= DBNAME
```
