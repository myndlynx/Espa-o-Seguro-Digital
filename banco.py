from datetime import datetime, timedelta

consultas_db = []


def proximo_id():
    """Gera o próximo ID de consulta com base no maior ID já existente.
    Usado tanto por aluno.py quanto por psicologo.py, para nunca gerar
    o mesmo ID duas vezes."""
    if not consultas_db:
        return 1
    return max(c['id'] for c in consultas_db) + 1


lista_campi = [
    {'nome': 'Areia'}, {'nome': 'Cabedelo'}, {'nome': 'Cajazeiras'},
    {'nome': 'Campina Grande'}, {'nome': 'Catolé do Rocha'}, {'nome': 'Esperança'},
    {'nome': 'Guarabira'}, {'nome': 'Itabaiana'}, {'nome': 'Itaporanga'},
    {'nome': 'João Pessoa'}, {'nome': 'Mangabeira (João Pessoa)'}, {'nome': 'Monteiro'},
    {'nome': 'Patos'}, {'nome': 'Pedras de Fogo'}, {'nome': 'Picuí'},
    {'nome': 'Princesa Isabel'}, {'nome': 'Santa Rita'}
]

usuarios = [
    {"matricula": "202414610001", "senha": "12345a", "nome": "João Aluno", "tipo": "aluno"},
    {"matricula": "202414610003", "senha": "12345b", "nome": "Maria Aluna", "tipo": "aluno"},
    {"matricula": "202414610002", "senha": "12345p", "nome": "Dra. Ana Costa", "tipo": "psicologo", "campus": "Santa Rita"},
    {"matricula": "202414610004", "senha": "12345p", "nome": "Dr. Carlos Silva", "tipo": "psicologo", "campus": "João Pessoa"}
]

def atualizar_consultas_concluidas():
    """Marca como 'Concluída' toda consulta 'Agendado' cujo horário já passou.
    Chamada tanto pelo módulo do aluno quanto pelo do psicólogo."""
    agora = datetime.utcnow() - timedelta(hours=3)
    for c in consultas_db:
        if c.get('status') == 'Agendado':
            try:
                data_hora_consulta = datetime.strptime(
                    f"{c['data']} {c['horario']}",
                    "%d/%m/%Y %H:%M"
                )
                if data_hora_consulta <= agora:
                    c['status'] = 'Concluída'
            except ValueError:
                pass