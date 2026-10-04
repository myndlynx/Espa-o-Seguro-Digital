from datetime import datetime, timedelta

consultas_db = []
dicas_db = [
    {'id': 1, 'titulo': 'Durma bem', "texto": (
        "Durma entre 8h e 10h por noite. Essa é a faixa indicada para adolescentes; "
        "para adultos, o recomendado costuma ser de 7h a 9h. O sono não é tempo perdido: "
        "é durante a noite que o cérebro organiza o que você aprendeu no dia, fixa a memória "
        "e se prepara para aprender de novo.\n\n"

        "Dormir pouco aparece rápido na rotina de estudos. Fica mais difícil se concentrar, "
        "esquecer o conteúdo vira rotina, o humor oscila e a ansiedade tende a aumentar, "
        "principalmente em época de provas. Muita gente troca a noite de sono por uma "
        "madrugada de estudo, mas estudar cansado rende menos e pode atrapalhar o desempenho "
        "no dia seguinte.\n\n"

        "Algumas atitudes ajudam a dormir melhor:\n"
        "• Tente dormir e acordar em horários parecidos todos os dias, inclusive nos fins de semana.\n"
        "• Evite telas, como celular, TV e computador, pelo menos 30 minutos antes de deitar.\n"
        "• Reduza café, chá preto, energéticos e refrigerantes à tarde e à noite.\n"
        "• Deixe o quarto escuro, silencioso e com temperatura agradável.\n"
        "• Evite refeições pesadas perto da hora de dormir.\n"
        "• Crie uma pequena rotina para desacelerar, como ler, ouvir música calma ou respirar fundo.\n\n"

        "Cochilos curtos de até 20 minutos durante o dia podem ajudar a recuperar a energia, "
        "mas cochilar por muito tempo perto da noite pode atrapalhar o sono.\n\n"

        "Se você dorme mal por muitos dias seguidos, acorda cansado mesmo dormindo bastante "
        "ou sente que o sono está afetando seus estudos e seu bem-estar, procure o "
        "atendimento psicológico do seu campus. Cuidar do sono também é cuidar da saúde mental."),
        'data': '04/10/2026', 'autor': 'Dr. Carlos Silva'},
    {"id": 2, "titulo": "Organize seus estudos", "texto": "Montar uma rotina de estudos ajuda a reduzir a ansiedade antes das provas. Separe blocos de 50 minutos com pausas curtas de 10 minutos, defina uma meta pequena para cada bloco e comece pelas matérias mais difíceis, quando você ainda está com a mente descansada. Evite deixar tudo para a véspera: estudar um pouco por dia é mais eficiente do que estudar muito em uma noite só. Cuide também do sono e da alimentação, porque o cérebro descansado aprende melhor.", "data": "04/10/2026", 'autor':'Dra. Ana Costa'}
]


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