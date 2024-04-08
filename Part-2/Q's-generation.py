import openai
import pymongo
import os
import configparser

config = configparser.ConfigParser()
config.read('configuration.properties')
openai.api_key = config['openai']['OPENAI_API_KEY'] 

mongo_client = pymongo.MongoClient(config['mongodb']['MONGODB_CONNECTION_STRING'])
db = mongo_client[config['mongodb']['DATABASE_NAME']]
collection = db[config['mongodb']['COLLECTION_NAME']]

def process_text_files_and_generate_analysis(text_files, output_file):
    sample_questions=''
    for file_path in text_files:
        with open(file_path, 'r') as file:
            sample_questions += file.read()

    prompt = f"Here are few sample questions:\n{sample_questions[:16385]}\n\n. Perform detailed analysis on the format, question creation and how the Answers and explaination are given. Also mention few generalized examples in them."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
        # max_tokens=500
    )

    combined_analysis = response['choices'][0]['message']['content']
    with open(output_file, 'w') as output:
        output.write(combined_analysis)
    
    return combined_analysis

def generate_questions_from_mongo(mongo_summary, combined_analysis, num_questions=50):
    prompt = f"Following is the analysis of historical questions:\n{combined_analysis}. \n\n Refer this and generate {num_questions} new questions strictly in mentioned format based on following topic - \n {mongo_summary} provide explanations for each answer."
    messages = [{"role": "user", "content": prompt}]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        temperature=0.1
        # max_tokens=4096
    )
    
    first = response['choices'][0]['message']['content']
    final = first
    for i in range(1):
        
    
        messages.append({"role": "assistant", "content": first})
        messages.append({"role": "user", "content": f"Generate next {num_questions} more questions"})
    
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
            temperature=0.1
            # max_tokens=4096
        )
        first = response['choices'][0]['message']['content']
        final += response['choices'][0]['message']['content']
    
    return final


def print_questions_with_numbers(generated_questions):
    for i, question in enumerate(generated_questions, start=1):
        print(f"\n{i}:")
        print(question)

output_file = 'analysis.txt' 

text_files = ["parsed-text-files/sample-level-i-questions1_1.txt", "parsed-text-files/sample-level-i-questions2_1.txt", "parsed-text-files/sample-level-i-questions3_1.txt"]

if os.path.exists(output_file):
    with open(output_file,'r') as f:
        combined_analysis = f.read()
else:
    combined_analysis = process_text_files_and_generate_analysis(text_files, output_file)


summaries = collection.find(
    {"NameOfTheTopic": {"$in": ["Introduction to Linear Regression", "Sampling and Estimation", "Hypothesis Testing"]}},
    {"Summary": 1, "_id": 0}
)
mongo_summary =  [summary["Summary"] for summary in summaries][0]

generated_questions = generate_questions_from_mongo(mongo_summary, combined_analysis, num_questions=50)

print(generated_questions)

