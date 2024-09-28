# 🖥️ Upgradify 🎮

Este é um projeto desenvolvido em Django e Machine Learning para ajudar pais, tios, avós e outros familiares a
verificarem se o computador que estão comprando para o neto, filho, sobrinho (ou até para si mesmos!) é adequado para
jogos. A aplicação analisa as especificações do computador e fornece uma avaliação indicando se ele é "gamer" ou não.

## 🚀 Funcionalidades

- **Análise de Hardware**: Compara as especificações da CPU, GPU, RAM e armazenamento com os requisitos dos jogos mais
  populares.
- **Modelo de Machine Learning**: Um modelo de Machine Learning classifica o computador como "Gamer" ou "Não Gamer" com
  base nas especificações de hardware fornecidas.
- **Recomendações Personalizadas**: Oferece sugestões para melhorar o desempenho do computador em jogos (como upgrades
  de hardware).
- **Interface Intuitiva**: Interface simples e fácil de usar, feita para quem não entende de tecnologia.

## 🛠️ Tecnologias Utilizadas

- **Django**: Framework web para backend e frontend.
- **Python**: Linguagem de programação principal.
- **Scikit-Learn**: Biblioteca de Machine Learning usada para treinar e testar o modelo.
- **BeautifulSoup**: Para extrair informações de benchmarks de hardware.
- **Bootstrap**: Framework de design para criar uma interface amigável e responsiva.

## 📊 Como Funciona

1. **Entradas do Usuário**: Os familiares inserem as especificações do computador que desejam comprar (como processador,
   placa de vídeo, memória RAM e armazenamento).
2. **Análise de Dados**: O sistema compara essas especificações com os requisitos mínimos e recomendados para jogos e
   utiliza um modelo de Machine Learning para classificar o computador.
3. **Resultado**: O sistema retorna uma avaliação, indicando se o computador é adequado para jogos e oferece sugestões
   para possíveis melhorias.

## 🏗️ Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- Pip (gerenciador de pacotes do Python)
- Virtualenv (opcional, mas recomendado)
- Banco de dados PostgreSQL ou MySQL

### Passo a Passo

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/bohredd/is-pc-gamer.git
   cd verificador-gamer
   ```

2. **Crie e ative um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use venv\Scripts\activate
   ```

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   python -m spacy download pt_core_news_sm
   ```

4. **Configure o banco de dados no arquivo settings.py**:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'nome_do_banco',
           'USER': 'usuario',
           'PASSWORD': 'senha',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```


5. **Execute as migrações para configurar o banco de dados**:

   ```python
   python manage.py migrate
   ```

6. **Carregue os dados de hardware para treino do modelo (opcional)**:

   ```bash
   python manage.py loaddata dados_hardware.json
   ```

7. **Inicie o servidor de desenvolvimento**:

   ```bash
   python manage.py runserver
   ```

8. **Acesse o aplicativo no navegador**:

   ```bash
   http://localhost:8000
   ```

# ⚙️ Uso

Acesse a página principal da aplicação e preencha o formulário com as especificações do computador. O sistema irá
analisar os dados e fornecer um diagnóstico sobre se o computador é "Gamer" ou não. Se o computador não for adequado, o
sistema sugere upgrades no hardware.

## 🤖 Machine Learning

O modelo de Machine Learning foi treinado utilizando benchmarks de performance de hardware e requisitos de jogos
populares. O objetivo do modelo é prever se uma combinação de CPU, GPU, RAM e armazenamento é suficiente para jogos.

O pipeline de Machine Learning envolve:

- Coleta de dados de benchmarks via web-scrapping.
- Treinamento de um modelo de classificação (usando Random Forest ou SVM).
- Busca de dados de periféricos via Spacy.
- Avaliação da precisão do modelo com dados reais de hardware.
- Testes unitários de predição de recomendação dos hardwares

## 🤖 Obtenção de Dados de Hardware de um anúncio

- O sistema também oferece uma funcionalidade para extrair as especificações de hardware de um anúncio de computador.
  Basta inserir o URL do anúncio e o sistema irá extrair as informações relevantes automaticamente.
- Caso queira testar via CLI, use o comando:
   ``` python
  python ./app/manage.py pc_infos "dados pc"
  ```

- Exemplos:
   ``` python
  python ./app/manage.py pc_infos "Este computador vem equipado com um Processador Intel Core i7-2600K, uma placa de vídeo NVIDIA GeForce RTX 3060 12GB e 16 GB DDR4 de Memória RAM."
  ```

   ``` python
  python ./app/manage.py pc_infos "O sistema vem com um processador AMD Ryzen 9 5900X e uma placa de vídeo NVIDIA GeForce RTX 3080 10GB, além de 32 GB DDR4 de memória RAM."
   ```
  
   ``` python
  python ./app/manage.py pc_infos "Este PC conta com um Intel Core i5-10400F, uma Radeon RX 570 8GB e 16GB DDR4 de RAM."
   ```

   ``` python
   python ./app/manage.py pc_infos "O laptop é equipado com um processador Intel Celeron N4020 e gráficos integrados Intel HD Graphics, com 8GB de RAM DDR3."
   ```
    
   ``` python
   python ./app/manage.py pc_infos "A máquina de servidor usa um Intel Xeon E5-2687W e uma placa de vídeo AMD Radeon Vega 64 com 12 GB de RAM DDR4."
   ```

   ``` python
   python ./app/manage.py pc_infos "O PC conta com um AMD Ryzen Threadripper 3990X, sem placa de vídeo dedicada, e 64GB de memória DDR4."
   ```
## 📦 API

O projeto também oferece uma API RESTful para permitir que desenvolvedores integrem a verificação em outras aplicações.

### Exemplos de Endpoints:

- **POST** `/api/verificar/` – Envia as especificações do computador e retorna a avaliação.
- **GET** `/api/recomendacoes/` – Obtém recomendações de upgrades para o hardware.

## 📝 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Fork o repositório.
2. Crie uma nova branch: `git checkout -b minha-nova-feature`.
3. Faça as alterações e commit: `git commit -m 'Adiciona nova feature'`.
4. Envie para o seu fork: `git push origin minha-nova-feature`.
5. Crie um Pull Request no GitHub.

## 📄 Licença

Este projeto está licenciado sob a MIT License.
