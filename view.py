import json
import tkinter as tk
from tkinter import filedialog, scrolledtext

# Load JSON data from the provided file
#json_file_path = 'Warehouse/v0.4_output_on_10_29_2024_at_15_22.json'
# Prompt to choose JSON file within the 'Warehouse' subdirectory
json_file_path = filedialog.askopenfilename(initialdir="Warehouse", title="Select JSON File",
                                            filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
data_list = []
convo_list = []
with open(json_file_path, 'r') as file:
    # Read all lines, assuming each JSON object starts with '{' on a new line
    for line in file:
        line = line.strip()
        if line.startswith("{"):  # Check if line begins with a JSON object
            try:
                data = json.loads(line)
                data_list.append(data)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON object: {e}")

        if line.startswith("["):
            try:
                data = json.loads(line)
                convo_list.append(data)
            except json.JSONDecodeError as e:
                print(f"Skipping invalid JSON object: {e}")
#print(convo_list)
# Set up the GUI
root = tk.Tk()
root.title("Dialogue Viewer")

# Configure row and column weights for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a ScrolledText widget
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_area.grid(row=0, column=0, sticky="nsew")  # Enables expansion in all directions

# Display each JSON object (configuration + dialogues)
for idx, data in enumerate(data_list):
    text_area.insert(tk.END, f"Entry {idx + 1}:\n")
    
    # Show Alice's and Bob's instructions
    text_area.insert(tk.END, "Alice's Instructions:\n")
    text_area.insert(tk.END, f"{data.get('alice_instructions')}\n\n")
    
    text_area.insert(tk.END, "Bob's Instructions:\n")
    text_area.insert(tk.END, f"{data.get('bob_instructions')}\n\n")

    # display contex

    # Display sender and content for each entry in convelist[0]
    for entry in convo_list[idx]:
        sender = entry.get("sender", "Unknown")
        content = entry.get("content", "No content available")
        # Display the sender and content in the format "Sender: Content"
        text_area.insert(tk.END, f"{sender}: {content}\n\n")

        # Display dialogue content if available
        dialogue = data.get("dialogue", [])
        if dialogue:
            text_area.insert(tk.END, "Dialogue:\n\n")
            for entry in dialogue:
                sender = entry.get("sender", "Unknown")
                content = entry.get("content", "No content available")
                text_area.insert(tk.END, f"{sender}: {content}\n\n")
    text_area.insert(tk.END, "-"*400 + "\n\n")

# Make text area read-only
text_area.configure(state='disabled')

# Run the GUI event loop
root.mainloop()