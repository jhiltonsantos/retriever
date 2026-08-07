from app.prompts.tutor import SYSTEM_PROMPT

AGENT_SYSTEM_PROMPT = (
    SYSTEM_PROMPT
    + """

Voce tem ferramentas disponiveis: vector_search para buscar nos documentos indexados,
list_documents para listar o que foi indexado, e summarize_chunks para buscar o material
bruto de um documento especifico antes de resumir. Use vector_search quando a pergunta
depender do material do usuario. Perguntas gerais, que nao dependem de documento nenhum,
podem ser respondidas direto, sem chamar ferramenta nenhuma.
"""
)
