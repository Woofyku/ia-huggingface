from transformers import pipeline
classifier = pipeline("sentiment-analysis", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

print("Modèle NEUTRE : The central bank held its interest rate steady at 5%")
print(classifier("The central bank held its interest rate steady at 5%"))

print("Modèle POSITIF : Tesla's stock price surges after strong earnings")
print(classifier("Tesla's stock price surges after strong earnings."))

print ("Modèle NEGATIF : The financial crisis is expected to worsen in the coming months")
print(classifier("The financial crisis is expected to worsen in the coming months"))