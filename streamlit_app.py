import streamlit as st
from datetime import datetime, timedelta

# Lista de Alimentos com Pontos e Calorias incorporada
alimentos = [
    {"Tipo do Alimento": "Abacate médio", "Pontos": 80, "Calorias": 288},
    {"Tipo do Alimento": "Abacaxi", "Pontos": 10, "Calorias": 36},
    {"Tipo do Alimento": "Abóbora", "Pontos": 5, "Calorias": 18},
    {"Tipo do Alimento": "Abobrinha", "Pontos": 0, "Calorias": 0},
    {"Tipo do Alimento": "Abobrinha Recheada", "Pontos": 40, "Calorias": 144},
    # Adicione o restante dos itens da lista conforme necessário
]

# Controle de navegação
if "page" not in st.session_state:
    st.session_state.page = "home"

# Inicializar o estado para a data e o consumo diário
if "data_diario" not in st.session_state:
    st.session_state.data_diario = datetime.today()
if "consumo_diario" not in st.session_state:
    st.session_state.consumo_diario = {"Café da manhã": [], "Almoço": [], "Lanches": [], "Jantar": []}
if "calorias_totais" not in st.session_state:
    st.session_state.calorias_totais = 0
if "pontos_totais" not in st.session_state:
    st.session_state.pontos_totais = 0

# Função para alternar entre páginas
def switch_page(page):
    st.session_state.page = page

# Página de cálculo de TMB
def calcular_tmb():
    st.title("Calculadora de Taxa Metabólica Basal (TMB) e Meta de Dieta de Pontos")

    sexo = st.radio("Qual é o seu sexo?", ('Masculino', 'Feminino'))
    idade = st.number_input("Qual é a sua idade em anos?", min_value=0, value=None, step=1)
    peso = st.number_input("Qual é o seu peso em kg?", min_value=0.0, value=None, step=0.1)
    altura = st.number_input("Qual é a sua altura em cm?", min_value=0.0, value=None, step=0.1)

    if idade is not None and peso is not None and altura is not None:
        if sexo == 'Masculino':
            tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * idade)
        else:
            tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * idade)

        st.write(f"**Sua TMB é aproximadamente {tmb:.2f} calorias por dia.**")

        nivel_atividade = st.selectbox(
            "Escolha o seu nível de atividade física:",
            [
                "Sedentário (pouco ou nenhum exercício)",
                "Levemente ativo (exercício leve 1 a 3 dias por semana)",
                "Moderadamente ativo (exercício moderado 3 a 5 dias por semana)",
                "Muito ativo (exercício intenso 6 a 7 dias por semana)",
                "Extremamente ativo (exercício físico muito intenso ou trabalho físico)"
            ]
        )

        fatores_atividade = {
            "Sedentário (pouco ou nenhum exercício)": 1.2,
            "Levemente ativo (exercício leve 1 a 3 dias por semana)": 1.375,
            "Moderadamente ativo (exercício moderado 3 a 5 dias por semana)": 1.55,
            "Muito ativo (exercício intenso 6 a 7 dias por semana)": 1.725,
            "Extremamente ativo (exercício físico muito intenso ou trabalho físico)": 1.9
        }

        gasto_total = tmb * fatores_atividade[nivel_atividade]
        st.write(f"**Seu gasto calórico total aproximado é de {gasto_total:.2f} calorias por dia.**")

        meta_calorias = max(gasto_total - 1000, 1000 if sexo == 'Feminino' else 1200)
        meta_pontos = meta_calorias / 3.6

        st.session_state.meta_calorias = meta_calorias
        st.session_state.meta_pontos = meta_pontos

        st.markdown(
            f'''
            <div style="border: 2px solid #FFD700; padding: 20px; border-radius: 10px; background-color: #FFFFE0; color: black;">
                <h3 style="text-align: center;">Metas de Dieta</h3>
                <p style="text-align: center; font-size: 20px;"><b>Meta calórica diária: {meta_calorias:.2f} calorias</b></p>
                <p style="text-align: center; font-size: 20px;"><b>Meta diária em pontos: {meta_pontos:.2f} pontos</b></p>
            </div>
            ''', unsafe_allow_html=True
        )

    if st.button("Ir para o Diário Alimentar"):
        switch_page("diario_alimentar")

# Página de diário alimentar
def diario_alimentar():
    st.title("Diário Alimentar")
    st.write("Registre aqui o que você consumiu nas refeições.")

    # Seção de data com botões para avançar e retroceder
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅️"):
            st.session_state.data_diario -= timedelta(days=1)
    with col2:
        st.write(st.session_state.data_diario.strftime("%d/%m/%Y"))
    with col3:
        if st.button("➡️"):
            st.session_state.data_diario += timedelta(days=1)

    # Função auxiliar para criar cada seção de refeição e sumarizar calorias e pontos
    def criar_secao_refeicao(nome_refeicao):
        st.header(f"{nome_refeicao} - Calorias: {sum([item['Calorias'] for item in st.session_state.consumo_diario[nome_refeicao]])} | Pontos: {sum([item['Pontos'] for item in st.session_state.consumo_diario[nome_refeicao]])}")

        # Seleção do alimento e cálculo de calorias e pontos
        alimento_selecionado = st.selectbox(f"Selecione o alimento para {nome_refeicao}:", ["Nenhum"] + [alimento["Tipo do Alimento"] for alimento in alimentos])
        
        if alimento_selecionado != "Nenhum":
            alimento_info = next(item for item in alimentos if item["Tipo do Alimento"] == alimento_selecionado)
            st.session_state.consumo_diario[nome_refeicao].append({
                "Alimento": alimento_selecionado,
                "Calorias": alimento_info["Calorias"],
                "Pontos": alimento_info["Pontos"]
            })
            st.session_state.calorias_totais += alimento_info["Calorias"]
            st.session_state.pontos_totais += alimento_info["Pontos"]

    # Criando seções para cada refeição
    criar_secao_refeicao("Café da manhã")
    criar_secao_refeicao("Almoço")
    criar_secao_refeicao("Lanches")
    criar_secao_refeicao("Jantar")

    # Exibindo o resumo diário
    st.markdown(
        f'''
        <div style="border: 2px solid #4682B4; padding: 20px; border-radius: 10px; background-color: #E0FFFF; color: black;">
            <h3 style="text-align: center;">Resumo Diário</h3>
            <p style="text-align: center; font-size: 20px;"><b>Meta de Calorias: {st.session_state.meta_calorias:.2f}</b></p>
            <p style="text-align: center; font-size: 20px;"><b>Calorias Consumidas: {st.session_state.calorias_totais:.2f}</b></p>
            <p style="text-align: center; font-size: 20px;"><b>Saldo de Calorias: {st.session_state.meta_calorias - st.session_state.calorias_totais:.2f}</b></p>
            <p style="text-align: center; font-size: 20px;"><b>Meta de Pontos: {st.session_state.meta_pontos:.2f}</b></p>
            <p style="text-align: center; font-size: 20px;"><b>Pontos Consumidos: {st.session_state.pontos_totais:.2f}</b></p>
            <p style="text-align: center; font-size: 20px;"><b>Saldo de Pontos: {st.session_state.meta_pontos - st.session_state.pontos_totais:.2f}</b></p>
        </div>
        ''', unsafe_allow_html=True
    )

       if st.button("Voltar para o Cálculo de TMB"):
        switch_page("home")

# Controle de navegação entre as páginas
if st.session_state.page == "home":
    calcular_tmb()
elif st.session_state.page == "diario_alimentar":
    diario_alimentar()
