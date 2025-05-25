import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
import random
import pandas as pd
from faker import Faker
from datetime import datetime

client = MongoClient("mongodb://mongo:27017/")
db = client["eshop"]
collection = db["clients"]
collection2 = db["products"]
collection3 = db["orders"]

fake = Faker()

def generate_fake_clients(num_records):
    return [{
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
        "phone_number": fake.phone_number(),
    } for _ in range(num_records)]

def generate_fake_products(num_records):
    base_names = [f"Produto {chr(65 + i % 26)}{i//26 if i >= 26 else ''}" for i in range(num_records)]
    return [{
        "name": base_names[i],
        "price": round(random.uniform(10.0, 1000.0), 2),
        "stock": random.randint(0, 1000)
    } for i in range(num_records)]

def generate_fake_orders(num_records):
    clients = list(collection.find())
    products = list(collection2.find())
    if not clients or not products:
        return []
    return [{
        "client_id": random.choice(clients)["_id"],
        "product_id": random.choice(products)["_id"],
        "quantity": random.randint(1, 5),
        "purchase_date": fake.date_time_this_year()
    } for _ in range(num_records)]

st.set_page_config(page_title="E-Shop Big Data App", layout="wide")
st.title("E-Shop Brasil - Gestão de Dados")

st.sidebar.title("🔧 Seções")
section = st.sidebar.radio("Escolha uma seção:", [
    "Clientes", "Produtos", "Pedidos", "Análise de Dados"])

if section == "Clientes":
    st.header("Clientes")
    num = st.number_input("Nº de clientes falsos:", 1, 1000, 5)
    if st.button("Gerar Clientes"):
        data = generate_fake_clients(num)
        collection.insert_many(data)
        st.success(f"{num} clientes inseridos.")

    if st.button("Visualizar Clientes"):
        clients = list(collection.find())
        for c in clients:
            c["_id"] = str(c["_id"])
        st.dataframe(pd.DataFrame(clients))

    client_id = st.text_input("ID do Cliente para excluir:")
    if st.button("Excluir Cliente"):
        try:
            collection.delete_one({"_id": ObjectId(client_id)})
            st.success("Cliente excluído com sucesso!")
        except:
            st.error("ID inválido.")

elif section == "Produtos":
    st.header("Produtos")
    num = st.number_input("Nº de produtos falsos:", 1, 1000, 5)
    if st.button("Gerar Produtos"):
        data = generate_fake_products(num)
        collection2.insert_many(data)
        st.success(f"{num} produtos inseridos.")

    if st.button("Visualizar Produtos"):
        products = list(collection2.find())
        for p in products:
            p["_id"] = str(p["_id"])
        st.dataframe(pd.DataFrame(products))

    product_id = st.text_input("ID do Produto para excluir:")
    if st.button("Excluir Produto"):
        try:
            collection2.delete_one({"_id": ObjectId(product_id)})
            st.success("Produto excluído com sucesso!")
        except:
            st.error("ID inválido.")

elif section == "Pedidos":
    st.header("Pedidos")
    num = st.number_input("Nº de pedidos falsos:", 1, 1000, 5)
    if st.button("Gerar Pedidos"):
        data = generate_fake_orders(num)
        if data:
            collection3.insert_many(data)
            st.success(f"{num} pedidos inseridos.")
        else:
            st.error("Clientes ou produtos insuficientes.")

    if st.button("Visualizar Pedidos"):
        pedidos = list(collection3.find())
        for p in pedidos:
            p["_id"] = str(p["_id"])
            p["client_id"] = str(p["client_id"])
            p["product_id"] = str(p["product_id"])
        st.dataframe(pd.DataFrame(pedidos))

    pedido_id = st.text_input("ID do Pedido para excluir:")
    if st.button("Excluir Pedido"):
        try:
            collection3.delete_one({"_id": ObjectId(pedido_id)})
            st.success("Pedido excluído com sucesso!")
        except:
            st.error("ID inválido.")

elif section == "Análise de Dados":
    st.header("📊 Análise de Dados da E-Shop Brasil")
    st.write("Esta seção mostra métricas e gráficos gerados a partir dos pedidos cadastrados.")

    pedidos = list(collection3.find())
    produtos = {str(p["_id"]): p for p in collection2.find()}

    # Faturamento e total de pedidos
    faturamento_total = 0
    dados_vendas = []
    vendas_produtos = {}

    for p in pedidos:
        produto = produtos.get(str(p["product_id"]))
        if produto:
            valor = produto["price"] * p["quantity"]
            faturamento_total += valor
            data = p["purchase_date"]
            if isinstance(data, str):
                data = pd.to_datetime(data)
            dados_vendas.append({
                "data": data.date(),
                "valor": valor
            })

            nome_produto = produto["name"]
            vendas_produtos[nome_produto] = vendas_produtos.get(nome_produto, 0) + p["quantity"]

    # Métricas Resumo
    col1, col2 = st.columns(2)
    col1.metric("Total de Pedidos", len(pedidos))
    col2.metric("Faturamento Estimado", f"R$ {faturamento_total:,.2f}")

    # Gráfico de vendas por data
    st.subheader("📈 Vendas por Data")
    if dados_vendas:
        df_vendas = pd.DataFrame(dados_vendas)
        df_vendas_grouped = df_vendas.groupby("data").sum().reset_index()
        df_vendas_grouped = df_vendas_grouped.sort_values("data")
        st.line_chart(df_vendas_grouped.set_index("data")["valor"])
    else:
        st.info("Nenhum pedido registrado para gerar o gráfico.")

    # Gráfico de produtos mais vendidos
    st.subheader("🏆 Produtos Mais Vendidos")
    if vendas_produtos:
        df_produtos = pd.DataFrame(list(vendas_produtos.items()), columns=["Produto", "Quantidade Vendida"])
        df_produtos = df_produtos.sort_values(by="Quantidade Vendida", ascending=False)
        st.bar_chart(df_produtos.set_index("Produto"))
    else:
        st.info("Nenhuma venda registrada para análise de produtos.")

        
    




