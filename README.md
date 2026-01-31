# Dashboard-Vendas-Jogos
Esse repositório tem como finalidade armazenar o código de criação de um dashboard de vendas de jogos, após o tratamento da respectiva base.


Este projeto consiste em um dashboard interativo desenvolvido com Streamlit, Pandas e Plotly, com o objetivo de analisar as vendas globais de videogames a partir de um dataset público amplamente utilizado em estudos exploratórios.

O dashboard permite analisar:
- Jogos mais vendidos
- Vendas por plataforma
- Editoras com maior volume de vendas
- Distribuição regional das vendas (América do Norte, União Europeia e Japão)

---

## 📊 Dataset

O dataset utilizado contém informações sobre:
- Nome do jogo
- Plataforma
- Ano de lançamento
- Gênero
- Editora
- Vendas por região
- Vendas globais (em milhões de unidades)

As vendas regionais estão agregadas nas seguintes categorias:
- América do Norte
- União Europeia
- Japão
- Outras regiões

---

## 🧹 Tratamento de Dados

Antes da construção do dashboard, foi realizado um processo de limpeza e preparação dos dados, resultando no dataframe final `df_limpo`.

### 1️⃣ Tratamento de valores nulos em variáveis categóricas

Para colunas categóricas (como editoras), os valores nulos foram substituídos por uma categoria explícita:

```text
"Não informado".
##

### Justificativa:

As colunas representam volume de vendas (em milhões de unidades)
#Os valores nulos em colunas de vendas foram substituídos por 0 (zero).
Um valor nulo, nesse contexto, indica ausência de registro de vendas naquela região

Substituir por zero evita distorções em agregações (soma, média)

Garante consistência matemática nos cálculos do dashboard

Essa decisão assume que a falta de valor indica venda inexistente ou não registrada, e não erro de medição.
