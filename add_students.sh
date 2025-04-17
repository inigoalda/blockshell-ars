#!/bin/bash

echo "[*] Ajout de 63 étudiants dans la blockchain..."

output_file="students.txt"
> "$output_file"  # Vider le fichier s'il existe déjà

for i in $(seq 1 63); do
  uid="u$((1000 + i))"
  email="etudiant${i}@epita.fr"
  nom="Nom${i}"
  prenom="Prenom${i}"

  # Génère un faux contenu image en base64 (sans sauts de ligne)
  image=$(convert -size 100x100 xc: +noise Random /tmp/random.png && base64 /tmp/random.png)

  # Utilise jq pour garantir un JSON bien formé sur une seule ligne
  jq -nc \
    --arg uid "$uid" \
    --arg email "$email" \
    --arg nom "$nom" \
    --arg prenom "$prenom" \
    --arg image "$image" \
    '{uid_epita: $uid, email_epita: $email, nom: $nom, prenom: $prenom, image: $image}' >> "$output_file"
done

# Exécute la commande dotx avec le fichier comme argument
echo "dotx ./students.txt" | blockshell init

echo "[✔] Tous les étudiants ont été ajoutés à la blockchain depuis le fichier $output_file."

