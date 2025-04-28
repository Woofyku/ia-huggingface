
import matplotlib.pyplot as plt
import gradio as gr
from transformers import pipeline
from langdetect import detect, LangDetectException

# Charger le modèle
classifier = pipeline("sentiment-analysis", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

def analyze_sentiment_with_barplot(text):
    # Vérification entrée vide ou trop courte
    if not text or not text.strip():
        return "Error : Enter non empty prompt.", None
    if len(text.strip()) < 10:
        return "Error : Too short text for a relevant analysis.", None

    # Détection de la langue
    try:
        lang = detect(text)
        if lang != "en":
            return "Error : The text must be written in English for correct analysis.", None
    except LangDetectException:
        return "Error: Unable to detect the language of the text. Please rephrase.", None

    # Analyse du sentiment avec gestion des exceptions
    try:
        result = classifier(text)[0]
        sentiment = result['label'].lower()  # 'positive', 'neutral', 'negative'
        score = result['score']

        # Préparer les valeurs pour le barplot
        labels = ['positive', 'neutral', 'negative']
        values = [score if sentiment == l else 0 for l in labels]

        # Générer le barplot
        fig, ax = plt.subplots()
        bars = ax.bar([l.capitalize() for l in labels], values, color=['green', 'gray', 'red'])
        ax.set_ylim(0, 1)
        ax.set_ylabel('Score')
        ax.set_title('Sentiment Analysis Score')
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, value + 0.02, f"{value:.2f}", ha='center', va='bottom')

        output_text = f"Sentiment: {sentiment.capitalize()} (score: {score:.2f})"
        return output_text, fig
    except Exception as e:
        return f"Error while analysis : {str(e)}", None

iface = gr.Interface(
    fn=analyze_sentiment_with_barplot,
    inputs=gr.Textbox(placeholder="You may write a financial news here...", label="Input Text"),
    outputs=["text", "plot"],
    title="Financial Sentiment Analysis",
    description="Welcome to our sentiment analysis tool for economic news.",
)

if __name__ == "__main__":
    iface.launch()
