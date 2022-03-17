def default_preprocessing(context: str, question: str) -> str:
    return f"context:{context} | question:{question}"

def default_posprocessing(result: str) -> str:
    return result