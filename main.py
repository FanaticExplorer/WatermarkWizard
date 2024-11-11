import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
import os
from tkinter import filedialog, messagebox
import threading
from link import Link

ctk.set_default_color_theme("dark-blue")
script_dir = os.path.dirname(os.path.abspath(__file__))


class WatermarkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Watermark Wizard")
        icon_path = os.path.join(script_dir, "icon.ico")
        self.iconbitmap(icon_path)
        self.geometry("600x700")

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)

        # Initialize variables
        self.image_path = None
        self.preview_image = None
        self.update_timer = None
        self.rotation = None
        self.opacity_label = None
        self.opacity = None
        self.font_size_label = None
        self.font_size = None
        self.watermark_text = None
        self.file_path = None
        self.rotation_label = None
        self.preview_label = None

        # Create frames
        self.create_input_frame()
        self.create_options_frame()
        self.create_preview_frame()
        self.create_action_frame()
        Link(
            self,
            text="💻Made by FanaticExplorer💻",
            link="https://bento.me/FanaticExplorer",
        ).grid(row=4, column=0, padx=10, pady=(0, 10))

    def create_input_frame(self):
        # Input Frame
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        # File selection
        ctk.CTkLabel(input_frame, text="Image:").grid(row=0, column=0, padx=10, pady=10)
        self.file_path = ctk.CTkEntry(input_frame)
        self.file_path.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(input_frame, text="Browse", command=self.browse_file).grid(
            row=0, column=2, padx=10, pady=10
        )

        # Watermark text
        ctk.CTkLabel(input_frame, text="Text:").grid(row=1, column=0, padx=10, pady=10)
        self.watermark_text = ctk.CTkEntry(input_frame)
        self.watermark_text.grid(
            row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew"
        )
        self.watermark_text.insert(0, "WATERMARK")
        self.watermark_text.bind(
            "<KeyRelease>", lambda e: self.schedule_preview_update()
        )

    def create_options_frame(self):
        # Options Frame
        options_frame = ctk.CTkFrame(self)
        options_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        options_frame.grid_columnconfigure(1, weight=1)

        # Font size
        ctk.CTkLabel(options_frame, text="Font Size:").grid(
            row=0, column=0, padx=10, pady=5
        )
        self.font_size = ctk.CTkSlider(
            options_frame, from_=8, to=72, number_of_steps=64
        )
        self.font_size.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.font_size.set(36)
        self.font_size_label = ctk.CTkLabel(options_frame, text="36")
        self.font_size_label.grid(row=0, column=2, padx=10, pady=5)
        self.font_size.configure(command=self.on_slider_change)

        # Opacity
        ctk.CTkLabel(options_frame, text="Opacity:").grid(
            row=1, column=0, padx=10, pady=5
        )
        self.opacity = ctk.CTkSlider(
            options_frame, from_=0, to=255, number_of_steps=255
        )
        self.opacity.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.opacity.set(128)
        self.opacity_label = ctk.CTkLabel(options_frame, text="128")
        self.opacity_label.grid(row=1, column=2, padx=10, pady=5)
        self.opacity.configure(command=self.on_slider_change)

        # Rotation
        ctk.CTkLabel(options_frame, text="Rotation:").grid(
            row=2, column=0, padx=10, pady=5
        )
        self.rotation = ctk.CTkSlider(
            options_frame, from_=0, to=360, number_of_steps=720
        )
        self.rotation.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.rotation.set(30)
        self.rotation_label = ctk.CTkLabel(options_frame, text="30.0°")
        self.rotation_label.grid(row=2, column=2, padx=10, pady=5)
        self.rotation.configure(command=self.on_slider_change)

    def schedule_preview_update(self):
        """Schedule a preview update with debouncing"""
        if self.update_timer is not None:
            self.after_cancel(self.update_timer)
        self.update_timer = self.after(100, self.update_preview, None)  # 100ms delay

    # noinspection PyUnusedLocal
    def on_slider_change(self, value):
        # Update labels
        self.font_size_label.configure(text=f"{int(self.font_size.get())}")
        self.opacity_label.configure(text=f"{int(self.opacity.get())}")
        self.rotation_label.configure(text=f"{self.rotation.get():.1f}°")
        # Schedule preview update
        self.schedule_preview_update()

    def create_preview_frame(self):
        # Preview Frame
        preview_frame = ctk.CTkFrame(self)
        preview_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(2, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(1, weight=1)

        # Preview Label
        ctk.CTkLabel(preview_frame, text="Preview").grid(
            row=0, column=0, padx=10, pady=5
        )
        self.preview_label = ctk.CTkLabel(preview_frame, text="No image selected")
        self.preview_label.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    def create_action_frame(self):
        # Action Frame
        action_frame = ctk.CTkFrame(self)
        action_frame.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)

        # Only Save button
        ctk.CTkButton(action_frame, text="Save", command=self.save_image).grid(
            row=0, column=0, padx=10, pady=10
        )

    def browse_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*"),
            ]
        )
        if filename:
            self.image_path = filename
            self.file_path.delete(0, ctk.END)
            self.file_path.insert(0, filename)
            self.update_preview()

    def add_watermark(self, preview=False):
        if not self.image_path:
            return None

        try:
            # Open the image
            with Image.open(self.image_path) as img:
                # Convert to RGBA if not already
                if img.mode != "RGBA":
                    img = img.convert("RGBA")

                # Create watermark layer
                padding_factor = 0.5
                new_size = (
                    int(img.size[0] * (1 + padding_factor)),
                    int(img.size[1] * (1 + padding_factor)),
                )
                watermark = Image.new("RGBA", new_size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(watermark)

                # Try to use Arial font, fall back to default if not available
                try:
                    font = ImageFont.truetype("arial.ttf", int(self.font_size.get()))
                except (OSError, ValueError):
                    font = ImageFont.load_default()

                # Get text size
                text = self.watermark_text.get() or "Watermark"
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                # Calculate spacing
                x_spacing = text_width * 1.2
                y_spacing = text_height * 4.5

                # Calculate grid
                num_cols = int(new_size[0] / x_spacing) + 4
                num_rows = int(new_size[1] / y_spacing) + 4

                # Draw watermark pattern
                start_x = -text_width
                start_y = -text_height * 2
                opacity = int(self.opacity.get())

                for row in range(num_rows):
                    x_offset = (row % 2) * (x_spacing / 2)
                    for col in range(num_cols):
                        x = start_x + x_offset + col * x_spacing
                        y = start_y + row * y_spacing
                        draw.text(
                            (x, y), text, font=font, fill=(255, 255, 255, opacity)
                        )

                # Rotate watermark
                rotation = float(self.rotation.get())
                if rotation:
                    watermark = watermark.rotate(rotation, expand=False)

                # Crop watermark
                left_offset = int(img.size[0] * padding_factor / 2)
                top_offset = int(img.size[1] * padding_factor / 2)
                watermark = watermark.crop(
                    (
                        left_offset,
                        top_offset,
                        left_offset + img.size[0],
                        top_offset + img.size[1],
                    )
                )

                # Combine images
                watermarked = Image.alpha_composite(img, watermark)

                if preview:
                    # Resize for preview
                    preview_size = (300, 300)
                    watermarked.thumbnail(preview_size, Image.Resampling.LANCZOS)

                return watermarked

        except Exception as e:
            messagebox.showerror("Error", f"Error processing image: {str(e)}")
            return None

    # noinspection PyUnusedLocal
    def update_preview(self, *args):
        if not self.image_path:
            return

        preview_image = self.add_watermark(preview=True)
        if preview_image:
            # Convert to PhotoImage
            photo = ctk.CTkImage(preview_image, size=preview_image.size)
            self.preview_label.configure(image=photo, text="")
            # Keep a reference
            self.preview_image = photo

    def save_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first!")
            return

        # Get save path
        file_name, file_ext = os.path.splitext(self.image_path)
        initial_file = f"{file_name}_watermarked"
        save_path = filedialog.asksaveasfilename(
            initialfile=os.path.basename(initial_file),
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        )

        if save_path:
            # Process in a thread to prevent UI freezing
            def save_thread():
                watermarked = self.add_watermark(preview=False)
                if watermarked:
                    try:
                        watermarked.save(save_path, "PNG")
                        messagebox.showinfo("Success", "Image saved successfully!")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error saving image: {str(e)}")

            threading.Thread(target=save_thread, daemon=True).start()


if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()
