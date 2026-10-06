"""ETL: lê clientes de um CSV, gera uma mensagem de marketing por cliente e salva em outro CSV."""
import os

import pandas as pd

PASTA = os.path.dirname(os.path.abspath(__file__))
ENTRADA = os.path.join(PASTA, "dados", "usuarios.csv")
SAIDA = os.path.join(PASTA, "dados", "usuarios_com_mensagem.csv")
MODELO = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


def mensagem_local(nome):
    """Texto de reserva usado quando não há IA disponível."""
    return f"{nome.split()[0]}, investir hoje garante tranquilidade amanhã."


def gerar_mensagem(cliente, nome):
    """Pede à IA uma mensagem curta; se não houver IA ou ela falhar, usa o texto de reserva."""
    if cliente is None:
        return mensagem_local(nome)
    try:
        resposta = cliente.chat.completions.create(
            model=MODELO,
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": f"Crie uma mensagem para {nome} sobre a importância dos investimentos. "
                           "Máximo de 100 caracteres. Responda só com a mensagem.",
            }],
        )
        return (resposta.choices[0].message.content or "").strip().strip('"') or mensagem_local(nome)
    except Exception as erro:
        print(f"IA falhou para {nome} ({erro}); usando mensagem local.")
        return mensagem_local(nome)


def criar_cliente_ia():
    if not os.getenv("GROQ_API_KEY"):
        print("GROQ_API_KEY não definida: usando mensagem local.")
        return None
    from groq import Groq
    return Groq()


if __name__ == "__main__":
    df = pd.read_csv(ENTRADA, dtype=str)                                         # Extração
    cliente = criar_cliente_ia()
    df["Mensagem"] = [gerar_mensagem(cliente, nome) for nome in df["Nome"]]      # Transformação
    df.to_csv(SAIDA, index=False, encoding="utf-8")                              # Carregamento
    print(df[["Nome", "Mensagem"]].to_string(index=False))
