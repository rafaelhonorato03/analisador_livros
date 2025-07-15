# 📚 Analisador de Livros - Análise Inteligente de Narrativas

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red.svg)](https://streamlit.io/)
[![NLP](https://img.shields.io/badge/NLP-spaCy-green.svg)](https://spacy.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Transforme qualquer livro em insights valiosos através de análise computacional avançada de personagens e narrativas.**

## 🎯 Visão Geral

O **Analisador de Livros** é uma ferramenta revolucionária que utiliza Processamento de Linguagem Natural (NLP) e análise de redes para desvendar os segredos ocultos em qualquer obra literária. Através de uma interface web intuitiva, você pode fazer upload de livros em PDF e obter análises profundas sobre personagens, relacionamentos e estrutura narrativa.

### ✨ Principais Recursos

- 🔍 **Detecção Automática de Personagens** - Identifica e extrai personagens usando NLP avançado
- 📊 **Análise de Frequência** - Visualiza os personagens mais importantes da narrativa
- 📈 **Evolução Temporal** - Acompanha como os personagens aparecem ao longo da história
- 🕸️ **Rede de Relacionamentos** - Mapeia interações entre personagens de forma interativa
- 🌉 **Análise de Personagens-Ponte** - Identifica personagens cruciais para a trama
- 🏘️ **Detecção de Comunidades** - Agrupa personagens por afinidades narrativas
- ⚡ **Processamento Otimizado** - Análise eficiente mesmo em livros extensos

## 🚀 Demonstração Rápida

1. **Upload do Livro**: Arraste e solte qualquer arquivo PDF
2. **Análise Automática**: O sistema processa o texto em minutos
3. **Visualizações Interativas**: Explore os resultados através de gráficos e redes
4. **Insights Profundos**: Descubra padrões ocultos na narrativa

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.8+
- **Interface Web**: Streamlit
- **Processamento de PDF**: PyMuPDF
- **NLP**: spaCy (modelo português)
- **Análise de Dados**: Pandas, NumPy
- **Visualização**: Matplotlib, Seaborn
- **Análise de Redes**: NetworkX, PyVis
- **Detecção de Comunidades**: python-louvain

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/analisador_livros.git
   cd analisador_livros
   ```

2. **Crie um ambiente virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   streamlit run app.py
   ```

5. **Acesse no navegador**
   ```
   http://localhost:8501
   ```

## 📖 Como Usar

### 1. Interface Principal
- Acesse a aplicação web através do navegador
- A interface é intuitiva e responsiva

### 2. Upload do Arquivo
- Clique em "Arraste e solte seu arquivo PDF aqui"
- Selecione qualquer livro em formato PDF
- O sistema automaticamente iniciará a análise

### 3. Explorando os Resultados

#### 📊 Gráficos Gerais
- Visualize os personagens mais frequentes
- Entenda a hierarquia de importância na narrativa

#### 📈 Dispersão e Evolução
- Veja onde cada personagem aparece no livro
- Analise a evolução temporal das menções
- Compare múltiplos personagens simultaneamente

#### 🕸️ Rede de Relacionamentos
- Explore conexões interativas entre personagens
- Tamanho dos nós = frequência do personagem
- Espessura das linhas = força das interações

#### 🌉 Personagens-Ponte
- Identifique personagens cruciais para a trama
- Análise de centralidade de intermediação
- Descubra quem conecta diferentes grupos

#### 🏘️ Detecção de Comunidades
- Visualize grupos naturais de personagens
- Ajuste o número de personagens analisados
- Explore estatísticas detalhadas de cada comunidade

## 🔧 Configurações Avançadas

### Personalizando a Análise

O sistema permite ajustes finos para diferentes tipos de literatura:

- **Tamanho do chunk**: Otimize para livros muito grandes
- **Número de personagens**: Foque nos mais relevantes ou tenha visão ampla
- **Sensibilidade de detecção**: Ajuste para diferentes estilos de escrita

### Formatos Suportados

- ✅ PDF (recomendado)
- ✅ Texto extraível
- ✅ Múltiplos idiomas (com modelos spaCy apropriados)

## 📊 Exemplos de Análise

### Casos de Uso

1. **Análise Literária Acadêmica**
   - Estudos de personagens em obras clássicas
   - Análise comparativa entre autores
   - Pesquisa em narratologia computacional

2. **Escrita Criativa**
   - Balanceamento de personagens em romances
   - Verificação de desenvolvimento de personagens
   - Análise de estrutura narrativa

3. **Educação**
   - Ferramenta didática para análise literária
   - Visualização de conceitos narrativos
   - Estudo de técnicas de escrita

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Aqui estão algumas formas de contribuir:

### Como Contribuir

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Áreas para Melhoria

- [ ] Suporte a mais formatos de arquivo
- [ ] Análise de sentimento dos personagens
- [ ] Detecção de arcos narrativos
- [ ] Comparação entre múltiplos livros
- [ ] API REST para integração
- [ ] Análise de diálogos específicos

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **Thais André** pela inspiração inicial com seu trabalho sobre ["NLTK e Processamento de Linguagem Natural"](https://dev.to/thaisandre/nltk-e-processamento-de-linguagem-natural-3l49#:~:text=nltk%20(Natural%20Language%20Toolkit)%20%C3%A9,redes%20sociais%20e%20p%C3%A1ginas%20web.), que apresentou o uso da biblioteca NLTK para analisar o livro "Alice no País das Maravilhas" - este projeto foi fundamental para o desenvolvimento do Analisador de Livros
- **spaCy** pela excelente biblioteca de NLP
- **Streamlit** pela plataforma de desenvolvimento web
- **NetworkX** pelas ferramentas de análise de redes
- **Comunidade open source** por todas as bibliotecas utilizadas

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/analisador_livros/issues)
- **Documentação**: [Wiki do Projeto](https://github.com/seu-usuario/analisador_livros/wiki)
- **Email**: rafael.honorato03@gmail.com

---

<div align="center">

**⭐ Se este projeto foi útil para você, considere dar uma estrela! ⭐**

*Transformando a análise literária através da tecnologia*

</div>

