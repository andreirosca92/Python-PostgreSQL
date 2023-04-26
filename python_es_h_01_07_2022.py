import psycopg2
from decimal import Decimal

with psycopg2.connect(host="localhost",database="postgres",user="postgres", password="xxx",port="5432" ) as conn:

    with conn.cursor() as cur:
        
        
        cur.execute("""
                            CREATE TEMP TABLE IF NOT EXISTS PRODUTTORE(
                            codice VARCHAR(20) PRIMARY KEY,
                            nome VARCHAR(80) NOT NULL,
                            nazione VARCHAR(80) NOT NULL
                            )"""
        )
        print('Esito della creazione della tabella PRODUTTORE:{:s}\n'.format(cur.statusmessage))
        cur.execute(""" CREATE TEMP TABLE IF NOT EXISTS SOSTANZA(
                            id VARCHAR(20) PRIMARY KEY,
                            nomeSostanza VARCHAR(80) NOT NULL,
                            categoria INTEGER NOT NULL


                            )"""
        )
        print('Esito della creazione della tabella SOSTANZA:{:s}\n'.format(cur.statusmessage))
        cur.execute("""CREATE TEMP TABLE IF NOT EXISTS FARMACO(
                            codice SERIAL PRIMARY KEY,
                            nomeFarmaco VARCHAR(80) NOT NULL,
                            principioAttivo VARCHAR(80) REFERENCES SOSTANZA(id),
                            produttore VARCHAR(80) REFERENCES PRODUTTORE(codice),
                            prezzo DECIMAL(8,2) NOT NULL 
                           
                            )
                            """
        )
        print('Esito della creazione della FARMACO:{:s}\n'.format(cur.statusmessage))
        cur.execute("""SELECT COUNT(*) FROM SOSTANZA AS s JOIN FARMACO AS f ON f.principioAttivo=s.nomeSostanza JOIN PRODUTTORE AS p ON p.nome=f.produttore""")
        righe=cur.fetchone()[0]
        if righe==0:
            cur.execute("""INSERT INTO PRODUTTORE (codice,nome,nazione) VALUES
                            (%s,%s,%s),
                            (%s,%s,%s),
                            (%s,%s,%s),
                            (%s,%s,%s),
                            (%s,%s,%s)""",
                            ("P1", "Mylan","USA",
                            "P2", "IBSA","SVIZZERA",
                            "P3", "BAYER", "GERMANIA",
                            "P4", "ANGELINI", "ITALIA",
                            "P5", "RECKITT BENCKISER","GERMANIA")
                            
            )
            cur.execute("""INSERT INTO SOSTANZA (id, nomeSostanza, categoria) VALUES
                            (%s,%s,%s),
                            (%s,%s,%s),
                            (%s,%s,%s),
                            (%s,%s,%s),
                            (%s,%s,%s)""",
                            ("S001","Ibuprofene", 1,
                            "S002","Levotiroxina sodica",1,
                            "S003","Acido acetilsalicilico",1,
                            "S004","Paracetamolo",1,
                            "S005","Ibuprofene",1)
            )
            cur.execute("""INSERT INTO FARMACO(codice,nomeFarmaco,principioAttivo, produttore, prezzo) VALUES
                            (%s,%s,%s,%s,%s),
                            (%s,%s,%s,%s,%s),
                            (%s,%s,%s,%s,%s),
                            (%s,%s,%s,%s,%s),
                            (%s,%s,%s,%s,%s)""",
                            (1,"BRUFEN","S001","P1", Decimal("6.77"),
                            2,"Tiche","S002","P2",Decimal("9.90"),
                            3,"ASPIRINA","S003","P3", Decimal("5.00"),
                            4,"TACHIPIRINA","S004","P4", Decimal("7.99"),
                             5,"NARUFEN","S005","P5",Decimal("10.00"))
            )
    
    conn.commit()
    conn.isolation_level='REPEATABLE READ'
    principioAttivo=input("Inserisci un nome della sostanza [Ibuprofene]?:")
    with  conn.cursor() as curr:
        curr.execute("""SELECT f.codice, f.nomeFarmaco, f.prezzo, p.nome FROM FARMACO AS f JOIN SOSTANZA AS s ON s.id=f.principioAttivo\
                        JOIN PRODUTTORE AS p ON p.codice=f.produttore WHERE s.nomeSostanza=(%s) ORDER BY p.nome""",(principioAttivo,))
        lista=curr.fetchall()
        print('='*70)
        stringformat1="||{:>8s}||{:>20s}||{:>10s}||{:>15s}  ||"
        stringformat2="||{:>8d} ||{:>20s}||{:>10.2f}€||{:>15s}||"
        print(stringformat1.format("indice","nome farmaco","prezzo","nome produttore"))
        print('='*70)
        if len(lista)>0:
            for row in lista:
                     
                print(stringformat2.format(row[0],row[1],row[2],row[3]))
            print('='*70)
        else:
            print("Nessun farmaco presente per il principio attivo selezionato")

conn.close()
                    
