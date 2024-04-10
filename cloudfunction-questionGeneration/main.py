from openai import OpenAI
from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
import os
from google.cloud import storage
import google.cloud.storage
import json
import functions_framework
import sys
import openai
import pymongo
import configparser


@functions_framework.http
def generate_questions(request):
    try:
        # config = configparser.ConfigParser()
        # config.read('configuration.properties')
        openai.api_key = os.environ.get('OPENAI_API_KEY')

        mongo_client = os.environ.get('MONGODB_CONNECTION_STRING')
        db = os.environ.get('DATABASE_NAME')
        collection = os.environ.get('COLLECTION_NAME')
        

        PATH = os.environ.get('gcp_PATH')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH     
        storage_client = storage.Client()
        
        def gcp_store_from_string(string_data, file_name):
            # bucket = storage_client.get_bucket('bucket_name')
            bucket = os.environ.get('bucket')
            blob = bucket.blob(file_name)
            blob.upload_from_string(string_data)

        def gcp_read_string(file_name):
            # bucket = storage_client.get_bucket('bucket_name')
            bucket = os.environ.get('bucket')
            blob = bucket.blob(file_name)
            return str(blob.download_as_string())


        def process_text_files_and_generate_analysis(text_files, output_file):
            sample_questions=''
            for file_path in text_files:
                sample_questions += gcp_read_string(file_path)

            prompt = f"Here are few sample questions:\n{sample_questions[:16385]}\n\n. Perform detailed analysis on the format, question creation and how the Answers and explanation are given. Also mention few generalized examples in them."

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
                # max_tokens=500
            )

            combined_analysis = response['choices'][0]['message']['content']

            
            gcp_store_from_string(combined_analysis, output_file)

            return combined_analysis
            


        def generate_questions_from_mongo(mongo_summary, combined_analysis,collection_name, num_questions=50 , max_single_prompt = 5):
            if num_questions < max_single_prompt:
                max_single_prompt = num_questions
                
            print("Total remaining Questions: ",num_questions,", Questions to be Generated in current run: ",max_single_prompt)

            
            prompt = f"""Following is the analysis of historical questions: 
            {combined_analysis}
            
            
            Refer the formatting of this analysis and strictly generate {max_single_prompt} new questions and provide their solutions on :
            {mongo_summary}
            
            
            Ensure that each question had for options and solutions provide thorough explanation for why a particular choice is correct and list explanation why each other answer choices are incorrect. 
            Each generated question should be numbered and have four following sections,--> Question Number:, --> Question: , --> Option:, --> Explanation:
            Add *--------------* between each generated questions with all sections of one question together.
            """


            # prompt = f"Following is the analysis of historical questions:\n{combined_analysis}. \n\n Refer this and generate {num_questions} new questions and their solutions strictly as per {combined_analysis} based on following topic - \n {mongo_summary}"
            messages = [{"role": "user", "content": prompt}]
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
                temperature=0.1
                # max_tokens=4096
            )
            
            first = response['choices'][0]['message']['content']
            final = first
            
            pushed = store_generated_questions_in_mongo(first, collection_name)
            num_questions -= pushed
            
            
            while num_questions > 0:
                if num_questions < max_single_prompt:
                    max_single_prompt = num_questions
                    
                print("Total remaining Questions: ",num_questions,", Questions to be Generated in current run: ",max_single_prompt)
                
                messages.append({"role": "assistant", "content": first})
                messages.append({"role": "user", "content": f"Generate next {max_single_prompt} more questions"})
            
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0125",
                    messages=messages,
                    temperature=0.1
                    # max_tokens=4096
                )
                first = response['choices'][0]['message']['content']
                final += response['choices'][0]['message']['content']
                
                
                pushed = store_generated_questions_in_mongo(first, collection_name)
                if pushed==0:
                    print(first)
                num_questions -= pushed
                
            
            return final



        def store_generated_questions_in_mongo(generated_questions, generated_questions_collection):
            total = 0
            for question_with_solution in generated_questions.split("*--------------*"):
                
                
                if "explanation" in question_with_solution.lower():
                    solution_set = question_with_solution.split("Explanation:")
                    
                    question = solution_set[0]
                    solution = "".join(solution_set[1:])
                    
                    question = question.replace("Question Number: ","").replace("Question: ","").replace("Option:","Options:")
                    
                    
                    generated_questions_collection.insert_one({
                        "question": question.strip().replace("-->",""),
                        # "correct_answer": correct_answer.strip(),
                        "answer": solution.strip().replace("-->","")

                    })
                    total +=1
                else:
                    # print(question_with_solution.lower())
                    pass
                    # print("Warning: 'explanation:' not found in question_with_solution.")
            print("Split Genearted Questions: ", len(generated_questions.split("*--------------*")),", Pushed to Mongo: ", total)
            
            return total
        
        def execute_main_function():
                output_file = 'analysis.txt'
                text_files = ["pdfToText/sample-questions1.txt", "pdfToText/sample-questions2.txt", "pdfToText/sample-questions3.txt"]
                combined_analysis = process_text_files_and_generate_analysis(text_files, output_file)

                summaries = collection.find(
                    {"NameOfTheTopic": {"$in": ["Introduction to Linear Regression", "Sampling and Estimation", "Hypothesis Testing"]}},
                    {"Summary": 1, "_id": 0}
                )
                mongo_summary = "\n\n".join([summary["Summary"] if summary["Summary"] is not None else "" for summary in summaries])

                SetACollection = os.environ.get('SET_A_COLLECTION_NAME')
                SetBCollection = os.environ.get('SET_B_COLLECTION_NAME')

                # Generate and store SetA if it doesn't exist
                if os.environ.get('SET_A_COLLECTION_NAME') not in db.list_collection_names():
                    SetA = generate_questions_from_mongo(mongo_summary, combined_analysis, SetACollection, num_questions=50, max_single_prompt=50)

                # Generate and store SetB if it doesn't exist
                if os.environ.get('SET_B_COLLECTION_NAME') not in db.list_collection_names():
                    SetB = generate_questions_from_mongo(mongo_summary, combined_analysis, SetBCollection, num_questions=50, max_single_prompt=50)

                return "Success"

            # Call the main function execution
        return execute_main_function()
        
    except Exception as e:
        return f"Fail: {str(e)}"
        

        
        
        
        
        
        
        
        
        
        
        
        
