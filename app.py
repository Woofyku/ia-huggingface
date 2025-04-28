from transformers import pipeline
import gradio as gr

classifier = pipeline("sentiment-analysis", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
def analyze_sentiment(text):
if not text:
return "Entrez une phrase."
result = classifier(text)[0]
return f"Sentiment : {result['label']} (Score: {result['score']:.2f})"
iface = gr.Interface(fn=analyze_sentiment, inputs="text", outputs="text")
iface.launch()