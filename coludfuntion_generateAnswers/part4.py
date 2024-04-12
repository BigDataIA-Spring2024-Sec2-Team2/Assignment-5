import functions_framework
import openai
from pymongo import MongoClient
from bson.objectid import ObjectId
from pinecone import Pinecone
import os
from dotenv import load_dotenv
import pymongo
from pymongo import MongoClient
import certifi

load_dotenv()

def process_documents(all_documents, collection_los, los_pinecone, key):
    correct = 0
    for document in all_documents:
        question = document['question']

        if key ==0:
          answer = (((document['answer']).split())[4])[0]
        elif key ==1:
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

    return correct

def main():
    key = os.getenv('GPT_key') 
    mongo_url = os.getenv('mongo_url') 
    db_name = os.getenv('db_name') 
    collection_los_name = os.getenv('collection_los') 
    collection_set_A_name = os.getenv('collection_set_A') 
    collection_set_B_name = os.getenv('collection_set_B') 
    key_pinecone = os.getenv('key_pinecone') 
    index_name = os.getenv('index_name')

    openai.api_key = key
    client = pymongo.MongoClient(mongo_url,tlsCAFile=certifi.where())
    db = client[db_name]

    collection_set_A = db[collection_set_A_name]
    collection_set_B = db[collection_set_B_name]
    collection_los = db[collection_los_name]

    pinecone = Pinecone(api_key=key_pinecone)
    los_pinecone = pinecone.Index(name=index_name)
    
    all_documents_A = collection_set_A.find()
    all_documents_B = collection_set_B.find()

    correct_A = process_documents(all_documents_A, collection_los, los_pinecone, 0)
    correct_B = process_documents(all_documents_B, collection_los, los_pinecone, 1)

    print("Correct answers for set A:", correct_A)
    print("Correct answers for set B:", correct_B)
  
main()