import tkinter as tk
from tkinter import ttk, messagebox
import requests

# fallback rates (fixed)
fallback_rates = {
    "USD": {"BRL": 5.6, "EUR": 0.92, "GBP": 0.79},
    "BRL": {"USD": 0.18, "EUR": 0.16, "GBP": 0.14},
    "EUR": {"USD": 1.09, "BRL": 6.1, "GBP": 0.86},
    "GBP": {"USD": 1.26, "BRL": 7.1, "EUR": 1.16},
}

# emojis/símbolos dos países
flags = {
    "USD": "🇺🇸",
    "BRL": "🇧🇷",
    "EUR": "🇪🇺",
    "GBP": "🇬🇧"
}

# real taxes from API
def get_rates(base):
    url = f"https://api.exchangerate.host/latest?base={base}&symbols=USD,BRL,EUR,GBP"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get("rates", fallback_rates[base])
    except:
        return fallback_rates[base]

# função de conversão
def convert(amount, from_currency, to_currency):
    rates = get_rates(from_currency)
    if to_currency not in rates:
        return None
    return amount * rates[to_currency]

# mostrar taxas atuais
def show_rates(base):
    rates = get_rates(base)
    rates_text = " | ".join([f"{flags[cur]} {cur}: {rate:.2f}" for cur, rate in rates.items()])
    rates_label.config(text=f"Current rates ({flags[base]} {base}): {rates_text}")

# clique do botão
def on_convert():
    try:
        amount = float(amount_entry.get())
        from_currency = from_combo.get()
        to_currency = to_combo.get()
        result = convert(amount, from_currency, to_currency)
        if result:
            result_label.config(text=f"{flags[from_currency]} {amount} {from_currency} = {flags[to_currency]} {result:.2f} {to_currency}")
            show_rates(from_currency)
        else:
            messagebox.showerror("Error", "Conversion not available!")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

# GUI setup
root = tk.Tk()
root.title("💰 Currency Converter")
root.geometry("450x300")
root.configure(bg="#f0f0f0")

# título
tk.Label(root, text="💸 Currency Converter", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

# entrada de valor
tk.Label(root, text="Amount:", font=("Arial", 12), bg="#f0f0f0").pack()
amount_entry = tk.Entry(root, font=("Arial", 12))
amount_entry.pack(pady=5)

# moeda de origem
tk.Label(root, text="From:", font=("Arial", 12), bg="#f0f0f0").pack()
from_combo = ttk.Combobox(root, values=["USD", "BRL", "EUR", "GBP"], font=("Arial", 12))
from_combo.pack()
from_combo.current(0)

# moeda de destino
tk.Label(root, text="To:", font=("Arial", 12), bg="#f0f0f0").pack()
to_combo = ttk.Combobox(root, values=["USD", "BRL", "EUR", "GBP"], font=("Arial", 12))
to_combo.pack()
to_combo.current(1)

# botão converter
tk.Button(root, text="Convert", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=on_convert).pack(pady=10)

# resultado
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg="#f0f0f0")
result_label.pack(pady=5)

# taxas atuais
rates_label = tk.Label(root, text="", font=("Arial", 10), bg="#f0f0f0")
rates_label.pack(pady=5)

# iniciar com taxas do USD
show_rates("USD")

root.mainloop()
