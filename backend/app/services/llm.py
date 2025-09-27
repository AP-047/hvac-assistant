from transformers import pipeline

# Initialize once when service starts
generator = pipeline(
    "text-generation", 
    model="microsoft/DialoGPT-medium",  # 345M params, good for chat
    tokenizer="microsoft/DialoGPT-medium",
    device_map="auto"
)

def generate_answer(prompt: str) -> str:
    response = generator(
        prompt, 
        max_length=200, 
        num_return_sequences=1,
        temperature=0.7,
        pad_token_id=generator.tokenizer.eos_token_id
    )
    return response[0]['generated_text'][len(prompt):].strip()