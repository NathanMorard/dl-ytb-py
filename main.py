import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox  

output_folder = 'musique_mp3'

#creation interface stylisé recup url playlist youtube
def valider():
    url = value.get().strip()
    if url == "":
        labelerreur.config(text="Ce champ ne peut pas être vide.")
        labelerreur.pack(pady=(5, 0))
    else:
        mafenetre_pour_url.quit()

# Fenêtre
mafenetre_pour_url = tk.Tk()
mafenetre_pour_url.title("Playlist YouTube")
mafenetre_pour_url.geometry("800x400")
mafenetre_pour_url.configure(bg="#1e1e1e")
mafenetre_pour_url.resizable(False, False)

# Label
monlabel = tk.Label(
    mafenetre_pour_url,
    text="Entrez l'URL de la playlist YouTube :",
    bg="#1e1e1e",
    fg="white",
)
monlabel.pack(pady=(20, 10))

# Champ de saisie
value = tk.StringVar()
entree = tk.Entry(
    mafenetre_pour_url,
    textvariable=value,
    width=35,
    relief="flat"
)
entree.pack(ipady=5)

# Bouton
bouton = tk.Button(
    mafenetre_pour_url,
    text="Valider",
    command=valider,
    bg="#0026ff",
    fg="white",
    relief="flat",
    cursor="hand2",
    activebackground="#cc0000"
)
bouton.pack(pady=15, ipadx=10, ipady=5)

# Label erreur (caché au départ)
labelerreur = tk.Label(
    mafenetre_pour_url,
    text="",
    fg="#ff5555",
    bg="#1e1e1e",
    font=("Helvetica", 10)
)

mafenetre_pour_url.mainloop()

playlist_url = value.get()


if playlist_url == "":
    exit()
else:
    print("la")
    mafenetre_pour_url.destroy()

#selectionner dossier de destination
root = tk.Tk()
root.withdraw() 
dossier_destination = filedialog.askdirectory(title="Sélectionner le dossier de destination")
if not dossier_destination:
    messagebox.showerror("Erreur", "Aucun dossier sélectionné. Le programme va se fermer.")
    exit()

# Crée le dossier de sortie complet
chemin_output = os.path.join(dossier_destination, output_folder)
os.makedirs(chemin_output, exist_ok=True)



#recupére toute les mussiques deja presentes dans le dossier de destination
existing_files = set()
print(existing_files)

for root_dir, _, files in os.walk(chemin_output):
    for file in files:
        if file.endswith('.mp3'):
            existing_files.add(os.path.splitext(file)[0])

def skip_if_exists(info, *, incomplete):
    title = info.get("title", "").strip()

    for existing in existing_files:
        if title in existing:
            return f"Déjà présent : {title}"

    return None  # None = autorisé

#dl playlist youtube en mp3 avec yt-dlp
#Configurer les options de téléchargement et de conversion
ydl_opts = {
    'noplaylist': False,
    'outtmpl': os.path.join(chemin_output, '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'),
    'format': 'bestaudio/best',
    'extract_audio': True,
    'audioformat': 'mp3',
    'keepvideo': False,
    'addmetadata': True,

    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],

    'match_filter': skip_if_exists,

    'progress_hooks': [
        lambda d: print(f"État: {d['status']} | Fichier: {d.get('filename', '')}")
    ]
}

#Exécuter le téléchargement
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Démarrage du téléchargement de la playlist : {playlist_url}")
        ydl.download([playlist_url])
        print("Toutes les vidéos ont été téléchargées et converties en MP3.")
        
except Exception as e:
    print(f"Une erreur est survenue : {e}")