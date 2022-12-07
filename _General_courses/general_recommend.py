import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3

# df_lecture = pd.read_csv('general_courses.csv', encoding='utf_8_sig')
# df_lecture['teacher_course'] = df_lecture['teacher'] + ' - ' + df_lecture['course_name']
# df_lecture = df_lecture.reindex(columns=['id', 'teacher', 'course_name', 'teacher_course', 'assignment', 'test', 'in_group', 'attend', 'report'])
# df_lecture = df_lecture.drop(labels=range(270, 350), axis=0)
# df_lecture['ratings'] = ''
# df_lecture
# df_student = pd.DataFrame(columns=['user1'], index=['assignment', 'test', 'in_group', 'attend', 'report'])
# df_student['user1'] = [1, 5, 0, 5, 0]
# rating = list(df_student['user1'])

def read_data():
    df_lecture = pd.read_csv('general_courses.csv', encoding='utf_8_sig')
    df_lecture['teacher_course'] = df_lecture['teacher'] + ' - ' + df_lecture['course_name']
    df_lecture = df_lecture.reindex(columns=['id', 'teacher', 'course_name', 'teacher_course', 'assignment', 'test', 'in_group', 'attend', 'report'])
    df_lecture = df_lecture.drop(labels=range(270, 350), axis=0)
    df_lecture['ratings'] = ''

    types = ['assignment', 'test', 'in_group', 'attend', 'report']
    s = []
    for i in range(len(df_lecture)):
        for type in types:
            s.append(df_lecture.at[i, type])
        df_lecture.at[i, 'ratings'] = s
        s = []
    return df_lecture

def combine(df_lecture):
    types = ['assignment', 'report', 'test', 'in_group', 'attend']
    s = []
    features = {}
    for i in range(1, len(df_lecture.index)):
        for type in types:
            s.append(df_lecture.at[i, type])
        features[df_lecture.at[i, 'teacher_course']] = s
        s = []
    return features

def create_student(user_id):
    df_student = pd.DataFrame(columns=['user1'], index=['assignment', 'test', 'in_group', 'attend', 'report'])

# def get_student_rating(id, df_student):
#     return df_student[id]
# test = np.array(get_student_rating('user1'))

# def con_sql():
    # con = sqlite3.connect('general_courses.db')
    # cur = con.cursor()
    # with open('temp_GC.csv', 'r', encoding='utf_8_sig') as file:
    #     for row in file:
    #         cur.execute('INSERT INTO General_courses VALUES (?,?,?,?,?,?,?,?,?,?)', row.split(','))
    #         con.commit()
    # con.close()
    # for i in range(len(df_lecture.index)):
    #     if int(df_lecture.iloc[i, 4]) == 1:
    #     df_lecture.iloc[i, 4] = float(10)

# def recommend(course_name):
#     temp = {}
#     for course in features.keys():
#         temp[course] = cosine_similarity([features[course_name]], [features[course]])[0][0]
#     temp.pop(course_name)
#     top = sorted(temp.items(), key=lambda x: x[1], reverse=True)
#     top = top[1:12]
#     for i in range(10):
#         print(top[i][0])
#     print(top)
# recommend('姜杰 - 統計與生活')

def recommend(course_name, features):
    temp = pd.DataFrame(columns=['course', 'similarity'], index=range(len(features)))
    for i, course in enumerate(features.keys(), start=1):
        sim = cosine_similarity([features[course_name]], [features[course]])[0][0]
        temp.loc[i] = [course, sim]
    temp = temp.sort_values(by='similarity', ascending=False)
    temp = temp.reset_index(drop=True)
    temp = temp.drop(temp[temp['course'] == course_name].index)
    return temp.loc[:10, ['course', 'similarity']]

def recommend_student(student, features):
    temp = pd.DataFrame(columns=['course', 'similarity'], index=range(len(features)))
    for i, course in enumerate(features.keys()):
        sim = cosine_similarity([student], [features[course]])[0][0]
        temp.loc[i] = [course, sim]
    temp = temp.sort_values(by='similarity', ascending=False)
    temp = temp.reset_index(drop=True)
    return temp.loc[:9, ['course', 'similarity']]

if __name__ == '__main__':
    # create_student()
    lectures = read_data()
    _lectures = combine(lectures)
    Recommendation = recommend('姜杰 - 統計與生活', _lectures)
    # Recommendation2 = recommend_student('user1', _lectures)
    print(Recommendation)