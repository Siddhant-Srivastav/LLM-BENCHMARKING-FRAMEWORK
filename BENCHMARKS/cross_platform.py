from groq import Groq
import json
import time
from groq.types.chat.chat_completion import ChatCompletion
import ollama
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import RUN_PER_PROMPTS
model_groq="llama-3.1-8b-instant"
model_ollama="gemma3:4b"
models_score={model_groq:0,model_ollama:0}
models_latency={model_groq:[],model_ollama:[]}
     
client=Groq(api_key=os.getenv("API_KEY"))
from DATASETS.prompt_stability import PROMPTS
Judges=["llama-3.3-70b-versatile", 
    "meta-llama/llama-4-scout-17b-16e-instruct", 
    "llama-3.1-8b-instant"]
results=[]
task_stats={}
from utils import groq_response,ollama_response, write_cross_platform_csv
def judge(prompt,answer_a,answer_b):
    votes=[]
    for Judge in Judges:
     judge_prompt=f"""
You are a fair evaluator.
Compare the two answers of same question based on:
1 Correctness
2 Completeness
3 Clarity
4 Helpfulness
then decide which answer is better.
Question:{prompt}
Answer A:{answer_a}
Answer B:{answer_b}
If Answer A is better then reply A 
If Answer B is better then reply B
Rules:
1: Reply only A or B
2: Do not give any explaination , extra text
Which is better? 
"""
     response=client.chat.completions.create(
        model=Judge,
        messages=[{"role":"user","content":judge_prompt}],
        timeout=32.0

    )
     vote=response.choices[0].message.content.strip().upper()
     if(vote in ["A","B"]):
       votes.append(vote)
    if(votes.count("A")>votes.count("B")):
       return "A",votes
    elif(votes.count("B")>votes.count("A")):
       return "B",votes
    else:
       return "Tie"

        
for Category,prompt in PROMPTS.items():
   lat_groq=[]
   lat_ollama=[]
   if Category not in task_stats:
         task_stats[Category]={}
   if model_groq not in task_stats[Category]:
         task_stats[Category][model_groq]={
           "latencies":[],
           "length":[],
           "rounds":0 }
   if model_ollama not in task_stats[Category]:
         task_stats[Category][model_ollama]={
           "latencies":[],
           "length":[],
           "rounds":0}
   for i in range(RUN_PER_PROMPTS):
    try:
     # Collect responses from models
     ans_groq,latency1=groq_response(model_groq,prompt)
     task_stats[Category][model_groq]["latencies"].append(latency1)
     task_stats[Category][model_groq]["rounds"]+=1
    except Exception as e:
       print(f"Groq error in {Category}:{e}")
    try:
      ans_ollama,latency2=ollama_response(model_ollama,prompt)
      task_stats[Category][model_ollama]["latencies"].append(latency2)
      task_stats[Category][model_ollama]["rounds"]+=1
      lat_groq.append(latency1) 
      lat_ollama.append(latency2)
    except Exception as e:
       print(f"Ollama error in {Category}:{e}")
    try:
     # Evaluate responses using LLM-as-Judge
     better=judge(prompt,ans_groq,ans_ollama)
     if("A" in better):
      models_score[model_groq]+=1
     elif("B" in better):
      models_score[model_ollama]+=1
     else:
       continue
    except Exception as e:
       print("Error in judge evaluation")
    results.append({ "Category":Category,
            "Prompt":prompt,
            "Model A":model_groq,
            "Model B":model_ollama,
            "Better Accuracy":better}
        )
   avg_latgroq=sum(lat_groq)/len(lat_groq)
   avg_latollama=sum(lat_ollama)/len(lat_ollama)
   models_latency[model_groq].append(avg_latgroq)
   models_latency[model_ollama].append(avg_latollama)
   a=sorted(models_score.items(),key=lambda x:x[1],reverse=True)
print(f"The Model with better Accuracy is{a[0][0]} ")
avglat_groq=sum(models_latency[model_groq])/len(models_latency[model_groq])
avglat_ollama=sum(models_latency[model_ollama])/len(models_latency[model_ollama])
avg_latency_with_models={ avglat_groq:model_groq,avglat_ollama:model_ollama} 
print(f"The Model with Better speed is: {avg_latency_with_models[min(avglat_groq,avglat_ollama)]}")
# Save results to JSON for later analysis
os.makedirs("RESULTS",exist_ok=True)
with open("RESULTS/models_comaparison.json","w") as file:
  json.dump(results,file,indent=4)
write_cross_platform_csv(task_stats)

   





