# Lab 6 – Error Analysis Report

## 1. Task definition

- Selected task:
- Input:
- Output schema:
- LLM used:
- Prompt execution method: Web UI / API / local model

## 2. Testset

- Number of reviews:
- Number of positive reviews:
- Number of negative reviews:
- Number of easy reviews:
- Number of mixed reviews:
- Number of ambiguous reviews:
- Number of keyword-trap reviews:
- Number of long reviews:

## 3. Prompt v1 – Baseline Prompt

Paste Prompt v1 or link to file.

Briefly explain:

- What does this prompt ask the LLM to do?
- What output format does it require?

## 4. Prompt v2 – Improved Prompt

Paste Prompt v2 or link to file.

Briefly explain:

- What weaknesses of Prompt v1 does Prompt v2 try to fix?
- What rules or constraints are added?

## 5. Prompt v3 – CoT-inspired Prompt

Paste Prompt v3 or link to file.

Briefly explain:

- What step-by-step checking behavior does Prompt v3 encourage?
- Does it reveal full reasoning or only return final JSON?

## 6. Quantitative comparison

| Metric | Prompt v1 | Prompt v2 | Prompt v3 CoT | Comment |
|---|---:|---:|---:|---|
| Accuracy | | | | |
| Valid JSON rate | | | | |
| Evidence exactness rate | | | | |
| Hallucination count | | | | |
| Outside knowledge count | | | | |
| Overconfidence count | | | | |
| Error count | | | | |

## 7. Error buckets

| Error bucket | Count v1 | Count v2 | Count v3 CoT | Example review_id | Comment |
|---|---:|---:|---:|---|---|
| wrong_sentiment | | | | | |
| invalid_json | | | | | |
| hallucinated_evidence | | | | | |
| outside_knowledge | | | | | |
| missed_positive_aspect | | | | | |
| missed_negative_aspect | | | | | |
| keyword_trap | | | | | |
| mixed_review_failure | | | | | |
| overconfident | | | | | |
| cot_not_helpful | | | | | |

## 8. Three interesting errors

### Error 1

- Review ID:
- Review type: easy / mixed / ambiguous / keyword_trap / long_review
- Gold sentiment:
- Prompt version:
- What happened:
- Why it matters:
- How Prompt v2 or Prompt v3 tries to fix it:

### Error 2

- Review ID:
- Review type: easy / mixed / ambiguous / keyword_trap / long_review
- Gold sentiment:
- Prompt version:
- What happened:
- Why it matters:
- How Prompt v2 or Prompt v3 tries to fix it:

### Error 3

- Review ID:
- Review type: easy / mixed / ambiguous / keyword_trap / long_review
- Gold sentiment:
- Prompt version:
- What happened:
- Why it matters:
- How Prompt v2 or Prompt v3 tries to fix it:

## 9. Reflection

Answer briefly:

- What did the LLM do well?
- What kind of review was difficult?
- Did Prompt v2 improve over Prompt v1? Give evidence.
- Did Prompt v3 CoT improve over Prompt v2? Give evidence.
- Did CoT ever make the output worse, longer, or harder to parse?
- What would you improve next?

## 10. Final conclusion

Write 5–7 sentences answering:

> Which prompt is most reliable for CineSense, and why?

Your conclusion must refer to metrics and error examples, not only personal feeling.
