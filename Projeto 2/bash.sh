#!/bin/bash
cd test
mkdir riscv
mkdir objdump 
. compilar.sh
cd riscv
for file in *.riscv ; do riscv64-linux-gnu-objdump -d $file > ../objdump/${file//.riscv/}; done
cd ../..
mkdir logs
python3 simulador.py