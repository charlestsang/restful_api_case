#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

# api model stack data in 3 domains

# /users
# sample col: 'user_id','user_type','display_name','location'
users_path = './data/stack_users_sample.csv'

# /questions
# sample col: 'user_id','question_id','title'
ques_path = './data/stack_questions_sample.csv'

# /answers
# sample col: 'answer_id','question_id','is_accepted'
anws_path = './data/stack_answers_sample.csv'

class Users(Resource):
    def get(self):
        data = pd.read_csv(users_path,sep='\t')  # read local CSV file
        data = data.to_dict()  # convert dataframe to dict
        return {'data': data}, 200  # return data and 200 OK

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('user_id', required=True, type = int)  # add args
        parser.add_argument('user_type', required=True, type = str)
        parser.add_argument('display_name', required=True, type= str)
        parser.add_argument('location', required=True, type = str)
        args = parser.parse_args()  # parse arguments to dictionary

        # read  CSV
        data = pd.read_csv(users_path,sep='\t')

        if args['user_id'] in list(data['user_id']):
            return {
                'message': f"'{args['user_id']}' already exists."
            }, 409
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'user_id': [args['user_id']],
                'user_type': [args['user_type']],
                'display_name': [args['display_name']],
                #'location': [args['location']]
                'location': [[]]
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('users_path', index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK

    def put(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('user_id', required=True)  # add args
        parser.add_argument('location', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv(users_path,sep='\t')
        
        if args['user_id'] in list(data['user_id']):
            # evaluate strings of lists to lists 
            data['location'] = data['location'].apply(
                lambda x: ast.literal_eval(x)
            )
            # select our user
            user_data = data[data['user_id'] == args['user_id']]

            # update user's locations
            user_data['location'] = user_data['location'].values[0].append(args['location'])
            
            # save back to CSV
            data.to_csv(users_path, index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the userId does not exist
            return {
                'message': f"'{args['user_id']}' user not found."
            }, 404

    def delete(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('user_id', required=True)  # add userId arg
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv(users_path,sep='\t')
        
        if args['user_id'] in list(data['user_id']):
            # remove data entry matching given userId
            data = data[data['user_id'] != args['user_id']]
            
            # save back to CSV
            data.to_csv(users_path, index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        else:
            # otherwise we return 404 because userId does not exist
            return {
                'message': f"'{args['user_id']}' user not found."
            }, 404

                    
class Questions(Resource):
    def get(self):
        data = pd.read_csv(ques_path, sep='\t')  # read local CSV
        return {'data': data.to_dict()}, 200  # return data dict and 200 OK
    
    def post(self):
        #'user_id','question_id','title'
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('question_id', required=True, type=int)  # add args
        parser.add_argument('title', required=True, type = str)
        parser.add_argument('user_id', required=True, type = int)
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv(ques_path,sep='\t')
    
        # check if question_id already exists
        if args['question_id'] in list(data['question_id']):
            # if locationId already exists, return 401 unauthorized
            return {
                'message': f"'{args['question_id']}' already exists."
            }, 409
        else:
            # otherwise, we can add the new question record
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'question_id': [args['question_id']],
                'title': [args['title']],
                'user_id': [args['user_id']]
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv(ques_path, index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK
    
    def patch(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('question_id', required=True, type=int)  # add args
        parser.add_argument('title', store_missing=False, type = str)  # name/rating are optional
        parser.add_argument('user_id', store_missing=False, type = int)
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv(ques_path,sep='\t')
        
        # check that the location exists
        if args['question_id'] in list(data['question_id']):
            # if it exists, we can update it, first we get user row
            user_data = data[data['question_id'] == args['question_id']]
            
            # if name has been provided, we update name
            if 'title' in args:
                user_data['title'] = args['title']
            # if rating has been provided, we update rating
            if 'user_id' in args:
                user_data['user_id'] = args['user_id']
            
            # update data
            data[data['question_id'] == args['question_id']] = user_data
            # now save updated data
            data.to_csv(ques_path, index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        
        else:
            # otherwise we return 404 not found
            return {
                'message': f"'{args['question_id']}' question does not exist."
            }, 404
    
    def delete(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('question_id', required=True, type=int)  # add question_id arg
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv(ques_path,sep='\t')
        
        # check that the question_id exists
        if args['question_id'] in list(data['question_id']):
            # if it exists, we delete it
            data = data[data['question_id'] != args['question_id']]
            # save the data
            data.to_csv(ques_path, index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        
        else:
            # otherwise we return 404 not found
            return {
                'message': f"'{args['question_id']}' question does not exist."
            }

class Answers(Resource):
    def get(self):
        data = pd.read_csv(anws_path, sep='\t')  # read local CSV
        return {'data': data.to_dict()}, 200  # return data dict and 200 OK
    
    def post(self):
        #'answer_id','question_id','is_accepted'
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('answer_id', required=True, type=int)  # add args
        parser.add_argument('question_id', required=True, type = int)
        parser.add_argument('is_accepted', required=True, type = str)
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv(anws_path,sep='\t')
    
        # check if question_id already exists
        if args['answer_id'] in list(data['answer_id']):
            # if locationId already exists, return 401 unauthorized
            return {
                'message': f"'{args['answer_id']}' already exists."
            }, 409
        else:
            # otherwise, we can add the new question record
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'answer_id': [args['answer_id']],
                'question_id': [args['question_id']],
                'is_accepted': [args['is_accepted']]
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv(anws_path, index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK
    
    def patch(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('answer_id', required=True, type=int)  # add args
        parser.add_argument('question_id', store_missing=False, type = int)  # name/rating are optional
        parser.add_argument('is_accepted', store_missing=False, type = str)
        args = parser.parse_args()  # parse arguments to dictionary
        
        # read our CSV
        data = pd.read_csv(anws_path,sep='\t')
        
        # check that the location exists
        if args['answer_id'] in list(data['answer_id']):
            # if it exists, we can update it, first we get user row
            user_data = data[data['answer_id'] == args['answer_id']]
            
            # if name has been provided, we update name
            if 'question_id' in args:
                user_data['question_id'] = args['question_id']
            # if rating has been provided, we update rating
            if 'is_accepted' in args:
                user_data['is_accepted'] = args['is_accepted']
            
            # update data
            data[data['answer_id'] == args['answer_id']] = user_data
            # now save updated data
            data.to_csv(anws_path, index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        
        else:
            # otherwise we return 404 not found
            return {
                'message': f"'{args['answer_id']}' answer does not exist."
            }, 404
    
    def delete(self):
        parser = reqparse.RequestParser()  # initialize parser
        parser.add_argument('answer_id', required=True, type=int)  # add question_id arg
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv(anws_path,sep='\t')
        
        # check that the question_id exists
        if args['answer_id'] in list(data['answer_id']):
            # if it exists, we delete it
            data = data[data['answer_id'] != args['answer_id']]
            # save the data
            data.to_csv(anws_path, index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200
        
        else:
            # otherwise we return 404 not found
            return {
                'message': f"'{args['answer_id']}' answer does not exist."
            }
        
        
api.add_resource(Users, '/users')  # add endpoints
api.add_resource(Questions, '/questions')
api.add_resource(Answers, '/answers')

# It is possible to creaye sqlite database with SQLAlchemy 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# ma = Marshmallow(app)

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app

