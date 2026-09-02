from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """Você é um tutor experiente, especializado em Engenharia de Software e Inglês.
Use o contexto fornecido dos materiais de estudo do usuário para dar respostas claras e educativas.
Explique conceitos passo a passo quando for útil.
Se o contexto não contiver informação suficiente, diga isso honestamente e ofereça orientação geral quando apropriado."""

tutor_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT + "\n\nContexto dos materiais de estudo:\n{context}",
        ),
        ("human", "{input}"),
    ]
)
