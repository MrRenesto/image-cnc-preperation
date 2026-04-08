import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from image_processor import (
    load_image, convert_to_bw, 
    detect_edges_canny, detect_edges_sobel, detect_edges_laplacian,
    detect_edges_prewitt, detect_edges_scharr, detect_edges_contour
)


class CNCImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CNC Image Preparation Tool")
        self.root.geometry("1000x700")
        
        # State variables
        self.original_image = None
        self.current_image = None
        self.display_image = None
        self.zoom_level = 1.0  # 1.0 = 100%, 0.5 = 50%, 2.0 = 200%
        
        # Pan state
        self.pan_start_x = 0
        self.pan_start_y = 0
        self.is_panning = False
        
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
        
        # Edge detection algorithm selector
        algo_label = tk.Label(control_frame, text="Edge Detection:", 
                             font=("Arial", 10, "bold"), bg="#f0f0f0")
        algo_label.pack(pady=(10, 5))
        
        self.algorithm_var = tk.StringVar(value="Canny")
        self.algorithm_combo = ttk.Combobox(
            control_frame, 
            textvariable=self.algorithm_var,
            values=["Canny", "Sobel", "Laplacian", "Prewitt", "Scharr", "Contour"],
            state="readonly",
            width=18
        )
        self.algorithm_combo.pack(pady=5)
        
        btn_edges = tk.Button(control_frame, text="Detect Edges", 
                             command=self.detect_edges, width=20, height=2)
        btn_edges.pack(pady=10)
        
        btn_save = tk.Button(control_frame, text="Save PNG", 
                            command=self.save_image, width=20, height=2)
        btn_save.pack(pady=10)
        
        # Zoom level indicator
        self.zoom_label = tk.Label(control_frame, text="Zoom: 100%", 
                                  bg="#f0f0f0", font=("Arial", 10))
        self.zoom_label.pack(pady=(30, 10))
        
        zoom_hint = tk.Label(control_frame, text="Use mouse wheel to zoom\nClick & drag to pan", 
                           bg="#f0f0f0", font=("Arial", 9), fg="#666666")
        zoom_hint.pack(pady=5)
        
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
        
        # Bind mouse events
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)  # Windows/Mac
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)    # Linux scroll up
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)    # Linux scroll down
        self.canvas.bind("<ButtonPress-1>", self.on_pan_start)
        self.canvas.bind("<B1-Motion>", self.on_pan_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_pan_end)
        
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
        """Apply selected edge detection algorithm."""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        try:
            algorithm = self.algorithm_var.get()
            
            # Apply the selected algorithm
            if algorithm == "Canny":
                self.current_image = detect_edges_canny(self.current_image)
            elif algorithm == "Sobel":
                self.current_image = detect_edges_sobel(self.current_image)
            elif algorithm == "Laplacian":
                self.current_image = detect_edges_laplacian(self.current_image)
            elif algorithm == "Prewitt":
                self.current_image = detect_edges_prewitt(self.current_image)
            elif algorithm == "Scharr":
                self.current_image = detect_edges_scharr(self.current_image)
            elif algorithm == "Contour":
                self.current_image = detect_edges_contour(self.current_image)
            
            self.display_current_image()
            self.update_status(f"Applied {algorithm} edge detection")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect edges: {str(e)}")
    
    def reset_image(self):
        """Reset to original image."""
        if self.original_image is None:
            messagebox.showwarning("Warning", "No image loaded!")
            return
        
        self.current_image = self.original_image.copy()
        self.zoom_level = 1.0
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
    
    def on_mouse_wheel(self, event):
        """Handle mouse wheel zoom."""
        if self.current_image is None:
            return
        
        # Get mouse position on canvas
        mouse_x = self.canvas.canvasx(event.x)
        mouse_y = self.canvas.canvasy(event.y)
        
        # Determine zoom direction
        if event.num == 5 or event.delta < 0:  # Scroll down
            zoom_factor = 0.9
        else:  # Scroll up
            zoom_factor = 1.1
        
        # Calculate new zoom level
        old_zoom = self.zoom_level
        self.zoom_level = max(0.1, min(self.zoom_level * zoom_factor, 5.0))
        
        # Only update if zoom changed
        if self.zoom_level != old_zoom:
            self.display_current_image()
            
            # Adjust scroll position to zoom toward mouse cursor
            if self.zoom_level > old_zoom:
                scale = self.zoom_level / old_zoom
                new_x = mouse_x * scale - event.x
                new_y = mouse_y * scale - event.y
                self.canvas.xview_moveto(new_x / (self.canvas.winfo_width() * scale))
                self.canvas.yview_moveto(new_y / (self.canvas.winfo_height() * scale))
    
    def on_pan_start(self, event):
        """Start panning with mouse."""
        if self.current_image is None:
            return
        
        self.is_panning = True
        self.canvas.scan_mark(event.x, event.y)
        self.canvas.config(cursor="fleur")  # Change cursor to move icon
    
    def on_pan_move(self, event):
        """Pan the image with mouse drag."""
        if not self.is_panning or self.current_image is None:
            return
        
        # Scroll the canvas based on drag
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    def on_pan_end(self, event):
        """End panning."""
        self.is_panning = False
        self.canvas.config(cursor="")
    
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
        
        # Apply zoom level
        new_width = int(pil_image.width * self.zoom_level)
        new_height = int(pil_image.height * self.zoom_level)
        
        # Only resize if dimensions are reasonable
        if new_width > 0 and new_height > 0:
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage
        self.display_image = ImageTk.PhotoImage(pil_image)
        
        # Display on canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        
        # Update zoom label
        self.zoom_label.config(text=f"Zoom: {int(self.zoom_level * 100)}%")
    
    def update_status(self, message):
        """Update status label."""
        self.status_label.config(text=message)


def main():
    root = tk.Tk()
    app = CNCImageApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
