from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

def charger_modele():
    """Charge le modèle et le tokenizer pré-entraînés."""
    tokenizer = AutoTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
    model = AutoModelForSequenceClassification.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return nlp

def analyser_sentiment(nlp, texte):
    """Analyse le sentiment d'un texte donné."""
    resultat = nlp(texte)
    label = resultat[0]['label']
    score = resultat[0]['score']
    return label, score

def main():
    """Fonction principale pour tester l'analyse de sentiment."""
    nlp = charger_modele()

    # Exemple de phrase financière
    texte = """XYZ Corporation's stock soared by 20% after reporting record-breaking annual profits and announcing a significant dividend increase for shareholders."""
    label, score = analyser_sentiment(nlp, texte)
    print(f"Phrase : {texte}")
    print(f"Sentiment : {label} (Score : {score:.4f})\n")

    # Tester avec des phrases personnalisées
    print("Entrez vos phrases financières (une par ligne). Tapez 'fin' pour terminer.")
    while True:
        phrase = input("Votre phrase : ")
        if phrase.lower() == 'fin':
            break
        label, score = analyser_sentiment(nlp, phrase)
        print(f"Sentiment : {label} (Score : {score:.4f})\n")

if __name__ == "__main__":
    main()
