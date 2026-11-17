# Online Retail II – Análise de Dados e Segmentação de Clientes

## Sobre o projeto

Projeto de Ciência de Dados desenvolvido a partir do dataset Online Retail II, com o objetivo de explorar dados transacionais de um e-commerce e investigar padrões de comportamento dos clientes.

O projeto utiliza SQL e Python para estruturar, consultar e analisar os dados, aplicando técnicas de engenharia de atributos, análise RFM e Machine Learning para segmentação de clientes.

## Objetivos

- Explorar e compreender os dados transacionais.
- Construir consultas SQL para análise de vendas e comportamento dos clientes.
- Desenvolver indicadores de Recência, Frequência e Valor Monetário (RFM).
- Investigar o ciclo de vida e a atividade dos clientes.
- Aplicar técnicas de clustering para identificar grupos de clientes com comportamentos semelhantes.

## Dataset

O projeto utiliza o dataset [Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii), disponibilizado pelo UCI Machine Learning Repository.

O conjunto de dados contém transações de um varejista online britânico, abrangendo o período de dezembro de 2009 a dezembro de 2011.

## Metodologia

### 1. Preparação e armazenamento dos dados

- Conversão dos dados originais de Excel para CSV utilizando Pandas.
- Criação de banco de dados SQLite para armazenamento das transações.
- Importação dos registros em lotes (*chunks*) utilizando Pandas e SQLAlchemy.
- Criação de índices para otimização das consultas SQL.

### 2. Análise de dados com SQL

Desenvolvimento de consultas analíticas para investigar diferentes aspectos do comportamento dos clientes:

- **Customer Lifecycle:** análise do ciclo de vida dos clientes.
- **RFM:** cálculo de Recência, Frequência e Valor Monetário.
- **DAU:** acompanhamento de clientes ativos diariamente.
- **MAU:** acompanhamento de clientes ativos mensalmente.
- **Rolling 28D Active:** análise de clientes ativos em janelas móveis de 28 dias.

### 3. Segmentação de clientes com Machine Learning

Aplicação de técnicas de aprendizado não supervisionado utilizando os indicadores RFM:

- Construção de atributos de Recência, Frequência e Valor Monetário.
- Aplicação de transformação logarítmica (`log1p`) para reduzir a assimetria das variáveis.
- Padronização dos atributos utilizando `StandardScaler`.
- Agrupamento de clientes utilizando K-Means, com quatro clusters.
- Avaliação da qualidade dos agrupamentos por meio do Silhouette Score.
- Utilização de PCA para redução de dimensionalidade e visualização dos clusters em duas dimensões.

## Tecnologias utilizadas

- **Linguagem:** Python.
- **Banco de dados:** SQLite.
- **Manipulação de dados:** Pandas, NumPy.
- **Consultas:** SQL, SQLAlchemy.
- **Machine Learning:** Scikit-learn (K-Means, StandardScaler, PCA e Silhouette Score).
- **Visualização:** Matplotlib e Seaborn.

## Estrutura do projeto

```text
projeto-port/
├── data/
│   ├── raw/
│   ├── processed/
│   └── database/
├── scripts/
│   ├── excel_to_csv.py
│   ├── create_database.py
│   ├── execute_query.py
│   └── customer_segmentation.py
├── sql/
│   └── analytics/
│       ├── customer_lifecycle.sql
│       ├── customer_rfm.sql
│       ├── dau.sql
│       ├── mau.sql
│       └── rolling_28d_active.sql
├── environment.yml
├── requirements.txt
└── README.md
```

## Como executar

### 1. Clonar o repositório

```bash
git clone https://github.com/joaoSilvaL/projeto-port.git
cd projeto-port
```

### 2. Configurar o ambiente

Utilizando Conda:

```bash
conda env create -f environment.yml
conda activate projeto-port
```

Ou utilizando pip:

```bash
pip install -r requirements.txt
```

### 3. Preparar os dados

Executar o script de conversão do arquivo Excel para CSV:

```bash
python scripts/excel_to_csv.py
```

### 4. Criar o banco de dados

```bash
python scripts/create_database.py
```

### 5. Executar consultas SQL

Exemplo de execução da consulta RFM:

```bash
python scripts/execute_query.py --query analytics/customer_rfm.sql --date 2011-12-10
```

### 6. Executar a segmentação de clientes

```bash
python scripts/customer_segmentation.py
```

## Referências

Chen, D. (2012). *Online Retail II* [Dataset]. UCI Machine Learning Repository.

https://doi.org/10.24432/C5CG6D

## Licença

O dataset Online Retail II é disponibilizado sob a licença Creative Commons Attribution 4.0 International (CC BY 4.0).

A licença do código-fonte deve ser consultada no arquivo LICENSE, caso disponibilizado.
