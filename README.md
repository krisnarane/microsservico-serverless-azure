# Microsserviço Serverless para Validação de CPF - Azure Functions

Este projeto implementa um microsserviço serverless na Azure Functions para validar CPFs brasileiros. Ele recebe um CPF via requisição HTTP e retorna um JSON indicando se o CPF é válido ou não.

## Funcionalidades

- ✅ **Validação de formato do CPF**: Verifica se o CPF possui 11 dígitos e não é uma sequência repetitiva
- ✅ **Verificação do dígito verificador**: Implementa o algoritmo oficial de validação do CPF brasileiro
- ✅ **Resposta em formato JSON**: Retorna resultado estruturado com status de validação
- ✅ **Suporte a múltiplos formatos**: Aceita CPF com ou sem formatação (pontos e hífen)
- ✅ **Múltiplos métodos HTTP**: Suporte a requisições GET e POST

## Tecnologias Utilizadas

- **Azure Functions Python 3.x**: Plataforma serverless da Microsoft Azure
- **Azure CLI**: Ferramenta de linha de comando para deploy
- **Azure Functions Core Tools**: Desenvolvimento e teste local

## Estrutura do Projeto

```
microsservico-serverless-azure/
├── function_app.py          # Função principal do Azure Functions
├── cpf_validator.py         # Lógica de validação do CPF
├── host.json               # Configuração do runtime do Azure Functions
├── local.settings.json     # Configurações locais de desenvolvimento
├── requirements.txt        # Dependências Python
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Documentação do projeto
```

## API Endpoints

### POST /api/validate-cpf

Valida um CPF enviado no corpo da requisição.

**Request Body:**
```json
{
  "cpf": "123.456.789-09"
}
```

**Response (CPF Válido):**
```json
{
  "cpf": "123.456.789-09",
  "valid": true,
  "message": "CPF is valid"
}
```

**Response (CPF Inválido):**
```json
{
  "cpf": "111.111.111-11",
  "valid": false,
  "message": "CPF is invalid"
}
```

### GET /api/validate-cpf?cpf=12345678909

Valida um CPF enviado como parâmetro de query.

**Response (CPF Válido):**
```json
{
  "cpf": "12345678909",
  "valid": true,
  "message": "CPF is valid"
}
```

## Algoritmo de Validação

O algoritmo implementa as regras oficiais de validação do CPF brasileiro:

1. **Formato**: Deve ter exatamente 11 dígitos
2. **Sequência repetitiva**: Não pode ser uma sequência de dígitos iguais (ex: 111.111.111-11)
3. **Dígitos verificadores**: Os dois últimos dígitos devem ser calculados corretamente

### Cálculo dos Dígitos Verificadores

**Primeiro dígito verificador:**
- Multiplica cada um dos 9 primeiros dígitos por pesos de 10 a 2
- Soma os resultados
- Calcula o resto da divisão por 11
- Se resto < 2, dígito = 0; senão, dígito = 11 - resto

**Segundo dígito verificador:**
- Multiplica cada um dos 10 primeiros dígitos por pesos de 11 a 2
- Soma os resultados
- Calcula o resto da divisão por 11
- Se resto < 2, dígito = 0; senão, dígito = 11 - resto

## Desenvolvimento Local

### Pré-requisitos

- Python 3.8 ou superior
- Azure Functions Core Tools
- Azure CLI (para deploy)

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

### Executar Localmente

```bash
func start
```

A função estará disponível em: `http://localhost:7071/api/validate-cpf`

### Testando a API

**Teste com GET:**
```bash
curl "http://localhost:7071/api/validate-cpf?cpf=123.456.789-09"
```

**Teste com POST:**
```bash
curl -X POST "http://localhost:7071/api/validate-cpf" \
  -H "Content-Type: application/json" \
  -d '{"cpf": "123.456.789-09"}'
```

## Deploy na Azure

### 1. Login na Azure
```bash
az login
```

### 2. Criar Resource Group
```bash
az group create --name rg-cpf-validator --location brazilsouth
```

### 3. Criar Storage Account
```bash
az storage account create \
  --name stcpfvalidator \
  --resource-group rg-cpf-validator \
  --location brazilsouth \
  --sku Standard_LRS
```

### 4. Criar Function App
```bash
az functionapp create \
  --resource-group rg-cpf-validator \
  --consumption-plan-location brazilsouth \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --name func-cpf-validator \
  --storage-account stcpfvalidator
```

### 5. Deploy da Função
```bash
func azure functionapp publish func-cpf-validator
```

## Exemplos de Uso

### CPFs Válidos para Teste
- `123.456.789-09` ou `12345678909`
- `111.444.777-35` ou `11144477735`
- `529.982.247-25` ou `52998224725`

### CPFs Inválidos para Teste
- `111.111.111-11` (sequência repetitiva)
- `123.456.789-00` (dígitos verificadores incorretos)
- `12345678` (formato incorreto)

## Tratamento de Erros

A API retorna os seguintes códigos de status:

- **200 OK**: CPF processado com sucesso (válido ou inválido)
- **400 Bad Request**: CPF não fornecido na requisição
- **500 Internal Server Error**: Erro interno do servidor

## Monitoramento

O Azure Functions fornece métricas automáticas:
- Número de execuções
- Duração das execuções
- Erros e exceções
- Uso de recursos

Acesse o portal do Azure para visualizar as métricas em tempo real.
