# Josther Ozuna
# 28/03/2025
# Arxiu plantilla diferents programes python

import psycopg

# Funció per connectar a la base de dades
def connectar_db():
    try:
        connexio = psycopg.connect(
            dbname="chinook_v2",  # Canvia-ho pel nom de la teva base de dades
            user="postgres",  # Canvia-ho pel teu usuari
            password="12345678",  # Canvia-ho per la teva contrasenya
            host="localhost",
            port=5432
        )
        return connexio
    except psycopg.Error as e:
        print("Error en la connexió a la base de dades: ", e)
        return None

# Funció per consultar tots els artistes
def obtenir_tots_els_artistes(conn):
    if not conn:
        print("No s'ha pogut establir la connexió.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT artist_id, name FROM artist;")
        artistes = cursor.fetchall()

        if artistes:
            for artista in artistes:
                print("ID: ", artista[0], ", NOM: ", artista[1])
        else:
            print("No hi han resultats")
    except psycopg.Error as e:
        print("Error en obtenir els artistes: ", e)
    finally:
        if cursor:
            cursor.close()

# Funció per buscar artistes per nom
def buscar_artista_per_nom(conn):
    if not conn:
        print("Connexió inexistent.")
        return

    nom = input("Introdueix el nom de l'artista: ")
    cursor = conn.cursor()
    cursor.execute("SELECT artist_id, name FROM artist WHERE name ILIKE %s;", (f"%{nom}%",))
    artistes = cursor.fetchall()

    if artistes:
        for artista in artistes:
            print("ID: ", artista[0], ", NOM: ", artista[1])
    else:
        print("No hi han resultats")
    cursor.close()

# Funció per mostrar els 5 primers àlbums d'un artista
def obtenir_primers_albums(conn):
    if not conn:
        print("La connexió no és vàlida.")
        return

    nom_artista = input("Escriu el nom de l'artista: ")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT al.album_id, al.title, ar.name
        FROM album al
        JOIN artist ar ON al.artist_id = ar.artist_id
        WHERE ar.name ILIKE %s
        LIMIT 5;
    """, (f"%{nom_artista}%",))
    albums = cursor.fetchall()

    if albums:
        for album in albums:
            print("ID: ", album[0], ", TÍTOL: ", album[1], ", ARTISTA: ", album[2])
    else:
        print("No hi han resultats")
    cursor.close()

# Funció per afegir un nou artista
def afegir_artista(conn):
    if not conn:
        print("No hi ha enllaç amb la base de dades.")
        return

    nom = input("Introdueix el nom de l'artista nou: ")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO artist (name) VALUES (%s);", (nom,))
    conn.commit()
    print("Artista afegit correctament.")
    cursor.close()

# Funció per modificar el nom d'un artista
def modificar_artista(conn):
    if not conn:
        print("Falta la connexió.")
        return

    id_artista = input("Introdueix la ID de l'artista a canviar: ")
    nou_nom = input("Introdueix el nom nou de l'artista: ")
    cursor = conn.cursor()
    cursor.execute("UPDATE artist SET name = %s WHERE artist_id = %s;", (nou_nom, id_artista))
    conn.commit()
    print("Nom de l'artista actualitzat.")
    cursor.close()

# Funció per eliminar un artista
def eliminar_artista(conn):
    if not conn:
        print("Connexió necessària.")
        return

    id_artista = input("Introdueix la ID de l'artista que vols suprimir: ")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM artist WHERE artist_id = %s;", (id_artista,))
    conn.commit()
    print("Artista eliminat correctament.")
    cursor.close()

# Menú principal
def menu():
    connexio = connectar_db()
    if not connexio:
        return  # Surt si no hi ha connexió

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1 - Llistar tots els artistes")
        print("2 - Buscar artista per nom")
        print("3 - Mostrar primers àlbums")
        print("4 - Incloure artista")
        print("5 - Canviar nom d'artista")
        print("6 - Esborrar artista")
        print("7 - Sortir")

        opcio = input("Tria una opció: ")

        if opcio == '1':
            obtenir_tots_els_artistes(connexio)
        elif opcio == '2':
            buscar_artista_per_nom(connexio)
        elif opcio == '3':
            obtenir_primers_albums(connexio)
        elif opcio == '4':
            afegir_artista(connexio)
        elif opcio == '5':
            modificar_artista(connexio)
        elif opcio == '6':
            eliminar_artista(connexio)
        elif opcio == '7':
            print("Acabant el programa...")
            break
        else:
            print("Opció no vàlida.")

    connexio.close()

# Executar el menú
if __name__ == "__main__":
    menu()