def final_prompt(report_chunks, report_prompt):
    final_llm_prompt = f"""
You are provided with the most relevant repository context retrieved from a vector database.

Use ONLY the retrieved repository context below to complete the requested task.

If the requested information is not available in the retrieved repository context, do not invent, assume, or infer it.
Instead, clearly state that the information is not available in the retrieved repository context.
Base every answer strictly on the retrieved repository context.

**REMEMBER** : 

Return ONLY valid JSON that exactly matches the following schema.
Do not include markdown, code fences, explanations, or extra text.

Repository Context:
{report_chunks}


Task:
{report_prompt}

"""
    return final_llm_prompt