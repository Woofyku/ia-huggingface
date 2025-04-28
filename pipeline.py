from transformers import pipeline
classifier = pipeline("sentiment-analysis", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

print("Modèle POSITIF")
print(classifier("Tesla's stock price surges after strong earnings."))

print ("Modèle NEGATIF")
print(classifier("The financial crisis is expected to worsen in the coming months"))

print("Modèle NEUTRE")
print("The central bank held its interest rate steady at 5%")
