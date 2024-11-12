import streamlit as st

# Controle de navegação
if "page" not in st.session_state:
    st.session_state.page = "home"

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

        st.markdown(
            f'''
            <div style="border: 2px solid #FFD700; padding: 20px; border-radius: 10px; background-color: #FFFFE0; color: black;">
                <h3 style="text-align: center;">Metas de Dieta</h3>
                <p style="text-align: center; font-size: 20px;"><b>Meta calórica diária: {meta_calorias:.2f} calorias</b></p>
                <p style="text-align: center; font-size: 20px;"><b>Meta diária em pontos: {meta_pontos:.2f} pontos</b></p>
            </div>
            ''', unsafe_allow_html=True
        )

    # Botão para mudar para a página de diário alimentar
    if st.button("Ir para o Diário Alimentar"):
        switch_page("diario_alimentar")

# Página de diário alimentar
def diario_alimentar():
    st.title("Diário Alimentar")
    st.write("Registre aqui o que você consumiu nas refeições.")

    # Função auxiliar para criar cada seção de refeição
    def criar_secao_refeicao(nome_refeicao):
        st.header(nome_refeicao)
        
        # Opção de selecionar alimento de uma lista
        alimento_selecionado = st.selectbox(f"Selecione o alimento para {nome_refeicao}:", ["Nenhum", "Maçã", "Banana", "Iogurte", "Pão Integral", "Ovo Cozido"])
        
        if alimento_selecionado != "Nenhum":
            st.write(f"Você adicionou **{alimento_selecionado}** ao {nome_refeicao}.")

        # Opção de fazer upload de uma foto do prato
        foto = st.file_uploader(f"Tire uma foto do seu prato para {nome_refeicao}:", type=["jpg", "jpeg", "png"])
        
        if foto is not None:
            st.write("Foto enviada! O sistema está analisando...")
            # Aqui chamamos a função do GPT "Fiscal da Dieta" para analisar a foto e registrar a refeição
            # resultado = fiscal_da_dieta_analisar_foto(foto, nome_refeicao)  # Exemplo de chamada de função
            # st.write(f"Alimentos identificados: {resultado}")

    # Criando seções para cada refeição
    criar_secao_refeicao("Café da manhã")
    criar_secao_refeicao("Almoço")
    criar_secao_refeicao("Lanches")
    criar_secao_refeicao("Jantar")

    # Botão para voltar à página de cálculo de TMB
    if st.button("Voltar para o Cálculo de TMB"):
        switch_page("home")

# Controle de navegação entre as páginas
if st.session_state.page == "home":
    calcular_tmb()
elif st.session_state.page == "diario_alimentar":
    diario_alimentar()
