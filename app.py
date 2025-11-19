from flask import Flask, render_template
import pandas as pd
import os
from flask import send_file


app = Flask(__name__)

# Caminho para o CSV dentro da pasta /data
DATA_PATH = os.path.join("data", "sample_diseases.csv")

# Carrega o CSV
df = pd.read_csv(DATA_PATH)


# -------------------------------
#        LANDING PAGE (index)
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------------
#        DASHBOARD / HOME
# -------------------------------
@app.route("/home")
def home():
    total_casos = df["casos"].sum()
    total_doencas = df["doenca"].nunique()
    municipios = df["municipio"].nunique()

    return render_template(
        "home.html",
        total_casos=total_casos,
        total_doencas=total_doencas,
        municipios=municipios
    )


# -------------------------------
#            DOENÇAS
# -------------------------------
@app.route("/doencas")
def doencas():
    tabela = df.to_html(classes="tabela", index=False)
    return render_template("doencas.html", tabela=tabela)


# -------------------------------
#            SOBRE
# -------------------------------
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


# -------------------------------
#      EXECUTAR SERVIDOR
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)

# -------------------------------
#        DOWNLOAD CSV
@app.route("/download")
def download():
    return send_file("data/sample_diseases.csv", as_attachment=True)
