from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
@app.route('/excluir', methods=['POST'])
def excluir():
    dados=request.get_json()
    paciente_id = dados.get('id')
    nome=dados.get('nome')
    cpf=dados.get('cpf')
    telefone=dados.get('telefone')
    email=dados.get('email')
    horario = datetime.now()

    with open('registro.txt','a', encoding='utf-8') as arquivo:
        arquivo.write(
            f''' 
            paciente excluído
            ID:{paciente_id};
            nome:{nome};
            cpf: {cpf};
            telefone: {telefone};
            email:{email};
            data:{horario}
            
            '''
        )
    print(f'paciente {paciente_id} recebido para exclusão')
    return jsonify({
        'mensagem':'exclusão processada'
    })
if __name__ == '__main__':
    app.run(port=5000)