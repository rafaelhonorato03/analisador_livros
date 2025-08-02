# Analisador de Narrativas: Desvendando Histórias com Ciência de Dados

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![spaCy](https://img.shields.io/badge/spaCy-v3.x-brightgreen?logo=spacy)](https://spacy.io/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Transforme qualquer livro em um dashboard interativo! Esse projeto utiliza **Processamento de Linguagem Natural (PLN)** para "ler" obras literárias em formato PDF, extrair os personagens e mapear suas jornadas e relacionametos, revelando a estrutura oculta da narrativa através de visualizaçõe de dados dinâmicas.

Já se perguntou quem é *realmente* o personagem central da trama? Ou como as "panelinhas" de personagens se formam e interagem? Esta ferramenta responde a essas e outras perguntas, combinando a paixão pela literatura com o poder da ciência de dados.

## Funcionalidades

A ferramenta realiza uma análise completa e apresenta os resultados em uma interface web amigável construída com Streamlit.

* ** 📊 Ranking de Protagonismo:** Gráfico de barras que quantifica os personagens mais mencionados, oferecendo uma visão clara de sua importância.
* ** 📈 Linha do Tempo da Narrativa:**
    * **Gráfico de Dispersão:** Mostra *exatamente* em que ponto do livro cada personagem aparece.
    * **Gráfico de Evolução (KDE):** Visualiza os 'picos de popularidade' dos personagens, mostrando onde suas presenças são mais densas na história.
* **🕸️ Rede de Relacionamentos Interativa:** Um grafo dinâmico onde os nós são personagens e as arestas representam a força de suas interações (baseado na coocorrência em sentenças). Quanto mais espessa a linha, mais forte o laço!
* **🏘️ Detecção de Comunidades (Clusters):** Utilizando o algoritmo de Louvain, a ferramenta identifica e colore automaticamente os "grupos sociais" ou "nucleos narrativos" dentro da história.
* **🌉 Análise de Personagens-Ponte:** Identifica, através da métrica de *centralidade de intermediação*, os personagens que são cruciais para conectar diferentes grupos e manter a trama coesa.
* **🔎 Estatísticas Detalhadas:** Oferece dados quantitativos sobre cada comunidade, como número de membros, interações internas e conexões externas.

## Demo Interativa

Teste a ferramenta agora mesmo! Faça o upload de um livro PDF e veja a mágica acontecer.

**Acesse o App Streamlit:** [https://livrospersonagens.streamlit.app/]

## Como Funciona? A arquitetura por trás da magia

O projeto é dividido em dois componentes principais: um back-end de análise robusto e um front-end interativo.

1. **Extração de Texto:** O 'AnalisadorDePersonagens' utiliza a biblioteca **PyMuPDF (Fitz)** para extrair texto de arquivos PDF.
2. **Processamento com NLP:** O texto extraído é processdo pelo **spaCy**, utilizando o modelo pré-treinado em português ('pt_core_news_sm'), para realizar o Reconhecimento de Entidades Nomeadas (NER), identificando todos os personagens ('PER').
3. **Análise de Agregação:** Os dados são estruturados com **Pandas**. A lógica calcula:
    * A frequência de cada personagem.
    * A posição normalizada de cada aparição.
    * As coocorrências (pares de personagens na mesma frase) para medir a força dos relacionamentos.
4. **Análise de Redes:** A biblioteca **Networkx** é usada para modelar a rede social dos personagens. O algoritmo de **Louvain** ('python-louvain') é aplicado para a detecção de comunidades.
5. **Visualização de Dados:**
    * **Matplotlib** e **Seaborn** geram os gráficos estáticos (barras, dispersão, densidade).
    * **Pyvis** renderiza os grafos de rede interativos, que permitem zoom, arrastar e explorar as conexões.
6. **Interface Web:** O **Streamlit** encapsula tudo, fornecendo uma interface web reativa com widgets para upload de arquivos, abas para navegação e sliders para interação dinâmica com os gráficos.

## instalação e Uso Local

Para executar esse projeto em sua máquina local, siga os passos abaixo.

### Pré-requisitos

* Python 3.9 ou superior
* Git

### Passos

1. **Clone o repositório:***
    ```bash
    git cline https://github.com/rafaelhonorato03/analisador_livros.git
    cd analisador_livros
    ```

2. **Cire e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # windows
    .\venv\Scripts\activate
    # macOS\Linux
    source venv/bin/activate

3. **Instale as dependências:**
    Crie um arquivo 'requirements.txt' com as bibliotecas do projeto e executie:
    ```bash
    pip install -r requirements.txt
    ```

4. **Baixe o modelo do spaCy:**
    O modelo de linguagem em português é essencial para a análise.
    ```bash
    python -m spacy download pt_core_news_sm
    ```

### Executando a Aplicação

Com tudo instalado, inicie o servidor do Streamlit com um único comando:

```bash
streamlit run app.py
```
Seu navegador abrirá automaticamente com a aplicação pronta para uso!

## Stack Tecnológico

* **Linguagem:** Python
* **Processamento de Linguagem Natural (PLN):** spaCy
* **Extração de Texto:** PyMuPDF (Fitz), EbookLib, BeautifulSoup4
* **Análise de Dados:** Pandas, Numpy
* **Visualização de Dados:** Matplotlib, Seaborn
* **Redes e Grafos:** NetworkX, Pyvis
* **Detecção de Comunidades:** python-louvain-community
* **Interface Web:** Streamlit

## Autor

Feito com ❤️ por **[Rafael Honorato]**

* **LinkedIn:** [https://www.linkedin.com/in/rafael-honorato03/](https://www.linkedin.com/in/rafael-honorato03/)
* **GitHub:** [https://github.com/rafaelhonorato03](https://github.com/rafaelhonorato03)
