import tkinter as tk
from tkinter import filedialog, scrolledtext
from utils.file_reader import read_encoded_file
from sys import exit
from assertiveness_observer import name_formal,name_pajama
# Load JSON data from the provided file
#json_file_path = 'Warehouse/v0.4_output_on_10_29_2024_at_15_22.json'
# Prompt to choose JSON file within the 'Warehouse' subdirectory
json_file_path = filedialog.askopenfilename(initialdir="Warehouse", title="Select JSON File",
                                            filetypes=(("JSON files", "*.json"), ("All files", "*.*")))

if len(json_file_path) == 0:
    print("No file selected. Exiting.")
    exit()

(convo_list, data_list) = read_encoded_file(json_file_path)

# Test function to see if the files are identified correctly. 
from utils.file_reader import identities_known, get_messages_from
print(f"Valid File: {identities_known(get_messages_from(json_file_path))}")

#print(convo_list)
# Set up the GUI
root = tk.Tk()
root.title(f"Dialogue Viewer for {json_file_path}")

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
    text_area.insert(tk.END, f"{name_pajama}'s Instructions:\n")
    text_area.insert(tk.END, f"{data.get('alice_instructions')}\n\n")
    
    text_area.insert(tk.END, f"{name_formal}'s Instructions:\n")
    text_area.insert(tk.END, f"{data.get('bob_instructions')}\n\n")

    # display contex

    # Display sender and content for each entry in convelist[0]
    for entry in convo_list[idx]:
        # get the person who sent the message
        role = entry.get("role")
        sender = entry.get("sender", "System" if (role == "user") else role)

        # get the function calls from the tool calls object
        tool_calls= entry.get("tool_calls", None)
        function_calls = list()
        if tool_calls:
            for call in tool_calls:
                call_type = call.get("type")
                if call_type == "function":
                    fn = call.get("function")
                    function_calls.append(f"{fn.get('name')}({fn.get('arguments')})")

        content = entry.get("content", None)
        # print(content)
        # print(num_tokens_from_messages(content))
        # Display the sender and content in the format "Sender: Content"
        if content:
            text_area.insert(tk.END, f"{sender}: {content}\n")
        # Display the function call in the format "Sender: Function"
        if function_calls:
            for call in function_calls:
                text_area.insert(tk.END, f"{sender}: {call}\n")
        text_area.insert(tk.END, "\n")

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