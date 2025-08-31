# currency_converter.py

# exchange rates (fixed for now)
rates = {
    "USD": {"BRL": 5.6, "EUR": 0.92, "GBP": 0.79},
    "BRL": {"USD": 0.18, "EUR": 0.16, "GBP": 0.14},
    "EUR": {"USD": 1.09, "BRL": 6.1, "GBP": 0.86},
    "GBP": {"USD": 1.26, "BRL": 7.1, "EUR": 1.16},
}

# conversion function
def convert(amount, from_currency, to_currency):
    try:
        rate = rates[from_currency][to_currency]
        return amount * rate
    except KeyError:
        return None

# terminal interface
print("=== Currency Converter ===")

amount = float(input("Enter the amount: "))
from_currency = input("From (USD, BRL, EUR, GBP): ").upper()
to_currency = input("To (USD, BRL, EUR, GBP): ").upper()

result = convert(amount, from_currency, to_currency)

if result:
    print(f"{amount} {from_currency} = {result:.2f} {to_currency}")
else:
    print("Conversion not available. Please check the currencies entered.")
