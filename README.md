# Crypto Bot - Monitor de Criptomoedas

Este é um bot que monitora criptomoedas em tempo real, fornecendo gráficos interativos e sinais de compra/venda baseados em análise técnica.

## Características

- Monitoramento em tempo real das principais criptomoedas
- Gráficos interativos com candlesticks
- Sinais de compra e venda baseados em médias móveis
- Preços em Euro (EUR)
- Interface web amigável
- Não requer chave de API

## Criptomoedas Monitoradas

- Bitcoin (BTC)
- Ethereum (ETH)
- Binance Coin (BNB)
- Cardano (ADA)
- Solana (SOL)

## Como Instalar

1. Certifique-se de ter o Python 3.7+ instalado
2. Clone este repositório
3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Usar

1. Execute o bot com o comando:
```bash
streamlit run crypto_bot.py
```

2. O navegador abrirá automaticamente com a interface do bot
3. Selecione a criptomoeda desejada no menu lateral
4. Observe o gráfico em tempo real e os sinais de compra/venda

## Estratégia de Trading

O bot utiliza uma estratégia baseada em médias móveis:
- Sinal de COMPRA: quando a média móvel de 20 períodos cruza acima da média de 50 períodos
- Sinal de VENDA: quando a média móvel de 20 períodos cruza abaixo da média de 50 períodos

## Aviso

Este bot é apenas uma ferramenta de análise e não deve ser usado como único critério para decisões de investimento. Sempre faça sua própria pesquisa e considere múltiplos fatores antes de investir em criptomoedas. 
