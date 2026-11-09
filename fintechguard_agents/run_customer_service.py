import asyncio

from agents import Runner

from fintechguard_agents.customer_service_agent import customer_service_agent


async def main():

    conversation_history = []

    messages = [
        "Olá, fui cobrado duas vezes na minha conta.",
        "Quero receber meu dinheiro de volta.",
        "Como faço para solicitar esse reembolso?"
    ]

    for turn, message in enumerate(messages, start=1):

        print(f"\n{'=' * 50}")
        print(f" TURNO {turn}")
        print(f"{'=' * 50}")

        print(f"CLIENTE: {message}")

        # Adiciona a nova mensagem ao histórico
        conversation_history.append({
            "role": "user",
            "content": message
        })

        result = await Runner.run(
            customer_service_agent,
            input=conversation_history
        )

        # Recupera o histórico completo, incluindo
        # chamadas de ferramentas e respostas do agente
        conversation_history = result.to_input_list()

        print(f"\nFINTECHGUARD: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())