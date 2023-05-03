import os, time, json

#Coleta todas os programas em c da pasta test
dirs = os.listdir("test/objdump")

#variáveis iniciais
instructions = []
num_of_inst = 0
PC = 0
memory = {}
inst_hex = 0
inst_bin = 0
inst_decoded = 0
logs = []
rd = 0
rd_int = 0
value_rd = 0
rs1 = 0
rs1_int = 0
value_rs1 = 0
rs2 = 0
rs2_int = 0
value_rs2 = 0
func3 = 0
func7 = 0
ufunctions = ['lui','auipc']
jfunctions = ['jal']
ifunctions = ['addi', 'lw', 'jalr', 'xori', 'lbu', 'slli', 'srai','lhu','andi','lb','lh','srli','sltiu', 'ebreak','slti','ori']
sfunctions = ['sw', 'sb', 'sh']
rfunctions = ['add','sltu','sub','mul','mulhu','div','divu','srl','sll','or','remu','and', 'xor', 'slt','sra']
bfunctions = ['bge','bne','bgeu','beq', 'bltu','blt']
while_key = False
start_time = 0
ciclos = 0
statistics = []

register_names = ['zero', 'ra', 'sp','gp','tp','t0','t1','t2','s0/fp','s1','a0','a1','a2','a3','a4','a5','a6','a7','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','t3','t4','t5','t6']

#funções
def memory_access(kind, position, value):
	if (kind == 'store'):
		memory[position] = value
		#print(memory)
	if (kind == 'load'):
		try:
			value = memory[position]
			return value
		except KeyError:
			#print("memory position isn't encountered returning zero")
			return hex(0)[2:].zfill(8)

def exec_inst(inst):
	global PC, value_rd
	# imm[31:12] rd (pg 14) ok
	if (inst == 'lui'):
		#imm
		imm = inst_bin[0:20]
		imm = imm + '0'*12
		imm_dec = int(imm, 2)
		imm = hex(imm_dec)[2:].zfill(8)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
			imm = hex(imm_dec & (2**32-1))[2:].zfill(8)
		if (rd_int == 0):
			imm = '0'*8
		registers[rd_int] = imm
		#rd
		value_rd = imm
		#log
		mnemonic = register_names[rd_int]+','+str(imm_dec)
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	# imm[31:12] rd (pg 14) ok
	if (inst == 'auipc'):
		#imm
		imm = inst_bin[0:20]
		imm = imm + '0'*12
		imm_dec = int(imm, 2)
		imm = hex(imm_dec)[2:].zfill(8)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
			imm = hex(imm_dec & (2**32-1))[2:].zfill(8)
		imm = int(imm, 16)+int(PC, 16)
		imm = hex(imm)[2:].zfill(8)
		if (rd_int == 0):
			imm = '0'*8
		registers[rd_int] = imm
		#rd
		value_rd = imm
		#log
		mnemonic = register_names[rd_int]+','+str(imm_dec)
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	# imm[20|10:1|11|19:12] rd (pg 15) ok
	if (inst == 'jal'):
		#rd
		if (rd_int != 0):
			value_rd = hex(int(PC, 16) + 4)[2:].zfill(8)
			registers[rd_int] = value_rd
		#imm
		imm = inst_bin[0]+inst_bin[12:20]+inst_bin[11]+inst_bin[1:11] + '0'
		x = int(imm, 2)
		if imm[0] == '1':
			x = (-1)*(2**len(imm) - x)
		#log
		mnemonic = register_names[rd_int]+','+str(x)
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + x)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 13) ok
	if (inst == 'addi'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		#rd
		value_rd_int = (value_rs1_dec + imm_dec)
		if(value_rd_int < 0):
			value_rd = hex(value_rd_int & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_int)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+str(imm_dec)
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:5] rs2 rs1 imm[4:0] (pg 19) ok
	if (inst == 'sw'):
		#imm
		imm = inst_bin[0:7]+inst_bin[20:25]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		#memory access
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		memory_pos_int = (value_rs1_dec + imm_dec)
		if(memory_pos_int < 0):
			memory_pos = hex(memory_pos_int & (2**32-1))[2:].zfill(8)
		else:
			memory_pos = hex(memory_pos_int)[2:].zfill(8)
		memory_value = value_rs2
		memory_access('store',memory_pos,memory_value.zfill(8))
		#log
		mnemonic = register_names[rs2_int]+','+str(imm_dec)+'('+register_names[rs1_int]+')'
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 19) ok
	if (inst == 'lw'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		#memory access
		memory_pos_int = (value_rs1_dec + imm_dec)
		if(memory_pos_int < 0):
			memory_pos = hex(memory_pos_int & (2**32-1))[2:].zfill(8)
		else:
			memory_pos = hex(memory_pos_int)[2:].zfill(8)
		memory_value = memory_access('load',memory_pos,'')
		#rd
		value_rd = memory_value
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd.zfill(8)
		#log
		mnemonic = register_names[rd_int]+','+str(imm_dec)+'('+register_names[rs1_int]+')'
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 16) ok
	if (inst == 'jalr'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		#rd
		if (rd_int != 0):
			value_rd = hex(int(PC, 16) + 4)[2:].zfill(8)
			registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+str(imm_dec)
		generate_log(mnemonic)
		PC_dec = imm_dec + value_rs1_dec
		PC_bin = bin(PC_dec)[2:].zfill(32)
		PC_bin = PC_bin[:31] + '0'
		PC_dec = int(PC_bin, 2)
		PC = hex(PC_dec)[2:].zfill(8)
	#imm[11:5] rs2 rs1 imm[4:0] (pg 19) ok
	if (inst == 'sb'):
		#imm
		imm = inst_bin[0:7]+inst_bin[20:25]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		#memory access
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		memory_pos_int = (value_rs1_dec + imm_dec)
		if(memory_pos_int < 0):
			memory_pos = hex(memory_pos_int & (2**32-1))[2:].zfill(8)
		else:
			memory_pos = hex(memory_pos_int)[2:].zfill(8)
		memory_value = value_rs2[6:]
		memory_access('store',memory_pos,memory_value.zfill(8))
		#log
		mnemonic = register_names[rs2_int]+','+str(imm_dec)+'('+register_names[rs1_int]+')'
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:5] rs2 rs1 imm[4:0] (pg 19) ok
	if (inst == 'sh'):
		#imm
		imm = inst_bin[0:7]+inst_bin[20:25]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		#memory access
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		memory_pos_int = (value_rs1_dec + imm_dec)
		if(memory_pos_int < 0):
			memory_pos = hex(memory_pos_int & (2**32-1))[2:].zfill(8)
		else:
			memory_pos = hex(memory_pos_int)[2:].zfill(8)
		memory_value = value_rs2[4:]
		memory_access('store',memory_pos,memory_value.zfill(8))
		#log
		mnemonic = register_names[rs2_int]+','+str(imm_dec)+'('+register_names[rs1_int]+')'
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 14) ok
	if (inst == 'xori'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
			kind = 'neg'
		else:
			kind = 'pos'
		if(kind == 'neg'):
			imm = '1'*20 + imm
		else:
			imm = imm.zfill(32)
		#rd
		value_rd_bin = ''
		for i in range(32):
			value_rd_bin = value_rd_bin + str(int(value_rs1_bin[i])^int(imm[i]))
		value_rd_int = int(str(value_rd_bin),2)
		if value_rd_bin[0] == '1':
			value_rd_int = (-1)*(2**len(value_rd_bin) - value_rd_int)
		if(value_rd_int < 0):
			value_rd = hex(value_rd_int & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_int)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+str(imm_dec)
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 19) ok
	if (inst == 'lbu'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		#memory access
		memory_pos_int = (value_rs1_dec + imm_dec)
		if(memory_pos_int < 0):
			memory_pos = hex(memory_pos_int & (2**32-1))[2:].zfill(8)
		else:
			memory_pos = hex(memory_pos_int)[2:].zfill(8)
		memory_value = memory_access('load',memory_pos,'')
		#rd
		value_rd = memory_value[6:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+str(imm_dec)+'('+register_names[rs1_int]+')'
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#shamt rs1 rd (pg 14) ok
	if (inst == 'slli'): 
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#shamt
		shamt = rs2_int
		#rd
		value_rd_bin = value_rs1_bin+'0'*shamt
		value_rd_bin = value_rd_bin[shamt:]
		value_rd_dec = int(str(value_rd_bin),2)
		if value_rd_bin[0] == '1':
			value_rd_dec = (-1)*(2**len(value_rd_bin) - value_rd_dec)
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+str(shamt)
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#shamt rs1 rd (pg 14) ok
	if (inst == 'srai'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
			kind = 'neg'
		else:
			kind = 'pos'
		#shamt
		shamt = rs2_int
		#rd
		if (kind == 'neg'):
			value_rd_bin = '1'*shamt+value_rs1_bin
			value_rd_bin = value_rd_bin[:32]
		else:
			value_rd_bin = '0'*shamt+value_rs1_bin
			value_rd_bin = value_rd_bin[:32]
		value_rd_dec = int(str(value_rd_bin),2)
		if value_rd_bin[0] == '1':
			value_rd_dec = (-1)*(2**len(value_rd_bin) - value_rd_dec)
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+str(shamt)
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 19) ok
	if (inst == 'lhu'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		#memory access
		memory_pos_int = (value_rs1_dec + imm_dec)
		if(memory_pos_int < 0):
			memory_pos = hex(memory_pos_int & (2**32-1))[2:].zfill(8)
		else:
			memory_pos = hex(memory_pos_int)[2:].zfill(8)
		memory_value = memory_access('load',memory_pos,'')
		#rd
		value_rd = memory_value[4:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+str(imm_dec)+'('+register_names[rs1_int]+')'
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 14) ok
	if (inst == 'andi'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
			kind = 'neg'
		else:
			kind = 'pos'
		#rd
		if(kind == 'neg'):
			imm = '1'*20 + imm
			#print(imm)
		else:
			imm = imm.zfill(32)
		value_rd_bin = ''
		for i in range(32):
			value_rd_bin = value_rd_bin + str(int(value_rs1_bin[i])&int(imm[i]))
		value_rd_dec = int(str(value_rd_bin),2)
		if value_rd_bin[0] == '1':
			value_rd_dec = (-1)*(2**len(value_rd_bin) - value_rd_dec)
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+str(imm_dec)
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 19) ok
	if (inst == 'lb'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		#memory access
		memory_pos_int = (value_rs1_dec + imm_dec)
		if(memory_pos_int < 0):
			memory_pos = hex(memory_pos_int & (2**32-1))[2:].zfill(8)
		else:
			memory_pos = hex(memory_pos_int)[2:].zfill(8)
		memory_value = memory_access('load',memory_pos,'')
		#rd
		memory_value_bin = bin(int(memory_value, 16))[2:].zfill(32)
		if memory_value_bin[0] == '1': #sext
			value_rd_bin = memory_value_bin[8:]
			value_rd_bin = '1'*24 + value_rd_bin
		else:
			value_rd_bin = memory_value_bin[8:].zfill(32)
		value_rd_dec = int(str(value_rd_bin),2)
		if value_rd_bin[0] == '1':
			value_rd_dec = (-1)*(2**len(value_rd_bin) - value_rd_dec)
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+str(imm_dec)+'('+register_names[rs1_int]+')'
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 19) ok
	if (inst == 'lh'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		#memory access
		memory_pos_int = (value_rs1_dec + imm_dec)
		if(memory_pos_int < 0):
			memory_pos = hex(memory_pos_int & (2**32-1))[2:].zfill(8)
		else:
			memory_pos = hex(memory_pos_int)[2:].zfill(8)
		memory_value = memory_access('load',memory_pos,'')
		#rd
		memory_value_bin = bin(int(memory_value, 16))[2:].zfill(32)
		if memory_value_bin[0] == '1':
			value_rd_bin = memory_value_bin[16:]
			value_rd_bin = '1'*16 + value_rd_bin
		else:
			value_rd_bin = memory_value_bin[16:].zfill(32)
		value_rd_dec = int(str(value_rd_bin),2)
		if value_rd_bin[0] == '1':
			value_rd_dec = (-1)*(2**len(value_rd_bin) - value_rd_dec)
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+str(imm_dec)+'('+register_names[rs1_int]+')'
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#rs2 rs1 rd (pg 15) ok
	if (inst == 'add'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		if value_rs2_bin[0] == '1':
			value_rs2_dec = (-1)*(2**len(value_rs2_bin) - value_rs2_dec)
		#rd
		value_rd_dec = value_rs1_dec+value_rs2_dec
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		if(len(value_rd) > 8):
			value_rd = value_rd[(len(value_rd)-8):]
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#shamt rs1 rd (pg 14) ok
	if (inst == 'srli'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#shamt
		shamt = rs2_int
		#rd
		value_rd_bin = '0'*shamt+value_rs1_bin
		value_rd_bin = value_rd_bin[:32]
		value_rd_dec = int(str(value_rd_bin),2)
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+str(shamt)
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#rs2 rs1 rd (pg 15) ok
	if (inst == 'sltu'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#rd
		if(value_rs1_dec < value_rs2_dec) and value_rs2_dec != 0:
			value_rd_dec = 1
		else:
			value_rd_dec = 0
		value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#rs2 rs1 rd (pg 15) ok
	if (inst == 'sub'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		if value_rs2_bin[0] == '1':
			value_rs2_dec = (-1)*(2**len(value_rs2_bin) - value_rs2_dec)
		#rd
		value_rd_dec = value_rs1_dec-value_rs2_dec
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		if(len(value_rd) > 8):
			value_rd = value_rd[(len(value_rd)-8):]
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#rs2 rs1 rd (pg 35) ok
	if (inst == 'mul'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		if value_rs2_bin[0] == '1':
			value_rs2_dec = (-1)*(2**len(value_rs2_bin) - value_rs2_dec)
		#rd
		value_rd_dec = value_rs1_dec*value_rs2_dec
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		#print(value_rd)
		if (rd_int == 0):
			value_rd = '0'*8
		if(len(value_rd) > 8):
			value_rd = value_rd[(len(value_rd)-8):]
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#rs2 rs1 rd (pg 35) ok
	if (inst == 'mulhu'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#rd
		value_rd_dec = value_rs1_dec*value_rs2_dec
		value_rd = hex(value_rd_dec)[2:].zfill(8)
		#print(value_rd)
		if (rd_int == 0):
			value_rd = '0'*8
		if(len(value_rd) > 8):
			value_rd = value_rd[:8]
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#rs2 rs1 rd (pg 36) ok
	if (inst == 'div'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		if value_rs2_bin[0] == '1':
			value_rs2_dec = (-1)*(2**len(value_rs2_bin) - value_rs2_dec)
		#rd
		if (value_rs2_dec != 0):
			value_rd_dec = value_rs1_dec//value_rs2_dec
		else:
			value_rd_dec = 0
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#rs2 rs1 rd (pg 36) ok
	if (inst == 'divu'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#rd
		if (value_rs2_dec != 0):
			value_rd_dec = value_rs1_dec//value_rs2_dec
		else:
			value_rd_dec = 0
		value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 13) ok
	if (inst == 'sltiu'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		if imm[0] == '1': #sext
			imm = '1'*20 + imm
			imm_dec = int(imm, 2)
		#rd
		if (value_rs1_dec < imm_dec):
			value_rd_dec = 1
		else:
			value_rd_dec = 0
		value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+str(imm_dec)
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[12|10:5] rs2 rs1 imm[4:1|11] (pg 17) ok
	if (inst == 'bge'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		if value_rs2_bin[0] == '1':
			value_rs2_dec = (-1)*(2**len(value_rs2_bin) - value_rs2_dec)
		#imm
		imm = inst_bin[0]+inst_bin[24]+inst_bin[1:7]+inst_bin[20:24]+'0'
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = -1*(2**len(imm) - imm_dec)
		#branch
		if (value_rs1_dec >= value_rs2_dec):
			PC = hex(int(PC, 16) + imm_dec)[2:].zfill(8)
		else:
			PC = hex(int(PC, 16) + 4)[2:].zfill(8)
		mnemonic = register_names[rs1_int]+','+register_names[rs2_int]+','+str(imm_dec)
		generate_log(mnemonic)
	#imm[12|10:5] rs2 rs1 imm[4:1|11] (pg 17) ok
	if (inst == 'bne'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		if value_rs2_bin[0] == '1':
			value_rs2_dec = (-1)*(2**len(value_rs2_bin) - value_rs2_dec)
		#imm
		imm = inst_bin[0]+inst_bin[24]+inst_bin[1:7]+inst_bin[20:24]+'0'
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = -1*(2**len(imm) - imm_dec)
		#branch
		if (value_rs1_dec != value_rs2_dec):
			PC = hex(int(PC, 16) + imm_dec)[2:].zfill(8)
		else:
			PC = hex(int(PC, 16) + 4)[2:].zfill(8)
		mnemonic = register_names[rs1_int]+','+register_names[rs2_int]+','+str(imm_dec)
		generate_log(mnemonic)
	#imm[12|10:5] rs2 rs1 imm[4:1|11] (pg 17) ok
	if (inst == 'bgeu'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#imm
		imm = inst_bin[0]+inst_bin[24]+inst_bin[1:7]+inst_bin[20:24]+'0'
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = -1*(2**len(imm) - imm_dec)
		#branch
		if (value_rs1_dec >= value_rs2_dec):
			PC = hex(int(PC, 16) + imm_dec)[2:].zfill(8)
		else:
			PC = hex(int(PC, 16) + 4)[2:].zfill(8)
		mnemonic = register_names[rs1_int]+','+register_names[rs2_int]+','+str(imm_dec)
		generate_log(mnemonic)
	#rs2 rs1 rd (pg 36) ok
	if (inst == 'srl'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#rd
		shamt = value_rs2_bin[27:]
		shamt_dec = value_rs2_dec = int(shamt, 2)
		value_rd_bin = '0'*shamt_dec+value_rs1_bin
		value_rd_bin = value_rd_bin[:32]
		value_rd_dec = int(str(value_rd_bin),2)
		value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[12|10:5] rs2 rs1 imm[4:1|11] (pg 17) ok
	if (inst == 'beq'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		if value_rs2_bin[0] == '1':
			value_rs2_dec = (-1)*(2**len(value_rs2_bin) - value_rs2_dec)
		#imm
		imm = inst_bin[0]+inst_bin[24]+inst_bin[1:7]+inst_bin[20:24]+'0'
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = -1*(2**len(imm) - imm_dec)
		#branch
		if (value_rs1_dec == value_rs2_dec):
			PC = hex(int(PC, 16) + imm_dec)[2:].zfill(8)
		else:
			PC = hex(int(PC, 16) + 4)[2:].zfill(8)
		mnemonic = register_names[rs1_int]+','+register_names[rs2_int]+','+str(imm_dec)
		generate_log(mnemonic)
	#rs2 rs1 rd (pg 36) ok
	if (inst == 'sll'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#rd
		shamt = value_rs2_bin[27:]
		shamt_dec = value_rs2_dec = int(shamt, 2)
		value_rd_bin = value_rs1_bin+'0'*shamt_dec
		value_rd_bin = value_rd_bin[shamt_dec:]
		value_rd_dec = int(str(value_rd_bin),2)
		value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#rs2 rs1 rd (pg 14) ok
	if (inst == 'or'):
		#rs1
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#rs2
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#rd
		value_rd_bin = ''
		for i in range(32):
			value_rd_bin = value_rd_bin + str(int(value_rs1_bin[i])|int(value_rs2_bin[i]))
		value_rd_dec = int(str(value_rd_bin),2)
		if value_rd_bin[0] == '1':
			value_rd_dec = (-1)*(2**len(value_rd_bin) - value_rd_dec)
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#rs2 rs1 rd (pg 36) ok
	if (inst == 'remu'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#if value_rs1_bin[0] == '1':
		#	value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#if value_rs2_bin[0] == '1':
		#	value_rs2_dec = (-1)*(2**len(value_rs2_bin) - value_rs2_dec)
		#rd
		if (value_rs2_dec != 0):
			value_rd_dec = value_rs1_dec%value_rs2_dec
		else:
			value_rd_dec = 0
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[12|10:5] rs2 rs1 imm[4:1|11] (pg 17) ok
	if (inst == 'bltu'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#imm
		imm = inst_bin[0]+inst_bin[24]+inst_bin[1:7]+inst_bin[20:24]+'0'
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = -1*(2**len(imm) - imm_dec)
		#branch
		if (value_rs1_dec < value_rs2_dec):
			PC = hex(int(PC, 16) + imm_dec)[2:].zfill(8)
		else:
			PC = hex(int(PC, 16) + 4)[2:].zfill(8)
		mnemonic = register_names[rs1_int]+','+register_names[rs2_int]+','+str(imm_dec)
		generate_log(mnemonic)
	#rs2 rs1 rd (pg 14) ok
	if (inst == 'and'):
		#rs1
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#rs2
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#rd
		value_rd_bin = ''
		for i in range(32):
			value_rd_bin = value_rd_bin + str(int(value_rs1_bin[i])&int(value_rs2_bin[i]))
		value_rd_dec = int(str(value_rd_bin),2)
		if value_rd_bin[0] == '1':
			value_rd_dec = (-1)*(2**len(value_rd_bin) - value_rd_dec)
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#000000000001 00000 000 00000 1110011 (pg 24)
	if (inst == 'ebreak'):
		mnemonic = ''
		generate_log(mnemonic)
		PC = '20000000'
	#rs2 rs1 rd (pg 15) ok
	if (inst == 'xor'):
		#rs1
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#rs2
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#rd
		value_rd_bin = ''
		for i in range(32):
			value_rd_bin = value_rd_bin + str(int(value_rs1_bin[i])^int(value_rs2_bin[i]))
		value_rd_dec = int(str(value_rd_bin),2)
		if value_rd_bin[0] == '1':
			value_rd_dec = (-1)*(2**len(value_rd_bin) - value_rd_dec)
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#rs2 rs1 rd (pg 15) ok
	if (inst == 'slt'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		if value_rs2_bin[0] == '1':
			value_rs2_dec = (-1)*(2**len(value_rs2_bin) - value_rs2_dec)
		#rd
		if(value_rs1_dec < value_rs2_dec):
			value_rd_dec = 1
		else:
			value_rd_dec = 0
		value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 13) ok
	if (inst == 'slti'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		
		if imm[0] == '1': #sext
			imm = '1'*20 + imm
			imm_dec = int(imm, 2)
			imm_dec = (-1)*(2**len(imm) - imm_dec)
		#rd
		if (value_rs1_dec < imm_dec):
			value_rd_dec = 1
		else:
			value_rd_dec = 0
		value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+str(imm_dec)+'('+register_names[rs1_int]+')'
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[11:0] rs1 rd (pg 13) ok
	if (inst == 'ori'):
		#rs1
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#imm
		imm = inst_bin[0:12]
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = (-1)*(2**len(imm) - imm_dec)
			kind = 'neg'
		else:
			kind = 'pos'
		#rd
		if(kind == 'neg'):
			imm = '1'*20 + imm
			#print(imm)
		else:
			imm = imm.zfill(32)
		value_rd_bin = ''
		for i in range(32):
			value_rd_bin = value_rd_bin + str(int(value_rs1_bin[i])|int(imm[i]))
		value_rd_dec = int(str(value_rd_bin),2)
		if value_rd_bin[0] == '1':
			value_rd_dec = (-1)*(2**len(value_rd_bin) - value_rd_dec)
		if(value_rd_dec < 0):
			value_rd = hex(value_rd_dec & (2**32-1))[2:].zfill(8)
		else:
			value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+str(imm_dec)
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#rs2 rs1 rd (pg 15) ok
	if (inst == 'sra'):
		#rs1
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		#rs2
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		#rd
		shamt = value_rs2_bin[27:]
		shamt_dec = int(shamt, 2)
		if value_rs1_bin[0] == '1':
			value_rd_bin = '1'*shamt_dec+value_rs1_bin
		else:
			value_rd_bin = '0'*shamt_dec+value_rs1_bin
		value_rd_bin = value_rd_bin[:32]
		value_rd_dec = int(str(value_rd_bin),2)
		value_rd = hex(value_rd_dec)[2:].zfill(8)
		if (rd_int == 0):
			value_rd = '0'*8
		registers[rd_int] = value_rd
		#log
		mnemonic = register_names[rd_int]+','+register_names[rs1_int]+','+register_names[rs2_int]
		generate_log(mnemonic)
		PC = hex(int(PC, 16) + 4)[2:].zfill(8)
	#imm[12|10:5] rs2 rs1 imm[4:1|11] (pg 17) ok
	if (inst == 'blt'):
		#rs1
		value_rs1_dec = int(value_rs1, 16)
		value_rs1_bin = bin(int(value_rs1, 16))[2:].zfill(32)
		if value_rs1_bin[0] == '1':
			value_rs1_dec = (-1)*(2**len(value_rs1_bin) - value_rs1_dec)
		#rs2
		value_rs2_dec = int(value_rs2, 16)
		value_rs2_bin = bin(int(value_rs2, 16))[2:].zfill(32)
		if value_rs2_bin[0] == '1':
			value_rs2_dec = (-1)*(2**len(value_rs2_bin) - value_rs2_dec)
		#imm
		imm = inst_bin[0]+inst_bin[24]+inst_bin[1:7]+inst_bin[20:24]+'0'
		imm_dec = int(imm, 2)
		if imm[0] == '1':
			imm_dec = -1*(2**len(imm) - imm_dec)
		#branch
		if (value_rs1_dec < value_rs2_dec):
			PC = hex(int(PC, 16) + imm_dec)[2:].zfill(8)
		else:
			PC = hex(int(PC, 16) + 4)[2:].zfill(8)
		mnemonic = register_names[rs1_int]+','+register_names[rs2_int]+','+str(imm_dec)
		generate_log(mnemonic)

def generate_log(mnemonic):
	log = 'PC='+str(PC.upper())+' ['+inst_hex.upper()+'] X'+"{:02d}".format(rd_int)+'='+str(value_rd).upper()+' X'+"{:02d}".format(rs1_int)+'='+str(value_rs1).upper()+' X'+"{:02d}".format(rs2_int)+'='+str(value_rs2).upper()+" {:<8}".format(inst_decoded)+mnemonic
	logs.append(log)
	#print(logs)


for code in dirs:
	#Reseta as variaveis
	while_key = True
	start_time = time.time()
	ciclos = 0
	#print(dirs)
	num_of_inst = 0
	memory = {}
	instructions = []
	registers = [0]*32
	for i in range(32):
		registers[i] = hex(0)[2:].zfill(8)
	logs = []

	#Carrega as instruções e salva na memória
	f = open("test/objdump/"+code, "r")
	instruction_list = f.read()
	split_line_instruction = instruction_list.splitlines()
	for i in split_line_instruction:
		if (i == ''):
			continue
		elif (i[0] != ' '):
			continue
		i = i.replace(" ", "")
		i = i.replace(":", "")
		#i.strip()
		i = i.split(sep="	")
		#print(i)
		instructions.append(i)
		num_of_inst = num_of_inst + 1
		memory_access('store',hex(int(i[0], 16))[2:].zfill(8),i[1])
	#define o PC inicial
	PC = hex(int(instructions[0][0], 16))[2:].zfill(8)
	#print(instructions)
	#salvar instruções na memória

	#Ciclo de Fetch-decode-execute
	while(while_key):
		#Fetch
		if PC == '20000000':
			with open("logs/"+code+".log", 'w') as f:
				f.write('\n'.join(logs))
				#print(code)
				#print(logs)
				statistic = {'Time per cicle (microseconds)': float("{:.2f}".format(((time.time() - start_time)/ciclos)*10**6)), 'Code': str(code), 'Cicles': ciclos, 'Execution time (milliseconds)': "{:.2f}".format((time.time() - start_time)*10**3)}
				statistics.append(statistic)
				#print("--- code: %s, cicles: %d, time: %s seconds ---" % (code, ciclos, time.time() - start_time))
				while_key = False
				continue
		inst_hex = memory_access('load',PC, '')
		
		#Decode
		inst_bin = bin(int(inst_hex, 16))[2:].zfill(32)
		opcode = inst_bin[25::]
		rd = inst_bin[20:25]
		rd_int = int(rd,2)
		func3 = inst_bin[17:20]
		value_rd = registers[rd_int]
		rs1 = inst_bin[12:17]
		rs1_int = int(rs1,2)
		value_rs1 = registers[rs1_int]
		rs2 = inst_bin[7:12]
		rs2_int = int(rs2,2)
		value_rs2 = registers[rs2_int]
		func7 = inst_bin[:7]
		#print(opcode)
		if(opcode == '0110111'): #lui
			#print("lui")
			inst_decoded = 'lui'
		elif(opcode == '0010111'): #auipc
			#print("auipc")
			inst_decoded = 'auipc'
		elif(opcode == '1101111'): #jal
			#print("jal")
			inst_decoded = 'jal'
		elif(opcode == '0010011' and func3 == '000'): #addi
			#print("addi")
			inst_decoded = 'addi'
		elif(opcode == '0010011' and func3 == '100'): #xori
			#print("xori")
			inst_decoded = 'xori'
		elif(opcode == '0010011' and func3 == '111'): #andi
			#print("andi")
			inst_decoded = 'andi'
		elif(opcode == '0010011' and func3 == '110'): #ori
			#print("ori")
			inst_decoded = 'ori'
		elif(opcode == '0100011' and func3 == '010'): #sw
			#print("sw")
			inst_decoded = 'sw'
		elif(opcode == '0100011' and func3 == '000'): #sb
			#print("sb")
			inst_decoded = 'sb'
		elif(opcode == '0100011' and func3 == '001'): #sh
			#print("sh")
			inst_decoded = 'sh'
		elif(opcode == '0000011' and func3 == '010'): #lw
			#print("lw")
			inst_decoded = 'lw'
		elif(opcode == '0000011' and func3 == '000'): #lb
			#print("lb")
			inst_decoded = 'lb'
		elif(opcode == '0000011' and func3 == '001'): #lh
			#print("lh")
			inst_decoded = 'lh'
		elif(opcode == '0000011' and func3 == '100'): #lbu
			#print("lbu")
			inst_decoded = 'lbu'
		elif(opcode == '0000011' and func3 == '101'): #lhu
			#print("lhu")
			inst_decoded = 'lhu'
		elif(opcode == '0010011' and func3 == '001' and func7 == '0000000'): #slli
			#print("slli")
			inst_decoded = 'slli'
		elif(opcode == '0010011' and func3 == '011'): #sltiu
			#print("sltiu")
			inst_decoded = 'sltiu'
		elif(opcode == '0010011' and func3 == '010'): #slti
			#print("slti")
			inst_decoded = 'slti'
		elif(opcode == '0010011' and func3 == '101' and func7 == '0000000'): #srli
			#print("srli")
			inst_decoded = 'srli'
		elif(opcode == '0010011' and func3 == '101' and func7 == '0100000'): #srai
			#print("srai")
			inst_decoded = 'srai'
		elif(opcode == '0110011' and func3 == '000' and func7 == '0000000'): #add
			#print("add")
			inst_decoded = 'add'
		elif(opcode == '0110011' and func3 == '000' and func7 == '0100000'): #sub
			#print("sub")
			inst_decoded = 'sub'
		elif(opcode == '0110011' and func3 == '000' and func7 == '0000001'): #mul
			#print("mul")
			inst_decoded = 'mul'
		elif(opcode == '0110011' and func3 == '011' and func7 == '0000001'): #mulhu
			#print("mulhu")
			inst_decoded = 'mulhu'
		elif(opcode == '0110011' and func3 == '100' and func7 == '0000001'): #div
			#print("div")
			inst_decoded = 'div'
		elif(opcode == '0110011' and func3 == '101' and func7 == '0000001'): #divu
			#print("divu")
			inst_decoded = 'divu'
		elif(opcode == '0110011' and func3 == '101' and func7 == '0000000'): #srl
			#print("srl")
			inst_decoded = 'srl'
		elif(opcode == '0110011' and func3 == '101' and func7 == '0100000'): #sra
			#print("sra")
			inst_decoded = 'sra'
		elif(opcode == '0110011' and func3 == '001' and func7 == '0000000'): #sll
			#print("sll")
			inst_decoded = 'sll'
		elif(opcode == '0110011' and func3 == '011' and func7 == '0000000'): #sltu
			#print("sltu")
			inst_decoded = 'sltu'
		elif(opcode == '0110011' and func3 == '010' and func7 == '0000000'): #slt
			#print("slt")
			inst_decoded = 'slt'
		elif(opcode == '0110011' and func3 == '110' and func7 == '0000000'): #or
			#print("or")
			inst_decoded = 'or'
		elif(opcode == '0110011' and func3 == '111' and func7 == '0000000'): #and
			#print("and")
			inst_decoded = 'and'
		elif(opcode == '0110011' and func3 == '100' and func7 == '0000000'): #xor
			#print("xor")
			inst_decoded = 'xor'
		elif(opcode == '0110011' and func3 == '111' and func7 == '0000001'): #remu
			#print("remu")
			inst_decoded = 'remu'
		elif(opcode == '1100111' and func3 == '000'): #jalr
			#print("jalr")
			inst_decoded = 'jalr'
		elif(opcode == '1100011' and func3 == '101'): #bge
			#print("bge")
			inst_decoded = 'bge'
		elif(opcode == '1100011' and func3 == '111'): #bgeu
			#print("bgeu")
			inst_decoded = 'bgeu'
		elif(opcode == '1100011' and func3 == '001'): #bne
			#print("bne")
			inst_decoded = 'bne'
		elif(opcode == '1100011' and func3 == '000'): #beq
			#print("beq")
			inst_decoded = 'beq'
		elif(opcode == '1100011' and func3 == '110'): #bltu
			#print("bltu")
			inst_decoded = 'bltu'
		elif(opcode == '1100011' and func3 == '100'): #blt
			#print("blt")
			inst_decoded = 'blt'
		elif(opcode == '1110011' and func3 == '000' and func7 == '0000000' and rd == '00000' and rs1 == '00000' and rs2 == '00001'): #ebreak
			#print("ebreak")
			inst_decoded = 'ebreak'
		else:
			break	 
		
		#execute
		ciclos += 1
		exec_inst(inst_decoded)

def sort(e):
	return e['Time per cicle (microseconds)']

statistics.sort(key=sort) 

with open("estatísticas.txt", 'w') as f:
	f.write(json.dumps(statistics, indent = 4))
	print("Finalizado")
	
	#paginas importantes
	# RV32I Base Instruction Set - 104
	# RV32M Standard Extension - 105
	# Assembler mnemonics - 109
