# Explicação do código da classe GLC

Este projeto implementa uma classe Python para representar e simplificar gramáticas livres de contexto (GLC). O foco principal é remover símbolos inúteis da gramática, isto é:

- símbolos inférteis: não geram palavras válidas;
- símbolos inalcançáveis: não podem ser alcançados a partir do símbolo inicial.

A lógica está contida no arquivo GLC.PY e a execução dos exemplos está no arquivo testesGLC.py.

---

## 1. O que a classe GLC representa

A classe GLC recebe quatro entradas no construtor:

- variaveis: conjunto de variáveis não terminais (Vn)
- terminais: conjunto de símbolos terminais (Vt)
- producao: dicionário com as regras de produção
- inicial: símbolo inicial da gramática

Exemplo de estrutura:

```python
GLC(
    variaveis=['S', 'A', 'B'],
    terminais=['a', 'b'],
    producao={
        'S': [['a', 'B'], ['B'], ['']],
        'A': [['a']],
        'B': [['b', 'B']]
    },
    inicial='S'
)
```

### Como os dados são armazenados

No construtor, os conjuntos são convertidos em `set`, o que facilita a verificação e a remoção de elementos repetidos.

A estrutura de produções é transformada para um formato mais fácil de manipular:

```python
self.producao = {v: [list(p) for p in prods] for v, prods in producao.items()}
```

Isso significa que cada regra da forma:

```python
'S': [['a','B'], ['B'], ['']]
```

fica armazenada como uma lista de listas, onde cada lista representa um lado direito da produção.

---

## 2. Função limparGramatica()

Esta função serve para remover do dicionário de produções qualquer variável que não esteja mais presente no conjunto `self.variaveis`.

### Objetivo

Depois de aplicar a simplificação da gramática, algumas variáveis podem ter sido removidas. Essa função garante que a estrutura final fique consistente.

### Como funciona

A função cria um novo dicionário `nova_producao` e adiciona somente as variáveis que ainda fazem parte da gramática atual.

---

## 3. Função eliminar_inferteis()

Essa função remove os símbolos inférteis, ou seja, variáveis que não conseguem gerar nenhuma palavra terminal válida.

### Ideia do algoritmo

O código usa uma abordagem iterativa:

1. começa com um conjunto de símbolos considerados “férteis”;
2. verifica quais variáveis podem ser geradas a partir de símbolos já conhecidos;
3. repete o processo até que nenhum novo símbolo fértil seja encontrado.

### Passo a passo

- `ferteis_variaveis` começa vazio;
- `ferteis_total` começa como o conjunto de terminais + o símbolo vazio `''`.

Em seguida, o programa percorre todas as regras da gramática:

- se o lado esquerdo da produção ainda não foi marcado como fértil;
- e todos os símbolos do lado direito já estão em `ferteis_total`, então essa variável passa a ser fértil.

Esse processo é repetido até que não haja mais mudanças.

### O que acontece depois

Depois de descobrir quais variáveis são férteis, o programa:

- identifica os símbolos inférteis;
- remove esses símbolos do conjunto `self.variaveis`;
- limpa as produções que não fazem mais parte da gramática.

### Objetivo final

Isso elimina variáveis que nunca geram palavras válidas, deixando a gramática mais limpa e correta.

---

## 4. Função eliminar_inalcancaveis()

Essa função remove os símbolos inalcançáveis.

### Conceito

Um símbolo é inalcançável quando não pode ser alcançado a partir do símbolo inicial da gramática.

### Como o algoritmo funciona

1. inicia com o símbolo inicial como o único símbolo alcançável;
2. percorre as regras da gramática;
3. sempre que encontrar uma variável já alcançável, verifica quais símbolos aparecem no lado direito da produção;
4. se o símbolo for uma variável, ele passa a ser alcançável;
5. se for um terminal, ele também é registrado como alcançável.

Esse processo continua até que nenhuma nova variável ou terminal seja encontrado.

### Depois da análise

O programa compara:

- `self.variaveis` com os símbolos alcançáveis de variável;
- `self.terminais` com os símbolos alcançáveis de terminal.

Os símbolos que não fazem parte desse conjunto alcançável são removidos da gramática.

---

## 5. Função simplificar()

Essa função apenas chama as duas etapas principais em sequência:

```python
def simplificar(self):
    self.eliminar_inferteis()
    self.eliminar_inalcancaveis()
```

Ou seja:

1. remove símbolos inférteis;
2. remove símbolos inalcançáveis.

Esse é o processo principal de simplificação da gramática.

---

## 6. Função exibir()

A função `exibir()` imprime a gramática na tela de forma organizada.

Ela mostra:

- conjunto de variáveis `Vn`
- conjunto de terminais `Vt`
- todas as regras de produção
- símbolo inicial

Ela também converte a produção `['']` em `ε` (epsilon), que representa a produção vazia.

---

## 7. Função rodar_teste()

Essa função é usada para executar uma demonstração completa da gramática.

O fluxo é:

1. imprime a gramática original;
2. chama `simplificar()`;
3. imprime a gramática já simplificada.

É um recurso útil para visualizar o efeito das etapas de eliminação de símbolos inúteis.

---

## 8. Como os exemplos do arquivo testesGLC.py ajudam a entender

No arquivo testesGLC.py há três exemplos:

### Gramática 1

Mostra uma gramática com símbolos inférteis.

### Gramática 2

Mostra uma gramática com símbolos inalcançáveis.

### Gramática 3

Mostra uma gramática que possui ambos os problemas: símbolos inférteis e inalcançáveis.

Esses testes servem para confirmar que o algoritmo funciona corretamente ao simplificar gramáticas.

---

## 9. Resumo do funcionamento geral

Em resumo, o código faz o seguinte:

1. recebe uma gramática;
2. identifica quais variáveis geram palavras válidas;
3. remove as variáveis que não conseguem gerar nada útil;
4. identifica quais símbolos podem ser alcançados a partir do símbolo inicial;
5. remove os símbolos inacessíveis;
6. mostra a gramática final simplificada.

Esse processo é importante porque gramáticas simplificadas são mais fáceis de analisar, de estudar e de usar em algoritmos de linguagem formal.

---

## 10. Conclusão

O código é uma implementação prática de dois conceitos fundamentais da teoria de linguagens formais:

- eliminação de símbolos inférteis;
- eliminação de símbolos inalcançáveis.

Com isso, a classe GLC transforma uma gramática original em uma versão mais limpa e mais adequada para estudos e aplicações.
