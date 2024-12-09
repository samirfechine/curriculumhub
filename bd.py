import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import *
from tkinter import messagebox
class bd():
    def conectar():
        try:
            
            conexao = mysql.connector.connect(
                host ='10.18.0.108',
                database = 'curriculo2',
                user = 'samir',
                password ='samir'
            )
            if conexao.is_connected():
                print("Conexão bem sucedida ao MySQL")
                return conexao
            else:
                print("Falha na conexão ao MySQL")
                return None
        except Error as e:
            print ("Erro ao conectar ao MySQL", e)
            return None
    
    def listar_dados(conexao):
        try:
            cursor = conexao.cursor()
            cursor.execute("select * from vagas;")
            resultados = cursor.fetchall()
            print("Dados da tabela")
            for i in resultados:
                print(i)
            cursor.close()
        except mysql.connector.Error as erro:
            print("Erro ao listar os dados", erro)
    def listar_experiencia(conexao):
        try:
            cursor = conexao.cursor()
            cursor.execute("select experiencia from vagas;")
            resultados = cursor.fetchall()
            print("Dados da tabela")
            for i in resultados:
                print(i)
            cursor.close()
        except mysql.connector.Error as erro:
            print("Erro ao listar os dados", erro)
    def listar_escolaridade(conexao):
        try:
            cursor = conexao.cursor()
            cursor.execute("select escolaridade from vagas;")
            resultados = cursor.fetchall()
            print("Dados da tabela")
            for i in resultados:
                print(i)
            cursor.close()
        except mysql.connector.Error as erro:
            print("Erro ao listar os dados", erro)
    def listar_habilidade(conexao, vaga_selecionada):
        cursor = conexao.cursor()
        cursor.execute("select habilidade from vagas where nome_da_vaga = '"+vaga_selecionada+"';")
        resultados = cursor.fetchall()
        habilidades = [resultado[0] for resultado in resultados]
        cursor.close()
        return ' '.join(habilidades)
    def listar_vagas(conexao):
        cursor = conexao.cursor()
        cursor.execute("select nome_da_vaga from vagas;")
        vagas = cursor.fetchall()
        return vagas
    def listar_hab_candidato(conexao,cpf):
            cursor = conexao.cursor()
            cursor.execute("select habilidade from candidato where cpf='"+cpf+"';")
            resultados = cursor.fetchall()
            habilidades = [resultado[0] for resultado in resultados]
            cursor.close()
            return ' '.join(habilidades)
    def listar_email(conexao,cpf):
        cursor = conexao.cursor()
        cursor.execute("select email from candidato where cpf='"+cpf+"';")
        resultados = cursor.fetchall()
        email = [resultado[0] for resultado in resultados]
        cursor.close()
        return ' '.join(email)
    def listar_experiencia(conexao, nome_da_vaga):
        cursor = conexao.cursor()
        cursor.execute("select experiencia from vagas where nome_da_vaga='"+nome_da_vaga+"';")
        resultados = cursor.fetchall()
        experiencia= [resultado[0] for resultado in resultados]
        cursor.close()
        return ' '.join(experiencia)
    def listar_idade(conexao, nome_da_vaga):
        cursor = conexao.cursor()
        cursor.execute("select idade from vagas where nome_da_vaga='"+nome_da_vaga+"';")
        idade = cursor.fetchone()
        return idade[0] if idade else None
    def listar_escolaridade(conexao, nome_da_vaga):
        cursor = conexao.cursor()
        cursor.execute("select escolaridade from vagas where nome_da_vaga='"+nome_da_vaga+"';")
        resultados = cursor.fetchall()
        escolaridade = [resultado[0] for resultado in resultados]
        cursor.close()
        return ' '.join(escolaridade)
    def fechar_conexao(conexao):
        if conexao.is_connected():
            conexao.close()
            print("Conexão fechada")

    def inserir_vagas(conexao,nome_da_vaga, habilidade, escolaridade, idade, experiencia, periodo,descricao):
        cursor = conexao.cursor()
        cursor.execute("insert into vagas(nome_da_vaga,habilidade, escolaridade, idade, experiencia, periodo,descricao) values('"+nome_da_vaga+"','"+habilidade+"','"+escolaridade+"', '"+idade+"','"+experiencia+"','"+periodo+"','"+descricao+"');")
        conexao.commit()
        print("vaga adicionado com sucesso")
        cursor.close()


    def inserir_candidato(conexao,nome_da_vaga,nome,cpf,telefone,sexo,idade,endereco,email,escolaridade,periodo,experiencia,habilidade):
        cursor = conexao.cursor()
        cursor.execute("insert into candidato(nome_da_vaga,nome, cpf,telefone, sexo, idade,endereco,email,escolaridade,periodo,experiencia, habilidade) values('"+nome_da_vaga+"','"+nome+"', '"+cpf+"','"+telefone+"', '"+sexo+"', '"+idade+"', '"+endereco+"', '"+email+"','"+escolaridade+"', '"+periodo+"', '"+experiencia+"', '"+habilidade+"');")
        conexao.commit()
        print("vaga adicionado com sucesso")
        cursor.close()

    def atualizar_candidato(conexao,cpfantigo,nome_da_vaga,novonome,novocpf,novotelefone,novosexo,novaidade,novoendereco,novoemail,novaescolaridade,novoperiodo,novaexperiencia,novahabilidade):
        cursor = conexao.cursor()
        cursor.execute("update candidato set nome_da_vaga='"+nome_da_vaga+"',nome='"+novonome+"', cpf='"+novocpf+"',telefone='"+novotelefone+"', sexo='"+novosexo+"', idade='"+novaidade+"', endereco='"+novoendereco+"', escolaridade='"+novaescolaridade+"', periodo='"+novoperiodo+"', experiencia='"+novaexperiencia+"', habilidade='"+novahabilidade+"' where cpf='"+cpfantigo+"'; ")
        conexao.commit()
        if cursor.rowcount>0:
            print("candidato atualizado com sucesso!")
        else:
            print("candidato não encontrado")
        cursor.close()
    def listar_vagas(conexao):
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM vagas")
        vagas = cursor.fetchall()
        return vagas
    def apagar_candidato(conexao, cpf):
        try:
            cursor= conexao.cursor()
            query= "DELETE FROM candidato WHERE cpf = '"+cpf+"'"
            cursor.execute(query)
            conexao.commit()
            if cursor.rowcount>0:
                print("Cliente deletado com sucesso!")
            else:
                print("Nenhum cliente encontrado com esse ID.")
            cursor.close()
        except mysql.connector.Error as erro:
            print(f"Erro ao deletar dados:{erro}")    
        

        #st.write("Escolaridade:", cadastro['escolaridade'])