# Lab 6 Rubric – CineSense Prompt Evaluation

Total: 10 points

| Criteria | Points | Description |
|---|---:|---|
| Testset quality | 1.5 | 20–50 reviews; includes easy, mixed, ambiguous, keyword-trap, and long-review cases; labels are clear and reasonable |
| Prompt design | 2.0 | Prompt v1, v2, and v3 CoT are meaningfully different; v2 and v3 improve on identified weaknesses of v1 |
| Experiment execution | 1.5 | All three prompts are run on the same testset; output files are complete and organized |
| Quantitative evaluation | 2.0 | Includes accuracy, valid JSON rate, evidence exactness rate, hallucination count, outside knowledge count, and overconfidence count |
| Error analysis | 2.0 | Uses error buckets correctly; includes concrete review examples; explains why each error matters |
| Reflection and conclusion | 1.0 | Clearly discusses whether Prompt v2 and Prompt v3 CoT improved reliability; conclusion is evidence-based |

## Performance levels

### Excellent

- Testset includes diverse and challenging cases.
- Prompt improvements are intentional and clearly explained.
- Evaluation is complete and consistent.
- Error examples are specific and insightful.
- Reflection avoids unsupported claims.

### Good

- Required files are complete.
- Metrics are mostly correct.
- Prompt versions are different but not deeply analyzed.
- Error analysis includes examples but may not fully connect them to prompt design.

### Needs improvement

- Testset is too small or lacks difficult cases.
- Prompt versions are almost identical.
- Output files are incomplete.
- Evaluation is based mostly on personal judgement.
- Error analysis is vague or missing concrete evidence.

## Notes for grading CoT

Do not award points simply because a prompt uses CoT-style wording.

Award points when students show evidence that Prompt v3 CoT:

- improves accuracy;
- improves evidence quality;
- reduces hallucination;
- handles mixed or keyword-trap reviews better;
- or, if it does not improve results, the student explains why using evidence.
