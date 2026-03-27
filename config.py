# WE HAVE PUT ALL THE CONSTRAINTS HERE
TEMPERATURE=0.2
MAX_TOKENS=512
RUN_PER_PROMPTS=3
#MODELS TO BENCHMARK
MODELS=["llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "qwen/qwen3-32b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
   ]
# JUDGE MODELS
JUDGES=["llama-3.3-70b-versatile", 
    "meta-llama/llama-4-scout-17b-16e-instruct", 
    "llama-3.1-8b-instant"]