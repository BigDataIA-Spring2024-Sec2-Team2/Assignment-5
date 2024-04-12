import openai
from pymongo import MongoClient
from bson.objectid import ObjectId
from pinecone import Pinecone
import os
from dotenv import load_dotenv
import pymongo
import certifi
import csv
import pandas as pd

load_dotenv()

def process_documents(all_documents, collection_los, los_pinecone, key, csv_writer):
    correct = 0
    for document in all_documents:
        question = document['question']

        if key ==0:
          set = "A"
          answer = (((document['answer']).split())[4])[0]
        elif key ==1:
          set = "B"
          answer = (((document['answer']).split())[0])[0]

        embedded_question = openai.Embedding.create(
            input=question, 
            model=os.getenv('embedding_model'),
        ).data[0].embedding

        found = los_pinecone.query(vector=embedded_question, top_k=3, include_metadata=True)
        context = ''

        for each in found['matches']:
            mongoId = ObjectId(each['id'])
            mongo_result = collection_los.find_one({"_id": mongoId})
            los = mongo_result.get("LearningSummary")
            context += los

        query = "Based on this context" + context + "Answer the following question by only giving the correct option id (like A or B or C or D) and not any other text " + question

        messages = [{"role": "user", "content": query}]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            temperature=0.1
        )
        gpt_response = response['choices'][0]['message']['content']

        if gpt_response[0] == answer:
            correct += 1
            match = 1
        else: 
           match = 0
        question = question.replace('\n', ' ')
        csv_writer.writerow([set, question, gpt_response[0], answer, match])

    return correct

def main():
    key = os.getenv('GPT_key') 
    mongo_url = os.getenv('mongo_url') 
    db_name = os.getenv('db_name') 
    collection_los_name = os.getenv('collection_los') 
    collection_set_A_name = os.getenv('collection_set_A') 
    collection_set_B_name = os.getenv('collection_set_B') 
    collection_part_4_report = os.getenv('collection_part_4_report')
    key_pinecone = os.getenv('key_pinecone') 
    index_name = os.getenv('index_name')

    openai.api_key = key
    client = pymongo.MongoClient(mongo_url,tlsCAFile=certifi.where())
    db = client[db_name]

    collection_set_A = db[collection_set_A_name]
    collection_set_B = db[collection_set_B_name]
    collection_los = db[collection_los_name]
    collection_part_4_report = db[collection_part_4_report]

    pinecone = Pinecone(api_key=key_pinecone)
    los_pinecone = pinecone.Index(name=index_name)
    
    all_documents_A = collection_set_A.find()
    all_documents_B = collection_set_B.find()

    with open('Part4_report.csv', 'w', newline='') as csvfile:
        fieldnames = ['Set', 'Question', 'GPT Answer', 'KB Answer', 'Match']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        correct_A = process_documents(all_documents_A, collection_los, los_pinecone, 0, writer)
        correct_B = process_documents(all_documents_B, collection_los, los_pinecone, 1, writer)

        print("Correct answers for set A:", correct_A)
        print("Correct answers for set B:", correct_B)

        df = pd.read_csv("Part4_report.csv")   
        data_dict = df.to_dict(orient='records')
        collection_part_4_report.insert_many(data_dict)
  
main()
