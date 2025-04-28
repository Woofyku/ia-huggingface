from transformers import pipeline
import gradio as gr

classifier = pipeline("sentiment-analysis", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

def analyze_sentiment(text):
    if not text:
        return "Entrez une phrase."
    result = classifier(text)[0]
    return f"Sentiment : {result['label']} (Score: {result['score']:.2f})"

iface = gr.Interface(
    fn=analyze_sentiment,
    inputs=gr.Textbox(placeholder="Écrivez une actualité financière ici...", label="Texte d'entrée"),
    outputs="text",
    title="Analyse de Sentiment Financier",
    description="Bienvenue dans notre outil d'analyse des sentiments pour les nouvelles économiques. Entrez une phrase et découvrez si elle est positive, négative ou neutre."
)

iface.launch()