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

# generated_questions_collection = db.create_collection("generated_questions")


def process_text_files_and_generate_analysis(text_files, output_file):
    sample_questions=''
    for file_path in text_files:
        with open(file_path, 'r') as file:
            sample_questions += file.read()

    prompt = f"Here are few sample questions:\n{sample_questions[:16385]}\n\n. Perform detailed analysis on the format, question creation and how the Answers and explanation are given. Also mention few generalized examples in them."

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

def generate_questions_from_mongo(mongo_summary, combined_analysis, num_questions=1 , max_single_prompt = 5):
    if num_questions < max_single_prompt:
        max_single_prompt = num_questions
    
    prompt = f"""Following is the analysis of historical questions: 
    {combined_analysis}
    
    
    Refer the formatting of this analysis and generate {max_single_prompt} new questions and provide their solutions on :
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
    
    num_questions -= max_single_prompt
    while num_questions > 0:
        if num_questions < max_single_prompt:
            max_single_prompt = num_questions
    
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
        
        num_questions -= max_single_prompt
    
    return final


def print_questions_with_numbers(generated_questions):
    for i, question in enumerate(generated_questions, start=1):
        print(f"\n{i}:")
        print(question)



def store_generated_questions_in_mongo(generated_questions, generated_questions_collection):
    # print(generated_questions.split("\n\n")[0])
    for question_with_solution in generated_questions.split("*--------------*"):
        

        if "explanation" in question_with_solution.lower():
            solution_set = question_with_solution.split("Explanation:")
            
            question = solution_set[0]
            solution = "".join(solution_set[1:])
            
            question = question.replace("Question Number: ","").replace("Question: ","").replace("Option:","Options:")
            
            # print(solution.strip().split("Therefore, the correct answer is")[1].strip()[0])

            # solution_parts = solution.strip().split("Correct answer:")            

            # if len(solution_parts) == 2:
            #     correct_answer = solution_parts[1].strip()[0]
            #     whole_answer = solution.strip()
            # else:
            #     print("Warning: Unable to split solution into correct answer and whole answer.")
            #     correct_answer = "Not available"
            #     whole_answer = "Not available"

            generated_questions_collection.insert_one({
                "question": question.strip().replace("-->",""),
                # "correct_answer": correct_answer.strip(),
                "answer": solution.strip().replace("-->","")
            })
        else:
            print(question_with_solution.lower())
            print("Warning: 'explanation:' not found in question_with_solution.")
            
        


if __name__ == "__main__":
    output_file = 'analysis.txt' 
    text_files = ["parsed-text-files/sample-level-i-questions1_1.txt", "parsed-text-files/sample-level-i-questions2_1.txt", "parsed-text-files/sample-level-i-questions3_1.txt"]

    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            combined_analysis = f.read()
    else:
        combined_analysis = process_text_files_and_generate_analysis(text_files, output_file)

    summaries = collection.find(
        {"NameOfTheTopic": {"$in": ["Introduction to Linear Regression", "Sampling and Estimation", "Hypothesis Testing"]}},
        {"Summary": 1, "_id": 0}
    )
    
    mongo_summary = "\n\n".join([summary["Summary"] if summary["Summary"] is not None else "" for summary in summaries])


    SetACollection = db[config['mongodb']['SET_A_COLLECTION_NAME']]
    SetBCollection = db[config['mongodb']['SET_B_COLLECTION_NAME']]
    
    # Generate and store SetA if it doesn't exist
    if config['mongodb']['SET_A_COLLECTION_NAME'] not in db.list_collection_names():
        SetA = generate_questions_from_mongo(mongo_summary, combined_analysis, num_questions=50, max_single_prompt=5)
        with open("SetA.txt", 'w', encoding="utf-8") as output:
            output.write(SetA)
        store_generated_questions_in_mongo(SetA, SetACollection)
    else:
        print("SetA already exists")

    # Generate and store SetB if it doesn't exist
    if config['mongodb']['SET_B_COLLECTION_NAME'] not in db.list_collection_names():
        # SetB_prompt = f"This is SetB. Following is the analysis of historical questions:\n{combined_analysis}. \n\n Refer this and generate 50 new questions and their solutions strictly as per {combined_analysis} based on following topic - \n {mongo_summary}"
        SetB = generate_questions_from_mongo(mongo_summary, combined_analysis, num_questions=50, max_single_prompt=5)
        with open("SetB.txt", 'w', encoding="utf-8") as output:
            output.write(SetB)
        store_generated_questions_in_mongo(SetB, SetBCollection)
    else:
        print("SetB already exists")


# SetBCollection = db[config['mongodb']['SET_B_COLLECTION_NAME']]
# with open("SetB.txt", 'r', encoding="utf-8") as output:
#     SetB = output.read()
    
#     # print(len(SetB.split("*--------------*")))
    
#     # print(SetB.split("*--------------*")[2])
    
#     store_generated_questions_in_mongo(SetB, SetBCollection)