from flask import Flask, render_template, send_file
import pandas as pd
import os

app = Flask(__name__)

# Caminho do CSV novo
DATA_PATH = os.path.join("data", "base_arboviroses_3anos.csv")

def load_data():
    """Carrega a base do CSV a partir de `DATA_PATH`.
    Esta função lê o arquivo do disco a cada chamada.
    """
    if os.path.exists(DATA_PATH):
        try:
            return pd.read_csv(DATA_PATH)
        except Exception:
            return pd.DataFrame({
                "casos_dengue": [0],
                "casos_chikungunya": [0],
                "casos_zika": [0],
                "ano": [2023]
            })
    else:
        return pd.DataFrame({
            "casos_dengue": [0],
            "casos_chikungunya": [0],
            "casos_zika": [0],
            "ano": [2023]
        })

# carrega uma vez para usar em rotas
df = load_data()

# garante colunas numéricas e sem NaNs
for col in ["casos_dengue", "casos_chikungunya", "casos_zika", "numero_obitos"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# -----------------------------
# ROTAS DO PROJETO
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html", landing=True)

@app.route("/home")
def home():
    # Carrega dados
    df = load_data()
    
    # Garante colunas numéricas e sem NaNs
    for col in ["casos_dengue", "casos_chikungunya", "casos_zika", "internacoes", "mortes", 
                "chuva_mm", "atendimentos", "capacidade", "tempo_espera_min", "impacto_pct"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # ===== TOTAIS SIMPLES =====
    total_dengue = int(df["casos_dengue"].sum()) if "casos_dengue" in df.columns else 0
    total_chikungunya = int(df["casos_chikungunya"].sum()) if "casos_chikungunya" in df.columns else 0
    total_zika = int(df["casos_zika"].sum()) if "casos_zika" in df.columns else 0
    total_casos = total_dengue + total_chikungunya + total_zika
    municipios = int(df["municipio"].nunique()) if "municipio" in df.columns else 0

    # ===== GRÁFICO 1: CASOS POR ANO =====
    if "ano" in df.columns:
        anos = sorted([int(x) for x in df["ano"].dropna().unique()])
    else:
        anos = []

    casos_ano = []
    for ano in anos:
        sub = df[df["ano"] == ano]
        s = 0
        for c in ["casos_dengue", "casos_chikungunya", "casos_zika"]:
            if c in sub.columns:
                s += int(sub[c].sum())
        casos_ano.append(s)

    # ===== GRÁFICO 2: DISTRIBUIÇÃO POR DOENÇA =====
    distro_labels = ["Dengue", "Chikungunya", "Zika"]
    distro_values = [
        int(df["casos_dengue"].sum()) if "casos_dengue" in df.columns else 0,
        int(df["casos_chikungunya"].sum()) if "casos_chikungunya" in df.columns else 0,
        int(df["casos_zika"].sum()) if "casos_zika" in df.columns else 0,
    ]

    # ===== GRÁFICO 3: TOP 10 BAIRROS =====
    if "bairro" in df.columns:
        df_copy = df.copy()
        df_copy["total_casos"] = 0
        for c in ["casos_dengue", "casos_chikungunya", "casos_zika"]:
            if c in df_copy.columns:
                df_copy["total_casos"] += df_copy[c]
        bairro_grp = df_copy.groupby("bairro")["total_casos"].sum().sort_values(ascending=False)
        bairros = list(bairro_grp.head(10).index)
        casos_bairros = [int(x) for x in bairro_grp.head(10).values]
    else:
        bairros = []
        casos_bairros = []

    # ===== GRÁFICO 4: IMPACTO DAS CHUVAS (SCATTER) =====
    if "chuva_mm" in df.columns and "casos_dengue" in df.columns:
        df_scatter = df[["chuva_mm", "casos_dengue"]].dropna()
        chuva_vals = [float(x) for x in df_scatter["chuva_mm"].values[:100]]  # limite 100 pontos
        dengue_vals = [int(x) for x in df_scatter["casos_dengue"].values[:100]]
    else:
        chuva_vals = []
        dengue_vals = []

    # ===== GRÁFICO 5: INTERNAÇÕES POR ANO =====
    if "internacoes" in df.columns and "ano" in df.columns:
        internacoes_ano = []
        for ano in anos:
            sub = df[df["ano"] == ano]
            internacoes_ano.append(int(sub["internacoes"].sum()) if "internacoes" in sub.columns else 0)
    else:
        internacoes_ano = [0] * len(anos)

    # ===== GRÁFICO 6: MORTALIDADE POR ANO =====
    if "mortes" in df.columns and "ano" in df.columns:
        mortes_ano = []
        for ano in anos:
            sub = df[df["ano"] == ano]
            mortes_ano.append(int(sub["mortes"].sum()) if "mortes" in sub.columns else 0)
    else:
        mortes_ano = [0] * len(anos)

    # ===== GRÁFICO 7: CAPACIDADE VS ATENDIMENTO POR MÊS (agregado) =====
    if "mes" in df.columns and "atendimentos" in df.columns and "capacidade" in df.columns:
        meses_labels = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
        atendimentos_mes = []
        capacidade_mes = []
        for m in range(1, 13):
            sub = df[df["mes"] == m]
            atendimentos_mes.append(int(sub["atendimentos"].sum()) if len(sub) > 0 else 0)
            capacidade_mes.append(int(sub["capacidade"].mean()) if len(sub) > 0 else 0)
    else:
        meses_labels = []
        atendimentos_mes = []
        capacidade_mes = []

    # ===== GRÁFICO 8: TEMPO MÉDIO DE ESPERA POR BAIRRO (top 10) =====
    if "bairro" in df.columns and "tempo_espera_min" in df.columns:
        bairro_tempo = df.groupby("bairro")["tempo_espera_min"].mean().sort_values(ascending=False)
        bairros_tempo = list(bairro_tempo.head(10).index)
        tempos = [round(float(x), 1) for x in bairro_tempo.head(10).values]
    else:
        bairros_tempo = []
        tempos = []

    return render_template(
        "home.html",
        # Totais
        total_casos=total_casos,
        total_dengue=total_dengue,
        total_chikungunya=total_chikungunya,
        total_zika=total_zika,
        municipios=municipios,
        # Gráfico 1
        anos=anos,
        casos_ano=casos_ano,
        # Gráfico 2
        distro_labels=distro_labels,
        distro_values=distro_values,
        # Gráfico 3
        bairros=bairros,
        casos_bairros=casos_bairros,
        # Gráfico 4
        chuva_vals=chuva_vals,
        dengue_vals=dengue_vals,
        # Gráfico 5
        internacoes_ano=internacoes_ano,
        # Gráfico 6
        mortes_ano=mortes_ano,
        # Gráfico 7
        meses_labels=meses_labels,
        atendimentos_mes=atendimentos_mes,
        capacidade_mes=capacidade_mes,
        # Gráfico 8
        bairros_tempo=bairros_tempo,
        tempos=tempos,
        title="Dashboard"
    )

@app.route("/doencas")
def doencas():
    # Mostra a tabela completa com todas as colunas
    if df.empty:
        tabela_html = "<p>Nenhum dado disponível.</p>"
    else:
        # Seleciona colunas principais para exibição
        colunas_exibir = ["municipio", "ano", "mes", "bairro", "casos_dengue", 
                         "casos_chikungunya", "casos_zika", "classificacao"]
        
        # Filtra apenas colunas que existem
        colunas_exibir = [col for col in colunas_exibir if col in df.columns]
        
        if colunas_exibir:
            # ordenar por ano (decrescente) para trazer anos mais recentes no topo
            if 'ano' in df.columns:
                df_exibir = df[colunas_exibir].sort_values(by='ano', ascending=False)
            else:
                df_exibir = df[colunas_exibir]
            # mostrar todas as linhas (o dataset tem ~850 linhas; enviar para o cliente é aceitável)
            tabela_html = df_exibir.to_html(classes="table-auto w-full", index=False)
        else:
            tabela_html = df.head(100).to_html(classes="table-auto w-full", index=False)

    return render_template(
        "doencas.html",
        tabela=tabela_html,
        title="Doenças"
    )

@app.route("/campanhas")
def campanhas():
    # Usa caminho baseado no diretório da aplicação
    base_dir = os.path.dirname(os.path.abspath(__file__))
    campanhas_dir = os.path.join(base_dir, "static", "images", "campanhasImg")
    imagens = []
    
    print(f"[DEBUG] Procurando campanhas em: {campanhas_dir}")
    print(f"[DEBUG] Pasta existe? {os.path.exists(campanhas_dir)}")
    
    if os.path.exists(campanhas_dir):
        # lista arquivos de imagem da pasta
        extensoes = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
        todos_arquivos = os.listdir(campanhas_dir)
        print(f"[DEBUG] Arquivos encontrados: {todos_arquivos}")
        
        imagens = [f for f in todos_arquivos 
                   if os.path.splitext(f)[1].lower() in extensoes]
        imagens.sort()  # ordena alfabeticamente
        print(f"[DEBUG] Imagens filtradas: {imagens}")
    else:
        print(f"[DEBUG] Pasta NÃO encontrada em: {campanhas_dir}")
    
    return render_template(
        "campanhas.html",
        imagens=imagens,
        title="Campanhas de Saúde"
    )

@app.route("/sobre")
def sobre():
    return render_template("sobre.html", title="Sobre o Projeto")

# -----------------------------
# DOWNLOAD DA PLANILHA
# -----------------------------

@app.route("/download")
def download():
    return send_file(DATA_PATH, as_attachment=True)


# -----------------------------
# INICIAR SERVIDOR
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
