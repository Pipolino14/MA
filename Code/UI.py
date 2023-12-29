import customtkinter as cti


cti.set_appearance_mode("dark")
cti.set_default_color_theme("dark-blue")

root = cti.CTk()
root.geometry("1950x1080")

def poopyhead():
    print("poopyhead")

frame = cti.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = cti.CTkLabel(master=frame, text="Calculating of the fittest", font=('Take Cover', 54))
label.pack(pady=12, padx=10)

entry1 = cti.CTkEntry(master=frame, placeholder_text="Instert some Text here")
entry1.pack(pady=12, padx=10)

entry1 = cti.CTkEntry(master=frame, placeholder_text="Lol some text again")
entry1.pack(pady=12, padx=10)

button = cti.CTkButton(master=frame, text="Buton", command=poopyhead)
button.pack(pady=12, padx=10)

checkbox = cti.CTkCheckBox(master=frame, text="This is a checkbox")
checkbox.pack(pady=12, padx=10)

root.mainloop()