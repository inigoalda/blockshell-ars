#!/bin/bash

FILE="chain.txt"
TMP_FILE="chain_tmp.txt"

# Check that jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: 'jq' is required but not installed."
    exit 1
fi

# Display all indexes and the corresponding names
echo "Available entries:"
jq -c '.[] | {index, nom: .data.nom, prenom: .data.prenom}' "$FILE"

# Ask for index
read -p "Enter the index of the entry you want to edit: " IDX

# Verify index exists
ENTRY=$(jq ".[] | select(.index == $IDX)" "$FILE")
if [ -z "$ENTRY" ]; then
    echo "Error: No entry found with index $IDX."
    exit 1
fi

# Show the entry
# Show the entry with trimmed image
echo "Selected entry:"
echo "$ENTRY" | jq '{
  index,
  previousHash,
  data: {
    uid_epita: .data.uid_epita,
    email_epita: .data.email_epita,
    nom: .data.nom,
    prenom: .data.prenom,
    image: (.data.image | if length > 10 then "\(.[0:10])...\((length - 10)) more chars" else . end)
  },
  timestamp,
  nonce,
  hash
}'


# Let user choose which field to edit
FIELDS=("uid_epita" "email_epita" "nom" "prenom" "image")
echo "Editable fields:"
select FIELD in "${FIELDS[@]}"; do
    if [[ " ${FIELDS[*]} " == *" $FIELD "* ]]; then
        break
    else
        echo "Invalid selection."
    fi
done

# Ask for new value
read -p "Enter new value for $FIELD: " NEW_VALUE

# Update the entry
jq --argjson index "$IDX" --arg field "$FIELD" --arg new_value "$NEW_VALUE" '
  map(if .index == $index then
        .data[$field] = $new_value
      else
        .
      end)
' "$FILE" > "$TMP_FILE" && mv "$TMP_FILE" "$FILE"

echo "Entry updated successfully."

