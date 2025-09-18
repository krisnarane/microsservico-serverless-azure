import azure.functions as func
import json
import re

def is_valid_cpf(cpf: str) -> bool:
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        sum = 0
        for j in range(0, i):
            sum += int(cpf[j]) * ((i + 1) - j)
        digit = ((sum * 10) % 11) % 10
        if int(cpf[i]) != digit:
            return False
    return True

def main(req: func.HttpRequest) -> func.HttpResponse:
    cpf = req.params.get('cpf')
    if not cpf:
        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                json.dumps({'error': 'CPF não informado'}),
                status_code=400,
                mimetype='application/json'
            )
        cpf = req_body.get('cpf')
    if not cpf:
        return func.HttpResponse(
            json.dumps({'error': 'CPF não informado'}),
            status_code=400,
            mimetype='application/json'
        )
    valido = is_valid_cpf(cpf)
    return func.HttpResponse(
        json.dumps({'cpf': cpf, 'valido': valido}),
        status_code=200,
        mimetype='application/json'
    )
