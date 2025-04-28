import os
import base64
import streamlit as st
from transformers import pipeline
import yfinance as yf
import matplotlib.pyplot as plt

# ————— STYLES & THÈME —————
def inject_global_styles(font_path: str, bg_image_path: str):
    # Vérification des fichiers
    if not os.path.isfile(font_path):
        st.error(f"Police introuvable : {font_path}")
        return
    if not os.path.isfile(bg_image_path):
        st.error(f"Image de fond introuvable : {bg_image_path}")
        return
    
    font_b64 = load_base64(font_path)
    bg_b64   = load_base64(bg_image_path)
    
    css = f"""
    <style>
      /* 1) Police BreakingBad globale */
      @font-face {{
          font-family: 'BreakingBad';
          src: url(data:font/otf;base64,{font_b64}) format('opentype');
      }}
      html, body, [class*="st-"], [class^="st-"], 
      [data-testid="stAppViewContainer"] *, [data-testid="stSidebar"] * {{
          font-family: 'BreakingBad', sans-serif !important;
      }}
      /* 2) Fond d'écran */
      [data-testid="stAppViewContainer"] {{
          background: url("data:image/jpeg;base64,{bg_b64}") no-repeat center center fixed;
          background-size: cover;
      }}
      /* 3) Zones d'entrée en police standard, texte noir */
      [data-testid="stTextArea"] textarea,
      [data-testid="stTextInput"] input {{
          font-family: sans-serif !important;
          color: black !important;
      }}
      /* 4) Sorties de résultat en sans-serif blanc */
      .user-standard-font {{
          font-family: sans-serif !important;
          color: white !important;
      }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Fonction pour charger les fichiers en base64
def load_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

# Fonction pour styliser le texte
def stylize_text(text):
    return text

# Fonction pour afficher les graphiques forex avec yfinance
def plot_forex(pair):
    ticker = f"{pair[:3]}{pair[3:6]}=X" if len(pair) >= 6 else f"{pair}=X"
    data = yf.download(ticker, period="1mo")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data.index, data['Close'])
    ax.set_title(f"Cours {pair}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Prix")
    st.pyplot(fig)

# Fonction pour afficher le widget TradingView
def tradingview_widget(pair):
    html = f"""
    <div class="tradingview-widget-container">
      <div id="tradingview_chart"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget({{
        "width": 800,
        "height": 500,
        "symbol": "FX:{pair}",
        "interval": "D",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "fr",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tradingview_chart"
      }});
      </script>
    </div>
    """
    st.components.v1.html(html, height=550)

# ————— APPLICATION PRINCIPALE —————
def main():
    BASE        = os.path.dirname(__file__)
    FONT_PATH   = os.path.join(BASE, "breakingbad-font.otf")
    BG_IMAGE    = os.path.join(BASE, "breakingbad-wallpaper.jpg")
    LOGO_PATH   = os.path.join(BASE, "heisenberg.png")
    
    inject_global_styles(FONT_PATH, BG_IMAGE)
    
    # Header
    st.image(LOGO_PATH, width=180)
    
    # Utilisation de HTML simple sans f-strings pour le texte stylisé
    header_text = stylize_text('Analyse de Sentiment Financier')
    st.markdown(
        f"<h1 style='text-align:center; font-size:50px'>{header_text}</h1>",
        unsafe_allow_html=True
    )
    
    # Ligne problématique corrigée - séparation en chaîne normale
    desc_text = stylize_text('Cette application analyse le sentiment de vos textes financiers.')
    st.markdown(
        "<p style='text-align:center; font-size:22px'>" + 
        desc_text +
        "</p>",
        unsafe_allow_html=True
    )
    
    # Ligne problématique corrigée - séparation en chaîne normale
    guide_text = stylize_text('Entrez un texte ci-dessous pour obtenir l\'analyse.')
    st.markdown(
        "<p style='text-align:center; font-size:22px'>" + 
        guide_text +
        "</p>",
        unsafe_allow_html=True
    )
    
    # Sentiment
    text = st.text_area("Entrez votre texte ici", "")
    if st.button("Analyser le sentiment"):
        if text.strip():
            clf = pipeline("sentiment-analysis",
                           model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
            res = clf(text)[0]
            sentiment_result = f"<div class='user-standard-font'>**Sentiment :** {res['label']}  |  **Score :** {res['score']:.2f}</div>"
            st.markdown(sentiment_result, unsafe_allow_html=True)
        else:
            st.markdown(
                "<div class='user-standard-font'>Veuillez entrer un texte pour l'analyse.</div>",
                unsafe_allow_html=True
            )
    
    st.markdown("---")
    
    # Forex
    pair = st.text_input("Paire Forex (ex. EURUSD, GBPJPY)", "EURUSD")
    method = st.selectbox("Source des données", ["yfinance", "TradingView widget"])
    if st.button("Afficher le graphique"):
        if method == "yfinance":
            plot_forex(pair)
        else:
            tradingview_widget(pair)

if __name__ == "__main__":
    main()