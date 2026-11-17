import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser, threading, datetime

try:
    import speech_recognition as sr
except Exception:
    sr = None
try:
    import pyttsx3
    tts = pyttsx3.init()
    tts.setProperty("rate", 165)
except Exception:
    tts = None

def speak(text):
    if tts:
        def run():
            try:
                tts.say(text); tts.runAndWait()
            except Exception:
                pass
        threading.Thread(target=run, daemon=True).start()

def add(who, msg):
    chat.config(state="normal")
    chat.insert("end", f"{who}: {msg}\\n\\n")
    chat.see("end")
    chat.config(state="disabled")

def command(text):
    c = text.lower().strip()
    if "youtube" in c or "यूट्यूब" in c:
        webbrowser.open("https://youtube.com"); return "YouTube खोल रहा हूँ।"
    if "google" in c or "गूगल" in c:
        webbrowser.open("https://google.com"); return "Google खोल रहा हूँ।"
    if "chatgpt" in c or "ai chat" in c or "एआई चैट" in c:
        webbrowser.open("https://chatgpt.com"); return "ChatGPT खोल रहा हूँ।"
    if "time" in c or "समय" in c:
        return "अभी समय है " + datetime.datetime.now().strftime("%I:%M %p")
    if "date" in c or "तारीख" in c:
        return "आज की तारीख है " + datetime.datetime.now().strftime("%d-%m-%Y")
    return "कमांड मिली। AI बातचीत के लिए 'AI Chat खोलें' बटन दबाएँ।"

def send():
    msg = entry.get().strip()
    if not msg: return
    entry.delete(0, "end"); add("आप", msg)
    answer = command(msg); add("JARVIS", answer); speak(answer)

def listen():
    if sr is None:
        messagebox.showerror("Voice", "Voice module उपलब्ध नहीं है।"); return
    mic_btn.config(state="disabled", text="सुन रहा हूँ...")
    def worker():
        result = None
        try:
            rec = sr.Recognizer()
            with sr.Microphone() as source:
                rec.adjust_for_ambient_noise(source, duration=0.5)
                audio = rec.listen(source, timeout=5, phrase_time_limit=7)
            result = rec.recognize_google(audio, language="hi-IN")
        except Exception:
            pass
        def done():
            mic_btn.config(state="normal", text="🎤 बोलें")
            if result:
                entry.delete(0, "end"); entry.insert(0, result); send()
            else:
                messagebox.showwarning("Voice", "आवाज़ समझ नहीं आई। इंटरनेट और माइक्रोफोन जाँचें।")
        app.after(0, done)
    threading.Thread(target=worker, daemon=True).start()

def calc():
    try:
        amount = float(amount_in.get()); rate = float(gst_in.get() or "0")
        total = amount * (1 + rate / 100)
        result.config(text=f"GST सहित कुल: ₹{total:,.2f}  |  GST: ₹{total-amount:,.2f}")
    except ValueError:
        messagebox.showerror("गलती", "सही रकम और GST प्रतिशत डालें।")

app = tk.Tk()
app.title("JARVIS PC V1")
app.geometry("760x640"); app.minsize(650, 550); app.configure(bg="#101827")
style = ttk.Style(); style.theme_use("clam")
style.configure("TButton", font=("Segoe UI", 10), padding=7)
style.configure("TLabel", background="#101827", foreground="#f2f5f9", font=("Segoe UI", 10))
style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"), foreground="#64d8ff")
style.configure("Sub.TLabel", foreground="#b9c6d6")

head = ttk.Frame(app, padding=16); head.pack(fill="x")
ttk.Label(head, text="JARVIS", style="Title.TLabel").pack(anchor="w")
ttk.Label(head, text="आपका Personal Desktop Assistant • Version 1", style="Sub.TLabel").pack(anchor="w")
bar = ttk.Frame(app, padding=(16,0,16,10)); bar.pack(fill="x")
ttk.Button(bar, text="Google", command=lambda:webbrowser.open("https://google.com")).pack(side="left", padx=(0,7))
ttk.Button(bar, text="YouTube", command=lambda:webbrowser.open("https://youtube.com")).pack(side="left", padx=7)
ttk.Button(bar, text="AI Chat खोलें", command=lambda:webbrowser.open("https://chatgpt.com")).pack(side="left", padx=7)

frame = ttk.Frame(app, padding=(16,0,16,8)); frame.pack(fill="both", expand=True)
chat = tk.Text(frame, wrap="word", bg="#182437", fg="#f2f5f9", insertbackground="white",
               relief="flat", font=("Segoe UI",11), padx=12, pady=12)
chat.pack(side="left", fill="both", expand=True)
scroll = ttk.Scrollbar(frame, command=chat.yview); scroll.pack(side="right", fill="y")
chat.configure(yscrollcommand=scroll.set, state="disabled")
add("JARVIS", "नमस्ते Prakash जी! लिखकर या 🎤 बोलकर कमांड दें।")

inp = ttk.Frame(app, padding=(16,0,16,12)); inp.pack(fill="x")
entry = ttk.Entry(inp, font=("Segoe UI",11)); entry.pack(side="left", fill="x", expand=True, padx=(0,8))
entry.bind("<Return>", lambda e: send())
ttk.Button(inp, text="भेजें", command=send).pack(side="left", padx=(0,8))
mic_btn = ttk.Button(inp, text="🎤 बोलें", command=listen); mic_btn.pack(side="left")

box = ttk.LabelFrame(app, text="Medical Store Quick GST Calculator", padding=12)
box.pack(fill="x", padx=16, pady=(0,12))
ttk.Label(box, text="बेस रकम (₹)").grid(row=0,column=0,sticky="w",padx=4)
amount_in = ttk.Entry(box,width=16); amount_in.insert(0,"1000"); amount_in.grid(row=1,column=0,padx=4,pady=4)
ttk.Label(box, text="GST %").grid(row=0,column=1,sticky="w",padx=4)
gst_in = ttk.Entry(box,width=12); gst_in.insert(0,"5"); gst_in.grid(row=1,column=1,padx=4,pady=4)
ttk.Button(box,text="कुल निकालें",command=calc).grid(row=1,column=2,padx=8)
result = ttk.Label(box,text="GST सहित कुल: ₹1,050.00"); result.grid(row=2,column=0,columnspan=3,sticky="w",padx=4,pady=8)
ttk.Label(app,text="Voice के लिए इंटरनेट और माइक्रोफोन चाहिए। AI Chat बटन ChatGPT वेबसाइट खोलता है।",
          style="Sub.TLabel",padding=(16,0,16,12)).pack(anchor="w")
app.mainloop()
