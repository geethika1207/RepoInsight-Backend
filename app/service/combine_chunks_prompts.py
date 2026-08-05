
def combine_retrieval_chunks(chunk1, chunk2):
    combined_chunks = chunk1 + chunk2

    # it is used to remove same chunks in boh retrieval chunnks
    combined_chunks_without_duplicates = dict.fromkeys(combined_chunks)  # it returns strings vertically like A B C
    final_chunks = "\n\n".join(combined_chunks_without_duplicates)   # it groups those individual strings with 2 new line gaps in list  ["A, "B", "C"]

    return final_chunks 



def summary_technology_stack_prompts(prompt1, prompt2):
    PROJECT_OVERVIEW_QUERY = f"""
        {prompt1}

        {prompt2}

    The two tasks above must be completed independently.

    Return ONLY one valid JSON object in the exact format below.

    The value of "Repository_summary" must contain ONLY the repository summary.

    The value of "Technology_stack" must contain ONLY the technology stack information.

    Do not mix information between the two sections.

    Do not include markdown.
    Do not include code fences.
    Do not include explanations.
    Do not add extra fields.
    Do not omit any fields.

    {{
        "repository_summary" :{{
            "overall_summary" : "..."
        }}
        "technology_stack" :{{
           "programming_language" : "...",
           "backend_framework" : "...",
           "frontend_framework" : "...",
           "libraries" : [...],
           "database" : "...",
           "orm" : "...",
           "vector_database" : "...",
           "ai/llm_models" : [...],
           "embedding_model" : "...",
           "authentication" : "...",
           "cache" : "...",
           "bachground_jobs queue" : "...",
           "cloud & deployment" : "...",
           "external api's / services" : [...],
           "development tools" : [...],   
           "testing frameworks" : [...]
        }}
    }}

"""


def architecture_flow_database_flow_prompts(prompt1, prompt2):
    PROJECT_flow_QUERY = f"""
        {prompt1}

        {prompt2}

    The two tasks above must be completed independently.

    Return ONLY one valid JSON object in the exact format below.

    The value of "Repository_summary" must contain ONLY the repository summary.

    The value of "Technology_stack" must contain ONLY the technology stack information.

    Do not mix information between the two sections.

    Do not include markdown.
    Do not include code fences.
    Do not include explanations.
    Do not add extra fields.
    Do not omit any fields.

    {{
        "architecture_flow" :{{
              "architecture_flow": [
                    "...",
                    "...",
                    "..."
                ],
                "architecture_summary": "..."
        }}
        "database_flow" :{{
            "database_flow" : [...],
            "database_summary" : "..."
        }}
    }}

"""


def architecture_review_code_quality_review_prompts(prompt1, prompt2):
    PROJECT_review_QUERY = f"""
        {prompt1}

        {prompt2}

    The two tasks above must be completed independently.

    Return ONLY one valid JSON object in the exact format below.

    The value of "Repository_summary" must contain ONLY the repository summary.

    The value of "Technology_stack" must contain ONLY the technology stack information.

    Do not mix information between the two sections.

    Do not include markdown.
    Do not include code fences.
    Do not include explanations.
    Do not add extra fields.
    Do not omit any fields.

    {{
        "architecture_review" :{{
            "overall_architecture" : "...",
            "strengths" : [...],
            "improvement_suggestions" : [...]
        }}
        "code_quality_review" :{{
            "code quality_review" : "...",
            "strengths" : [...],
            "improvement_suggestions" : [...]
        }}
    }}

"""


def production_review_security_review_prompts(prompt1, prompt2):
    PROJECT_review_QUERY = f"""
        {prompt1}

        {prompt2}

    The two tasks above must be completed independently.

    Return ONLY one valid JSON object in the exact format below.

    The value of "Repository_summary" must contain ONLY the repository summary.

    The value of "Technology_stack" must contain ONLY the technology stack information.

    Do not mix information between the two sections.

    Do not include markdown.
    Do not include code fences.
    Do not include explanations.
    Do not add extra fields.
    Do not omit any fields.

    {{
        "production_review" :{{
            "production_readiness" : "...",
            "strengths" : [...],
            "improvement_suggestions" : [...]
        }}
        "security_review" :{{
            "security_review" : "...",
            "strengths" : [...],
            "improvement_suggestions" : [...]
        }}
    }}

"""
