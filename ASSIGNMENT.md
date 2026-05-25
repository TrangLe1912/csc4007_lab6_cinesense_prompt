# Lab 6 Assignment – CineSense Prompt Evaluation

## 1. Context

In previous labs, you worked with IMDB movie review sentiment analysis using traditional ML, neural networks, recurrent models, and Transformer-based models.

In this lab, you will use an LLM as a sentiment analysis system and evaluate whether its prompt is reliable.

The key question is:

> How do we know whether a prompt is trustworthy for movie review analysis?

## 2. Task

Build and evaluate prompts for CineSense, an LLM-based assistant for analyzing movie reviews.

Minimum task:

- Input: one movie review.
- Output: sentiment label, short explanation, and evidence phrases.
- Sentiment labels: `positive` or `negative`.

Advanced task:

- Extract aspects such as acting, story, visuals, music, pacing, ending, dialogue, and direction.
- Assign polarity to each aspect.
- Estimate confidence.
- Detect unsupported evidence or hallucination.

## 3. Required prompts

You must create and compare three prompt versions.

### Prompt v1 – Baseline prompt

Use or adapt:

```text
prompts/prompt_template_v1.txt
```

This prompt should be simple and direct.

### Prompt v2 – Improved prompt

Use or adapt:

```text
prompts/prompt_template_v2.txt
```

This prompt should improve v1 by adding clearer rules, stricter output format, exact evidence, and constraints against unsupported information.

### Prompt v3 – CoT-inspired prompt

Use or adapt:

```text
prompts/prompt_template_v3_cot.txt
```

This prompt should encourage the LLM to check the review step by step before returning the final JSON.

Important: the final answer must still be valid JSON only. Do not output a long reasoning paragraph.

## 4. Testset requirement

Create a testset with 20–50 reviews.

Use:

```text
data/student_testset_template.csv
```

Your testset should include different review types:

| Type | Meaning |
|---|---|
| easy | Sentiment is clear |
| mixed | Review contains both praise and criticism |
| ambiguous | Overall sentiment is not obvious |
| keyword_trap | Surface words may mislead the model |
| long_review | Review is longer than usual |

## 5. Running the prompts

Run all three prompts on the same testset.

You may use one of the following methods:

1. Web UI: ChatGPT, Gemini, Claude, etc.
2. API: Gemini API, Groq API, OpenRouter, etc.
3. Local model: Ollama or another local LLM.
4. Sample outputs, only if API or internet access is unavailable.

Save your results as:

```text
result_v1.csv
result_v2.csv
result_v3_cot.csv
```

Each result file should include:

```text
review_id,review_text,gold_sentiment,prompt_version,llm_output
```

## 6. Evaluation

Evaluate each prompt using:

```text
eval/eval_template.csv
```

Required metrics:

| Metric | Meaning |
|---|---|
| Accuracy | Correct sentiment prediction rate |
| Valid JSON rate | Percentage of valid JSON outputs |
| Evidence exactness rate | Percentage of outputs with exact evidence from the review |
| Hallucination count | Number of outputs that invent unsupported content |
| Outside knowledge count | Number of outputs that use facts not stated in the review |
| Overconfidence count | Number of uncertain cases with too high confidence |

Create three evaluation files:

```text
eval_v1.csv
eval_v2.csv
eval_v3_cot.csv
```

## 7. Error analysis report

Use:

```text
submissions/error_analysis_template.md
```

Your report must include:

1. Task definition.
2. Testset summary.
3. Prompt v1, v2, and v3.
4. Quantitative comparison table.
5. Error bucket table.
6. Three interesting error examples.
7. Reflection on whether CoT helped.
8. Final conclusion.

## 8. Submission structure

Submit a folder named:

```text
lab6_submission/
```

Required files:

```text
lab6_submission/
├── prompt_v1.txt
├── prompt_v2.txt
├── prompt_v3_cot.txt
├── testset.csv
├── result_v1.csv
├── result_v2.csv
├── result_v3_cot.csv
├── eval_v1.csv
├── eval_v2.csv
├── eval_v3_cot.csv
└── error_analysis.md
```

## 9. Important reminder

Do not judge prompts by feeling.

A good prompt must be supported by:

- testset results;
- metrics;
- error buckets;
- concrete examples;
- clear reflection.

CoT is not automatically better. You must prove whether it helps using your evaluation results.
