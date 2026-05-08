from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/excluir', methods=['POST'])
def excluir():
    dados=request.get_jason()
    paciente_id = dados.get('id')
    print(f'paciente{paciente_id} recebido para exclusão')
    return jsonify({
        'mensagem':'exclusão processada'
    })
if __name__ == 'main':
    app.run(port=5000)