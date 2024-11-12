# Atualizando o código para definir os valores padrão dos campos como 0 e salvar novamente

codigo_atualizado = """
import streamlit as st

def calcular_tmb():
    st.title("Calculadora de Taxa Metabólica Basal (TMB)")

    # Pergunta o sexo
    sexo = st.radio("Qual é o seu sexo?", ('Masculino', 'Feminino'))
    idade = st.number_input("Qual é a sua idade em anos?", min_value=0, value=0)
    peso = st.number_input("Qual é o seu peso em kg?", min_value=0.0, value=0.0)
    altura = st.number_input("Qual é a sua altura em cm?", min_value=0.0, value=0.0)

    if sexo == 'Masculino':
        tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
    else:
        tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)

    st.write(f"Sua TMB é aproximadamente {tmb:.2f} calorias por dia.")

    # Nível de atividade
    nivel_atividade = st.selectbox(
        "Escolha o seu nível de atividade física:",
        ["Sedentário", "Levemente ativo", "Moderadamente ativo", "Muito ativo", "Extremamente ativo"]
    )

    fatores_atividade = {
        "Sedentário": 1.2,
        "Levemente ativo": 1.375,
        "Moderadamente ativo": 1.55,
        "Muito ativo": 1.725,
        "Extremamente ativo": 1.9
    }

    gasto_total = tmb * fatores_atividade[nivel_atividade]
    st.write(f"Seu gasto calórico total aproximado é de {gasto_total:.2f} calorias por dia.")

calcular_tmb()
"""

# Salvando o código atualizado em um novo arquivo .py
file_path_atualizado = "/mnt/data/calculadora_tmb_com_zero.py"
with open(file_path_atualizado, "w") as file:
    file.write(codigo_atualizado)

file_path_atualizado


calcular_tmb()
