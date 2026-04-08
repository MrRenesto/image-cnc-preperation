import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from image_processor import load_image, convert_to_bw, detect_edges_canny


class CNCImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CNC Image Preparation Tool")
        self.root.geometry("1000x700")
        
        # State variables
        self.original_image = None
        self.current_image = None
        self.display_image = None
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        # Control panel (left side)
        control_frame = tk.Frame(self.root, width=200, bg="#f0f0f0")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Title
        title = tk.Label(control_frame, text="CNC Image Tool", 
                        font=("Arial", 16, "bold"), bg="#f0f0f0")
        title.pack(pady=20)
        
        # Buttons
        btn_load = tk.Button(control_frame, text="Load Image", 
                           command=self.load_image, width=20, height=2)
        btn_load.pack(pady=10)
        
        btn_bw = tk.Button(control_frame, text="Convert to B&W", 
                          command=self.convert_bw, width=20, height=2)
        btn_bw.pack(pady=10)
        
        btn_edges = tk.Button(control_frame, text="Detect Edges", 
                             command=self.detect_edges, width=20, height=2)
        btn_edges.pack(pady=10)
        
        btn_save = tk.Button(control_frame, text="Save PNG", 
                            command=self.save_image, width=20, height=2)
        btn_save.pack(pady=10)
        
        # Reset button
        btn_reset = tk.Button(control_frame, text="Reset to Original", 
                             command=self.reset_image, width=20, height=2,
                             bg="#ffcccc")
        btn_reset.pack(pady=30)
        
        # Status label
        self.status_label = tk.Label(control_frame, text="Ready", 
                                    bg="#f0f0f0", wraplength=180)
        self.status_label.pack(side=tk.BOTTOM, pady=20)
        
        # Image display area (right side)
        display_frame = tk.Frame(self.root, bg="white")
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas for image display
        self.canvas = tk.Canvas(display_frame, bg="#e0e0e0")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbars
        h_scrollbar = tk.Scrollbar(display_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        v_scrollbar = tk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
    def load_image(self):
        """Load an image file."""
        filepath = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if filepath:
            try:
                self.original_image = load_image(filepath)
                self.current_image = self.original_image.copy()
                self.display_current_image()
                self.update_status(f"Loaded: {filepath.split('/')[-1]}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def convert_bw(self):
        """Convert current image to black and white."""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        try:
            self.current_image = convert_to_bw(self.current_image)
            self.display_current_image()
            self.update_status("Converted to B&W")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert: {str(e)}")
    
    def detect_edges(self):
        """Apply Canny edge detection."""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        try:
            self.current_image = detect_edges_canny(self.current_image)
            self.display_current_image()
            self.update_status("Applied edge detection")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect edges: {str(e)}")
    
    def reset_image(self):
        """Reset to original image."""
        if self.original_image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        
        self.current_image = self.original_image.copy()
        self.display_current_image()
        self.update_status("Reset to original")
    
    def save_image(self):
        """Save current image as PNG."""
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if filepath:
            try:
                cv2.imwrite(filepath, self.current_image)
                self.update_status(f"Saved: {filepath.split('/')[-1]}")
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def display_current_image(self):
        """Display the current image on canvas."""
        if self.current_image is None:
            return
        
        # Convert from OpenCV BGR to RGB
        if len(self.current_image.shape) == 3:
            display_img = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        else:
            display_img = self.current_image
        
        # Convert to PIL Image
        pil_image = Image.fromarray(display_img)
        
        # Resize if too large (max 800x600)
        max_width, max_height = 800, 600
        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.display_image = ImageTk.PhotoImage(pil_image)
        
        # Display on canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
    
    def update_status(self, message):
        """Update status label."""
        self.status_label.config(text=message)


def main():
    root = tk.Tk()
    app = CNCImageApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
