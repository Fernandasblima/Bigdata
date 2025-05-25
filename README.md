 Introdução
  💻 Apresentação do Problema e Contexto da Aplicação
Com o crescimento do comércio eletrônico, a gestão eficiente de dados de clientes, produtos e pedidos tornou-se essencial. Este projeto propõe a construção de uma aplicação para gerenciar dados de uma loja fictícia, utilizando tecnologias modernas que facilitam o desenvolvimento, a manipulação e a análise de dados de maneira eficiente e escalável.


 💻  Objetivos do Projeto
Criar uma aplicação web interativa utilizando Streamlit.


Gerar dados sintéticos para testes de volume e performance com Faker.


Utilizar MongoDB como banco de dados NoSQL para armazenar e manipular grandes volumes de dados.


Fazer a aplicação e o banco de dados com Docker para garantir um ambiente isolado, padronizado e portátil em containers.


 Descrição do Projeto
 ✅  Uso do Docker
É utilizado para criar um ambiente de desenvolvimento isolado e replicável, evitando problemas de compatibilidade de dependências entre diferentes sistemas operacionais.
A orquestração é realizada com docker-compose, que sobe dois containers:


MongoDB: banco de dados NoSQL para armazenar os dados.


Aplicação Streamlit: interface web que interage com o banco.

✅ Configuração do Container com MongoDB
O serviço MongoDB é configurado na porta padrão 27017.


Utiliza volume persistente para manter os dados mesmo após reiniciar o container.


A aplicação Streamlit se conecta ao MongoDB utilizando o URI:
 mongodb://mongo:27017/

✅ Descrição da Aplicação (app.py)
A aplicação desenvolvida com Streamlit permite:
Conectar-se automaticamente ao container MongoDB.


Realizar as seguintes operações:


⭕Inserção: Geração e inserção de dados sintéticos para clientes, produtos e pedidos.


⭕Manipulação: Exclusão de registros pelo ID.


⭕Leitura: Consultas e exibição de dados em tabelas interativas.


📊 Além disso, a aplicação oferece gráficos interativos para análise de vendas, faturamento e volume de pedidos.

Implementaçao do docker ,mongo DB,streamlit.
Docker-compose up –build
Esse comando irá,construir a imagem da aplicação,baixar a imagem do Mongodb,iniciar os container conectados em rede.
 Funcionalidades da Aplicação
Inserção de dados > geração automática de dados,inserção em coleções do Mongodb .
Manipulação de dados > exclusão de registros por ID,visualização de dados em tabelas.
Consulta e interface gráfica > exibição de total de faturamento,gráfico de vendas ao longo do tempo.





