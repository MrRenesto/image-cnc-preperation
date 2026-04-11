"""Main window UI for CNC Image Preparation Tool."""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
from services import ImageService


class CNCImageApp:
    """Main application window."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("CNC Image Preparation Tool")
        self.root.geometry("1000x700")
        
        # Service layer
        self.image_service = ImageService()
        
        # State variables
        self.original_image = None
        self.current_image = None
        self.display_image = None
        self.zoom_level = 1.0
        
        # Pan state
        self.is_panning = False
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create the user interface."""
        self._create_control_panel()
        self._create_display_area()
    
    def _create_control_panel(self):
        """Create left control panel."""
        control_frame = tk.Frame(self.root, width=200, bg="#f0f0f0")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Title
        title = tk.Label(control_frame, text="CNC Image Tool", 
                        font=("Arial", 16, "bold"), bg="#f0f0f0")
        title.pack(pady=20)
        
        # Action buttons
        self._create_action_buttons(control_frame)
        
        # Edge detection algorithm selector
        self._create_algorithm_selector(control_frame)
        
        # Zoom controls
        self._create_zoom_controls(control_frame)
        
        # Status label
        self.status_label = tk.Label(control_frame, text="Ready", 
                                    bg="#f0f0f0", wraplength=180)
        self.status_label.pack(side=tk.BOTTOM, pady=20)
    
    def _create_action_buttons(self, parent):
        """Create action buttons."""
        btn_load = tk.Button(parent, text="Load Image", 
                           command=self.load_image, width=20, height=2)
        btn_load.pack(pady=10)
        
        btn_bw = tk.Button(parent, text="Convert to B&W", 
                          command=self.convert_bw, width=20, height=2)
        btn_bw.pack(pady=10)
    
    def _create_algorithm_selector(self, parent):
        """Create edge detection algorithm selector."""
        algo_label = tk.Label(parent, text="Edge Detection:", 
                             font=("Arial", 10, "bold"), bg="#f0f0f0")
        algo_label.pack(pady=(10, 5))
        
        algorithms = self.image_service.get_available_algorithms()
        self.algorithm_var = tk.StringVar(value=algorithms[0] if algorithms else "Canny")
        self.algorithm_combo = ttk.Combobox(
            parent, 
            textvariable=self.algorithm_var,
            values=algorithms,
            state="readonly",
            width=18
        )
        self.algorithm_combo.pack(pady=5)
        
        btn_edges = tk.Button(parent, text="Detect Edges", 
                             command=self.detect_edges, width=20, height=2)
        btn_edges.pack(pady=10)
        
        btn_save = tk.Button(parent, text="Save PNG", 
                            command=self.save_image, width=20, height=2)
        btn_save.pack(pady=10)
    
    def _create_zoom_controls(self, parent):
        """Create zoom controls."""
        self.zoom_label = tk.Label(parent, text="Zoom: 100%", 
                                  bg="#f0f0f0", font=("Arial", 10))
        self.zoom_label.pack(pady=(30, 10))
        
        zoom_hint = tk.Label(parent, text="Use mouse wheel to zoom\nClick & drag to pan", 
                           bg="#f0f0f0", font=("Arial", 9), fg="#666666")
        zoom_hint.pack(pady=5)
        
        btn_reset = tk.Button(parent, text="Reset to Original", 
                             command=self.reset_image, width=20, height=2,
                             bg="#ffcccc")
        btn_reset.pack(pady=30)
    
    def _create_display_area(self):
        """Create image display area."""
        display_frame = tk.Frame(self.root, bg="white")
        display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(display_frame, bg="#e0e0e0")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self._bind_mouse_events()
    
    def _bind_mouse_events(self):
        """Bind mouse event handlers."""
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)
        self.canvas.bind("<ButtonPress-1>", self.on_pan_start)
        self.canvas.bind("<B1-Motion>", self.on_pan_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_pan_end)
    
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
                self.original_image = self.image_service.load_image(filepath)
                self.current_image = self.original_image.copy()
                self.display_current_image()
                filename = filepath.split('/')[-1].split('\\')[-1]
                self.update_status(f"Loaded: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
    
    def convert_bw(self):
        """Convert current image to black and white."""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        try:
            self.current_image = self.image_service.convert_to_bw(self.current_image)
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
            self.current_image = self.image_service.detect_edges(
                self.current_image, algorithm
            )
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
                self.image_service.save_image(filepath, self.current_image)
                filename = filepath.split('/')[-1].split('\\')[-1]
                self.update_status(f"Saved: {filename}")
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def on_mouse_wheel(self, event):
        """Handle mouse wheel zoom."""
        if self.current_image is None:
            return
        
        mouse_x = self.canvas.canvasx(event.x)
        mouse_y = self.canvas.canvasy(event.y)
        
        zoom_factor = 0.9 if (event.num == 5 or event.delta < 0) else 1.1
        
        old_zoom = self.zoom_level
        self.zoom_level = max(0.1, min(self.zoom_level * zoom_factor, 5.0))
        
        if self.zoom_level != old_zoom:
            self.display_current_image()
            
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
        self.canvas.config(cursor="fleur")
    
    def on_pan_move(self, event):
        """Pan the image with mouse drag."""
        if not self.is_panning or self.current_image is None:
            return
        
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
        
        pil_image = Image.fromarray(display_img)
        
        new_width = int(pil_image.width * self.zoom_level)
        new_height = int(pil_image.height * self.zoom_level)
        
        if new_width > 0 and new_height > 0:
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        self.display_image = ImageTk.PhotoImage(pil_image)
        
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.display_image)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        
        self.zoom_label.config(text=f"Zoom: {int(self.zoom_level * 100)}%")
    
    def update_status(self, message):
        """Update status label."""
        self.status_label.config(text=message)
