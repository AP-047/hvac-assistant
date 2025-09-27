from transformers import pipeline

generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    device_map="auto"
)

def generate_answer(prompt: str) -> str:
    result = generator(prompt, max_length=150, do_sample=False)
    return result[0]["generated_text"]