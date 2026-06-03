from GLC import GLC, rodar_teste

gramatica1 = GLC(
    variaveis=['S', 'A', 'B'],
    terminais=['a', 'b'],
    producao={
        'S': [['a', 'B'], ['B']],
        'A': [['a']],
        'B': [['b', 'B']]
    },
    inicial='S'
)
#GLC.rodar_teste("Gramática 1", gramatica1)

gramatica2 = GLC(
    variaveis=['S', 'A', 'C'],
    terminais=['a', 'c'],
    producao={
        'S': [['a', 'A']],
        'A': [['a']],
        'C': [['c']]
    },
    inicial='S'
)
#GLC.rodar_teste("Gramática 2", gramatica2)

gramatica3 = GLC(
    variaveis=['S', 'A', 'B', 'C', 'D'],
    terminais=['a', 'b', 'c', 'd'],
    producao={
        'S': [['a', 'A'], ['b', 'B']],
        'A': [['c', 'C']],
        'B': [['b']],
        'C': [['c', 'C']],
        'D': [['d']]
    },
    inicial='S'
)
#GLC.rodar_teste("Gramática 3", gramatica3)

if __name__ == "__main__":
    rodar_teste("Gramática 1 - Simbolo Infértil", gramatica1)
    rodar_teste("Gramática 2 - Simbolo Inalcançável", gramatica2)
    rodar_teste("Gramática 3 - Simbolos Inférteis e Inalcançáveis", gramatica3)