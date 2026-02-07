from groq import Groq
import time
import os
from config import TEMPERATURE,MAX_TOKENS
import ollama
import csv
client=Groq(api_key=os.getenv('API_KEY'))


def groq_response(model, prompt): 
    start = time.time()
    response = client.chat.completions.create(
        model=model, 
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=512
    )
    latency = round(time.time() - start, 2)
    return response.choices[0].message.content, latency


def ollama_response(model,prompt):
        start=time.time()
        response=ollama.chat(
           model=model,
           messages=[{"role":"user","content":prompt}],
           options={ "temperature":0.2,
           "max_tokens":512
           }


   )
        latency=round(time.time()-start,2)
        return response["message"]["content"],latency


def write_groq_csv(task_stats,filename="groq-model-results.csv"):
      with open(filename,"w",newline="")as f:
            writer=csv.writer(f)
            writer.writerow([
                  "category",
                  "model",
                  "avg-latency_sec",
                  "avg_response_length",
                  "rounds"
            ])
            for category in task_stats:
                  for model in task_stats[category]:
                        data=task_stats[category][model]
                        if data["rounds"]==0:
                              continue
                        writer.writerow([category,model,
                            round(sum(data['latencies'])/len(data['latencies']),3 ),
                        round(sum(data["length"]) /len(data['length']),3  )  ,
                              data['rounds']      ])
                              
                         
def write_cross_platform_csv(task_stats,filename="cross_platform_results.csv"):
      with open(filename,"w",newline="") as f:
            writer=csv.writer(f)
            writer.writerow([
                  "task",
                  "model",
                  "avg_latency_sec",
                  "rounds"            
            ])
            for Category in task_stats:
                        for model in task_stats[Category]:
                              data=task_stats[Category][model]
                              if data["rounds"]==0:
                                    continue
                              writer.writerow([
                                    Category, 
                                    model,
   round(sum(data["latencies"])/len(data["latencies"]  ),3),
   data["rounds"]                           
                              ])  
                              
