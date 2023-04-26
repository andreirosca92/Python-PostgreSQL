

import psycopg2
from datetime import date
from decimal import Decimal


with psycopg2.connect(host="localhost",database="postgres",user="postgres", password="xxx",port="5432" ) as conn:
        
	with conn.cursor() as cursore:
		
		cursore.execute("""CREATE TEMP TABLE IF NOT EXISTS Prodotti(
				id INTEGER PRIMARY KEY,
				nome VARCHAR(20) NOT NULL,
				prezzo DECIMAL(6,2) NOT NULL,
				dataUltimaModifica DATE NOT NULL
		
				)"""
                )
		print('Esito della creazione della tabella Prodotti:{:s}\n'.format(cursore.statusmessage))
		cursore.execute("""SELECT count(*) FROM Prodotti""")
		numeroRighe=cursore.fetchone()[0]
		if numeroRighe==0:
			cursore.execute("""INSERT INTO Prodotti(id, nome, prezzo, dataUltimaModifica) VALUES
                                (%s,%s,%s,%s),
                                (%s,%s,%s,%s),
                                (%s,%s,%s,%s),
                                (%s,%s,%s,%s)""",
                                (1,"banane", Decimal("1.90"), date(2020,1,7),
                                2,"biscotti",Decimal("2.00"), date(2020, 1, 19),
                                3,"arance",Decimal("3.00"), date(2020,1, 19),
                                4,"carta igienica",Decimal("2.20"), date(2020, 1, 19))
                        )
			print ("Esito dell’ inserimento delle 4 tuple :{:s}".format(cursore.statusmessage ))
		else:
			print("La tabella è già presente con delle tuple e quindi nessuna tupla è stata aggiunta.")
		cursore.execute("""SELECT * FROM Prodotti""")
		lista=cursore.fetchall()
		if len(lista)>0:
			for row in lista:
		
				print(row[0], row[1], row[2],row[3])
	conn.commit()
	prezzo=float(input("Inserire un prezzo?: "))
	nomeProdotto=input("Inserisci un prodotto? ['biscotti','banane', 'arance','carta igienica']:")
	
	conn.set_session(isolation_level='REPEATABLE READ')
	with conn.cursor() as cursore:
		
		cursore.execute("""UPDATE Prodotti SET prezzo=(%s) WHERE nome=(%s) AND (%s)>=prezzo""", (prezzo,nomeProdotto, prezzo))
		cursore.execute("""SELECT * FROM Prodotti""")
		
		lista=cursore.fetchall()
		if len(lista)>0:
			for row in lista:
				print(row[0], row[1], row[2], row[3])
		cursore.execute("""SELECT nome, dataUltimaModifica FROM Prodotti ORDER BY nome ASC, dataUltimaModifica DESC""")
		lista=cursore.fetchall()
		if len(lista)>0:
			for row in lista:
				print(row[0], row[1])
				
		else:
			print("Non si puo mettere il prodotto X nei Prodotti\n")
	
	
conn.close()


	
