# 📊 DataSaúde Pentecoste
Sistema acadêmico para análise de doenças recorrentes no município de Pentecoste – CE.

---

## 🚀 Tecnologias
```txt
- Python 3.14
- Flask
- Pandas
- Chart.js
- HTML5 + CSS3
- Ambiente Virtual (venv)
```
---

## 📦 Como rodar o projeto
🐍 0️⃣ Antes de tudo: qual comando Python usar no seu PC?

Dependendo da instalação do Python, o comando pode ser:
```txt
Tipo de Instalação	   |Comando correto
Python.org oficial	   |py ou python
Microsoft Store	      |python
Instalações antigas	  |python3
PCs com conflito	     |py -3
```
👉 Para descobrir qual funciona, rode no CMD:
```txt
py --version
python --version
python3 --version
py -3 --version

```
Use o comando que retornar a versão do Python.

💡Se o seu PC só funcionar com py, troque python → py em tudo.
### 1. Clonar o repositório
git clone (https://github.com/Eric-Sousadev/projeto-DataSaude-Pentecoste.git)

cd DataSaude-Flask



### 2. Criar o ambiente virtual
py -m venv venv


### 3. Ativar (Windows)
 
venv\Scripts\activate

### 4. Instalar dependências
py -m pip install flask pandas


### 5. Rodar o servidor
py app.py


Acesse no navegador:
http://127.0.0.1:5000


----

## 📁 Estrutura do Projeto
```txt
Projeto-DataSaude/
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── base_arboviroses_3anos.csv
│   └── sample_diseases.csv
│
├── db/
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── images/
│   │   ├── campanhasImg/
│   │   ├── imgSite/
│   │   ├── logos/
│   │   └── membros/
│   │
│   └── js/
│       └── script.js
│
├── templates/
│   ├── base.html
│   ├── campanhas.html
│   ├── doencas.html
│   ├── home.html
│   ├── index.html
│   └── sobre.html
│
└── venv/
|-app.py
|-README.md
```
---

## 👨‍💻 Equipe
Projeto desenvolvido para disciplina de Big Data / Python, Faculdade Unifanor Wyden – 2025.

---

## 📌 Objetivo
Criar uma plataforma simples e acessível para monitoramento de doenças prevalentes no município de Pentecoste-CE, com possibilidade de integração com a prefeitura no futuro.


