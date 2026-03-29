from groq import Groq
from dotenv import load_dotenv
from itertools import combinations
import json
import os
import matplotlib.pyplot as p
import sys 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import write_groq_csv
load_dotenv()
client=Groq(api_key=os.getenv("API_KEY"))
from config import MODELS,JUDGES
from DATASETS.prompt_robustness import PROMPTS
from utils import groq_response,ollama_response
def judge(prompt,answer_a,answer_b):
    votes=[]
    for Judge in JUDGES:
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
     try:
      response=client.chat.completions.create(
        model=Judge,
        messages=[{"role":"user","content":judge_prompt}],
      )
      vote=response.choices[0].message.content.strip().upper()
     except Exception as e:
       print(f"Error in judge Prompt")
       continue
     if(vote in ["A","B"]):
       votes.append(vote)
    if(votes.count("A")>votes.count("B")):
       return "A",votes
    elif votes.count("B")>votes.count("A"):
       return "B",votes
    else:
       return "Tie",votes
    
score_counts={m:0 for m in MODELS}
latencies={m:[] for m in MODELS}
results=[]
task_stats={}
for model_a,model_b in combinations(MODELS,2):
  for category,prompt_list in list(PROMPTS.items()):
     for prompt in prompt_list:
       if category not in task_stats:
         task_stats[category]={}
       if model_a not in task_stats[category]:
         task_stats[category][model_a]={
           "latencies":[],
           "length":[],
           "rounds":0

         }
       if model_b not in task_stats[category]:
         task_stats[category][model_b]={
           "latencies":[],
           "length":[],
           "rounds":0

         }
      # Collect responses from  models
       ans_m1,l1=groq_response(model_a,prompt)
       len_m1=len(ans_m1.split())
       latencies[model_a].append(l1)
       task_stats[category][model_a]["latencies"].append(l1)
       task_stats[category][model_a]["length"].append(len_m1)
       task_stats[category][model_a]["rounds"]+=1
  
       ans_m2,l2=groq_response(model_b,prompt)
       len_m2=len(ans_m2.split())
       latencies[model_b].append(l2)
       task_stats[category][model_b]["latencies"].append(l2)
       task_stats[category][model_b]["length"].append(len_m2)
       task_stats[category][model_b]["rounds"]+=1
       if(ans_m1 is None or ans_m2 is None):
        continue
       try:
        # Evaluate responses using LLM-as-judge
        Better,votes=judge(prompt,ans_m1,ans_m2)
        results.append({
          "Category":category,
          "Prompt":prompt,
          "Model A":model_a,
          "Model B":model_b,
          "Answer A":ans_m1,
          "Answer B":ans_m2,
          "Better": Better,
          "Latency A":l1,
          "Latency B":l2,
          "Length A":len_m1,
          "Length B":len_m2,
          "Votes":votes
       })
        if(Better=="A"):
          score_counts[model_a]+=1
        elif(Better=="B"):
          score_counts[model_b]+=1
       except Exception as e:
        print("Error in judge evaluation")
# Save results to JSON for later analysis
os.makedirs("RESULTS",exist_ok=True)
with open("RESULTS/main_results.json","w") as file:
   json.dump(results,file,indent=2) 
print("Qualitative Evaluation Summary:")
for model,score in sorted(score_counts.items(),key=lambda x:x[1],reverse=True):
   avg_latency=sum(latencies[model])/len(latencies[model])
   print(f"{model}:{score}|Average latency:{avg_latency:.2f}s")

models=list(score_counts.keys())
scores=list(score_counts.values())
p.figure(figsize=(0.5))
p.bar(models,scores)
p.xlabel("Models")
p.ylabel("Score")
p.title("LLM Benchmark: Qualitative Evaluation")
p.xsticks(rotation=20)
p.grid(axis="y",linestyle="--",alppha=0.8)
p.tightlayout()
p.savefig("RESULTS/model_scores.png",dpi=300)
p.show()
write_groq_csv(task_stats)
