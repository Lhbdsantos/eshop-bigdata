import streamlit as st
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["eshop"]
colecao = db["clientes"]

st.title("E-Shop Brasil - Sistema de Clientes")

st.subheader("Adicionar Cliente")

nome = st.text_input("Nome")
sobrenome = st.text_input("Sobrenome")

if st.button("Adicionar"):
    if nome and sobrenome:
        nome_completo = nome + " " + sobrenome  # CONCATENAÇÃO

        colecao.insert_one({
            "nome": nome,
            "sobrenome": sobrenome,
            "nome_completo": nome_completo
        })

        st.success("Cliente adicionado!")
    else:
        st.warning("Preencha todos os campos")

st.subheader("Clientes cadastrados")

clientes = list(colecao.find())

for c in clientes:
    nome = c.get("nome", "")
    sobrenome = c.get("sobrenome", "")
    st.write(f"{nome} {sobrenome}")

st.subheader("Editar Cliente")

nome_antigo = st.text_input("Nome completo atual")
novo_nome = st.text_input("Novo nome")
novo_sobrenome = st.text_input("Novo sobrenome")

if st.button("Atualizar"):
    if nome_antigo and novo_nome and novo_sobrenome:
        novo_nome_completo = novo_nome + " " + novo_sobrenome  # CONCATENAÇÃO

        resultado = colecao.update_one(
            {"nome_completo": nome_antigo},
            {"$set": {
                "nome": novo_nome,
                "sobrenome": novo_sobrenome,
                "nome_completo": novo_nome_completo
            }}
        )

        if resultado.modified_count > 0:
            st.success("Cliente atualizado!")
        else:
            st.warning("Cliente não encontrado")

st.subheader("Remover Cliente")

nome_delete = st.text_input("Nome completo para remover")

if st.button("Remover"):
    resultado = colecao.delete_one({"nome_completo": nome_delete})

    if resultado.deleted_count > 0:
        st.success("Removido!")
    else:
        st.warning("Cliente não encontrado")