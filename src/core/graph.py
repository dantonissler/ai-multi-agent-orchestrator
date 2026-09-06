"""Definição do StateGraph LangGraph para fluxo jurídico.

TODO: Implementar o grafo de estados determinístico:

    supervisor -> analyzer -> [favoravel] -> END
                            -> [desfavoravel] -> drafter -> filer -> END

Transições e checkpoints de validação humana serão definidos em código.
Nenhuma transição será delegada ao LLM.
"""
