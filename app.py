import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Impostazione tema grafico
ctk.set_appearance_mode("System")  # Segue il tema di Windows (Chiaro/Scuro)
ctk.set_default_color_theme("blue")

class VideoMergeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Video Merger Pro")
        self.geometry("600x450")
        self.resizable(False, False)
        
        self.video_paths = []
        
        # --- UI ELEMENTS ---
        self.title_label = ctk.CTkLabel(self, text="Seleziona i video da unire", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)
        
        # Lista dei file selezionati
        self.textbox = ctk.CTkTextbox(self, width=500, height=200, state="disabled")
        self.textbox.pack(pady=10)
        
        # Contenitore Pulsanti
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=15)
        
        self.add_btn = ctk.CTkButton(self.btn_frame, text="Aggiungi Video", command=self.add_videos)
        self.add_btn.grid(row=0, column=0, padx=10)
        
        self.clear_btn = ctk.CTkButton(self.btn_frame, text="Svuota Lista", fg_color="dark-red", hover_color="red", command=self.clear_list)
        self.clear_btn.grid(row=0, column=1, padx=10)
        
        self.merge_btn = ctk.CTkButton(self, text="Unisci ed Esporta Video", size=(200, 40), fg_color="green", hover_color="darkgreen", command=self.merge_videos)
        self.merge_btn.pack(pady=10)
        
        # Barra di stato
        self.status_label = ctk.CTkLabel(self, text="Pronto", font=ctk.CTkFont(size=12))
        self.status_label.pack(side="bottom", pady=10)

    def update_textbox(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        if not self.video_paths:
            self.textbox.insert("end", "Nessun video selezionato...")
        else:
            for i, path in enumerate(self.video_paths, 1):
                self.textbox.insert("end", f"{i}. {os.path.basename(path)}\n")
        self.textbox.configure(state="disabled")

    def add_videos(self):
        files = filedialog.askopenfilenames(
            title="Seleziona file video",
            filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov")]
        )
        if files:
            self.video_paths.extend(files)
            self.update_textbox()

    def clear_list(self):
        self.video_paths.clear()
        self.update_textbox()

    def merge_videos(self):
        if len(self.video_paths) < 2:
            messagebox.showwarning("Attenzione", "Seleziona almeno 2 video da unire.")
            return
            
        output_path = filedialog.asksaveasfilename(
            title="Salva video unito",
            defaultextension=".mp4",
            filetypes=[("MP4 Video", "*.mp4")]
        )
        
        if not output_path:
            return
            
        self.status_label.configure(text="Elaborazione in corso... Attendi.")
        self.update()
        
        try:
            clips = []
            # Carica le clip
            for path in self.video_paths:
                clips.append(VideoFileClip(path))
                
            # Esegue il merge
            final_clip = concatenate_videoclips(clips, method="compose")
            
            # Esporta il file finale (usa libx264 per massima compatibilità)
            final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            
            # Chiude le clip per liberare la memoria
            for clip in clips:
                clip.close()
            final_clip.close()
            
            self.status_label.configure(text="Completato con successo!")
            messagebox.showinfo("Successo", "Video unito ed esportato correttamente!")
            
        except Exception as e:
            self.status_label.configure(text="Errore durante il merge.")
            messagebox.showerror("Errore", f"Si è verificato un errore:\n{str(e)}")

if __name__ == "__main__":
    app = VideoMergeApp()
    app.update_textbox()
    app.mainloop()