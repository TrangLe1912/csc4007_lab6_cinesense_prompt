# Error Bucket Guide – Lab 6 CineSense

Use this guide when analyzing outputs from Prompt v1, Prompt v2, and Prompt v3 CoT.

## 1. Error bucket table

| Error bucket | Meaning | Example |
|---|---|---|
| none | Output is acceptable | Correct sentiment, valid JSON, evidence is present |
| wrong_sentiment | Predicted sentiment differs from gold label | Gold: negative, predicted: positive |
| missed_positive_aspect | LLM ignores an important positive phrase | Review praises acting, output only discusses pacing |
| missed_negative_aspect | LLM ignores an important negative phrase | Review criticizes pacing, output omits it |
| wrong_aspect_polarity | Aspect found but polarity is wrong | A criticized aspect is marked as positive |
| invalid_json | Output is not valid JSON or has extra prose | Markdown text instead of JSON only |
| hallucinated_evidence | Evidence phrase is not present in the review | Adds a phrase that the review never says |
| overconfident | Confidence is high for ambiguous or mixed review | Mixed review but confidence = high |
| outside_knowledge | Uses movie facts not in the review | Mentions awards, actors, box office |
| keyword_trap | Model follows surface words and misses the overall attitude | Review contains praise words but the final attitude is critical |
| mixed_review_failure | Model fails to weigh both praise and criticism | Output only uses one side of a mixed review |
| cot_not_helpful | Prompt v3 CoT still fails or gives no improvement | CoT prompt still predicts wrong sentiment or returns weak evidence |
| other | Important error not covered above | Explain in notes |

## 2. Minimum expectation

Students must:

- Evaluate at least 20 reviews.
- Compare Prompt v1, Prompt v2, and Prompt v3 CoT.
- Use the same testset for all prompts.
- Include at least 3 concrete examples of errors.
- Explain how Prompt v2 and Prompt v3 attempted to fix the errors of Prompt v1.

## 3. How to assign an error bucket

Use the most important error as the main bucket.

Recommended priority:

```text
invalid_json
wrong_sentiment
hallucinated_evidence / outside_knowledge
keyword_trap / mixed_review_failure
missed_positive_aspect / missed_negative_aspect
wrong_aspect_polarity
overconfident
cot_not_helpful
other
