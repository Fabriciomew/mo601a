import csv, os

#Coleta todas as subpastas de teste
dirs = os.listdir("test")

for folder in dirs:
	print(folder)
	try:
		#Variáveis iniciais
		A = 0
		B = 0
		C = 0
		D = 0
		E = 0
		F = 0
		G = 0
		H = 0
		I = 0
		J = 0
		K = 0
		L = 0
		M = 0
		N = 0
		O = 0
		P = 0
		Q = 0
		R = 0
		S = 0
		T = 0
		U = 0
		V = 0
		W = 0
		X = 0
		Y = 0
		Z = 0
		Tempo = 0
		header = []
		row = []
		rows = []
		entradas = []
		entradas_out = []
		entradas_out_initial = []
		entradas2 = []
		estimulos2 = []
		count = 0
		count2 = 0
		count3 = 0
		loop = 0
		verify = True

		#Funções que podem ser usadas no simulador
		def OR(A, B):
			return A | B

		def AND(A, B):
			return A & B

		def NOT(A):
			return ~A+2

		def NAND(A, B):
			return NOT(AND(A, B))

		def NOR(A, B):
			return NOT(OR(A, B))

		def XOR(A, B):
			return A ^ B

		def XNOR(A, B):
			return NOT(XOR(A, B))

		#Coleta as descrições dos circuitos

		f = open("test/"+folder+"/circuito.hdl", "r")
		circuito = f.read()
		split_circuito = circuito.splitlines();
		#print(split_circuito)

		#Adiciona virgula e parenteses aos códigos dos circuitos
		for i in split_circuito:
			split_i = i.split(sep="=")
			x = split_i[1].strip()
			x = x.split(sep=" ")
			if(x[0] != 'NOT'):
				x.insert(2,',')
			x.append(')')
			x.insert(1,'(')
			entradas_out.append(x)
			x = "".join(x)
			#print(x)	
			exec("%s = '%s'" % (i[0],x))
			entradas.append(i[0])

		#Comprime cada circuito em uma string única
		for i in range(len(entradas_out)):
			x = entradas_out[i]
			x = "".join(x)
			entradas_out_initial.append(x)

		iterations = len(entradas) ** 2

		#Para cada circuito substitui as letras referentes as saídas dos circuitos por seus cálculos, sendo que cada saída depende apenas dos estimulos de entrada,
		#caso dentro de 2 execuções ainda não tenha finalizado ele termina o loop para evitar infinito. 
		while count3 != iterations and loop < 2:
			count3 = 0
			count2 = 0
			count = 0
			loop = loop + 1 
			for i in entradas_out:
				for j in entradas:
					try:
						index = i.index(j)
						#i[index] = entradas_out[count]
						#entradas_out[count2] = i
						entradas_out[count2].pop(index)
						for k in range(len(entradas_out[count])):
							entradas_out[count2].insert((index + k),entradas_out[count][k])
						#print(i[index])
						#print(entradas_out)
					except ValueError:
						#print('item not present')
						count3 = count3 + 1
					count = count +1	
				count = 0
				count2 = count2 +1
			#print("\n\n")

		#Comprime cada circuito em uma string única
		for i in range(len(entradas)):
			#print(entradas[i])
			x = entradas_out[i]
			x = "".join(x)
			exec("%s = '%s'" % (entradas[i],x))

		#Coleta os estimulos e caso já não esteja, organiza os estimulos deixando um por linha
		f = open("test/"+folder+"/estimulos.txt", "r")
		#print(f.read())
		estimulos = f.read()
		split_estimulos = estimulos.splitlines();
		#print(split_estimulos)

		for line in split_estimulos:
			#print(len(line))
			try:
				index = line.index('=')
				split_line = line.split(sep="=")
				split_line[0] = split_line[0].strip()
				split_line[1] = split_line[1].strip()
				for i in range(len(split_line[0])):
					try:
						index = entradas2.index(split_line[0][i])
					except ValueError:
						entradas2.append(split_line[0][i])
					estimulos2.append(split_line[0][i]+"="+split_line[1][i])
				#print(split_line)
			except ValueError:
				estimulos2.append(line)
				#print('time')

		#coleta o header para os csv's de saída
		file = open("test/"+folder+'/esperado0.csv')
		csvreader = csv.reader(file)
		header = next(csvreader)

		#Calcula as saídas para atraso 0 para cada passagem de ciclo
		for line in estimulos2:
			try:
				index = line.index('=')
				exec(line)
			except ValueError:
				line = line.replace('+','')
				for i in range(int(line)):
					for j in header:
						if j == 'Tempo':
							row.append(eval(j))
						elif j in entradas:
							row.append(eval(eval(j)))
						else:
							row.append(eval(j))
					Tempo = Tempo + 1
					rows.append(row)
					row = []

		#Calcula a saída para os últimos estímulos e continua até que a curva de saída atual seja igual a anterior 
		while verify:
			for j in header:
				if j == 'Tempo':
					row.append(eval(j))
				elif j in entradas:
					#modificado
					try:
						row.append(eval(eval(j))) #antes só essa
					except:
						index = entradas.index(j)
						exec("%s = '%s'" % (j,entradas_out_initial[index]))
						row.append(eval(j))
					#modificado
				else:
					row.append(eval(j))
			#modificado - antes só if
			try:				
				if row[1:] == rows[Tempo-1][1:]:
					verify = False
			except:
				print("Apenas uma linha")
			#modificado
			Tempo = Tempo + 1
			rows.append(row)
			row = []

		#Salva as saídas para atraso 0 no CSV
		with open("test/"+folder+'/saida0.csv', 'w') as f:
		      
		    # using csv.writer method from CSV package
		    write = csv.writer(f)
		      
		    write.writerow(header)
		    write.writerows(rows)

		#print(rows)

		# Saída para atraso 1
		#Reseta as variáveis
		A = 0
		B = 0
		C = 0
		D = 0
		E = 0
		F = 0
		G = 0
		H = 0
		I = 0
		J = 0
		K = 0
		L = 0
		M = 0
		N = 0
		O = 0
		P = 0
		Q = 0
		R = 0
		S = 0
		T = 0
		U = 0
		V = 0
		W = 0
		X = 0
		Y = 0
		Z = 0
		Tempo = 0
		verify = True
		rows = []

		for j in header:
			row.append(0)

		#Calcula as saídas para atraso 1 para cada passagem de ciclo
		for line in estimulos2:
			try:
				index = line.index('=')
				exec(line)
			except ValueError:
				line = line.replace('+','')
				for i in range(int(line)):
					for j in range(len(header)):
						if header[j] not in entradas:
							row[j] = eval(header[j])
					rows.append(row[:])
					for j in range(len(header)):
						if (header[j] in entradas):
							index = entradas.index(header[j])
							row[j] = eval(entradas_out_initial[index])
					for j in range(len(header)):
						if (header[j] in entradas):
							index = entradas.index(header[j])
							exec("%s = %s" % (entradas[index],entradas_out_initial[index]))
					Tempo = Tempo + 1

		#Calcula a saída para os últimos estímulos e continua até que a curva de saída atual seja igual a anterior 
		while verify:
			for j in range(len(header)):
				if header[j] not in entradas:
					row[j] = eval(header[j])
			rows.append(row[:])
			for j in range(len(header)):
				if (header[j] in entradas):
					index = entradas.index(header[j])
					row[j] = eval(entradas_out_initial[index])
			for j in range(len(header)):
				if (header[j] in entradas):
					index = entradas.index(header[j])
					exec("%s = %s" % (entradas[index],entradas_out_initial[index]))
			#modificado - antes só if
			try:	
				if row[1:] == rows[Tempo-1][1:]:
					verify = False
			except:
				print("Apenas uma linha")
			#modificado
			Tempo = Tempo + 1

		#Salva as saídas para atraso 1 no CSV
		with open("test/"+folder+'/saida1.csv', 'w') as f:
		      
		    # using csv.writer method from CSV package
		    write = csv.writer(f)
		      
		    write.writerow(header)
		    write.writerows(rows)

		#print(rows)
		#print(entradas_out_initial)
		#A = eval(eval(entradas[0]))
		#B = eval(B)
		#print(estimulos2)
		#print(entradas2)
		#print(header)
		#print(entradas_out)
		print("ok")
	except:
		print("error")