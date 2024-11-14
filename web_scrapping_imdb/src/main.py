from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# Função para "arredondar" a coluna 'numero_avaliacoes'
def formatar_avaliacoes(avaliacoes):
    avaliacoes = str(avaliacoes).strip()  # Garantir que é uma string

    if 'mil' in avaliacoes:
        avaliacoes = avaliacoes.replace('mil', '').strip().replace(',', '.')
        try:
            avaliacoes = float(avaliacoes) * 1000  # Multiplicar por 1 mil
            return f"{int(avaliacoes):,}"
        except ValueError:
            return "N/A"

    elif 'mi' in avaliacoes:
        avaliacoes = avaliacoes.replace('mi', '').strip().replace(',', '.')
        try:
            avaliacoes = float(avaliacoes) * 1000000  # Multiplicar por 1 milhão
            return f"{int(avaliacoes):,}"
        except ValueError:
            return "N/A"

    return avaliacoes  # Caso já esteja em formato numérico

# Inicializando o driver do Selenium
driver = webdriver.Chrome()

# Acessando a página dos top 250 filmes
url = "https://www.imdb.com/chart/top"
driver.get(url)

# Esperando a página carregar
time.sleep(3)

# Pegando o conteúdo HTML da página
html = driver.page_source

# Usando BeautifulSoup para parsear o HTML
site = BeautifulSoup(html, 'html.parser')

# Coletando os dados
dados = []

# Pegando os 250 filmes
filmes = site.find(
    'ul', 
    attrs={'class': "ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 iyTDQy compact-list-view ipc-metadata-list--base"}
)

for filme in filmes:
    filme_titulo = filme.find('h3', attrs={'class': 'ipc-title__text'})
    data_lancamento = filme.find('span', attrs={'class': 'sc-5bc66c50-6 OOdsw cli-title-metadata-item'})
    duracao = filme.find('span', attrs={"class": "sc-5bc66c50-6 OOdsw cli-title-metadata-item"})
    proxima_duracao = duracao.find_next_sibling()
    numero_avaliacoes = filme.find('span', attrs={'class': 'ipc-rating-star--voteCount'})
    avaliacao = filme.find('span', attrs={'class': 'ipc-rating-star--rating'})

    dados.append({
        'filme': filme_titulo.text,
        'data_lancamento': data_lancamento.text,
        'Duração do Filme': proxima_duracao.text,
        'numero_avaliacoes': numero_avaliacoes.text,
        'avaliacao': avaliacao.text
    })

# Criando o DataFrame
df = pd.DataFrame(dados)

# Removendo os parênteses da coluna 'numero_avaliacoes'
df['numero_avaliacoes'] = df['numero_avaliacoes'].str.replace("(", "").str.replace(")", "")

# Aplicando a função de formatação
df['numero_avaliacoes'] = df['numero_avaliacoes'].apply(formatar_avaliacoes)

# Salvando os dados em um arquivo CSV
df.to_csv('Filmes.csv', index=False)

# Exibindo os dados
print(df)

# Fechando o driver
driver.quit()
