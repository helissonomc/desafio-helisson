# Desafio-Helisson Finnex

## Tecnologias utilizadas

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* Testes Automatizados
* [Docker](https://www.docker.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Postman](https://www.postman.com/)

## Executar Aplicação

```
sudo docker-compose up --build
```

O docker fará o build de uma imagem configurada no docker-compose, instalando as dependências necessárias, em seguida, o servidor local fica acessível em: http://localhost:8000 ou http://127.0.0.1:8000/. Além do container rodando o servidor Django, o docker-compose também cria um container para o PostgreSQL.

O repositorio possui o arquivo .env-sample, este arquivo é apenas um exemplo de como um arquivo .env tem que ser configurado no ambiente, para não deixar nenhum dado sensível a mostra para quem tem acesso ao repositório

## Detalhes da solução

### Autenticação
Foi usado o [Simple JWT]((https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)) para a geração e verificação de token, foi escolhido esta tecnologia, pois ela trás uma segurança maior para a API devido a validade dos tokens de accesso e refresh gerado. O token de acesso foi configurado para durar apenas 5 miutos e o de refresh 1 dia.

### Separação de papeis
Para separar os papéis entre **Administrador** e **Anunciante** foi utilizado o Group do Django. Quando um usuario é criado usando a API, já é registrado como **Anunciante**, já quando é criado um Super User usando o **manage.py**, o usuário já é associado ao grupo **Administrador**

### Model de Demanda
Dentro do model de demanda foi acrescentado o campo chamdo nome_peca, pois acredito que fica melhor de visualizar no admin do Django.

### Rotas
Foram implementados 3 Apps: 
 - User: Responsável pela criação e autenticação de usuários
    - Rota para o criar user: (POST) /api/user/create/
    - Rota para obter token de autenitcação: (POST) /api/user/token/
 - Demanda: Responsável pelo o CRUD de demanda:
    - Rota para criar Demanda: (POST) /api/demanda/
    - Rota para listar Demandas: (GET) /api/udemanda/
    - Rota para atualizar Demanda: (PATCH) /api/demanda/id_demanda/
    - Rota para deletar Demanda: (DELETE) /api/demanda/id_demanda/
    - Rota par finalizar Demanda: (PATCH) /api/demanda/finalizar/id_demanda/
- Core: Responsavel pelo o esqueleto do projeto, onde são encontrados, migrations. management, admin, models

Vale lembrar que estas rotas de demandas estão disponiveis apenas para usuário **Anunciante**.

## Testes
Foram implementados testes automatizados onde o resultado podemos vê na imagem abaixo:
![image](https://user-images.githubusercontent.com/60279210/145326170-f09eb9cb-eccc-4b85-b259-f235b169c7ac.png)

O Postman também foi usado para testar de forma manual a API. Podemos vê a collection que foi criada no arquivo **Desafio Hélisson.postman_collection.json** e o resultado do run desta collection no arquivo **Desafio Hélisson.postman_test_run.json**.
