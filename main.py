import tkinter as tk
from tkinter import messagebox
from textblob import TextBlob

def check_spelling():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Warning", "Please enter text.")
        return

    blob = TextBlob(text)
    corrected = str(blob.correct())
    result_label.config(text=f"Corrected: {corrected}")
    save_to_history(text, corrected)

def save_to_history(original, corrected):
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(f"Original: {original}\nCorrected: {corrected}\n{'-'*40}\n")

def clear_history():
    with open("history.txt", "w", encoding="utf-8") as f:
        f.truncate()
    messagebox.showinfo("History", "History cleared!")

def view_history():
    try:
        with open("history.txt", "r", encoding="utf-8") as f:
            content = f.read()
        history_win = tk.Toplevel(root)
        history_win.title("History")
        history_text = tk.Text(history_win, wrap="word")
        history_text.insert(tk.END, content)
        history_text.config(state="disabled")
        history_text.pack(expand=True, fill="both")
    except FileNotFoundError:
        messagebox.showerror("Error", "History file not found.")

root = tk.Tk()
root.title("Spelling Checker")
root.geometry("700x400")
root.config(bg="#dae6f6")

heading = tk.Label(root, text="Spelling Checker", font=("Arial", 20, "bold"), bg="#dae6f6", fg="#364971")
heading.pack(pady=10)

input_text = tk.Text(root, height=5, width=60, font=("poppins", 15))
input_text.pack(pady=10)

check_button = tk.Button(root, text="Check Spelling", font=("poppins", 14), bg="#008CBA", fg="white", command=check_spelling)
check_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("poppins", 14), bg="#dae6f6", fg="#364971")
result_label.pack()

menu_bar = tk.Menu(root)
options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="View History", command=view_history)
options_menu.add_command(label="Clear History", command=clear_history)
menu_bar.add_cascade(label="Settings", menu=options_menu)

root.config(menu=menu_bar)
root.mainloop()






#no need from this part
'''
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import Scrollbar
from textblob import TextBlob
import winsound
import speech_recognition as sr
import pyttsx3
import datetime

# Initialize speech engine
engine = pyttsx3.init()

# Initialize main window
root = tk.Tk()
root.title("Advanced Spelling Checker")
root.geometry("900x600")
is_dark_mode = False

# Functions
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            speak("Listening...")
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, text)
            speak("You said: " + text)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio")
        except sr.RequestError:
            messagebox.showerror("Error", "Speech Recognition service is unavailable")

def check_spelling():
    input_val = input_text.get("1.0", tk.END).strip()
    if not input_val:
        messagebox.showwarning("Input Error", "Please enter a word or sentence.")
        winsound.MessageBeep(winsound.MB_ICONHAND)
        return

    blob = TextBlob(input_val)
    corrected = str(blob.correct())

    input_text.delete("1.0", tk.END)
    input_text.insert(tk.END, corrected)

    # Save to history
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] Input: {input_val}\nCorrected: {corrected}\n{'-' * 40}"
    history_list.insert(tk.END, entry)

    # Save to file
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(entry + "\n")

    # Feedback
    if corrected.lower() == input_val.lower():
        messagebox.showinfo("Correct", "✅ Your spelling is correct.")
        winsound.MessageBeep(winsound.MB_ICONASTERISK)
    else:
        messagebox.showerror("Incorrect", f"❌ Spelling corrected.\nDid you mean:\n'{corrected}'?")
        winsound.MessageBeep(winsound.MB_ICONHAND)
        speak(f"Did you mean: {corrected}?")

def clear_history():
    history_list.delete(0, tk.END)
    with open("history.txt", "w", encoding="utf-8") as f:
        f.write("")  # Clear file

def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode

    bg = "#1e1e1e" if is_dark_mode else "#dae6f6"
    fg = "#ffffff" if is_dark_mode else "#364971"
    txt_bg = "#2d2d2d" if is_dark_mode else "white"

    root.config(bg=bg)
    heading.config(bg=bg, fg=fg)
    history_label.config(bg=bg, fg=fg)
    input_text.config(bg=txt_bg, fg=fg, insertbackground=fg)
    history_list.config(bg=txt_bg, fg=fg)
    frame.config(bg=bg)

# UI Components
heading = tk.Label(root, text="Advanced Spelling Checker", font=("Arial", 22, "bold"), bg="#dae6f6", fg="#364971")
heading.pack(pady=(20, 10))

input_text = tk.Text(root, height=5, width=80, font=("poppins", 14), bg="white", fg="black", wrap=tk.WORD, insertbackground="black")
input_text.pack(pady=10)
input_text.focus()

button_frame = tk.Frame(root, bg="#dae6f6")
button_frame.pack(pady=5)

check_btn = tk.Button(button_frame, text="Check Spelling", font=("poppins", 12, "bold"), bg="red", fg="white", command=check_spelling)
check_btn.grid(row=0, column=0, padx=5)

listen_btn = tk.Button(button_frame, text="🎤 Speech to Text", font=("poppins", 12, "bold"), command=listen)
listen_btn.grid(row=0, column=1, padx=5)

toggle_btn = tk.Button(button_frame, text="🌗 Toggle Dark Mode", font=("poppins", 12, "bold"), command=toggle_dark_mode)
toggle_btn.grid(row=0, column=2, padx=5)

clear_btn = tk.Button(button_frame, text="🧹 Clear History", font=("poppins", 12, "bold"), command=clear_history)
clear_btn.grid(row=0, column=3, padx=5)

history_label = tk.Label(root, text="History", font=("Arial", 16, "bold"), bg="#dae6f6", fg="#364971")
history_label.pack(pady=(10, 0))

frame = tk.Frame(root, bg="#dae6f6")
frame.pack(pady=10, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

history_list = tk.Listbox(frame, width=120, height=10, font=("poppins", 11), yscrollcommand=scrollbar.set)
history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=history_list.yview)

# Start GUI
root.mainloop()

'''
