import os
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps

class WallpaperGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wallpaper Generator")
        self.geometry("800x600")
        self.sticker_dir = "stickers"
        self.stickers = []
        self.selected_stickers = []
        self.boosted_stickers = []
        self.center_image_path = None
        self.background_image_path = None
        self.full_resolution_img = None  # Store the full-resolution image
        self.init_ui()

    def init_ui(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        # Page 1: Sticker Selection
        page1 = ttk.Frame(notebook)
        notebook.add(page1, text="Sticker Selection")
        self.init_sticker_selection(page1)

        # Page 2: Center & Background Image
        page2 = ttk.Frame(notebook)
        notebook.add(page2, text="Center & Background Image")
        self.init_center_background(page2)

        # Page 3: Preview & Save
        page3 = ttk.Frame(notebook)
        notebook.add(page3, text="Preview & Save")
        self.init_preview_save(page3)

        # Page 4: Boost Rate
        page4 = ttk.Frame(notebook)
        notebook.add(page4, text="Boost Rate")
        self.init_boost_rate(page4)

    def init_sticker_selection(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        self.sticker_vars = []

        sticker_canvas = tk.Canvas(frame)
        sticker_scroll = ttk.Scrollbar(frame, orient="vertical", command=sticker_canvas.yview)
        sticker_scroll.pack(side="right", fill="y")

        sticker_frame = ttk.Frame(sticker_canvas)
        sticker_frame.bind(
            "<Configure>",
            lambda e: sticker_canvas.configure(scrollregion=sticker_canvas.bbox("all"))
        )

        sticker_canvas.create_window((0, 0), window=sticker_frame, anchor="nw")
        sticker_canvas.configure(yscrollcommand=sticker_scroll.set)
        sticker_canvas.pack(fill="both", expand=True)

        if not os.path.exists(self.sticker_dir):
            os.makedirs(self.sticker_dir)

        for sticker_name in os.listdir(self.sticker_dir):
            sticker_var = tk.BooleanVar(value=True)  # Default to checked
            sticker_check = ttk.Checkbutton(sticker_frame, text=sticker_name, variable=sticker_var)
            sticker_check.pack(anchor="w")
            self.sticker_vars.append((sticker_var, sticker_name))

        button_frame = ttk.Frame(parent)
        button_frame.pack(fill="x", pady=5)

        select_all_btn = ttk.Button(button_frame, text="Select All", command=self.select_all_stickers)
        select_all_btn.pack(side="left", padx=5)

        deselect_all_btn = ttk.Button(button_frame, text="Deselect All", command=self.deselect_all_stickers)
        deselect_all_btn.pack(side="left", padx=5)

        # Add tooltips
        self.add_tooltip(select_all_btn, "Select all stickers.")
        self.add_tooltip(deselect_all_btn, "Deselect all stickers.")

    def select_all_stickers(self):
        for var, _ in self.sticker_vars:
            var.set(True)

    def deselect_all_stickers(self):
        for var, _ in self.sticker_vars:
            var.set(False)

    def init_center_background(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        center_img_label = ttk.Label(frame, text="Center Image:")
        center_img_label.grid(row=0, column=0, padx=5, pady=5)

        self.center_img_preview = ttk.Label(frame, text="No Image Loaded", width=30, relief="sunken")
        self.center_img_preview.grid(row=0, column=1, padx=5, pady=5)

        load_center_btn = ttk.Button(frame, text="Load Image", command=self.load_center_image)
        load_center_btn.grid(row=0, column=2, padx=5, pady=5)

        # Add tooltip
        self.add_tooltip(load_center_btn, "Load the image that will be centered in the wallpaper.")

        bg_img_label = ttk.Label(frame, text="Background Image:")
        bg_img_label.grid(row=1, column=0, padx=5, pady=5)

        self.bg_img_preview = ttk.Label(frame, text="No Image Loaded", width=30, relief="sunken")
        self.bg_img_preview.grid(row=1, column=1, padx=5, pady=5)

        load_bg_btn = ttk.Button(frame, text="Load Image", command=self.load_background_image)
        load_bg_btn.grid(row=1, column=2, padx=5, pady=5)

        # Add tooltip
        self.add_tooltip(load_bg_btn, "Load the background image for the wallpaper.")

        scale_label = ttk.Label(frame, text="Center Image Scale (%):")
        scale_label.grid(row=2, column=0, padx=5, pady=5)

        self.scale_var = tk.IntVar(value=100)
        scale_spin = ttk.Spinbox(frame, from_=10, to=200, textvariable=self.scale_var)
        scale_spin.grid(row=2, column=1, padx=5, pady=5)

        # Add tooltip
        self.add_tooltip(scale_spin, "Adjust the scale of the center image as a percentage.")

    def load_center_image(self):
        self.center_image_path = filedialog.askopenfilename(title="Select Center Image")
        if self.center_image_path:
            self.update_image_preview(self.center_img_preview, self.center_image_path)

    def load_background_image(self):
        self.background_image_path = filedialog.askopenfilename(title="Select Background Image")
        if self.background_image_path:
            self.update_image_preview(self.bg_img_preview, self.background_image_path)

    def update_image_preview(self, preview_label, image_path):
        try:
            img = Image.open(image_path)
            img.thumbnail((150, 150))  # Adjust size for preview
            img_tk = ImageTk.PhotoImage(img)
            preview_label.config(image=img_tk, text="")
            preview_label.image = img_tk  # Keep a reference to avoid garbage collection
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def init_preview_save(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        res_label = ttk.Label(frame, text="Wallpaper Resolution:")
        res_label.grid(row=0, column=0, padx=5, pady=5)

        self.res_width_var = tk.IntVar(value=1920)
        res_width_entry = ttk.Entry(frame, textvariable=self.res_width_var, width=10)
        res_width_entry.grid(row=0, column=1, padx=5, pady=5)

        x_label = ttk.Label(frame, text="x")
        x_label.grid(row=0, column=2, padx=5, pady=5)

        self.res_height_var = tk.IntVar(value=1080)
        res_height_entry = ttk.Entry(frame, textvariable=self.res_height_var, width=10)
        res_height_entry.grid(row=0, column=3, padx=5, pady=5)

        num_stickers_label = ttk.Label(frame, text="Number of Stickers:")
        num_stickers_label.grid(row=1, column=0, padx=5, pady=5)

        self.num_stickers_var = tk.IntVar(value=10)
        num_stickers_entry = ttk.Entry(frame, textvariable=self.num_stickers_var, width=10)
        num_stickers_entry.grid(row=1, column=1, padx=5, pady=5)

        scale_range_label = ttk.Label(frame, text="Sticker Scale Range (%):")
        scale_range_label.grid(row=2, column=0, padx=5, pady=5)

        self.scale_min_var = tk.IntVar(value=50)
        self.scale_max_var = tk.IntVar(value=150)
        scale_range_frame = ttk.Frame(frame)
        scale_range_frame.grid(row=2, column=1, padx=5, pady=5)

        scale_min_entry = ttk.Entry(scale_range_frame, textvariable=self.scale_min_var, width=5)
        scale_min_entry.pack(side="left")

        to_label = ttk.Label(scale_range_frame, text="to")
        to_label.pack(side="left", padx=5)

        scale_max_entry = ttk.Entry(scale_range_frame, textvariable=self.scale_max_var, width=5)
        scale_max_entry.pack(side="left")

        rotation_range_label = ttk.Label(frame, text="Sticker Rotation Range (°):")
        rotation_range_label.grid(row=3, column=0, padx=5, pady=5)

        self.rotation_min_var = tk.IntVar(value=-45)
        self.rotation_max_var = tk.IntVar(value=45)
        rotation_range_frame = ttk.Frame(frame)
        rotation_range_frame.grid(row=3, column=1, padx=5, pady=5)

        rotation_min_entry = ttk.Entry(rotation_range_frame, textvariable=self.rotation_min_var, width=5)
        rotation_min_entry.pack(side="left")

        to_label = ttk.Label(rotation_range_frame, text="to")
        to_label.pack(side="left", padx=5)

        rotation_max_entry = ttk.Entry(rotation_range_frame, textvariable=self.rotation_max_var, width=5)
        rotation_max_entry.pack(side="left")

        preview_btn = ttk.Button(frame, text="Preview Wallpaper", command=self.preview_wallpaper)
        preview_btn.grid(row=4, column=0, columnspan=2, pady=10)

        self.preview_canvas = tk.Canvas(frame, width=400, height=300, bg="gray")
        self.preview_canvas.grid(row=5, column=0, columnspan=4, pady=10)

        save_btn = ttk.Button(frame, text="Save Wallpaper", command=self.save_wallpaper)
        save_btn.grid(row=6, column=0, columnspan=2, pady=10)

        # Add tooltips
        self.add_tooltip(preview_btn, "Generate and preview the wallpaper based on current settings.")
        self.add_tooltip(save_btn, "Save the generated wallpaper to a file.")

    def init_boost_rate(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.boost_vars = []

        boost_info_label = ttk.Label(frame, text="Boost Multiplier Explanation:")
        boost_info_label.pack(anchor="w")

        boost_info_text = ("Increasing the multiplier for a sticker will increase its likelihood of appearing "
                            "more frequently on the wallpaper. A higher number means the sticker will have a "
                            "greater chance of being placed in the final wallpaper.")
        boost_info = ttk.Label(frame, text=boost_info_text, wraplength=600, justify="left")
        boost_info.pack(anchor="w", pady=5)

        for var, sticker_name in self.sticker_vars:
            boost_var = tk.DoubleVar(value=1.0)
            boost_label = ttk.Label(frame, text=f"Boost {sticker_name}:")
            boost_label.pack(anchor="w")

            boost_entry = ttk.Entry(frame, textvariable=boost_var, width=5)
            boost_entry.pack(anchor="w")

            self.boost_vars.append((boost_var, sticker_name))

    def add_tooltip(self, widget, text):
        Tooltip(widget, text)

    def preview_wallpaper(self):
        # Generating the wallpaper preview
        width = self.res_width_var.get()
        height = self.res_height_var.get()
        num_stickers = self.num_stickers_var.get()
        scale_min = self.scale_min_var.get()
        scale_max = self.scale_max_var.get()
        rotation_min = self.rotation_min_var.get()
        rotation_max = self.rotation_max_var.get()

        # Create the background image (white if no background image is selected)
        if self.background_image_path:
            bg_img = Image.open(self.background_image_path).resize((width, height))
        else:
            bg_img = Image.new('RGBA', (width, height), (255, 255, 255, 255))  # White background

        # Prepare the stickers with multipliers
        stickers = [sticker_name for var, sticker_name in self.sticker_vars if var.get()]
        if not stickers:
            messagebox.showerror("Error", "Please select at least one sticker.")
            return

        sticker_multipliers = {sticker_name: var.get() for var, sticker_name in self.boost_vars}

        # Paste the stickers onto the background
        for _ in range(num_stickers):
            sticker_name = random.choices(
                stickers,
                weights=[sticker_multipliers.get(name, 1.0) for name in stickers]
            )[0]
            sticker_img = Image.open(os.path.join(self.sticker_dir, sticker_name))

            scale = random.randint(scale_min, scale_max) / 100
            sticker_img = sticker_img.resize(
                (int(sticker_img.width * scale), int(sticker_img.height * scale))
            )

            rotation = random.randint(rotation_min, rotation_max)
            sticker_img = sticker_img.rotate(rotation, expand=True)

            # Ensure the sticker is within bounds but can overlap edges
            x = random.randint(-sticker_img.width // 2, width - sticker_img.width // 2)
            y = random.randint(-sticker_img.height // 2, height - sticker_img.height // 2)

            bg_img.paste(sticker_img, (x, y), sticker_img)

        # Paste the center image last, so it appears on top of the stickers
        if self.center_image_path:
            center_img = Image.open(self.center_image_path)
            center_img = center_img.resize(
                (int(center_img.width * self.scale_var.get() / 100), int(center_img.height * self.scale_var.get() / 100))
            )
            center_x = (width - center_img.width) // 2
            center_y = (height - center_img.height) // 2
            bg_img.paste(center_img, (center_x, center_y), center_img)

        # Save the full-resolution image
        self.full_resolution_img = bg_img

        # Scale down the image to fit within the preview canvas
        preview_width = self.preview_canvas.winfo_width()
        preview_height = self.preview_canvas.winfo_height()
        scale_ratio = min(preview_width / width, preview_height / height)
        preview_img = bg_img.resize(
            (int(width * scale_ratio), int(height * scale_ratio)), Image.LANCZOS
        )

        # Display the preview
        self.preview_img = ImageTk.PhotoImage(preview_img)
        self.preview_canvas.create_image(preview_width // 2, preview_height // 2, image=self.preview_img, anchor="center")

    def save_wallpaper(self):
        if not self.full_resolution_img:
            messagebox.showerror("Error", "No wallpaper generated to save.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if save_path:
            self.full_resolution_img.save(save_path, format="png")
            messagebox.showinfo("Success", "Wallpaper saved successfully.")

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="yellow", relief="solid", borderwidth=1, padx=5, pady=5)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

if __name__ == "__main__":
    app = WallpaperGeneratorApp()
    app.mainloop()
