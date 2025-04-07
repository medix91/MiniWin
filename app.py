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

    def preview_files():
        # Ouvrir une fenêtre popup avec la liste des fichiers dans l'archive
        popup = tk.Toplevel(app)
        popup.title("Contenu de l'archive")
        popup.geometry("300x200")

        # Liste des fichiers
        listbox = tk.Listbox(popup)
        listbox.pack(fill="both", expand=True)

        try:
            if fichier.endswith(".zip"):
                with zipfile.ZipFile(fichier, 'r') as zipf:
                    liste = zipf.namelist()
            elif fichier.endswith(".rar"):
                with rarfile.RarFile(fichier) as rf:
                    liste = rf.namelist()
            else:
                messagebox.showerror("Erreur", "Format non supporté.")
                return

            for name in liste:
                listbox.insert(tk.END, name)

            def extraire():
                try:
                    if fichier.endswith(".zip"):
                        with zipfile.ZipFile(fichier, 'r') as zipf:
                            zipf.extractall(dossier_sortie)
                    elif fichier.endswith(".rar"):
                        with rarfile.RarFile(fichier) as rf:
                            rf.extractall(dossier_sortie)

                    messagebox.showinfo("Succès", f"Fichier décompressé dans :\n{dossier_sortie}")
                    popup.destroy()
                except Exception as e:
                    messagebox.showerror("Erreur", f"Échec de la décompression :\n{e}")
                    popup.destroy()

            btn_extraire = tk.Button(popup, text="Extraire", command=extraire)
            btn_extraire.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir l'archive :\n{e}")

    preview_files()

# Interface principale
app = tk.Tk()
app.title("MiniWinRAR")
app.geometry("350x250")

btn_zip = tk.Button(app, text="Compresser un dossier (ZIP)", command=compresser_zip)
btn_zip.pack(pady=10)

btn_unzip = tk.Button(app, text="Décompresser (ZIP/RAR)", command=decompresser)
btn_unzip.pack(pady=10)

# Barre de progression
progress = ttk.Progressbar(app, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=20)

app.mainloop()
