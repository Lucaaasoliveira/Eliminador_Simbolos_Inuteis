class GLC:
    def __init__(self, variaveis, terminais, producao, inicial):
        self.variaveis = set(variaveis)
        self.terminais = set(terminais)
        self.producao = {v: [list(p) for p in prods] for v, prods in producao.items()}
        self.inicial = inicial
    

    # função para limpar produções que não tem mais variáveis válidas, ou seja, qualquer variável que não esteja mais presente no conjunto self.variaveis

    def limparGramatica(self):
        nova_producao = {}
        for v in self.variaveis:
            if v in self.producao:
                nova_producao[v] = self.producao[v]
        self.producao = nova_producao


    def eliminar_inferteis(self):
        print("Identificação de Símbolos Férteis")
        print(f"{'Iteração':<12} | {'Variáveis Férteis (Vn)':<25}")
        print("-" * 45)

        # começa vazio, 0 iteratividade
        ferteis_variaveis = set()

        #começa com o conjunto de terminais + o Epsilon
        ferteis_total = set(self.terminais) | {''}
        

        print(f"{0:<12} | {sorted(list(ferteis_variaveis))}")

        #aqui começa o looping, no qual a cada iteração, verificamos se alguma variável pode ser considerada fértil com base nas produções e no conjunto atual de símbolos férteis.

        iteracao = 1
        encontrou_novo = True
        

        while encontrou_novo:
            encontrou_novo = False
            tamanho_anterior = len(ferteis_variaveis)
            
            for simboloEsq, simbolosDir in self.producao.items():
                if simboloEsq not in ferteis_variaveis:
                    for simboloDir in simbolosDir:
                        if all(simbolo in ferteis_total for simbolo in simboloDir):
                            ferteis_variaveis.add(simboloEsq)
                            ferteis_total.add(simboloEsq)
                            break
            
            print(f"{iteracao:<12} | {sorted(list(ferteis_variaveis))}")
            
            if len(ferteis_variaveis) > tamanho_anterior:
                encontrou_novo = True
            iteracao += 1

        # deepois do loop para identificar quais são os símbolos férteis, pode-se identificar os inférteis e dai remover eles da gramática, ou seja, do conjunto self.variaveis

        removidos = self.variaveis - ferteis_variaveis
        if removidos:
            print(f"\n-> Símbolos inférteis identificados e removidos: {sorted(list(removidos))}")
        else:
            print("\n-> Nenhum símbolo infértil encontrado.")

        # aqui atualiza o conjunto de variáveis válidas
        self.variaveis &= ferteis_variaveis
        self.limparGramatica()

        # Dai depois de identificar os símbolos inférteis e retirar eles da gramática (sel.variaveis), retira-se das produções da gramática

        for simboloEsq in list(self.producao.keys()):
            filtradas = []
            for simboloDir in self.producao[simboloEsq]:
                if all(simbolo in ferteis_total for simbolo in simboloDir):
                    filtradas.append(simboloDir)
            if filtradas:
                self.producao[simboloEsq] = filtradas
            else:
                if simboloEsq in self.producao:
                    del self.producao[simboloEsq]
                self.variaveis.discard(simboloEsq)
        print("\n" + "="*50 + "\n")



    def eliminar_inalcancaveis(self):

        print("Identificação de Símbolos Alcançáveis")
        print(f"{'Iteração':<12} | {'Vn Alcançáveis':<20} | {'Vt Alcançáveis':<20}")
        print("-" * 60)

        # na iteração 0 Apenas o símbolo inicial é alcançável (por padrão é o S)
        vn_alcancaveis = {self.inicial}
        vt_alcancaveis = set()
        
        print(f"{0:<12} | {str(sorted(list(vn_alcancaveis))):<20} | {str(sorted(list(vt_alcancaveis))):<20}")


        #aqui começa o looping para encontrar os alcançáveis, sempre que uma variável é definida como alcançável, ela é adicionada e o looping se repete até a última linha da tabela ser igual a anterior

        iteracao = 1
        encontrou_novo = True
        while encontrou_novo:
            encontrou_novo = False
            tamanho_vn_ant = len(vn_alcancaveis)
            tamanho_vt_ant = len(vt_alcancaveis)
            
            for simboloEsq, simbolosDir in self.producao.items():
                if simboloEsq in vn_alcancaveis:
                    for simboloDir in simbolosDir:
                        for simbolo in simboloDir:
                            if simbolo != '':
                                if simbolo in self.variaveis:
                                    vn_alcancaveis.add(simbolo)
                                elif simbolo in self.terminais:
                                    vt_alcancaveis.add(simbolo)
            
            print(f"{iteracao:<12} | {str(sorted(list(vn_alcancaveis))):<20} | {str(sorted(list(vt_alcancaveis))):<20}")
            
            if len(vn_alcancaveis) > tamanho_vn_ant or len(vt_alcancaveis) > tamanho_vt_ant:
                encontrou_novo = True
            iteracao += 1

        # aqui identifica tanto as variaveis não terminais (self.variaveis) quanto as variavis terminais que não foram alcançadas, posteriormente eliminando elas da gramática.
        vn_inalcancaveis = self.variaveis - vn_alcancaveis
        vt_inalcancaveis = self.terminais - vt_alcancaveis
        
        if vn_inalcancaveis or vt_inalcancaveis:
            print(f"\n-> Símbolos inalcançáveis removidos: Vn={sorted(list(vn_inalcancaveis))} Vt={sorted(list(vt_inalcancaveis))}")
        else:
            print("\n-> Nenhum símbolo inalcançável encontrado.")

        # remove de fato as variáveis das produções
        self.variaveis &= vn_alcancaveis
        self.terminais &= vt_alcancaveis
        self.limparGramatica()
        print("\n" + "="*50 + "\n")
    
    # função apenas que chama as funções de eliminar inférteis e inalcançáveis
    def simplificar(self):
        self.eliminar_inferteis()
        self.eliminar_inalcancaveis()
    
    # função única e simplesmente para exibir na tela (Terminal)
    def exibir(self):
        print(f"Vn= {sorted(list(self.variaveis))}")
        print(f"Vt= {sorted(list(self.terminais))}")
        print("------------------------------------")
        for simboloEsq, simbolosDir in sorted(self.producao.items()):
            regras = ["".join(simboloDir) if simboloDir != [''] else "ε" for simboloDir in simbolosDir]
            print(f" {simboloEsq} -> {' | '.join(regras)}")
        print("------------------------------------")
        print(f"Simbolo inicial= {self.inicial}\n")


# função para que roda as outras funções necessárias para a exibição da gramática original, da eliminação e da simplificação (e posterior exibição simplificada.)
def rodar_teste(titulo, gramatica):
    print("=" * 60)
    print(f"EXECUÇÃO DO TESTE: {titulo}")
    print("=" * 60)
    print("GRAMÁTICA ORIGINAL:")
    gramatica.exibir()
    
    gramatica.simplificar()
    
    print("GRAMÁTICA SIMPLIFICADA FINAL:")
    gramatica.exibir()
    print("\n\n")