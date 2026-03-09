import os
from openai import OpenAI
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

# --- FERRAMENTAS ---

def pesquisar(query):
    print(f"--- [Buscando no Google: {query}] ---")
    search = GoogleSearch({
        "q": query,
        "api_key": os.getenv("SERPAPI_API_KEY")
    })
    results = search.get_dict()
    # Pegamos o primeiro resultado para não encher a memória da IA
    return results.get("organic_results", [{}])[0].get("snippet", "Sem resultados.")

def calcular(expressao):
    expressao_corrigida = expressao.replace("^", "**")  # Para permitir potências
    try:
        return str(eval(expressao_corrigida))
    except Exception as e:
        return f"Erro ao calcular: {e}"

# Mapeamos as funções para o código saber o que rodar
tools = {"pesquisar": pesquisar, "calcular": calcular}

# --- O BRAÇO DO AGENTE ---

system_prompt = """
Você é um Agente que resolve problemas em passos.
Estamos no ano de 2026. Sempre que pesquisar preços, use o ano corrente como referência
Comandos disponíveis:
- pesquisar: "termo de busca"
- calcular: "expressao matematica"

Siga sempre o formato:
Pensamento: O que vou fazer agora.
Ação: nome_da_ferramenta: "argumento"
PAUSE

Você receberá a Observação e continuará até dar a Answer final.
"""

def rodar_loop(pergunta):
    mensagens = [{"role": "system", "content": system_prompt}, {"role": "user", "content": pergunta}]
    
    for i in range(5): # Limite de 5 passos para não gastar API a toa
        response = client.chat.completions.create(model="gpt-4o", messages=mensagens)
        print(f"\nPasso {i+1}:\n{response.choices[0].message.content}")
        
        conteudo = response.choices[0].message.content
        if "Ação:" in conteudo:
            # Extração simples do comando
            acao_linha = [l for l in conteudo.split('\n') if "Ação:" in l][0]
            ferramenta = acao_linha.split("Ação: ")[1].split(":")[0].strip()
            argumento = acao_linha.split(":")[2].strip().replace('"', '')

            # Executa a ferramenta real
            resultado = tools[ferramenta](argumento)
            
            mensagens.append({"role": "assistant", "content": conteudo})
            mensagens.append({"role": "user", "content": f"Observação: {resultado}"})
        else:
            break

if __name__ == "__main__":
    print("Bem-vindo ao Agente LOOP! Digite sua pergunta ou escreva 'sair' para encerrar.")
    
    while True:
        pergunta = input("\nDigite sua pergunta: ")
        if pergunta.lower() == "sair":
            print("Encerrando o Agente LOOP :)")
            break
        rodar_loop(pergunta)