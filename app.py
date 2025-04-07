import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import rarfile
import os
import threading
import time

def compresser_zip():
    dossier = filedialog.askdirectory(title="Choisir le dossier à compresser")
    if not dossier:
        return

    nom_zip = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Fichiers ZIP", "*.zip")])
    if not nom_zip:
        return

    def run_zip():
        fichiers = []
        for root, _, files in os.walk(dossier):
            for file in files:
                fichiers.append(os.path.join(root, file))

        total = len(fichiers)
        if total == 0:
            messagebox.showwarning("Vide", "Aucun fichier à compresser.")
            return

        progress["maximum"] = total
        progress["value"] = 0

        with zipfile.ZipFile(nom_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i, chemin_complet in enumerate(fichiers):
                chemin_relatif = os.path.relpath(chemin_complet, dossier)
                zipf.write(chemin_complet, arcname=chemin_relatif)
                progress["value"] = i + 1
                time.sleep(0.01)  # Pour voir la progression

        messagebox.showinfo("Succès", f"Dossier compressé dans :\n{nom_zip}")
        progress["value"] = 0

    threading.Thread(target=run_zip).start()

def decompresser():
    fichier = filedialog.askopenfilename(title="Choisir un fichier à décompresser", filetypes=[("Fichiers ZIP/RAR", "*.zip *.rar")])
    if not fichier:
        return

    dossier_sortie = filedialog.askdirectory(title="Choisir le dossier de destination")
    if not dossier_sortie:
        return

    def run_extract():
        try:
            progress["value"] = 0
            if fichier.endswith(".zip"):
                with zipfile.ZipFile(fichier, 'r') as zipf:
                    liste = zipf.namelist()
                    progress["maximum"] = len(liste)
                    for i, name in enumerate(liste):
                        zipf.extract(name, dossier_sortie)
                        progress["value"] = i + 1
                        time.sleep(0.01)
            elif fichier.endswith(".rar"):
                with rarfile.RarFile(fichier) as rf:
                    liste = rf.namelist()
                    progress["maximum"] = len(liste)
                    for i, name in enumerate(liste):
                        rf.extract(name, path=dossier_sortie)
                        progress["value"] = i + 1
                        time.sleep(0.01)
            else:
                messagebox.showerror("Erreur", "Format non supporté.")
                return

            messagebox.showinfo("Succès", f"Fichier décompressé dans :\n{dossier_sortie}")
            progress["value"] = 0
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de la décompression :\n{e}")
            progress["value"] = 0

    threading.Thread(target=run_extract).start()

# Interface principale
app = tk.Tk()
app.title("MiniWinRAR")
app.geometry("350x200")

btn_zip = tk.Button(app, text="Compresser un dossier (ZIP)", command=compresser_zip)
btn_zip.pack(pady=10)

btn_unzip = tk.Button(app, text="Décompresser (ZIP/RAR)", command=decompresser)
btn_unzip.pack(pady=10)

# Barre de progression
progress = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=20)

app.mainloop()
