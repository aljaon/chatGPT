#https://platform.openai.com/account/billing/overview
#https://openai.com/pricing
#https://platform.openai.com/docs/introduction

import openai

class GPT_Instance():
    
    models = {"GPT3.5":"gpt-3.5-turbo", "gpt-3.5-turbo":"gpt-3.5-turbo", "GPT4":"gpt-4-1106-preview", "gpt-4-1106-preview":"gpt-4-1106-preview"}

    def __init__(self, api_key_file = "key.txt", t = 1, mx_tok = 256, temp = 0.7, model = "GPT3.5"):

        #GPT model
        self.model = self.models[model]
        
        #Import API key from file
        file = open(api_key_file, "r")
        self.api_key = file.read()
        file.close() 
        
        #GPT client
        self.client = openai.OpenAI(api_key=self.api_key)
        
        #Prompt params
        self.temp = temp
        self.mx_tok = mx_tok
        self.t = t
        
    def prompt(self, system_prompt, user_prompt):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}],
            temperature=self.temp,
            max_tokens=self.mx_tok,
            top_p=self.t
        )
        return completion.choices[0]
        
def test():
    GPT1 = GPT_Instance(temp = 0.0)
    result = GPT1.prompt("You are an AI who only types the answer to the question and nothing else.", "What is the value of 5 + 8?")
    print (result.message.content) 
    
test()