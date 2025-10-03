import ollama
import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar
import threading

historial = []

def enviar_mensaje():
    user_msg = entry.get().strip()
    if not user_msg:
        return
    entry.delete(0, tk.END)

    agregar_mensaje(user_msg, "user")
    historial.append({"role": "user", "content": user_msg})

    threading.Thread(target=consultar_ia, args=(historial[:],)).start()

def consultar_ia(contexto):
    try:
        response = ollama.chat(model="gemma3:4b", messages=contexto, stream=False)
        ai_msg = response["message"]["content"]
        historial.append({"role": "assistant", "content": ai_msg})
        ventana.after(0, lambda msg=ai_msg: agregar_mensaje(msg, "ai"))
    except Exception as e:
        ventana.after(0, lambda msg=str(e): agregar_mensaje(f"Error: {msg}", "ai"))

def agregar_mensaje(texto, tipo="user"):
    frame_msg = Frame(chat_frame, bg="white")
    frame_msg.pack(anchor="e" if tipo=="user" else "w", pady=3, padx=10)

    color = "blue" if tipo=="user" else "lightcoral"
    fg = "white" if tipo=="user" else "white"

    lbl = tk.Label(
        frame_msg, text=texto, bg=color, fg=fg,
        wraplength=250, justify="left", padx=10, pady=5,
        font=("Arial", 10), bd=0, relief="flat"
    )
    lbl.pack(anchor="e" if tipo=="user" else "w")

    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.configure(yscrollcommand=scrollbar.set)

ventana = tk.Tk()
ventana.title("Prueba IA")
ventana.geometry("350x500")
ventana.resizable(False, False)

enc = tk.Frame(ventana, bg="coral", padx=10, pady=10)
enc.pack(fill="x")
tk.Label(enc, text="Prueba IA", font=("Times", 16), fg="white", bg="coral").pack()

frame_chat = Frame(ventana, bg="white")
frame_chat.pack(fill="both", expand=True, padx=5, pady=5)

canvas = Canvas(frame_chat, bg="white")
canvas.pack(side="left", fill="both", expand=True)

scrollbar = Scrollbar(frame_chat, command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

chat_frame = Frame(canvas, bg="white")
canvas.create_window((0,0), window=chat_frame, anchor="nw")

chat_frame.bind("<Configure>", on_frame_configure)

inf = tk.Frame(ventana, bg="lightgray")
inf.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

entry = tk.Entry(inf, width=30)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
entry.bind("<Return>", lambda event: enviar_mensaje())

btn_enviar = tk.Button(inf, text="Enviar", command=enviar_mensaje)
btn_enviar.pack(side=tk.RIGHT, padx=5)

ventana.mainloop()
