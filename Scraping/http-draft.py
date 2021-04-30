import requests
import json
# import os

# TODO 
# Remover # da url da foto
# Baixar foto
# Construir base de dados das fotos
# Como adicionar aleatoriedade
# Fazer backups caso de perda ce conexao e continuar de onde parou. Como?
# Como saber o numero de paginas?


# Open base request string
with open('get_request.txt', 'r') as file:
    request_str = file.read()

# Format string to specify species and page
request_str_ij = request_str.format(code = '10001', page = '15')
res_ij = requests.get(request_str_ij,  verify=False)


def process_request(request):
    json_data = json.loads(request.text)
    # Pretty JSON
    json_formatted_str = json.dumps(json_data, indent=2)
    print(json_formatted_str)

process_request(res_ij)

