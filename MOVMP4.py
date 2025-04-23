import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path

# *** SET THIS PATH TO YOUR FFMPEG LOCATION ***
FFMPEG_PATH = r"C:\ffmpeg\ffmpeg-2025-04-21-git-9e1162bdf1-full_build\bin\ffmpeg.exe"
# If you need to manually specify ffprobe as well:
FFPROBE_PATH = r"C:\ffmpeg\ffmpeg-2025-04-21-git-9e1162bdf1-full_build\bin\ffprobe.exe"

class VideoConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("MOV to MP4 Converter")
        self.root.geometry("600x450")
        self.root.configure(padx=20, pady=20)
        self.root.resizable(True, True)
        
        # Check if FFmpeg paths exist
        self.ffmpeg_exists = os.path.exists(FFMPEG_PATH)
        self.ffprobe_exists = os.path.exists(FFPROBE_PATH)
        
        # Styling
        self.style = ttk.Style()
        self.style.configure("TButton", padding=10, font=('Helvetica', 10))
        self.style.configure("TLabel", font=('Helvetica', 11))
        self.style.configure("Header.TLabel", font=('Helvetica', 14, 'bold'))
        self.style.configure("Success.TLabel", foreground="green", font=('Helvetica', 11))
        self.style.configure("Error.TLabel", foreground="red", font=('Helvetica', 11))
        
        # Main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = ttk.Label(main_frame, text="MOV to MP4 Converter", style="Header.TLabel")
        header_label.pack(pady=(0, 20))
        
        # FFmpeg status
        ffmpeg_status_frame = ttk.Frame(main_frame)
        ffmpeg_status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ffmpeg_status = "Found" if self.ffmpeg_exists else "Not Found"
        ffmpeg_style = "Success.TLabel" if self.ffmpeg_exists else "Error.TLabel"
        
        ttk.Label(ffmpeg_status_frame, text=f"FFmpeg Status: {ffmpeg_status}", style=ffmpeg_style).pack(anchor=tk.W)
        ttk.Label(ffmpeg_status_frame, text=f"Path: {FFMPEG_PATH}").pack(anchor=tk.W)
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="File Selection")
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Input file
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        ttk.Label(input_frame, text="Input MOV file:").pack(side=tk.LEFT)
        
        self.input_path_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.input_path_var, width=50)
        input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        browse_input_btn = ttk.Button(input_frame, text="Browse", command=self.browse_input_file)
        browse_input_btn.pack(side=tk.LEFT, padx=(0, 0))
        
        # Output file
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        
        ttk.Label(output_frame, text="Output MP4 file:").pack(side=tk.LEFT)
        
        self.output_path_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path_var, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        browse_output_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output_file)
        browse_output_btn.pack(side=tk.LEFT, padx=(0, 0))
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Conversion Options")
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Quality option
        quality_frame = ttk.Frame(options_frame)
        quality_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(quality_frame, text="Quality:").pack(side=tk.LEFT)
        
        self.quality_var = tk.StringVar(value="high")
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.quality_var, 
                                     values=["low", "medium", "high", "original"],
                                     width=10, state="readonly")
        quality_combo.pack(side=tk.LEFT, padx=(5, 0))
        
        # Progress frame
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(self.progress_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=(20, 10))
        
        self.convert_btn = ttk.Button(buttons_frame, text="Convert", command=self.start_conversion)
        self.convert_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.cancel_btn = ttk.Button(buttons_frame, text="Cancel", command=self.cancel_conversion, state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Disable convert button if FFmpeg is not found
        if not self.ffmpeg_exists:
            self.convert_btn.config(state=tk.DISABLED)
            self.status_var.set("FFmpeg not found. Please check the path at the top of the script.")
        
        # Status variables
        self.conversion_active = False
        self.ffmpeg_process = None
    
    def browse_input_file(self):
        """Open file dialog to select input MOV file."""
        filepath = filedialog.askopenfilename(
            title="Select MOV file",
            filetypes=[("MOV files", "*.mov"), ("All files", "*.*")]
        )
        if filepath:
            self.input_path_var.set(filepath)
            # Auto-set output path
            input_path = Path(filepath)
            default_output = input_path.with_suffix('.mp4')
            self.output_path_var.set(str(default_output))
    
    def browse_output_file(self):
        """Open file dialog to select output MP4 file location."""
        filepath = filedialog.asksaveasfilename(
            title="Save MP4 file as",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if filepath:
            self.output_path_var.set(filepath)
    
    def start_conversion(self):
        """Start the conversion process in a separate thread."""
        if not self.ffmpeg_exists:
            messagebox.showerror("Error", f"FFmpeg not found at path: {FFMPEG_PATH}")
            return
            
        input_path = self.input_path_var.get().strip()
        output_path = self.output_path_var.get().strip()
        
        # Validation
        if not input_path:
            messagebox.showerror("Error", "Please select an input MOV file.")
            return
        
        if not output_path:
            messagebox.showerror("Error", "Please specify an output MP4 file location.")
            return
        
        if not os.path.exists(input_path):
            messagebox.showerror("Error", "Input file does not exist.")
            return
        
        if os.path.exists(output_path):
            if not messagebox.askyesno("Warning", "Output file already exists. Do you want to overwrite it?"):
                return
        
        # Update UI state
        self.conversion_active = True
        self.convert_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        self.status_var.set("Starting conversion...")
        
        # Start conversion in a separate thread
        conversion_thread = threading.Thread(target=self.convert_video, args=(input_path, output_path))
        conversion_thread.daemon = True
        conversion_thread.start()
    
    def convert_video(self, input_path, output_path):
        """Convert MOV to MP4 using FFmpeg."""
        try:
            # Determine quality settings
            quality = self.quality_var.get()
            
            if quality == "low":
                crf = "28"
                preset = "veryfast"
            elif quality == "medium":
                crf = "23"
                preset = "medium"
            elif quality == "high":
                crf = "18"
                preset = "slow"
            else:  # original
                crf = "0"
                preset = "medium"
            
            # Build FFmpeg command using the direct path
            cmd = [
                FFMPEG_PATH,
                "-i", input_path,
                "-c:v", "libx264",
                "-crf", crf,
                "-preset", preset,
                "-c:a", "aac",
                "-b:a", "192k",
                "-y",  # Overwrite output file
                output_path
            ]
            
            # Print the command being executed (for debugging)
            print("Executing command:", " ".join(cmd))
            
            # Run FFmpeg process with progress monitoring
            self.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Get input file duration for progress calculation
            total_duration = 100  # Default fallback duration
            
            if self.ffprobe_exists:
                try:
                    duration_cmd = [
                        FFPROBE_PATH, 
                        "-v", "error", 
                        "-show_entries", "format=duration", 
                        "-of", "default=noprint_wrappers=1:nokey=1", 
                        input_path
                    ]
                    
                    print("Executing probe command:", " ".join(duration_cmd))
                    
                    duration_output = subprocess.check_output(
                        duration_cmd, 
                        universal_newlines=True,
                        stderr=subprocess.STDOUT
                    )
                    
                    if duration_output.strip():
                        total_duration = float(duration_output.strip())
                        print(f"Video duration: {total_duration} seconds")
                except Exception as e:
                    print(f"Error getting duration: {e}")
            
            # Monitor progress
            for line in self.ffmpeg_process.stdout:
                if not self.conversion_active:
                    break
                
                # For debugging - print FFmpeg output
                print(line.strip())
                
                # Update status based on FFmpeg output
                self.root.after(0, lambda l=line: self.status_var.set(f"Converting: {l.strip()}"))
                
                # Try to parse time info for progress bar
                if "time=" in line:
                    try:
                        time_parts = line.split("time=")[1].split()[0].split(":")
                        if len(time_parts) == 3:
                            hours, minutes, seconds = time_parts
                            current_time = float(hours) * 3600 + float(minutes) * 60 + float(seconds)
                            progress = min(100, (current_time / total_duration) * 100)
                            self.root.after(0, lambda p=progress: self.progress_var.set(p))
                    except Exception as e:
                        print(f"Error parsing progress: {e}")
            
            # Check if process was canceled or completed successfully
            if self.conversion_active:
                return_code = self.ffmpeg_process.wait()
                if return_code == 0:
                    self.root.after(0, lambda: self.status_var.set("Conversion completed successfully!"))
                    self.root.after(0, lambda: self.progress_var.set(100))
                    self.root.after(0, lambda: messagebox.showinfo("Success", "Video converted successfully!"))
                else:
                    error_msg = f"Conversion failed with error code {return_code}"
                    self.root.after(0, lambda: self.status_var.set(f"Error: {error_msg}"))
                    self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
            
        except Exception as e:
            error_msg = str(e)
            print(f"Conversion error: {error_msg}")
            self.root.after(0, lambda: self.status_var.set(f"Error: {error_msg}"))
            self.root.after(0, lambda: messagebox.showerror("Error", f"Conversion failed: {error_msg}"))
        
        finally:
            # Reset UI state
            self.conversion_active = False
            self.ffmpeg_process = None
            self.root.after(0, lambda: self.convert_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.cancel_btn.config(state=tk.DISABLED))
    
    def cancel_conversion(self):
        """Cancel the active conversion process."""
        if self.conversion_active and self.ffmpeg_process:
            self.conversion_active = False
            try:
                # Terminate FFmpeg process
                self.ffmpeg_process.terminate()
                self.status_var.set("Conversion canceled.")
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverter(root)
    root.mainloop()