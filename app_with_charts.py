import matplotlib.pyplot as plt
import gradio as gr
from transformers import pipeline

# Charger le modèle
classifier = pipeline("sentiment-analysis", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

# Fonction d'analyse du sentiment avec graphique
def analyze_sentiment(text):
    if not text:
        return "Enter an english sentence understanble for the NLP."
    result = classifier(text)[0]
    sentiment = result['label']
    score = result['score']
    return sentiment, score

def generate_chart(label,score):
    # Affichage d'un graphique
    labels = ['Positive', 'Neutral', 'Negative']
    values = [score if label == 'positive' else 0, score if label == 'neutral' else 0, score if label == 'negative' else 0]
    
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    
    return fig

# Interface Gradio
iface = gr.Interface(
    fn1=analyze_sentiment,
    fn2=generate_chart,
    inputs=gr.Textbox(placeholder="Écrivez une actualité financière ici...", label="Texte d'entrée"),
    outputs=["text", "fig"],
    title="Analyse de Sentiment Financier",
    description="Bienvenue dans notre outil d'analyse des sentiments pour les nouvelles économiques.",
)

iface.launch()
