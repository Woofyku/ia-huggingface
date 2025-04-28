import matplotlib.pyplot as plt
import gradio as gr
from transformers import pipeline

# Charger le modèle
classifier = pipeline("sentiment-analysis", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

# Fonction d'analyse du sentiment avec graphique
def analyze_sentiment_with_chart(text):
    if not text:
        return "Enter an english sentence understandable for the NLP.", None

    result = classifier(text)[0]
    sentiment = result['label'].lower()  # 'positive', 'neutral', 'negative'
    score = result['score']

    # Préparer les valeurs pour le graphique
    labels = ['positive', 'neutral', 'negative']
    values = [score if sentiment == l else 0 for l in labels]

    # Générer le graphique
    fig, ax = plt.subplots()
    ax.pie(values, labels=[l.capitalize() for l in labels], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    # Texte de sortie
    output_text = f"Sentiment: {sentiment.capitalize()} (score: {score:.2f})"
    return output_text, fig

# Interface Gradio
iface = gr.Interface(
    fn=analyze_sentiment_with_chart,
    inputs=gr.Textbox(placeholder="Écrivez une actualité financière ici...", label="Texte d'entrée"),
    outputs=["text", "plot"],
    title="Analyse de Sentiment Financier",
    description="Bienvenue dans notre outil d'analyse des sentiments pour les nouvelles économiques.",
)

if __name__ == "__main__":
    iface.launch()