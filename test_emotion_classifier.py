from transformers import pipeline

# define pipeline
classifier = pipeline(
    "sentiment-analysis", model="michellejieli/emotion_text_classifier"
)
print(classifier("I love this!"))
