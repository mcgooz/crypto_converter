## Simple Crypto Converter

import requests
import re
from tkinter import *
from tkinter import ttk, messagebox, PhotoImage

## FUNCTIONS ##


# Convert button function carries user input to main
def convert_click():
    crypto = crypto_input.get()
    fiat = fiat_input.get()
    if root.winfo_exists():
        main(crypto, fiat)



# Initialise input to None (for program exit).
def main(c=None, f=None):
    try:
        # Runs user input through the check function then calls corresponding functions.
        result = input_check(c, f)
        # Nothing selected
        if result == "no_crypto":
            messagebox.showerror(message="Please select a cryptocurrency!")
        # Input in Euros; convert Euros to selected crypto, and update GUI.
        elif result == "f2c":
            fiat2crypto(f)
            f2c_update_GUI(f)
        # Input in crypto; convert selected crypto to Euros, and update GUI.
        elif result == "c2f":
            crypto2fiat(c)
            c2f_update_GUI(c)
        # Crypto selected but no further input.
        elif result == "empty":
            messagebox.showerror(message="Please enter an amount")
        # Post-conversion; reset to try again :D
        elif result == "clear":
            messagebox.showinfo(message="Please clear selection")
        # Input can't be converted to float (invalid input), try again.
        elif result == "invalid":
            messagebox.showerror(message="Please enter a valid number")
    except (TypeError, KeyError, TclError):
        return


# Check user input, return instruction to main.
def input_check(c, f):
    s = crypto_menu.get()
    if s == "Choose a cryptocurrency...":
        return "no_crypto"
    elif c == "" and f == "":
        return "empty"
    elif len(c) > 0 and len(f) > 0:
        return "clear"
    elif len(c) > 0 and f == "":
        if is_float(c):
            return "c2f"
        else:
            return "invalid"
    elif len(f) > 0 and c == "":
        if is_float(f):
            return "f2c"
        else:
            return "invalid"

# Remove letters, commas and euro symbol from input.
def input_strip(n):
    strip = re.sub("[a-zA-Z€,]", "", n)
    return strip.strip()


# Check that stripped input can be converted to float.
def is_float(n):
    n = input_strip(n)
    try:
        float(n)
        return True
    except ValueError:
        return False


# Convert crypto input to Euros using latest price.
def crypto2fiat(c):
    crypto_amount = input_strip(c)
    crypto = float(crypto_amount)
    c2f_value = crypto_price() * crypto
    return c2f_value


# Convert fiat input to crypto using latest price.
def fiat2crypto(f):
    fiat_amount = input_strip(f)
    fiat = float(fiat_amount)
    f2c_value = fiat / crypto_price()
    return f2c_value


# Function to update GUI with crypto to fiat results
def c2f_update_GUI(c):
    selected_crypto = crypto_menu.get()
    c2f_value = crypto2fiat(c)
    result = f"€{c2f_value:,.2f}"
    fiat_input.delete(0, END)
    fiat_input.insert(0, result)
    fiat_label.config(text="€€€")
    crypto_label.config(text=selected_crypto)
    c = input_strip(c)
    update_crypto = f"{selected_crypto} {float(c):,.8f}"
    crypto_input.delete(0, END)
    crypto_input.insert(0, update_crypto)


# Function to update GUI with fiat to crypto results
def f2c_update_GUI(f):
    selected_crypto = crypto_menu.get()
    f2c_value = fiat2crypto(f)
    result = f"{selected_crypto} {f2c_value:,.8f}"
    crypto_input.delete(0, END)
    crypto_input.insert(0, result)
    crypto_label.config(text=selected_crypto)
    fiat_label.config(text="€€€")
    f = input_strip(f)
    update_fiat = f"€{float(f):,.2f}"
    fiat_input.delete(0, END)
    fiat_input.insert(0, update_fiat)


# Retrieve current price of selected crypto via Binance API
def crypto_price():
    currency = "EUR"
    crypto_selection = crypto_menu.get()
    s = f"{crypto_selection}{currency}"
    try:
        response = requests.get(
            f"https://api.binance.com/api/v3/ticker/price?symbol={s}"
        )
        o = response.json()
        price = float(o["price"])
        return price
    except requests.RequestException:
        messagebox.showerror(
            message="Can't retrieve data at this time. In the meantime, just HODL! ;)"
        )
        return


# Clear button to reset all fields
def clear_click():
    fiat_input.delete(0, END)
    fiat_input.insert(0, "")
    crypto_input.delete(0, END)
    crypto_menu.set("Choose a cryptocurrency...")
    fiat_label.config(text="...")
    crypto_label.config(text="...")


# Function to track and update selected crypto denomination
def update_values(*args):
    selected_crypto = crypto_menu.get()
    crypto_label.config(text=f"Enter amount in {selected_crypto}")
    fiat_label.config(text="Enter amount in €")
    fiat_input.delete(0, END)
    crypto_input.delete(0, END)


# Destroy everything when closing window (might be cheating here)
def on_closing():
    root.destroy()


##### GUI #####

root = Tk()

# Set the size of the window
window_width = 350
window_height = 200

# Get current screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Find center points of x and y axis
center_x = int((screen_width / 2 - window_width / 2))
center_y = int((screen_height / 2 - window_height / 2))

# Set window position to middle of screen
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Set window title
root.title("Simple Crypto Converter")

# Set window colour
root.configure(background="gold1")

# Set window icon (not working in CS50 codespace)
root.iconbitmap("bitcoin.ico")

# Configure grid
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Disable window resize
root.resizable(False, False)

# Choose a crypto banner
banner = PhotoImage(file="banner.png")
choose_label = ttk.Label(root, image=banner)
choose_label.grid(column=0, row=0, columnspan=3, padx=3, pady=3)
choose_label.config(background="gold1", foreground="gray4")

# Crypto dropdown menu
crypto_options_menu = StringVar()
crypto_menu = ttk.Combobox(root, width=30, textvariable=crypto_options_menu)
crypto_menu.set("Choose a cryptocurrency...")
crypto_menu["values"] = ("BTC", "BCH", "ETH", "LTC", "XLM", "XRP")
crypto_menu.state(["readonly"])
crypto_menu.grid(column=0, row=1, columnspan=3, padx=3, pady=3)
crypto_menu.bind("<<ComboboxSelected>>", update_values)

# Crypto amount label
crypto_label = ttk.Label(root, text="...")
crypto_label.grid(column=0, row=2, padx=5, pady=7)
crypto_label.config(background="gold1", foreground="gray4")

# Crypto amount input field
crypto_input_box = StringVar()
crypto_input = ttk.Entry(
    root, width=25, textvariable=crypto_input_box, background="gray3"
)
crypto_input.grid(column=0, row=3, padx=3, pady=2)

# Equals label
equals_label = ttk.Label(root, text="=")
equals_label.grid(column=1, row=3, padx=5, pady=5)
equals_label.config(background="gold1", foreground="gray4")

# Fiat amount label
fiat_label = ttk.Label(root, text="...")
fiat_label.grid(column=2, row=2, padx=5, pady=5)
fiat_label.config(background="gold1", foreground="gray4")

# Fiat amount input field
fiat_input_box = StringVar()
fiat_input = ttk.Entry(root, width=25, textvariable=fiat_input_box)
fiat_input.grid(column=2, row=3, padx=3, pady=2)

# Label and field update based on dropdown
crypto_options_menu.trace_add("write", update_values)

# Clear button
button_clear = ttk.Button(root, text="Clear", command=clear_click)
button_clear.grid(column=2, row=4, padx=5, pady=10)

# Convert button
button_go = ttk.Button(root, text="Convert", command=convert_click)
button_go.grid(column=0, row=4, padx=5, pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

if __name__ == "__main__":
    main()
