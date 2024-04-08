import tkinter as tk
from subprocess import Popen, PIPE, STDOUT
import threading

class ElizaGuiApp:
    def __init__(self, master):
        self.master = master
        master.title("Eliza Chat")

        # Conversation display area
        self.conversation_area = tk.Text(master, state='disabled', height=30, width=100)
        self.conversation_area.pack(padx=20, pady=20)

        # User input field, initially disabled
        self.user_input = tk.Entry(master, state='disabled')
        self.user_input.bind("<Return>", self.send_input_to_eliza)
        self.user_input.pack(padx=20, pady=10, fill=tk.X)

        # Send button, initially disabled
        self.send_button = tk.Button(master, text="Send", state='disabled', command=lambda: self.send_input_to_eliza(None))
        self.send_button.pack(padx=10, pady=5)

        # Start Eliza button
        self.start_button = tk.Button(master, text="Start Eliza", command=self.start_eliza)
        self.start_button.pack(padx=20, pady=10)

        self.eliza_process = None

        self.master.update()






    def start_eliza(self):
        # Start Eliza as a subprocess
        self.eliza_process = Popen(['python3', '.\\eliza.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, text=True, bufsize=1)


        # Thread to read Eliza's responses
        self.read_thread = threading.Thread(target=self.read_from_eliza, daemon=True)
        self.read_thread.start()

        # Disable the start button and enable input field and send button
        self.start_button.config(state='disabled')
        self.user_input.config(state='normal')
        self.send_button.config(state='normal')

    def send_input_to_eliza(self, event):
        user_text = self.user_input.get()
        self.update_conversation("You: " + user_text)
        self.eliza_process.stdin.write(user_text + "\n")
        self.eliza_process.stdin.flush()
        self.user_input.delete(0, tk.END)

    def read_from_eliza(self):
        for line in self.eliza_process.stdout:
            self.update_conversation("Eliza: " + line.strip())

    def update_conversation(self, message):
        self.conversation_area.config(state='normal')
        self.conversation_area.insert(tk.END, message + "\n")
        self.conversation_area.config(state='disabled')
        self.conversation_area.yview(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ElizaGuiApp(root)
    root.mainloop()