
# Microsserviço Serverless para Validação de CPF na Azure

Bem-vindo ao projeto **microsservico-serverless-validacao-cpf-azure**! Este repositório traz um microsserviço moderno, escalável e totalmente serverless para validação de CPFs brasileiros, utilizando Azure Functions e Python.

---

## 🚀 O que este projeto faz?
Recebe um CPF via requisição HTTP e retorna um JSON informando se o CPF é válido ou não, considerando formato e dígitos verificadores.

---

## 🛠️ Tecnologias Utilizadas
- **Azure Functions**: Plataforma serverless da Microsoft para execução de funções sob demanda.
- **Python 3.x**: Linguagem principal para lógica de validação.
- **Azure CLI**: Gerenciamento e deploy na Azure.
- **Azure Functions Core Tools**: Execução e testes locais.

---

## 📦 Estrutura do Projeto

```
microsservico-serverless-validacao-cpf-azure/
├── ValidateCPF/
│   ├── function_app.py          # Lógica principal da função
│   └── __init__.py             # Indica pacote Python
├── host.json                   # Configuração global da Azure Function
├── local.settings.json         # Configurações locais (não versionar)
└── requirements.txt            # Dependências do projeto
```

---

## ✨ Como funciona?
1. O usuário faz uma requisição HTTP (GET ou POST) informando o CPF.
2. O serviço valida o formato e os dígitos verificadores do CPF.
3. Retorna um JSON:
	- `{"cpf": "12345678909", "valido": true}`

---

## 🔧 Como executar localmente

1. Instale as dependências:
	```bash
	pip install -r requirements.txt
	```
2. Instale o Azure Functions Core Tools:
	```bash
	npm install -g azure-functions-core-tools@4 --unsafe-perm true
	```
3. Inicie a função localmente:
	```bash
	func start
	```
4. Faça uma requisição HTTP:
	```bash
	curl -X GET "http://localhost:7071/api/ValidateCPF?cpf=12345678909"
	```

---

## ☁️ Deploy na Azure
1. Faça login na Azure:
	```bash
	az login
	```
2. Crie um Function App:
	```bash
	az functionapp create --resource-group <seu-grupo> --consumption-plan-location <região> --runtime python --functions-version 4 --name <nome-app> --storage-account <nome-storage>
	```
3. Faça o deploy:
	```bash
	func azure functionapp publish <nome-app>
	```

---

## 📚 Referências
- [Documentação Azure Functions](https://docs.microsoft.com/azure/azure-functions/)
- [Validação de CPF - Wikipedia](https://pt.wikipedia.org/wiki/Cadastro_de_pessoas_f%C3%ADsicas)

---

## 💡 Observações
- O arquivo `local.settings.json` **não deve ser versionado**.
- O microsserviço pode ser facilmente adaptado para outras validações.

---

## 👨‍💻 Autor
Projeto criado por Julia Krisnarane. Sinta-se livre para contribuir!
