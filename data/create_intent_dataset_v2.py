
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT_DIR / "data" / "intent_dataset_v2.csv"

examples = [
    # BILLING INQUIRY
    ("Why was I charged twice for the same purchase?", "billing inquiry"),
    ("I received an invoice with an amount different from what I expected.", "billing inquiry"),
    ("Can you explain the additional fee on my latest bill?", "billing inquiry"),
    ("My payment was deducted, but the invoice still shows it as unpaid.", "billing inquiry"),
    ("When will my next billing cycle begin?", "billing inquiry"),
    ("I need a copy of my last payment receipt.", "billing inquiry"),
    ("Why did the subscription price increase this month?", "billing inquiry"),
    ("Can I change the payment method associated with my account?", "billing inquiry"),
    ("I do not recognize a charge listed on my statement.", "billing inquiry"),
    ("How can I check the status of my recent payment?", "billing inquiry"),

    # CANCELLATION REQUEST
    ("I would like to cancel my subscription immediately.", "cancellation request"),
    ("Please terminate my current service plan.", "cancellation request"),
    ("I no longer want to receive this service.", "cancellation request"),
    ("How can I cancel my monthly membership?", "cancellation request"),
    ("Please stop renewing my subscription automatically.", "cancellation request"),
    ("I want to close my account and discontinue the service.", "cancellation request"),
    ("Can you cancel my order before it is shipped?", "cancellation request"),
    ("I would like to end my membership at the end of this month.", "cancellation request"),
    ("Please confirm that my cancellation request has been processed.", "cancellation request"),
    ("I want to unsubscribe from my current plan.", "cancellation request"),

    # PRODUCT INQUIRY
    ("What features are included in the premium version?", "product inquiry"),
    ("Does this product support wireless connectivity?", "product inquiry"),
    ("What is the difference between the basic and advanced plans?", "product inquiry"),
    ("Can you tell me the technical specifications of this device?", "product inquiry"),
    ("Is this product compatible with macOS?", "product inquiry"),
    ("What accessories are included with the purchase?", "product inquiry"),
    ("How long is the manufacturer's warranty?", "product inquiry"),
    ("Does this application offer a free trial?", "product inquiry"),
    ("Which payment plans are available for this product?", "product inquiry"),
    ("Can I use this service on multiple devices?", "product inquiry"),

    # REFUND REQUEST
    ("I want a refund for the product I purchased.", "refund request"),
    ("Please return the money charged for my last order.", "refund request"),
    ("I received the wrong item and would like my money back.", "refund request"),
    ("How can I request a refund for a cancelled order?", "refund request"),
    ("The product did not meet my expectations. I want a refund.", "refund request"),
    ("I was charged for an order that was never delivered. Please refund me.", "refund request"),
    ("I returned the product and would like to receive my money back.", "refund request"),
    ("Please tell me when my refund will be processed.", "refund request"),
    ("I accidentally purchased the same item twice and need one payment refunded.", "refund request"),
    ("I would like to know the procedure for getting a refund.", "refund request"),

    # TECHNICAL ISSUE
    ("The application crashes every time I try to open it.", "technical issue"),
    ("I cannot connect my device to the wireless network.", "technical issue"),
    ("The website displays an error whenever I try to log in.", "technical issue"),
    ("My device suddenly stopped turning on.", "technical issue"),
    ("The application freezes when I submit a form.", "technical issue"),
    ("I cannot reset my password because the reset page does not load.", "technical issue"),
    ("The latest update caused the application to stop working.", "technical issue"),
    ("My device battery is draining much faster than usual.", "technical issue"),
    ("I receive an unexpected error when uploading a file.", "technical issue"),
    ("The service is unavailable even though my internet connection works.", "technical issue"),
]

df = pd.DataFrame(
    examples,
    columns=["text", "intent"]
)

df["source"] = "synthetic"
df["review_status"] = "pending"

df.to_csv(OUTPUT_FILE, index=False)

print("Dataset inicial criado!")
print(f"Total de exemplos: {len(df)}")

print("\nDistribuição:")
print(df["intent"].value_counts())

print(f"\nArquivo salvo em: {OUTPUT_FILE}")
