# ETL com Python: mensagens de marketing para clientes

Projeto simples de Ciência de Dados que mostra o fluxo **ETL** (Extração, Transformação e Carregamento) com a Alternativa 2 do desafio: um CSV completo no lugar da API.

## Fluxo

1. **Extração**: lê `dados/usuarios.csv` (colunas `Nome`, `Conta` e `Cartao`) com pandas.
2. **Transformação**: gera para cada cliente uma mensagem de até 100 caracteres sobre a importância dos investimentos, usando a API do Groq (modelo `openai/gpt-oss-20b`). Sem chave de API, ou se a IA falhar, usa uma mensagem local.
3. **Carregamento**: salva `dados/usuarios_com_mensagem.csv` com a nova coluna `Mensagem`.

## Como executar

```bash
pip install -r requirements.txt
python etl.py
```

Para usar a IA, crie uma chave gratuita em console.groq.com e defina antes de rodar (PowerShell):

```powershell
$env:GROQ_API_KEY = "sua-chave"
python etl.py
```

Os dados do CSV são fictícios.

## Arquivos

| Arquivo | Descrição |
|---|---|
| `etl.py` | O ETL completo |
| `dados/usuarios.csv` | Entrada |
| `dados/usuarios_com_mensagem.csv` | Saída gerada |
| `requirements.txt` | Dependências |
