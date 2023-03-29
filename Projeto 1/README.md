# Projeto 1
Projeto da disciplina MO601 (Arquitetura de Computadores II)

## Ambiente
Esse algoritmo foi testado e desenvolvido no sistema operacional Ubuntu 18.04 LTS, usando a linguagem de programação Python versão 3.6.9, não foi usada nenhuma biblioteca externa, apenas as bibliotecas nativas "csv" e "os". Esse ambiente foi simulado dentro de um dockerfile, portanto só é necessário ter o pacote docker.io instalado, caso não possua usar os seguintes comandos para instalá-lo no ubuntu:

```
sudo apt update
sudo apt install docker.io
systemctl start docker
systemctl enable docker
```

## Execução

Clonar esse repositório em sua pasta de preferência. Acessar esta pasta e inserir os testes na pasta **test** dentro de subpastas, em cada subpasta deve ser colocado os arquivos "circuito.hdl", "estimulos.txt", "esperado0.csv" e "esperado1.csv", caso algum deles esteja faltando o algoritmo não funcionará corretamente.

Com os testes adicionados, acessar a pasta raiz **Projeto 1** e executar no terminal os comandos:
```
sudo docker build -t ubuntu-docker .
# cria a imagem necessária para a execução do algoritmo dentro do docker, esse processo pode demorar um pouco.

sudo docker image ls
# lista as imagens criadas, verificar se a imagem "ubuntu-docker" foi criada corretamente.

sudo docker run -v /home/fabricio/mo601a/Projeto\ 1:/home ubuntu-docker
# executa a imagem criada, lembrar de substituir na linha de cima "/home/fabricio" pelo diretório onde foi clonado o repositório.
```

Durante a execução é possível acompanhar pelo terminal qual subpasta está sendo analisada e se o algoritmo funcionou corretamente após receber a mensagem "ok", caso aconteça algum erro durante a execução dessa subpasta aparecerá a mensagem "error".

Após executar o docker, dentro de cada subpasta da pasta **test** será criado um alquivo chamado "saida0.csv" e "saida1.csv" que devem ser comparados respectivamente com os arquivos "esperado0.csv" e "esperado1.csv" para verificar se os circuitos foram simulados corretamente. Sempre garantir que os arquivos "esperado 0 e 1.csv" estejam corretos, já que eles são os responsáveis pela validação do simulador.
