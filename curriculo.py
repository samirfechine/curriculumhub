import streamlit as st
from bd import bd
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
st.set_page_config(
    page_title="curriculumHub",
    page_icon="📊",
    layout="wide"
)


st.image(image="https://i.ibb.co/JWYKmQC/De-Watermark-ai-1733765257276-Photoroom-3.png",width=500)
st.markdown("##### Bem vindo ao CurriculumHub! Aqui você pode cadastrar seu currículo e se candidatar a vagas de emprego.") 
# Rodapé com HTML e CSS embutido
footer = """
<style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f9f9f9;
        padding: 10px 20px;
        text-align: center;
        font-size: 12px;
        color: #888;
        border-top: 1px solid #e0e0e0;
    }
</style>
<div class="footer">
    © 2024 CurriculumHub. Todos os direitos reservados. | 
    <a href="https://www.seusite.com/politica" target="_blank">Política de Privacidade</a> | 
    <a href="https://www.seusite.com/termos" target="_blank">Termos de Uso</a> 
</div>
"""
st.markdown(footer, unsafe_allow_html=True)

# Menu de navegação
with st.sidebar:
    st.markdown("# Menu:")
    if st.button("📝 Cadastrar Currículo", key="botao_cadastrar_cv"):
        st.session_state['pagina'] = 'cadastrar'
    if st.button("✅ Atualizar Currículo"):
        st.session_state['pagina'] = 'atualizar'
    if st.button("❌ Deletar Currículo"):
        st.session_state['pagina'] = 'deletar'
    if st.button("⚙️ Cadastrar Vaga"):
        st.session_state['pagina'] = 'cadastrar_vaga'
    if st.button("📜 Listar Vagas"):
        st.session_state['pagina'] = 'listar_vaga'
def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)
    
    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula o primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - soma % 11
    if digito1 >= 10:
        digito1 = 0
    
    # Calcula o segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - soma % 11
    if digito2 >= 10:
        digito2 = 0
    
    # Verifica se os dígitos verificadores são iguais aos fornecidos
    return cpf[-2:] == f'{digito1}{digito2}'
    
def validar_email(email):
    padrao=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(padrao,email):
        return True
    else:
        return False
def limpar_texto(texto):
    # Remove pontuações e converte para minúsculas
    texto_limpo = re.sub(r'[^\w\s]', '', texto).lower()
    # Remove espaços extras
    texto_limpo = ' '.join(texto_limpo.split())
    return texto_limpo

def verificar_informacao(texto_predefinido, informacao_usuario):
    texto_predefinido_limpo = limpar_texto(texto_predefinido)
    informacao_usuario_limpo = limpar_texto(informacao_usuario)
    
    palavras_predefinidas = set(texto_predefinido_limpo.split())
    palavras_usuario = set(informacao_usuario_limpo.split())
    
    # Palavras em comum
    palavras_comum = palavras_predefinidas.intersection(palavras_usuario)
    print(palavras_comum)
    
    # Porcentagem baseada no texto predefinido
    porcentagem_comum = len(palavras_comum) / len(palavras_predefinidas) * 100

    # Resultado
    if porcentagem_comum >= 60:
        return True
    else:
        palavras_faltantes = palavras_predefinidas-palavras_usuario
        return palavras_faltantes
def enviar_email(destinatario, assunto, corpo):
    remetente = 'napnemaracanau@gmail.com'
    senha = 'svzf rsmd nknm skqa'

    # Configurar o servidor SMTP
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(remetente, senha)

    # Criar a mensagem de e-mail
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto
    mensagem.attach(MIMEText(corpo, 'plain'))

    # Enviar o e-mail
    servidor.send_message(mensagem)
    servidor.quit()
# Definindo a ordem de escolaridade
escolaridade_ordem = {
    "Ensino Médio Incompleto": 1,
    "Ensino Médio Completo": 2,
    "Ensino Superior Incompleto": 3,
    "Ensino Superior Completo": 4
}

# Função para validar a escolaridade
def validar_escolaridade(escolaridade_candidato, escolaridade_vaga):
    return escolaridade_ordem[escolaridade_candidato] >= escolaridade_ordem[escolaridade_vaga]
# Função para armazenar o estado do formulário
def submit_form():
    st.session_state['cadastro'] = {
        'nome': st.session_state['nome'],
        'cpf': st.session_state['cpf'],
        'telefone': st.session_state['telefone'],
        'sexo': st.session_state['sexo'],
        'idade': st.session_state['idade'],
        'endereco': st.session_state['endereco'],
        'email': st.session_state['email'],
        'escolaridade': st.session_state['escolaridade'],
        'periodo': st.session_state['periodo'],
        'experiencia': st.session_state['experiencia'],
        'habilidade': st.session_state['habilidade']
    }
    st.session_state['form_submitted'] = True
def submit_form2():
    st.session_state['atualizar'] = {
        'novonome': st.session_state['novonome'],
        'novocpf': st.session_state['novocpf'],
        'novotelefone': st.session_state['novotelefone'],
        'novosexo': st.session_state['novosexo'],
        'novaidade': st.session_state['novaidade'],
        'novoendereco': st.session_state['novoendereco'],
        'novoemail': st.session_state['novoemail'],
        'novaescolaridade': st.session_state['novaescolaridade'],
        'novoperiodo': st.session_state['novoperiodo'],
        'novaexperiencia': st.session_state['novaexperiencia'],
        'novahabilidade': st.session_state['novahabilidade']
    }
    st.session_state['form_submitted'] = True

# Ação quando o botão de cadastro for clicado
if st.session_state.get('pagina') == 'cadastrar':
    st.markdown("### Formulário de Cadastro")
    # Campos do formulário
    # Conectar ao banco de dados e listar vagas
    conexao = bd.conectar()
    vagas = bd.listar_vagas(conexao)
    vaga_opcoes = [vaga[0] for vaga in vagas]
    vaga_selecionada = st.selectbox("Selecione uma vaga:", vaga_opcoes, key="vaga")
    nome = st.text_input("Digite seu nome completo: ", key="nome")
    cpf = st.text_input("Digite seu CPF: ", key="cpf")
    telefone = st.text_input("Digite seu telefone com DDD: ", key="telefone")
    sexo = st.selectbox("Selecione seu sexo:" ,["","Masculino","Feminino"], key="sexo")
    idade = st.text_input("Digite sua idade:", key="idade")
    endereco = st.text_input("Digite seu endereço:", key="endereco")
    email = st.text_input("Digite seu email:", key="email")
    escolaridade = st.selectbox("Selecione seu grau de escolaridade:",["","Ensino Médio Incompleto","Ensino Médio Completo","Ensino Superior Incompleto","Ensino Superior Completo"], key="escolaridade")
    periodo = st.selectbox("Selecione o período desejado:" ,["","Meio período","Integral"], key="periodo")
    experiencia = st.selectbox("Tem experiência na área:" ,["","Sim","Não"], key="experiencia")
    habilidade = st.text_area("Descreva suas habilidades:", key="habilidade")

    # Botão de confirmação do cadastro
    submit_button = st.button("Confirmar Cadastro")

    # Quando o botão de cadastro for clicado
    if submit_button:
        # Verificando se todos os campos foram preenchidos
        if not nome or not cpf or not endereco or not sexo or not idade or not endereco or not email or not escolaridade or not periodo or not experiencia or not habilidade:
            st.warning("Por favor, preencha todos os campos obrigatórios!")
        else:
            if all(i.isalpha() or i.isspace() for i in nome):
                if validar_cpf (cpf):
                    if int(idade)>14 and int(idade)<80:
                        if validar_email(email):
                            submit_form()
                            st.success("Cadastro realizado com sucesso!")
                            st.write("Nome:", nome)
                            st.write("CPF:", cpf)
                            st.write("Telefone:", telefone)
                            st.write("Sexo:", sexo)
                            st.write("Idade:", idade)
                            st.write("Endereço:", endereco)
                            st.write("Email:", email)
                            st.write("Escolaridade:", escolaridade)
                            st.write("Periodo:", periodo)
                            st.write("Experiencia:", experiencia)
                            st.write("Escolaridade:", habilidade)

                            texto_predefinido = bd.listar_habilidade(conexao, vaga_selecionada).lower()
                            informacao_usuario = habilidade.lower()
                            validar = verificar_informacao(texto_predefinido, informacao_usuario)
                            if validar == True:
                                if bd.listar_experiencia(conexao,vaga_selecionada)== experiencia:
                                    idade_minima = bd.listar_idade(conexao, vaga_selecionada)
                                    if int(idade) >= idade_minima:
                                        if validar_escolaridade(escolaridade, bd.listar_escolaridade(conexao, vaga_selecionada)):
                                            destinatario = email
                                            assunto = "Você foi selecionado para a próxima fase"
                                            corpo = "Parabéns, Obrigado por conficar na curriculumHub, você foi selecionado para a próxima fase do processo seletivo, e estamos muito felizes em contar com você na próxima etapa. Em breve entraremos em contato para maiores informações. Até mais!"
                                            enviar_email(destinatario, assunto, corpo)
                                            conexao=bd.conectar()
                                            bd.inserir_candidato(conexao,vaga_selecionada,nome,cpf,telefone,sexo,idade,endereco,email,escolaridade,periodo,experiencia,habilidade)
                                        else:
                                            destinatario = email
                                            assunto = "Você não foi selecionado para a próxima fase"
                                            corpo = "Você não tem a escolaridade necessária de acordo com o que é solicitado pela vaga. Procure se adequar a escolaridade da vaga, terminando a sua graduação e, caso você não tenha começado ainda, procure uma faculdade Senac, mais perto de você e conheça as nossas graduações. Diga que veio pela curriculumHub e tenha descontos especiais na matrícula e na mensalidade. Conte com a curriculumHub para o seu sucesso no mercado de trabalho!"
                                            enviar_email(destinatario, assunto, corpo)
                                    else:
                                        destinatario = email
                                        assunto = "Você não foi selecionado para a próxima fase"
                                        corpo = "Você não tem a idade necessária de acordo com a solicitada pela vaga. Esperamos que aguarde a idade necessária ou então, procure uma outra vaga que se encaixe no seu perfil. Conte com a curriculumHub para o seu sucesso no mercado de trabalho!"
                                        enviar_email(destinatario, assunto, corpo)
                                else:
                                    destinatario = email
                                    assunto = "Você não foi selecionado para a próxima fase"
                                    corpo = "Você não tem a experiência necessária de acordo com a solicitada pela vaga. Solicitamos que você não desista e procure por uma vaga que se encaixe no seu perfil. Conte com a curriculumHub para o seu sucesso no mercado de trabalho!"
                                    enviar_email(destinatario, assunto, corpo)
                            else:
                                palavras_faltantes= verificar_informacao(texto_predefinido, informacao_usuario)
                                palavras_faltantes_str = ', '.join(palavras_faltantes)
                                destinatario = email
                                assunto = "Você não foi selecionado para a próxima fase"
                                corpo = "Você não tem as habilidades necessárias para ir para a próxima fase da vaga. recomendo você procurar cursos na área com os seguintes temas: "+palavras_faltantes_str+". Procure um Senac mais próximo de você e veja se esse curso está disponível, diga que veio pela curriculumHub e tenha descontos especiais na matrícula e na mensalidade. Conte com a curriculumHub para o seu sucesso no mercado de trabalho!"
                                enviar_email(destinatario, assunto, corpo)
                            
                        else:
                            st.error("Email inválido")
                    else:
                        st.error("Idade inválida")
                else:
                    st.error("CPF Inválido.")
            else:
                st.error("Nome inválido")
# Ação quando o botão de cadastro for clicado
elif st.session_state.get('pagina') == 'atualizar':
    st.markdown("### Atualização de Cadastro")
    
    # Campos do formulário
    cpfantigo = st.text_input("Digite o cpf do usuário que você deseja atualizar: ", key="cpfantigo")
    conexao = bd.conectar()
    vagas = bd.listar_vagas(conexao)
    vaga_opcoes = [vaga[0] for vaga in vagas]
    novavaga_selecionada = st.selectbox("Selecione uma vaga:", vaga_opcoes, key="vaga")
    novonome = st.text_input("Digite seu nome completo: ", key="novonome")
    novocpf = st.text_input("Digite seu CPF: ", key="novocpf")
    novotelefone = st.text_input("Digite seu telefone: ", key="novotelefone")
    novosexo = st.selectbox("Selecione seu sexo:" ,["","Masculino","Feminino"], key="novosexo")
    novaidade = st.text_input("Digite sua idade:", key="novaidade")
    novoendereco = st.text_input("Digite seu endereço:", key="novoendereco")
    novoemail = st.text_input("Digite seu email:", key="novoemail")
    novaescolaridade = st.selectbox("Selecione seu grau de escolaridade:",["","Ensino Médio Incompleto","Ensino Médio Completo","Ensino Superior Incompleto","Ensino Superior Completo"], key="novaescolaridade")
    novoperiodo = st.selectbox("Selecione o período desejado:" ,["","Meio período","Integral"], key="novoperiodo")
    novaexperiencia = st.selectbox("Tem experiência na área:" ,["","Sim","Não"], key="novaexperiencia")
    novahabilidade = st.text_area("Descreva suas habilidades:", key="novahabilidade")

    # Botão de confirmação do cadastro
    submit_button2 = st.button("Atualizar Cadastro")

    # Quando o botão de cadastro for clicado
    if submit_button2:
        # Verificando se todos os campos foram preenchidos
        if not novonome or not novocpf or not novotelefone or not novosexo or not novaidade or not novoendereco or not novoemail or not novaescolaridade or not novoperiodo or not novaexperiencia or not novahabilidade:
            st.warning("Por favor, preencha todos os campos obrigatórios!")
        else:
            if all(i.isalpha() or i.isspace() for i in novonome):
                if validar_cpf (novocpf):
                    if int(novaidade)>14 and int(novaidade)<80:
                        if validar_email(novoemail):
                            submit_form2()
                            st.success("Cadastro atualizado com sucesso!")
                            st.write("Nome:", novonome)
                            st.write("CPF:", novocpf)
                            st.write("Telefone:", novotelefone)
                            st.write("Sexo:", novosexo)
                            st.write("Idade:", novaidade)
                            st.write("Endereço:", novoendereco)
                            st.write("Email:", novoemail)
                            st.write("Escolaridade:", novaescolaridade)
                            st.write("Periodo:", novoperiodo)
                            st.write("Experiencia:", novaexperiencia)
                            st.write("Escolaridade:", novahabilidade)
                            conexao=bd.conectar()
                            bd.atualizar_candidato(conexao,cpfantigo,novavaga_selecionada,novonome,novocpf,novotelefone,novosexo,novaidade,novoendereco,novoemail,novaescolaridade,novoperiodo,novaexperiencia,novahabilidade)
            else:
                st.write("nome inválido")

# BOTÃO DELETAR CURRICULO                
elif st.session_state.get('pagina') == 'deletar':
    st.markdown("### Deletar Cadastro")
    cpfdeletar = st.text_input("Digite o cpf do usuário que você deseja deletar: ", key="cpfdeletar")
    submit_button3 = st.button("Deletar cadastro")
    if submit_button3:
        if not cpfdeletar:
            st.warning("Por favor, preencha o campo obrigatório!")
        else:
            conexao=bd.conectar()
            bd.apagar_candidato(conexao,cpfdeletar)
            st.success("Cadastro deletado com sucesso!")

# BOTÃO CADASTRAR VAGA
elif st.session_state.get('pagina') == 'cadastrar_vaga':
    st.markdown("### Cadastro de Vaga")
    nome_da_vaga = st.text_input("Digite o nome da vaga: ", key="nome_da_vaga")
    habilidade = st.text_input("Digite a habilidade necessária: ", key="habilidade")
    escolaridade = st.selectbox("Selecione a escolaridade necessária:",["","Ensino Médio Incompleto","Ensino Médio Completo","Ensino Superior Incompleto","Ensino Superior Completo"], key="escolaridade")
    idade = st.text_input("Digite a idade necessária:", key="idade")
    experiencia = st.selectbox("Requer experiência na área:" ,["","Sim","Não"], key="experiencia")
    periodo = st.selectbox("Selecione o período desejado:" ,["","Meio período","Integral"], key="periodo")
    descricao = st.text_area("Descreva a vaga:", key="descricao")
    submit_button4 = st.button("Cadastrar vaga")
    if submit_button4:
        if not habilidade or not escolaridade or not idade or not experiencia or not periodo or not descricao:
            st.warning("Por favor, preencha todos os campos obrigatórios!")
        else:
            conexao=bd.conectar()
            bd.inserir_vagas(conexao,nome_da_vaga, habilidade, escolaridade, idade, experiencia, periodo,descricao)
            st.success("Vaga cadastrada com sucesso!")
elif st.session_state.get('pagina') == 'listar_vaga':
    st.markdown("### Lista de Vagas")
    conexao = bd.conectar()
    vagas = bd.listar_vagas(conexao)
    if vagas:
        for vaga in vagas:
            st.write(f"Nome da Vaga: {vaga[0]}")
            st.write(f"Habilidade: {vaga[1]}")
            st.write(f"Escolaridade: {vaga[2]}")
            st.write(f"Idade: {vaga[3]}")
            st.write(f"Experiência: {vaga[4]}")
            st.write(f"Período: {vaga[5]}")
            st.write(f"Descrição: {vaga[6]}")
            st.write("---")
    else:
        st.write("Nenhuma vaga encontrada.")

            

    

    
