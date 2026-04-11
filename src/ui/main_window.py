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
        
        # ROI selection state
        self.selection_mode = False
        self.roi_start_canvas = None
        self.roi_end_canvas = None
        self.selected_roi_image = None
        
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
        
        btn_select_roi = tk.Button(parent, text="Select Object (ROI)", 
                                  command=self.enable_roi_selection, width=20, height=2)
        btn_select_roi.pack(pady=(10, 5))
        
        btn_clear_roi = tk.Button(parent, text="Clear Selection", 
                                 command=self.clear_roi_selection, width=20, height=2)
        btn_clear_roi.pack(pady=(5, 10))
        
        btn_line_art = tk.Button(parent, text="Generate Line Art", 
                                command=self.generate_line_art, width=20, height=2)
        btn_line_art.pack(pady=(5, 10))
        
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
                self.selection_mode = False
                self.selected_roi_image = None
                self.roi_start_canvas = None
                self.roi_end_canvas = None
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
            self.selected_roi_image = None
            self.selection_mode = False
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
            self.selected_roi_image = None
            self.selection_mode = False
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
        self.selection_mode = False
        self.selected_roi_image = None
        self.roi_start_canvas = None
        self.roi_end_canvas = None
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
        
        if self.selection_mode:
            self.roi_start_canvas = (
                self.canvas.canvasx(event.x),
                self.canvas.canvasy(event.y),
            )
            self.roi_end_canvas = self.roi_start_canvas
            self.display_current_image()
            return
        
        self.is_panning = True
        self.canvas.scan_mark(event.x, event.y)
        self.canvas.config(cursor="fleur")
    
    def on_pan_move(self, event):
        """Pan the image with mouse drag."""
        if self.current_image is None:
            return
        
        if self.selection_mode and self.roi_start_canvas is not None:
            self.roi_end_canvas = (
                self.canvas.canvasx(event.x),
                self.canvas.canvasy(event.y),
            )
            self.display_current_image()
            return
        
        if not self.is_panning:
            return
        
        self.canvas.scan_dragto(event.x, event.y, gain=1)
    
    def on_pan_end(self, event):
        """End panning."""
        if self.current_image is None:
            return
        
        if self.selection_mode and self.roi_start_canvas is not None and self.roi_end_canvas is not None:
            x1, y1 = self._canvas_to_image_coords(*self.roi_start_canvas)
            x2, y2 = self._canvas_to_image_coords(*self.roi_end_canvas)
            x1, x2 = sorted((x1, x2))
            y1, y2 = sorted((y1, y2))
            
            if (x2 - x1) < 2 or (y2 - y1) < 2:
                self.roi_start_canvas = None
                self.roi_end_canvas = None
                self.selected_roi_image = None
                self.display_current_image()
                self.update_status("Selection too small. Drag a larger ROI.")
                return
            
            self.selected_roi_image = (x1, y1, x2, y2)
            self.selection_mode = False
            self.roi_start_canvas = None
            self.roi_end_canvas = None
            self.display_current_image()
            self.update_status(f"ROI selected: {x2 - x1}x{y2 - y1}")
            return
        
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
        self._draw_roi_overlay()
        
        self.zoom_label.config(text=f"Zoom: {int(self.zoom_level * 100)}%")
    
    def update_status(self, message):
        """Update status label."""
        self.status_label.config(text=message)
    
    def enable_roi_selection(self):
        """Enable rectangle selection mode for object ROI."""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load and process an image first!")
            return
        
        self.selection_mode = True
        self.roi_start_canvas = None
        self.roi_end_canvas = None
        self.update_status("Selection mode active: drag on image to select object ROI.")
    
    def clear_roi_selection(self):
        """Clear selected ROI and selection mode."""
        self.selection_mode = False
        self.roi_start_canvas = None
        self.roi_end_canvas = None
        self.selected_roi_image = None
        self.display_current_image()
        self.update_status("ROI selection cleared.")
    
    def generate_line_art(self):
        """Generate contour-based line art for selected ROI."""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
        
        if self.selected_roi_image is None:
            messagebox.showwarning("Warning", "Please select an object ROI first!")
            return
        
        try:
            self.current_image, metadata = self.image_service.generate_line_art_from_roi(
                self.current_image,
                self.selected_roi_image,
                min_contour_area=20.0,
                line_thickness=1,
                use_morphology=True,
            )
            kept = metadata.get("contours_kept", 0)
            self.display_current_image()
            self.update_status(f"Generated line art from ROI (contours kept: {kept})")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate line art: {str(e)}")
    
    def _canvas_to_image_coords(self, canvas_x, canvas_y):
        """Convert canvas coordinates to image coordinates with zoom applied."""
        img_h, img_w = self.current_image.shape[:2]
        x = int(canvas_x / self.zoom_level)
        y = int(canvas_y / self.zoom_level)
        x = max(0, min(x, img_w - 1))
        y = max(0, min(y, img_h - 1))
        return x, y
    
    def _draw_roi_overlay(self):
        """Draw active or finalized ROI overlay on canvas."""
        if self.roi_start_canvas is not None and self.roi_end_canvas is not None:
            x1, y1 = self.roi_start_canvas
            x2, y2 = self.roi_end_canvas
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="#ff3333", width=2, dash=(6, 3))
        
        if self.selected_roi_image is not None:
            x1, y1, x2, y2 = self.selected_roi_image
            self.canvas.create_rectangle(
                x1 * self.zoom_level,
                y1 * self.zoom_level,
                x2 * self.zoom_level,
                y2 * self.zoom_level,
                outline="#33aa33",
                width=2,
            )
