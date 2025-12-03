import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import requests
from main import (
    download_soundcloud_thumbnails,
    copy_custom_images,
    add_text_to_images,
    clear_directory,
    open_directory,
    printd
)

class SoundCloudTierMakerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SoundCloud Tier Maker")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        # Main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Title
        title = ttk.Label(main_frame, text="SoundCloud Tier Maker", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # SoundCloud URL
        ttk.Label(main_frame, text="SoundCloud Profile URL:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Font Size
        ttk.Label(main_frame, text="Font Size:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.font_size_var = tk.IntVar(value=36)
        font_size_spinbox = ttk.Spinbox(main_frame, from_=8, to=72, textvariable=self.font_size_var, width=10)
        font_size_spinbox.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Text Position
        self.top_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="Place text on top (default: bottom)", variable=self.top_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Use Temp
        self.use_temp_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="Use existing temporary directory (skip download)", variable=self.use_temp_var).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Custom Images
        ttk.Label(main_frame, text="Custom Images:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.custom_images_listbox = tk.Listbox(main_frame, height=5, width=60)
        self.custom_images_listbox.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.custom_images_listbox.yview)
        scrollbar.grid(row=6, column=2, sticky=(tk.N, tk.S))
        self.custom_images_listbox.config(yscrollcommand=scrollbar.set)
        
        # Buttons for custom images
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(button_frame, text="Add Images", command=self.add_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_images).pack(side=tk.LEFT, padx=5)
        
        # Status
        ttk.Label(main_frame, text="Status:").grid(row=8, column=0, sticky=tk.W, pady=(10, 5))
        self.status_text = tk.Text(main_frame, height=8, width=70, state=tk.DISABLED)
        self.status_text.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        scrollbar_status = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        scrollbar_status.grid(row=9, column=2, sticky=(tk.N, tk.S))
        self.status_text.config(yscrollcommand=scrollbar_status.set)
        
        # Action Buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Button(action_frame, text="Process", command=self.process).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Open Output", command=self.open_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Exit", command=root.quit).pack(side=tk.LEFT, padx=5)
        
        # Configure column weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(9, weight=1)
        
        self.custom_images = []
    
    def log_status(self, message):
        """Add message to status text box."""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()
    
    def add_images(self):
        """Open file dialog to select images."""
        files = filedialog.askopenfilenames(
            filetypes=[("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")]
        )
        for file in files:
            if file not in self.custom_images:
                self.custom_images.append(file)
                self.custom_images_listbox.insert(tk.END, file)
        if files:
            self.log_status(f"Added {len(files)} image(s)")
    
    def remove_image(self):
        """Remove selected image from list."""
        selection = self.custom_images_listbox.curselection()
        if selection:
            index = selection[0]
            self.custom_images_listbox.delete(index)
            self.custom_images.pop(index)
            self.log_status("Image removed")
    
    def clear_images(self):
        """Clear all custom images."""
        self.custom_images.clear()
        self.custom_images_listbox.delete(0, tk.END)
        self.log_status("All images cleared")
    
    def open_output(self):
        """Open output directory."""
        try:
            open_directory("output")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open output directory: {e}")
    
    def process(self):
        """Process with threading to prevent UI freeze."""
        if not self.url_entry.get().strip():
            messagebox.showwarning("Input Error", "Please enter a SoundCloud profile URL")
            return
        
        thread = threading.Thread(target=self._process_thread, daemon=True)
        thread.start()
    
    def _process_thread(self):
        """Background processing thread."""
        try:
            profile_url = self.url_entry.get().strip()
            
            # Normalize URL
            if not profile_url.startswith("https://"):
                if profile_url.startswith("soundcloud.com/"):
                    profile_url = "https://" + profile_url
                else:
                    profile_url = "https://soundcloud.com/" + profile_url
            font_size = self.font_size_var.get()
            
            try:
                response = requests.head(profile_url, allow_redirects=True, timeout=5)
                if response.status_code == 404:
                    messagebox.showerror("Invalid URL", "SoundCloud profile URL returned 404 - please check the URL")
                    return
            except requests.RequestException as e:
                messagebox.showerror("Connection Error", f"Failed to validate URL (passing): {e}")
                pass
            
            self.log_status("Starting process...")
            
            # Clear/download
            if not self.use_temp_var.get():
                self.log_status("Clearing temporary directory...")
                clear_directory("temp")
                self.log_status("Downloading thumbnails...")
                download_soundcloud_thumbnails(profile_url)
            else:
                self.log_status("Using existing temporary directory...")
            
            # Copy custom images
            if self.custom_images:
                self.log_status(f"Copying {len(self.custom_images)} custom image(s)...")
                copy_custom_images(self.custom_images)
            
            # Clear output
            self.log_status("Clearing output directory...")
            clear_directory("output")
            
            # Add text
            self.log_status("Processing images with text...")
            add_text_to_images(top=self.top_var.get(), font_size=font_size)
            
            self.log_status("✅ Process completed successfully!")
            messagebox.showinfo("Success", "Tier maker processing completed!")
        
        except Exception as e:
            self.log_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = SoundCloudTierMakerGUI(root)
    root.mainloop()
