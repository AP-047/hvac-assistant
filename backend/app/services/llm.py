from transformers import pipeline

# Use a smaller model for faster loading (can upgrade later)
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",  # Using small for now
    device_map="auto"
)

def generate_answer(prompt: str) -> str:
    """Generate an answer using the language model with improved parameters"""
    try:
        result = generator(
            prompt, 
            max_length=300,      # Increased from 150 to 300
            min_length=50,       # Add minimum length
            do_sample=True,      # Enable sampling for more natural responses
            temperature=0.7,     # Add some creativity
            top_p=0.9,          # Use nucleus sampling
        )
        answer = result[0]["generated_text"].strip()
        
        # Ensure the answer is substantial
        if len(answer) < 20:
            return "I need more context to provide a comprehensive answer about this HVAC topic."
            
        return answer
        
    except Exception as e:
        print(f"LLM generation error: {e}")
        return "I'm sorry, I encountered an error while generating the response. Please try again."