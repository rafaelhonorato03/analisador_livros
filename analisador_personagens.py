import os
import re
import gc
import time
from itertools import combinations
from collections import Counter, defaultdict
from pathlib import Path
import spacy
import fitz
import pandas as pd
import numpy as np
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
from pyvis.network import Network
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

# Detecção de comunidades com a biblioteca louvain
try:
    import community.community_louvain as community_louvain
except ImportError:
    print("Aviso: A biblioteca 'python-louvain' não foi encontrada. A funcionalidade de detecção de comunidades não estará disponível.")
    community_louvain = None


# Classes de lógica de análise
class AnalisadorDePersonagens:
    """
    Classe para extrair, analisar e visualizar dados de personagens de um texto.
    """
    def __init__(self):
        """Inicializa o analisador, carregando os modelos necessários."""
        self.nlp = self._carregar_modelo_spacy()
        self.resultados = self._inicializar_resultados()
        self.nlp.max_length = 2000000 
        self.total_caracteres = 0

    @staticmethod
    def _carregar_modelo_spacy():
        """
        Carrega o modelo de linguagem do spaCy, que deve ser pré-instalado.
        """
        modelo = "pt_core_news_sm"
        try:
            return spacy.load(modelo)
        except OSError:
            raise RuntimeError(
                f"O modelo spaCy '{modelo}' não foi encontrado. "
                f"Certifique-se de que ele está listado corretamente em seu arquivo requirements.txt."
            )

    def _inicializar_resultados(self):
        """Retorna a estrutura de dados para armazenar os resultados da análise."""
        return {
            "frequencia": Counter(),
            "posicoes": defaultdict(list),
            "relacionamentos": Counter()
        }

    def _limpar_nome(self, nome_texto):
        """Remove títulos e excesso de espaços para agrupar nomes de personagens."""
        titulos = [
            'Sor', 'Lorde', 'Lady', 'Rei', 'Rainha', 'Senhor', 'Senhora',
            'Príncipe', 'Princesa', 'Dom', 'Dona'
        ]
        # Expressão regular para remover os títulos como palavras inteiras
        padrao = r'\b(' + '|'.join(titulos) + r')\b'
        nome_limpo = re.sub(padrao, '', nome_texto, flags=re.IGNORECASE)
        return nome_limpo.strip()
    
    def _extrair_texto_epub(self, epub_input):
        """ 
        Extrai o conteúdo de um arquivo Epub.
        *** ESTE MÉTODO FOI CORRIGIDO PARA SER FUNCIONAL E ROBUSTO ***
        """
        try:
            # A biblioteca ebooklib lida bem tanto com caminhos de arquivo quanto com bytes
            book = epub.read_epub(epub_input)
            
            # Itera sobre os itens do livro que são documentos de texto
            for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                content = item.get_content()
                soup = BeautifulSoup(content, 'html.parser')
                text = soup.get_text(separator='\n', strip=True)
                if text:
                    yield text
        except Exception as e:
            # Informa sobre o erro e continua, em vez de quebrar a aplicação
            print(f"Alerta: Não foi possível processar o EPUB. Pode estar corrompido ou protegido por DRM. Erro: {e}")
            # Retorna um gerador vazio para não quebrar o código que chama esta função
            yield from []
            
    def analisar_livro(self, pdf_input, tamanho_chunk=100000):
        """
        Processa um livro a partir de bytes de um arquivo PDF ou de um caminho de arquivo,
        otimizado para baixo consumo de memória.
        
        Args:
            pdf_input (bytes or str): Os bytes do arquivo PDF ou o caminho para ele.
            tamanho_chunk (int): O tamanho dos blocos de texto a serem processados por vez.
        """
        self.resultados = self._inicializar_resultados()
        self.total_caracteres = 0
        posicao_atual = 0

        is_pdf = False
        if isinstance(pdf_input, str):
            is_pdf = pdf_input.lower().endswith('.pdf')
        elif isinstance(pdf_input, bytes):
            is_pdf = pdf_input.startswith(b'%PDF')
        
        try:
            if is_pdf:
                if isinstance(pdf_input, bytes):
                    doc_pdf = fitz.open(stream=pdf_input, filetype="pdf")
                else:
                    doc_pdf = fitz.open(pdf_input)
                
                # Pre-calcula o tamanho total para normalização sem carregar tudo na memória
                self.total_caracteres = sum(len(page.get_text()) for page in doc_pdf)
                if self.total_caracteres == 0:
                    raise ValueError("O PDF parece estar vazio ou não contém texto extraível.")

                with doc_pdf:
                    # Processa página por página para manter o uso de memória baixo
                    for page_num, page in enumerate(doc_pdf):
                        texto_pagina = page.get_text()
                        if not texto_pagina:
                            continue

                        # Processa o texto da página com o modelo nlp
                        doc_nlp = self.nlp(texto_pagina)
                    
                        for sent in doc_nlp.sents:
                            personagens_na_frase = {
                                self._limpar_nome(ent.text) for ent in sent.ents 
                                if ent.label_ == "PER" and len(self._limpar_nome(ent.text).split()) < 4 and len(self._limpar_nome(ent.text)) > 2
                            }
                        
                            if not personagens_na_frase:
                                continue
                        
                            for p in personagens_na_frase:
                                # Calcula a posição relativa à posição inicial da página
                                posicao_absoluta = posicao_atual + sent.start_char
                                self.resultados["frequencia"][p] += 1
                                self.resultados["posicoes"][p].append(posicao_absoluta)
                        
                            if len(personagens_na_frase) > 1:
                                for par in combinations(sorted(list(personagens_na_frase)), 2):
                                    self.resultados["relacionamentos"][par] += 1
                    
                        # Atualiza a posição inicial para a próxima página
                        posicao_atual += len(texto_pagina)
                        gc.collect()
            
            else:
                # --- LÓGICA DO EPUB AJUSTADA PARA FUNCIONALIDADE ---
                # Calculo do tamanho total para normalização
                textos_epub = list(self._extrair_texto_epub(pdf_input))
                self.total_caracteres = sum(len(texto) for texto in textos_epub)
                if self.total_caracteres == 0:
                    raise ValueError("O EPUB parece estar vazio ou não contém texto extraível. Verifique se o arquivo não possui DRM (proteção de cópia).")
                
                for texto_capitulo in textos_epub:
                    self._processar_bloco_de_texto(texto_capitulo, posicao_atual)
                    posicao_atual += len(texto_capitulo)
                    gc.collect()


        except ValueError as ve:
            raise ve
        except Exception as e:
            # --- CORREÇÃO IMPORTANTE AQUI ---
            # A exceção é levantada corretamente, em vez de ser ignorada
            raise RuntimeError(f"Erro ao ler ou processar o arquivo: {e}")
        finally:
            gc.collect()

    def _processar_bloco_de_texto(self, texto, posicao_base):
        """ Processa um bloco de texto com o modelo nlp para encontrar personagens."""

        if not texto:
            return
        
        doc_nlp = self.nlp(texto)

        for sent in doc_nlp.sents:
            personagens_na_frase = {
                self._limpar_nome(ent.text) for ent in sent.ents
                if ent.label_ == "PER" and len(self._limpar_nome(ent.text).split()) < 4 and len(self._limpar_nome(ent.text)) > 2
                
            }

            if not personagens_na_frase:
                continue

            for p in personagens_na_frase:
                posicao_absoluta = posicao_base + sent.start_char
                self.resultados["frequencia"][p] += 1
                self.resultados["posicoes"][p].append(posicao_absoluta)

            if len(personagens_na_frase) > 1:
                for par in combinations(sorted(list(personagens_na_frase)), 2):
                    self.resultados["relacionamentos"][par] += 1

    # Gerando gráficos    
    def gerar_grafico_frequencia(self, top_n=25):
        """Gera um gráfico de barras com a frequência dos personagens."""
        mais_comuns = self.resultados["frequencia"].most_common(top_n)
        if not mais_comuns: return None
        
        df = pd.DataFrame(mais_comuns, columns=['Personagem', 'Frequência'])
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(x='Frequência', y='Personagem', data=df, palette='viridis', ax=ax)
        ax.set_title(f'Top {top_n} Personagens Mais Frequentes', fontsize=16)
        plt.tight_layout()
        return fig

    def gerar_grafico_dispersao(self, top_n=15):
        """Gera um gráfico de dispersão para mostrar onde os personagens aparecem no texto."""
        personagens_principais = [p for p, _ in self.resultados["frequencia"].most_common(top_n)]
        if not personagens_principais: return None

        n_personagens = len(personagens_principais)
        fig, axes = plt.subplots(n_personagens, 1, figsize=(14, 2 * n_personagens), sharex=True)
        if n_personagens == 1: axes = [axes]

        cores = plt.cm.viridis(np.linspace(0, 1, n_personagens))
        for i, personagem in enumerate(personagens_principais):
            ax = axes[i]
            # Verifica se total_caracteres não é zero para evitar divisão por zero
            if self.total_caracteres > 0:
                posicoes_norm = [(p / self.total_caracteres) * 100 for p in self.resultados["posicoes"].get(personagem, [])]
            else:
                posicoes_norm = []
            
            if posicoes_norm:
                ax.vlines(posicoes_norm, ymin=0, ymax=1, color=cores[i], alpha=0.7)
            
            ax.set_yticks([])
            ax.set_ylabel(personagem, rotation=0, ha='right', va='center', fontweight='bold')
            ax.set_xlim(0, 100)
        
        if axes.size > 0:
            axes[0].set_title('Dispersão de Aparições dos Personagens', fontsize=16, pad=20)
            axes[-1].set_xlabel('Posição no Texto (%)')
        
        plt.tight_layout()
        return fig

    def gerar_grafico_evolucao_dinamico(self, personagens_selecionados):
        """Gera um gráfico de densidade (KDE) para a evolução de personagens selecionados."""
        if not personagens_selecionados: return None
        
        fig, ax = plt.subplots(figsize=(14, 8))
        cores = plt.cm.tab10(np.linspace(0, 1, len(personagens_selecionados)))
        
        for i, personagem in enumerate(personagens_selecionados):
            if self.total_caracteres > 0:
                posicoes_norm = [(p / self.total_caracteres) * 100 for p in self.resultados["posicoes"].get(personagem, [])]
            else:
                posicoes_norm = []
                
            if posicoes_norm:
                sns.kdeplot(posicoes_norm, label=personagem, fill=True, alpha=0.3, color=cores[i], ax=ax, linewidth=2)
        
        ax.set_title('Evolução das Menções ao Longo do Livro', fontsize=16)
        ax.set_xlabel('Posição no Texto (%)', fontsize=12)
        ax.set_ylabel('Densidade de Menções', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
        
    def _criar_grafo_base(self, top_n):
        """Helper para criar um grafo NetworkX com os personagens e relacionamentos."""
        personagens_principais = {p for p, _ in self.resultados["frequencia"].most_common(top_n)}
        if not personagens_principais:
            return None

        G = nx.Graph()
        # Adiciona nós com tamanho baseado na frequência
        for p in personagens_principais:
            freq = self.resultados["frequencia"][p]
            G.add_node(p, size=np.log1p(freq) * 5, title=f"Menções: {freq}")
        
        # Adiciona arestas com peso baseado na força da interação
        for par, peso in self.resultados["relacionamentos"].items():
            if par[0] in G and par[1] in G:
                G.add_edge(par[0], par[1], weight=peso, title=f"Interações: {peso}")
        
        G.remove_nodes_from(list(nx.isolates(G))) # Remove personagens sem conexão
        return G if G.number_of_nodes() > 0 else None

    def gerar_rede_relacionamentos(self, top_n=30):
        """Gera um grafo interativo da rede de relacionamentos."""
        G = self._criar_grafo_base(top_n)
        if not G: return None
        
        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(G)
        net.set_options("""
        var options = {
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -100,
              "centralGravity": 0.01,
              "springLength": 200
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based"
          }
        }
        """)
        return net.generate_html(notebook=False)

    def gerar_rede_comunidades(self, top_n=50):
        """Gera um grafo interativo com detecção de comunidades (grupos)."""
        if not community_louvain:
            print("Função 'gerar_rede_comunidades' desabilitada pois 'python-louvain' não está instalado.")
            return None

        G = self._criar_grafo_base(top_n)
        if not G: return None

        partition = community_louvain.best_partition(G, weight='weight')
        for node, comm_id in partition.items():
            G.nodes[node]['group'] = comm_id
            G.nodes[node]['title'] += f"<br>Comunidade: {comm_id}"

        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(G)
        return net.generate_html(notebook=False)
        
    def analisar_pontes_narrativas(self, top_n=10):
        """Identifica personagens-ponte através da centralidade de intermediação."""
        G = self._criar_grafo_base(top_n=50) # Usa um grafo maior para a análise de centralidade
        if not G: return None

        # Calcula a centralidade
        betweenness = nx.betweenness_centrality(G, weight='weight', normalized=True)
        
        df_pontes = pd.DataFrame(list(betweenness.items()), columns=['Personagem', 'Centralidade de Intermediação'])
        return df_pontes.sort_values('Centralidade de Intermediação', ascending=False).head(top_n)

    def obter_estatisticas_comunidades(self, top_n=50):
        """Calcula e retorna estatísticas detalhadas para cada comunidade detectada."""
        if not community_louvain: return None

        G = self._criar_grafo_base(top_n)
        if not G: return None

        partition = community_louvain.best_partition(G, weight='weight')
        stats = defaultdict(lambda: {
            'personagens': [], 'frequencia_total': 0, 
            'interacoes_internas': 0, 'interacoes_externas': 0
        })

        for node, comm_id in partition.items():
            freq = self.resultados["frequencia"][node]
            stats[comm_id]['personagens'].append((node, freq))
            stats[comm_id]['frequencia_total'] += freq

        for p1, p2, data in G.edges(data=True):
            peso = data.get('weight', 1)
            comm1, comm2 = partition[p1], partition[p2]
            if comm1 == comm2:
                stats[comm1]['interacoes_internas'] += peso
            else:
                stats[comm1]['interacoes_externas'] += peso
                stats[comm2]['interacoes_externas'] += peso
        
        for comm_id in stats:
            stats[comm_id]['personagens'].sort(key=lambda x: x[1], reverse=True)

        return stats