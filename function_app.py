import azure.functions as func
import json
import logging
from cpf_validator import validate_cpf

app = func.FunctionApp()

@app.route(route="validate-cpf", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET", "POST"])
def validate_cpf_function(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function to validate Brazilian CPF numbers.
    
    Accepts:
    - GET request with 'cpf' query parameter
    - POST request with JSON body containing 'cpf' field
    
    Returns:
    JSON response with validation result
    """
    logging.info('CPF validation function triggered.')

    try:
        # Try to get CPF from query parameter (GET) or request body (POST)
        cpf = None
        
        if req.method == "GET":
            cpf = req.params.get('cpf')
        elif req.method == "POST":
            try:
                req_body = req.get_json()
                if req_body:
                    cpf = req_body.get('cpf')
            except ValueError:
                pass
        
        if not cpf:
            return func.HttpResponse(
                json.dumps({
                    "error": "CPF not provided. Use 'cpf' query parameter for GET or JSON body for POST.",
                    "valid": False
                }),
                status_code=400,
                mimetype="application/json"
            )
        
        # Validate the CPF
        is_valid = validate_cpf(cpf)
        
        # Prepare response
        response_data = {
            "cpf": cpf,
            "valid": is_valid,
            "message": "CPF is valid" if is_valid else "CPF is invalid"
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error processing CPF validation: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": "Internal server error",
                "valid": False
            }),
            status_code=500,
            mimetype="application/json"
        )