from itertools import count

class AFN:
    def __init__(self, estado_inicial: str, estado_final: str, transicao: dict):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.transicao = transicao

def regex_para_afn(regex: str) -> AFN:
    id_generator = count(1)

    def prox_estado_id() -> str: #Retorna o id do estado atual
        return f'S{next(id_generator)}'
    
    def adicionar_transicao(transicoes, origem, simbolo, destinos): #Faz a formatação do dicionario transição 
        if origem not in transicoes:
            transicoes[origem] = {}
        if simbolo not in transicoes[origem]:
            transicoes[origem][simbolo] = set()
        transicoes[origem][simbolo].update(destinos)

    def criar_afn_para_simbolo(simbolo: str) -> AFN: #Cria AFN para o simbolo atual
        estado_inicial = prox_estado_id()
        estado_final = prox_estado_id()
        transicao = {}
        adicionar_transicao(transicao, estado_inicial, simbolo, {estado_final})
        return AFN(estado_inicial, estado_final, transicao)
    
    def concatenar_afn(afn1: AFN, afn2: AFN) -> AFN: #Adiciona 2 classe AFN, estado inial afn1 e estado final afn2
        adicionar_transicao(afn1.transicao, afn1.estado_final, 'ε', {afn2.estado_inicial})
        return AFN(afn1.estado_inicial, afn2.estado_final, {**afn1.transicao, **afn2.transicao})
    
    def uniao_afn(afn1: AFN, afn2: AFN) -> AFN: #Cria um estado que vai ou para AFN1 ou AFN2
        estado_inicial = prox_estado_id()
        estado_final = prox_estado_id()
        transicao = {estado_inicial: {'ε': {afn1.estado_inicial, afn2.estado_inicial}},
                     afn1.estado_final: {'ε': {estado_final}},
                     afn2.estado_final: {'ε': {estado_final}},
                     **afn1.transicao, **afn2.transicao}
        return AFN(estado_inicial, estado_final, transicao)
    
    def asterisco_afn(afn: AFN) -> AFN: #cria dois estados, que servem para ir ao afn dado ou para o prox estado
        estado_inicial = prox_estado_id()
        estado_final = prox_estado_id()
        transicao = {estado_inicial: {'ε': {afn.estado_inicial, estado_final}},
                     afn.estado_final: {'ε': {afn.estado_inicial, estado_final}},
                     **afn.transicao}
        return AFN(estado_inicial, estado_final, transicao)

    def aplicar_operador(operadores, operandos): #Realiza a operação associada a cada operador
        operador = operadores.pop()
        if operador == '.':
            operandos.append(concatenar_afn(operandos.pop(-2), operandos.pop()))
        elif operador == '|':
            operandos.append(uniao_afn(operandos.pop(-2), operandos.pop()))
        elif operador == '*':
            operandos.append(asterisco_afn(operandos.pop()))

    operadores, operandos = [], []
    prioridade = {'*': 3, '.': 2, '|': 1} 
    
    for char in regex: #percorre o Regex dado, adicionando a operadores ou a operandos
        if char.isalnum():
            operandos.append(criar_afn_para_simbolo(char))
        elif char in {'*', '|', '.'}:
            while operadores and operadores[-1] != '(' and prioridade[operadores[-1]] >= prioridade[char]:
                aplicar_operador(operadores, operandos)
            operadores.append(char)
        elif char == '(':
            operadores.append(char)
        elif char == ')':
            while operadores[-1] != '(':
                aplicar_operador(operadores, operandos)
            operadores.pop()
    
    while operadores: #Aplica as operações que faltaram na lista de operadores
        aplicar_operador(operadores, operandos) 
    
    return operandos[0] #Retorna a AFN final

def formatar_transicoes(transicoes: dict) -> str: #Função para tornar o estados no dicionario de transição mais legivel na saída
    return "\n".join(f"{origem} --{simbolo}--> {', '.join(destinos)}" 
                for origem, destinos_simbolo in transicoes.items() 
                for simbolo, destinos in destinos_simbolo.items())

# Entrada e saída do AFN
regex = input("Digite a expressão regular: ")
afn = regex_para_afn(regex)
print("AFN:")
print(f"Estado Inicial: {afn.estado_inicial}")
print(f"Estado Final: {afn.estado_final}")
print("Transições:")
print(formatar_transicoes(afn.transicao))
