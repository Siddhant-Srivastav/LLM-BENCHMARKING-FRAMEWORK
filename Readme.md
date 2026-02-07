LLM BENCHMARKING FRAMEWORK:

# Introduction:

Large Language Models (LLMs) are increasingly deployed across diverse platforms and infrastructures. However, analyzing their behavior across
different execution environments and prompt formulations remains challenging due to:

: Infrastructure heterogeneity (cloud APIs vs. local inference).

: Variability in latency across execution environments.

: Sensitivity to prompt phrasing

: Overly complex or opaque evaluation pipelines

This project introduces a lightweight and extensible benchmarking framework that evaluates LLMs under three complementary perspectives: 

1. Stability across platforms, and

2. Robustness to real-world prompt variation. 

3. latency in different prompts.

The framework is designed to remain provider agnostic with future support planned for Gemini Models, while clarity, interpretability, and sound experimental design are maintained.

## Motive:

Most of the LLM evaluations either

1. Focused on a single platform

2. Reply to one-off prompt evaluations, or 

3. Introduce excessive complexity without clear justification.

This project addresses these gaps by asking:

1. How stable are model comparisons across heterogenous platforms?

2. How robust are models to natural variations in user prompts?

3. How do we benchmark LLMs without sacrificing simplicity or extensibility?

## Evaluation design

To avoid mixing objectives, the framework separates the evaluation into two independent benchmarks, each with a clearly defined goal.

# 1 Cross-Platform Benchmark:-

This benchmark mainly focused on the stability of LLMs:

Script='cross_benchmark.py'

Prompt Set = 'prompts_stability.py'

This benchmark compares models deployed on different models (e.g., Groq API, Ollama local inference).

# Methodology:

1. Identical prompts are executed multiple times. 

2. Latency values are averaged across runs.

3. Evaluation noise caused by network and hardware variability is reduced.

# Objective:

Measure performance stability and consistency under heterogeneous execution environments.

# 2 Groq Only Benchmark:

This benchmark mainly focuses on prompt robustness and latency of the LLMs.

Script='groq_benchmark.py'

Prompt Set='prompts_robustness.py'

This benchmark evaluates multiple Groq-hosted models under a shared infrastructure.

# Methodology;

1. Paraphrased variants of the same task are used.

2. Models are evaluated on their ability to handle natural prompt variation.

# Objective:

Measure robustness to prompt phrasing and real-world user input.

# Prompt Design;

Prompts are organized by type:

1. Math

2. Coding

3. Factual

4. Critical Thinking

Two problems Sets are maintained:

'prompts_stability.py': single canonical prompt per task

'prompts_robustness.py': multiple paraphrased variants per task.

This separation ensures clarity of experimental intent.

## Evaluation Metrics:

The framework focuses on core, interpretable metrics.

1. Qualitative Quality:

Assessed using an LLM as a judge approach based on correctness, completeness, clarity, and helpfulness.

2. Latency:

Measured and averaged where appropriate to reduce noise.

3. Task-wise performance:

Results are reported separately for each task category.

Platform-specific metrics such as token usage are intentionally excluded to preserve simplicity and clarity.
## Output

The framework can optionally generate CSV files summarizing evaluation results, including:
- average latency per model and task
- average response length
- number of evaluation rounds

CSV generation is disabled by default and can be enabled explicitly when needed
 

# Key Observations:

1. Model performance is task dependent rather than uniform.

2. Larger models show clearer advantages on coding-type prompts.

3. Prompts paraphrasing rarely alters relative rankings, indicating robustness in the LLMs we used.

4. In the cross-platform benchmark, LLM latencies show high deflections.

due to infrastructure differences.

5. Ollama based models exhibited higher latency,with qualitative performance varying across tasks.

# Design Philosophy:

1. One evaluation objective per benchmark 

2. Clarity over complexity

3. Real-world relevance over artificial rigor.

4. Easily accessible to the new services or platforms (e.g., Gemini)

# Future Work

1. Integration of Gemini Models

2. Expanded and multilingual prompt sets

3. Visualizing Dashboard

4. Automated experiment configuration.

# Project Structure:

LLM BENCHMARK/

|--config.py

|--cross_platform.py

|--groq_benchmark.py

|--prompts_stability.py

|--prompt_robustness.py

|--utils.py

|--Readme.md

# Setup

This project requires access to hosted LLM APIs.

Users must provide their own API keys via environment variables.

Create a '.env' file in the project root and add:

API_KEY=your_groq_api_key_here


# How to run:

pip install -r requirements.txt

python cross_platform.py

python groq_benchmark.py

## License

This project is licensed under the MIT License. See LICENSE.md for details.