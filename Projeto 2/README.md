# Projeto 2
Projeto da disciplina MO601 (Arquitetura de Computadores II)

## Ambiente
Esse algoritmo foi testado e desenvolvido no sistema operacional Ubuntu 18.04 LTS, usando a linguagem de programação Python versão 3.6.9, não foi usada nenhuma biblioteca externa, apenas as bibliotecas nativas "time", "json" e "os". Além disso foi usado o toolchain para riscv, caso não possua usar o seguinte comando para instalá-lo no ubuntu:

```
sudo apt-get install -y gcc-riscv64-linux-gnu
```

## Execução

Clonar esse repositório em sua pasta de preferência. Acessar a pasta raiz desse repositório e executar no terminal o comando:

```
. bash.sh
```

Após executar o bash, dentro da subpasta **test** será criado a pasta **riscv** e **objdump**. Em seguida será executado o bash **compilar.sh** que criará os executáveis dentro da pasta "riscv" e para cada executável, será executado o comando **riscv64-linux-gnu-objdump** que armazenará o resultado na pasta "objdump". Após isso ele retorna para a raiz do repositório e será criada uma pasta chamada **logs** e o código **simulador.py** será executado, armazenando os logs gerados nessa pasta com o formato ".log" além de criar o arquivo "estatísticas.txt" que mostra o tempo total de execução, número de ciclos e tempo por ciclo de cada um dos códigos executados.
