import tkinter as tk
from tkinter import ttk, messagebox
from subprocess import Popen, PIPE, STDOUT
import threading
from datetime import datetime

class ElizaGuiApp:
    def __init__(self, master):
        self.master = master
        master.title("Eliza Chat")
        
        # Adjust the style for better visuals
        style = ttk.Style()
        style.configure('TButton', font=('Segoe UI', 12), padding=6)
        style.configure('TLabel', font=('Segoe UI', 12), padding=6)
        style.configure('TEntry', font=('Segoe UI', 12), padding=6)
        
        self.master.geometry('800x800')  # Set initial size of window
        
        # Use a frame for conversation display area
        conversation_frame = ttk.Frame(master, padding="10 10 10 10")
        conversation_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Improved conversation area with padding and monospaced font
        self.conversation_area = tk.Text(conversation_frame, state='disabled', height=30, wrap='word', 
        borderwidth=1, relief="solid", font=('Roboto', 10), padx=10, pady=10)
        self.conversation_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = ttk.Frame(master, padding="10 10 10 10")
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        self.user_input = ttk.Entry(input_frame, state='disabled', font=('Segoe UI', 12))
        self.user_input.bind("<Return>", self.send_input_to_eliza)
        self.user_input.bind("<FocusIn>", self.clear_default_text)
        self.user_input.insert(0, "Type your message...")
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.send_button = ttk.Button(input_frame, text="Send", state='disabled', command=lambda: self.send_input_to_eliza(None))
        self.send_button.pack(side=tk.RIGHT, padx=10)

        self.start_button = ttk.Button(master, text="Start Eliza", command=self.start_eliza)
        self.start_button.pack(side=tk.BOTTOM, pady=5)

        self.eliza_process = None

    def start_eliza(self):
        # Start Eliza as a subprocess
        self.eliza_process = Popen(['python', '.\\eliza.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, text=True, bufsize=1)

        # Thread to read Eliza's responses
        self.read_thread = threading.Thread(target=self.read_from_eliza, daemon=True)
        self.read_thread.start()

        # Disable the start button and enable input field and send button
        self.start_button.config(state='disabled')
        self.user_input.config(state='normal')
        self.send_button.config(state='normal')

    def send_input_to_eliza(self, event):
        user_text = self.user_input.get()
        if user_text.strip():  # Ensure input is not empty
            self.update_conversation("You: " + user_text)  # Update conversation here
            self.eliza_process.stdin.write(user_text + "\n")
            self.eliza_process.stdin.flush()
            self.user_input.delete(0, tk.END)

    def read_from_eliza(self):
        for line in self.eliza_process.stdout:
            if line.strip():  # To skip empty lines
                if "Top 3 Dog Breeds" in line:  # Highlight top 3 dog breeds
                    self.update_conversation(line.strip(), is_bullet=True)
                else:
                    self.update_conversation("Eliza: " + line.strip())
                
        self.ask_to_start_again()  # Ask if user wants to start again after finishing dog breed identification

    def update_conversation(self, message, is_bullet=False):
        self.conversation_area.config(state='normal')
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_with_time = f"[{timestamp}] {message}"
        
        # Apply formatting
        if is_bullet:
            self.conversation_area.insert(tk.END, "• " + message_with_time + "\n", 'bullet')
        else:
            if "Eliza:" in message:
                # Apply formatting for Eliza's messages
                self.conversation_area.insert(tk.END, message_with_time + "\n", 'eliza')
            else:
                # Apply formatting for user's messages
                self.conversation_area.insert(tk.END, message_with_time + "\n", 'user')

        # Tag configurations for user, Eliza, and bullet messages with different colors
        self.conversation_area.tag_configure('user', foreground='blue')
        self.conversation_area.tag_configure('eliza', foreground='green')
        self.conversation_area.tag_configure('bullet', foreground='red', font=('Segoe UI', 10, 'bold'))

        # Scroll to the end of the conversation area and disable it
        self.conversation_area.yview(tk.END)
        self.conversation_area.config(state='disabled')
        
    def ask_to_start_again(self):
        response = messagebox.askyesno("Start Again?", "Would you like to start again?")
        if response == tk.YES:
            self.conversation_area.config(state='normal')
            self.conversation_area.delete('1.0', tk.END)  # Clear conversation area
            self.conversation_area.config(state='disabled')
            self.start_eliza()  # Restart Eliza chat
        else:
            self.master.quit()  # Close the application if the user chooses not to start again

    def clear_default_text(self, event):
        if self.user_input.get() == "Type your message...":
            self.user_input.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ElizaGuiApp(root)
    root.mainloop()
