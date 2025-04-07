# app.py
import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import rarfile
import os

def compresser_zip():
    dossier = filedialog.askdirectory(title="Choisir le dossier à compresser")
    if not dossier:
        return

    nom_zip = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Fichiers ZIP", "*.zip")])
    if not nom_zip:
        return

    with zipfile.ZipFile(nom_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dossier):
            for file in files:
                chemin_complet = os.path.join(root, file)
                chemin_relatif = os.path.relpath(chemin_complet, dossier)
                zipf.write(chemin_complet, arcname=chemin_relatif)

    messagebox.showinfo("Succès", f"Dossier compressé dans :\n{nom_zip}")

def decompresser():
    fichier = filedialog.askopenfilename(title="Choisir un fichier à décompresser", filetypes=[("Fichiers ZIP/RAR", "*.zip *.rar")])
    if not fichier:
        return

    dossier_sortie = filedialog.askdirectory(title="Choisir le dossier de destination")
    if not dossier_sortie:
        return

    try:
        if fichier.endswith(".zip"):
            with zipfile.ZipFile(fichier, 'r') as zipf:
                zipf.extractall(dossier_sortie)
        elif fichier.endswith(".rar"):
            with rarfile.RarFile(fichier) as rf:
                rf.extractall(dossier_sortie)
        else:
            messagebox.showerror("Erreur", "Format non supporté.")
            return

        messagebox.showinfo("Succès", f"Fichier décompressé dans :\n{dossier_sortie}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de la décompression :\n{e}")

# Interface avec Tkinter
app = tk.Tk()
app.title("MiniWinRAR")
app.geometry("300x150")

btn_zip = tk.Button(app, text="Compresser un dossier (ZIP)", command=compresser_zip)
btn_zip.pack(pady=10)

btn_unzip = tk.Button(app, text="Décompresser (ZIP/RAR)", command=decompresser)
btn_unzip.pack(pady=10)

app.mainloop()
