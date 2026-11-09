
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PATH = BASE_DIR / "data" / "fintechguard_supplemental.csv"

EXAMPLES = {
    "billing inquiry": [
        "Why was an additional fee applied to my account?",
        "I noticed unexpected service charges on my monthly statement.",
        "Can you explain the fees charged to my account this month?",
        "I need a breakdown of the charges on my latest bill.",
        "Why is my credit card statement showing a higher amount?",
        "Could you explain how the interest on my balance was calculated?",
        "I paid my full statement balance before the due date. Why was interest charged?",
        "There is an unfamiliar service fee on my bank statement.",
        "Gostaria de entender as tarifas aplicadas à minha conta.",
        "Por que apareceu uma cobrança adicional na minha fatura?",
        "Preciso consultar o detalhamento dos encargos cobrados.",
        "Minha fatura apresenta um valor diferente do que eu esperava.",
        "Poderiam explicar como foram calculados os juros da minha conta?",
        "Paguei o valor integral da fatura. Por que houve cobrança de juros?",
        "Identifiquei uma tarifa que não compreendi no meu extrato.",
        "Quero saber de onde veio esse encargo na minha conta.",
        "O valor da anuidade do cartão está correto?",
        "Preciso entender a cobrança de manutenção da conta.",
        "Why is my account showing a monthly maintenance fee?",
        "How can I see the calculation of the fees on my statement?",
        "My statement includes interest that I was not expecting.",
        "There seems to be a discrepancy in the total amount due.",
        "Can you clarify the foreign transaction fee on my purchase?",
        "I would like an explanation of the charges listed on my invoice.",
        "Apareceu uma taxa de serviço que não reconheço na fatura.",
        "Quero entender a cobrança de juros rotativos do meu cartão.",
        "O extrato mostra encargos adicionais. Como foram calculados?",
        "Por que o valor total da minha fatura aumentou?",
        "Gostaria de receber o detalhamento das tarifas bancárias.",
        "A cobrança da taxa de transferência está correta?"
    ],
    "technical issue": [
        "My account dashboard keeps showing a blank screen.",
        "The dashboard page gets stuck while loading.",
        "I cannot open my account overview on the website.",
        "The mobile banking application crashes when I open it.",
        "My transaction history page is not displaying any data.",
        "The account balance does not update after I refresh the page.",
        "I receive an error whenever I try to access the dashboard.",
        "The application freezes before reaching the login screen.",
        "O painel da minha conta não carrega corretamente.",
        "A página inicial fica travada quando tento abrir.",
        "Não consigo visualizar o resumo da minha conta.",
        "O aplicativo fecha sozinho quando tento acessar minha conta.",
        "Meu histórico de transações não aparece na tela.",
        "O saldo não atualiza mesmo depois de atualizar a página.",
        "Recebo uma mensagem de erro ao abrir o painel.",
        "A tela do aplicativo fica branca depois do login.",
        "Não consigo carregar os detalhes da minha conta.",
        "O site apresenta falha quando acesso a área do cliente.",
        "The dashboard takes forever to load and eventually times out.",
        "I cannot download my account statement because the page crashes.",
        "The mobile app displays a connection error despite having internet access.",
        "My profile settings page is not responding.",
        "The transaction search feature returns an error.",
        "The website stops responding whenever I open the account summary.",
        "O painel fica carregando sem apresentar nenhuma informação.",
        "A página de extrato apresenta erro ao tentar abrir.",
        "O sistema não responde quando clico em atualizar saldo.",
        "Não consigo acessar o aplicativo mesmo com a internet funcionando.",
        "A consulta de movimentações apresenta uma falha inesperada.",
        "O site trava sempre que tento acessar meus dados bancários."
    ]
}

def main():
    records = []

    for intent, messages in EXAMPLES.items():
        for message in messages:
            records.append({
                "text": message.strip(),
                "intent": intent
            })

    df = pd.DataFrame(records)

    df["normalized"] = (
        df["text"]
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    duplicates = df[df.duplicated("normalized", keep=False)]

    if not duplicates.empty:
        print("Foram encontrados textos duplicados:")
        print(duplicates[["text", "intent"]].to_string(index=False))
        return

    df = df.drop(columns=["normalized"])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

    print("Dataset complementar criado!")
    print(f"Arquivo: {OUTPUT_PATH}")
    print(f"Total de exemplos: {len(df)}")
    print("\nDistribuição:")
    print(df["intent"].value_counts().to_string())

if __name__ == "__main__":
    main()
