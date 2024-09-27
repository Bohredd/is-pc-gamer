# 🖥️ Verificador de Computador Gamer 🎮

Este é um projeto desenvolvido em Django e Machine Learning para ajudar pais, tios, avós e outros familiares a verificarem se o computador que estão comprando para o neto, filho, sobrinho (ou até para si mesmos!) é adequado para jogos. A aplicação analisa as especificações do computador e fornece uma avaliação indicando se ele é "gamer" ou não.

## 🚀 Funcionalidades

- **Análise de Hardware**: Compara as especificações da CPU, GPU, RAM e armazenamento com os requisitos dos jogos mais populares.
- **Modelo de Machine Learning**: Um modelo de Machine Learning classifica o computador como "Gamer" ou "Não Gamer" com base nas especificações de hardware fornecidas.
- **Recomendações Personalizadas**: Oferece sugestões para melhorar o desempenho do computador em jogos (como upgrades de hardware).
- **Interface Intuitiva**: Interface simples e fácil de usar, feita para quem não entende de tecnologia.
  
## 🛠️ Tecnologias Utilizadas

- **Django**: Framework web para backend e frontend.
- **Python**: Linguagem de programação principal.
- **Scikit-Learn**: Biblioteca de Machine Learning usada para treinar e testar o modelo.
- **BeautifulSoup**: Para extrair informações de benchmarks de hardware.
- **Bootstrap**: Framework de design para criar uma interface amigável e responsiva.

## 📊 Como Funciona

1. **Entradas do Usuário**: Os familiares inserem as especificações do computador que desejam comprar (como processador, placa de vídeo, memória RAM e armazenamento).
2. **Análise de Dados**: O sistema compara essas especificações com os requisitos mínimos e recomendados para jogos e utiliza um modelo de Machine Learning para classificar o computador.
3. **Resultado**: O sistema retorna uma avaliação, indicando se o computador é adequado para jogos e oferece sugestões para possíveis melhorias.

## 🏗️ Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- Pip (gerenciador de pacotes do Python)
- Virtualenv (opcional, mas recomendado)
- Banco de dados PostgreSQL ou MySQL

### Passo a Passo

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/verificador-gamer.git
   cd verificador-gamer
