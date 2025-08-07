import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from skinChecker import *

class ExpandableRow(tk.Frame):
    def __init__(self, master, title, content, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.is_expanded = False

        # Get the image 
        title = title.replace(" ", "").replace("'", "")  # Normalize title for image filename
        try:
            img = Image.open(f"data/icons/{title}_0.jpg")  # Replace with your image path
        except FileNotFoundError:
            img = Image.open("data/icons/Lux_0.jpg")
        img = img.resize((100, 100))
        self.img = ImageTk.PhotoImage(img)

        # Row header button
        self.button = ttk.Button(self, image=self.img, command=self.toggle)
        self.button.pack(fill='x', anchor='n')

        # Hidden content frame
        self.content_frame = tk.Frame(self)
        self.content_label = tk.Label(self.content_frame, text=content, anchor="w", justify="left")
        self.content_label.pack(fill='x', padx=10, pady=5, anchor='n')

    def toggle(self):
        if self.is_expanded:
            self.content_frame.pack_forget()
        else:
            self.content_frame.pack(fill='x')
        self.is_expanded = not self.is_expanded

class App(tk.Tk):
    def __init__(self, loot_data=None):
        super().__init__()
        self.title("Expandable Rows App")

        # Scrollable Canvas for large lists
        canvas = tk.Canvas(self, borderwidth=0, width=1200, height=800)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window(
                (canvas.winfo_reqwidth() // 2, canvas.winfo_reqheight() // 2),  # center coords
                window=self.scroll_frame,
                anchor="center"
            )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)


        # Add expandable rows
        for i, (champ, loot_vals) in enumerate(loot_data.items()):
            # Extract the valueable information from loot_vals
            text_content = f"Champion: {champ}\n\n"
            columns = 7
            for shard in loot_vals:
                text_content += f"Skin Shard: {shard['itemDesc']})\n"
                text_content += f"Upgrade Cost: {shard['upgradeEssenceValue']}\n"
                text_content += f"Skin Value: {shard['value']}\n"
                text_content += f"\n"
            text_content += f"Total Shards: {len(loot_vals)}"
            item = ExpandableRow(self.scroll_frame, champ, text_content)
            item.grid(row=i // columns, column=i % columns, padx=10, pady=10, sticky='n')

if __name__ == "__main__":
    champions = load_champions()
    skins = load_skins()
    loot = load_loot()

    loot_skin_shards = get_loot_skin_shards(loot)

    shards_for_no_skin_champs = find_shards_for_champs_with_no_skins(champions, skins, loot_skin_shards)

    app = App(shards_for_no_skin_champs)
    app.mainloop()
