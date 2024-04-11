import functions_framework
from openai import OpenAI
from pymongo import MongoClient
from bson.objectid import ObjectId
from pinecone import Pinecone
import os

def main(ids):

  # embedding_model = os.environ.get('embedding_model') 
  # key = os.environ.get('GPT_key') 
  # mongo_url = os.environ.get('mongo_url') 
  # db_name = os.environ.get('db_name') 
  # collection_name_source = os.environ.get('collection_name_source') 
  # key_pinecone = os.environ.get('key_pinecone') 
  # index_name = os.environ.get('index_name')
  # pinecone_question_namespace = os.environ.get('pinecone_question_namespace')
  # pinecone_answers_namespace = os.environ.get('pinecone_answers_namespace')
  
  embedding_model = "text-embedding-3-small" 
  key = "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"
  mongo_url = "mongodb+srv://anshulchaudhary218:CiH1LUuWQM1Qh8Lh@cluster0.lvdodo0.mongodb.net/"
  db_name = "assignment_5"
  collection_name_source = "SetA" 
  key_pinecone = "1b0334f4-f63c-4c7e-8c59-8d719e528a3a" 
  index_name = "question-embed-db"
  pinecone_question_namespace = "questions"
  
  try:
    #open AI
    openai_client = OpenAI(api_key=key)
    # MongoDB
    mongo_client = MongoClient(mongo_url)
    db = mongo_client[db_name]
    source_collection = db[collection_name_source]
    # Pinecone
    pinecone = Pinecone(api_key=key_pinecone)
    index = pinecone.Index(name=index_name)
    
    for id in ids:
      mongoId = ObjectId(id)
      mongo_result = source_collection.find_one({"_id": mongoId})
      
      if mongo_result is None:
        print("No result found in {} for id {}".format(collection_name_source, id))
        continue
      
      print("Generating Embedding for id {}".format(id))
      
      question = mongo_result.get("question")
      
      embedded_question = openai_client.embeddings.create(
          input=question, 
          model=embedding_model,
      ).data[0].embedding
      
      print(embedded_question)
      xc = index.query(vector=embedded_question, top_k=3, include_metadata=True, namespace=pinecone_question_namespace)
      print(xc["matches"])
      
  
  except:
    pass
  
main(["661838f6e40b3e4942bfe609"])