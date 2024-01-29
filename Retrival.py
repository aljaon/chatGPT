import GPT
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


GPT1 = GPT.GPT_Instance(model = "GPT4", temp = 0.1)


#Dictionary
class LLM_dictonary:
    
    def __init__(self, gpt, key, value):
        
        #GPT
        self.gpt = gpt
        
        #Key Value labels
        self.key = key
        self.value = value
        
        #Memory
        self.dictionary = {} 

    def dict_print(self):
        print(self.dictionary)
        
    def insert(self, key, value):
        self.dictionary[key] = value
    def get(self, name):
        return self.dictionary.get(name, "Unknown")
    
    def LLM_update(self, text, print_result = False):
        
        try:
            #Prompt
            prompt = f"""You are given the following map of key:value pairs representing {self.key}:{self.value}
            
            Given:
            
            {self.dictionary}
            
            A new piece of information received: :
            
            {text}
            
            If this information is not relevant or all the relevant keys already exist type in "no_change".
                
            Using the self.dictionary as the dictonary do not type anything except the python code to modify the dictonary such that the responce can be excecuted directly using exec()
            Do not type the '''python\n<Code>\n''' that chatGPT sometimes places between code"""
            
            
            result = GPT1.prompt("You are an AI who creates python scripts to be executed using exec(). You type the code required to complete the request and nothing else.", prompt)
            
            if print_result == True:
                    print("\n", result.message.content, "\n")
                    
            if result == "no_change":
                return
            
            exec(result.message.content)
            
        except Exception as err:
            print(f"An error has occurred: {err}")              
    def LLM_view(self, request):
        
        #Prompt
        prompt = f"""You are given the following map of key:value pairs representing {self.key}:{self.value}
        
        Given:
        
        {self.dictionary}
        
        Complete the following request:
        
        {request}"""
        
        result = GPT1.prompt("You are an AI who only types the answer to the question and nothing else.", prompt)
          
        #Return response
        return result.message.content

test1 = LLM_dictonary(GPT1, "Person", "Favorite Colour")
test1.LLM_update("Marys favorite colour is purple, while Judy's favorite colour is blue. Jakes favorite colour used to be yellow but is now green", True)
test1.dict_print()
print(test1.LLM_view("What is jakes favorite colour?"))




#JSON
example_dict_containers = {
    "phone_number_1": {
        "Number1": "212 555-1234",
        "Number2": "646 555-4567",
        "Number3": "01895-17777"
    },
    "Children": [
        "Catherine",
        "Thomas",
        "Trevor"
    ],
    "Name": "Andrew"
}
example_dict_containers_formatted = json.dumps(example_dict_containers, indent=4)
class LLM_dictonary_containers:
    
    def __init__(self, gpt, dictionary = {}):
        
        #GPT
        self.gpt = gpt
        
        #Memory
        self.dictionary = dictionary

    def print(self):
        formatted_data = json.dumps(self.dictionary, indent=4)
        print(formatted_data)
        
    #Manual
    def new_key(self, container_type, key):
        
        #Single value
        if container_type == "":
            self.dictionary[key] = ""
        #List
        elif container_type == "list":
            self.dictionary[key] = list()
        #Dict
        elif container_type == "dict":
            self.dictionary[key] = dict()
        #Set 
        elif container_type == "set":
            self.dictionary[key] = dict()
    def remove_key(self, key):
        if key in self.dictionary:
            del self.dictionary[key]

    #chatGPT      
    def LLM_modify(self, text, print_result = True):
        
        try:
            formatted_data = json.dumps(self.dictionary, indent=4)
            
            #Prompt
            prompt = f"""A dict is indexed by different keys.
            The values can be:
            
            single values for strings or values that can assumed be single such as a description or parameter
            dict for values that are each have a name/label/key.
            list for values that are given in list format with no label.
            
            An example of dictonary is:

            {example_dict_containers_formatted}

            Given:
            
            {formatted_data}
            
            A new piece of information received: 
            {text}
            
            If this information is not relevant or all the relevant keys already exist type in "no_change".
            
            Using the self.dictionary as the dictonary do not type anything except the python code to modify the dictonary such that the responce can be excecuted directly using exec()
            Do not type the '''python\n<Code>\n''' that chatGPT sometimes places between code"""
            
            result = GPT1.prompt("You are an AI who creates python scripts to be executed using exec(). You type the code required to complete the request and nothing else.", prompt)
            
            if print_result == True:
                print("\n", result.message.content, "\n")
                
            if result == "no_change":
                return

            exec(result.message.content)
            
        except Exception as err:
            print(f"An error has occurred: {err}")        
    def LLM_view(self, request):
        
        formatted_data = json.dumps(self.dictionary, indent=4)
        
        #Prompt
        prompt = f"""Given the following map/JSON:
        
        {formatted_data}
        
        Complete the following request:
        
        {request}"""
        
        
        result = GPT1.prompt("You are an AI who only types the answer to the question and nothing else.", prompt)
        
        #Return response
        return result.message.content


test2 = LLM_dictonary_containers(GPT1)
test2.LLM_modify("Log the following information into the dict using appropriate containers. \"Codes relevant to him are 123, 777 and 987 for item1, item3 and item4 respectivly. His favorite colours are blue and green. Birthday month is january.\"", True)
test2.print()
test2.LLM_modify("Apply the following modification the the dictonary \"Code 123 is replaced by 444\"", True)
test2.print()






#Pandas dataframe
class LLM_Pandas:
    def __init__(self, gpt, df):
        
        #GPT
        self.gpt = gpt
        
        #Dataframe
        self.df = df 
    def print(self):
        print(self.df.to_string(index=True)) 
    def LLM_modify(self, text, print_result = True):
        
        try:
            #Prompt
            prompt = f"""A dataframe is given bt self.df and contains:
            
            {self.df.to_string(index=True)}
            
            The promt recieved is: 
            {text}

            If this information is not relevant to the dataframe type in "no_change". 
            Using the self.df as the dataframe do not type anything except the python code to execute the prompt such that the responce can be excecuted directly using exec()
            For example for "Change Jakes age to 44" and Jake is the first row type "self.df.at[0, \"age\"] = 44
            Do not type the '''python\n<Code>\n''' that chatGPT sometimes places between code"""
            
            result = GPT1.prompt("You are an AI who creates python scripts to be executed using exec(). You type the code required to complete the request and nothing else.", prompt)
            
            if print_result == True:
                print("\n", result.message.content, "\n")
                
            if result == "no_change":
                return
        
            #Convert to list seperated by new line
            exec(result.message.content)
            
        except Exception as err:
            print(f"An error has occurred: {err}")

data = {'Name': ['John', 'Alice', 'Bob'],
        'Age': [25, 30, 22],
        'City': ['New York', 'San Francisco', 'Seattle']
        }
df = pd.DataFrame(data)


df_gpt = LLM_Pandas(GPT1, df)
df_gpt.print()
df_gpt.LLM_modify("Anohter two people need to be added first Kate, who is 33 and lives in London and Steve, a 59 year old who lives in Spain. Do not used pd.append as this is deprecated. After sort the rows by age descending")
df_gpt.print()
df_gpt.LLM_modify("Plot age of each person assuming import matplotlib.pyplot as plt is imported already and use a bar chart with a different colour for each person.")
#df_gpt.LLM_modify("Apply normalisation to the age in a new \"normalised_age\" column and standardisation in a new column \"standardised_age\"")