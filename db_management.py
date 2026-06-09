import csv

def save_bdd(collection, filename="static/base_de_donnee.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["nom", "ratio", "heros", "elixir", "level"])
        for carte in collection.collection:
            writer.writerow([carte.nom, carte.ratio, str(carte.heros), carte.elixir, carte.level])

def load_bdd(filename = "static/base_de_donnee.csv"):
    liste = []
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            if row[2] == "False":
                liste.append([row[0],float(row[1]),False, int(row[3]), int(row[4])])
            else:
                liste.append([row[0],float(row[1]),True, int(row[3]), int(row[4])])
    return liste

