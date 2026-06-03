
class GLC:
    def __init__(self, variaveis, terminais, producao, inicial):
        self.variaveis = set(variaveis)
        self.terminais = set(terminais)
        self.producao = {v: [list(p) for p in prods] for v, prods in producao.items()}
        self.inicial = inicial
    

    def limparGramatica(self):
        nova_producao = {}
        for v in self.variaveis:
            nova_producao[v] = self.producao[v]
        self.producao = nova_producao

    def eliminar_inferteis(self):
        ferteis = set(self.terminais) | {''}

        encontrou_novo = True
        while encontrou_novo:
            encontrou_novo = False
            for simboloEsq, simbolosDir in self.producao.items():
                if simboloEsq not in ferteis:
                    for simboloDir in simbolosDir:
                        if all(simbolo in ferteis for simbolo in simboloDir):
                            ferteis.add(simboloEsq)
                            encontrou_novo = True
                            break
        
        self.variaveis &= ferteis
        self.limparGramatica()

        for simboloEsq in list(self.producao.keys()):
            filtradas = []
            for simboloDir in self.producao[simboloEsq]:
                if all(simbolo in ferteis for simbolo in simboloDir):
                    filtradas.append(simboloDir)
                if filtradas:
                    self.producao[simboloEsq] = filtradas
                else:
                    del self.producao[simboloEsq]
                    self.variaveis.discard(simboloEsq)

    def eliminar_inalcancaveis(self):
        alcancaveis = set(self.inicial)

        encontrou_novo = True
        while encontrou_novo:
            encontrou_novo = False
            tamanho_anterior = len(alcancaveis)
            for simboloEsq, simbolosDir in self.producao.items():
                if simboloEsq in alcancaveis:

                    for simboloDir in simbolosDir:
                        for simbolo in simboloDir:
                            if simbolo != '' and simbolo not in alcancaveis:
                                alcancaveis.add(simbolo)
                    
            if len(alcancaveis) > tamanho_anterior:
                encontrou_novo = True
        
        self.variaveis &= alcancaveis
        self.terminais &= alcancaveis
        self.limparGramatica()
    
    def simplificar(self):
        self.eliminar_inferteis()
        self.eliminar_inalcancaveis()
    
    def exibir(self):
        print(f"Vn= {sorted(list(self.variaveis))}")
        print(f"Vt= {sorted(list(self.terminais))}")
        print("------------------------------------")
        for simboloEsq, simbolosDir in sorted(self.producao.items()):
            regras = ["".join(simboloDir) if simboloDir != [''] else "ε" for simboloDir in simbolosDir]
            print(f" {simboloEsq} -> {' | '.join(regras)}")
        print("------------------------------------")
        print(f"Simbolo inicial= {self.inicial}\n")


def rodar_teste(titulo, gramatica):
        print("-" * 50)
        print(f"Teste: {titulo}")
        print("-" * 50)
        print("Gramatica Original:")
        gramatica.exibir()
        gramatica.simplificar()
        print("Gramática simplificada (livre de simbolos inúteis):")
        gramatica.exibir()



    