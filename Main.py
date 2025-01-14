from itertools import count

class AFN:
    def __init__(self, estado_inicial: str, estado_final: str, transicao: dict):
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.transicao = transicao

def regex_para_afn(regex: str) -> AFN:
    id_generator = count(1)

    def prox_estado_id() -> str:
        return f's{next(id_generator)}'
    
    def adicionar_transicao(transicoes, origem, simbolo, destinos):
        if origem not in transicoes:
            transicoes[origem] = {}
        if simbolo not in transicoes[origem]:
            transicoes[origem][simbolo] = set()
        transicoes[origem][simbolo].update(destinos)

    def criar_afn_para_simbolo(simbolo: str) -> AFN:
        estado_inicial = prox_estado_id()
        estado_final = prox_estado_id()
        transicao = {}
        adicionar_transicao(transicao, estado_inicial, simbolo, {estado_final})
        return AFN(estado_inicial, estado_final, transicao)
    
    def concatenar_afn(afn1: AFN, afn2: AFN) -> AFN:
        adicionar_transicao(afn1.transicao, afn1.estado_final, 'ε', {afn2.estado_inicial})
        return AFN(afn1.estado_inicial, afn2.estado_final, {**afn1.transicao, **afn2.transicao})
    
    def uniao_afn(afn1: AFN, afn2: AFN) -> AFN:
        estado_inicial = prox_estado_id()
        estado_final = prox_estado_id()
        transicao = {estado_inicial: {'ε': {afn1.estado_inicial, afn2.estado_inicial}},
                     afn1.estado_final: {'ε': {estado_final}},
                     afn2.estado_final: {'ε': {estado_final}},
                     **afn1.transicao, **afn2.transicao}
        return AFN(estado_inicial, estado_final, transicao)
    
    def asterisco_afn(afn: AFN) -> AFN:
        estado_inicial = prox_estado_id()
        estado_final = prox_estado_id()
        transicao = {estado_inicial: {'ε': {afn.estado_inicial, estado_final}},
                     afn.estado_final: {'ε': {afn.estado_inicial, estado_final}},
                     **afn.transicao}
        return AFN(estado_inicial, estado_final, transicao)

    def aplicar_operador(operadores, operandos):
        operador = operadores.pop()
        if operador == '.':
            operandos.append(concatenar_afn(operandos.pop(-2), operandos.pop()))
        elif operador == '|':
            operandos.append(uniao_afn(operandos.pop(-2), operandos.pop()))
        elif operador == '*':
            operandos.append(asterisco_afn(operandos.pop()))

    operadores, operandos = [], []
    prioridade = {'*': 3, '.': 2, '|': 1}
    
    for char in regex:
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
    
    while operadores:
        aplicar_operador(operadores, operandos)
    
    return operandos[0]

def formatar_transicoes(transicoes: dict) -> str: 
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