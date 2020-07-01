<h1 align="center">
    Rock-Paper-Scissors Game
</h1>

<p align="center">
    <img width="40%" src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRP8bQAWR6JLBQP0Pg7GB-1c8YaKCwvz9ztrhwN5vjFO3MiExon&usqp=CAU" alt="Rock Paper Scissors Image"/>
</p>

<p align="center">
  <a href="#computer-projeto">Projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#dart-objetivos">Objetivos</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#boom-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#warning-regras-do-jogo">Regras do Jogo</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#mortar_board-como-executar-o-projeto">Como executar</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#family-como-contribuir">Como contribuir</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#memo-licença">Licença</a>
</p>

_________

### :computer: Projeto

<p align="justify">
Este é um desafio com o intuito de desenvolver uma aplicação distribuída que permite n jogadores participarem do jogo pedra, papel e tesoura. Cada jogador será considerado um cliente de uma arquitetura Cliente/Servidor e irá se comunicar com “Controlador do Jogo” que coordena o jogo.
</p>

### :dart: Objetivos

- Familiarizar-se com a programação utilizando a [API socket](https://docs.python.org/3/library/socket.html);<br>
- Implementar um protocolo para simular o jogo pedra, papel e tesoura, com n jogadores;<br>
- Enviar e receber dados em uma aplicação que utiliza a arquitetura Cliente/Servidor.

### :boom: Tecnologias

Esse projeto foi desenvolvido com as seguintes tecnologias:

- [Python](https://www.python.org/)

### :warning: Regras do Jogo

1. Papel ganha de Pedra;
2. Pedra ganha de Tesoura;
3. Tesoura ganha de Papel;
4. Um jogador somente será declarado eliminado se e somente se for derrotado por todos os seus oponentes em uma jogada;
5. Um jogador somente será declarado vencedor se e somente se vencer todos os seus oponentes em uma jogada.

### :mortar_board: Como executar o projeto

- Faça um clone deste repositório: `git clone https://github.com/maykew/RockPaperScissorsGame`;
- Entre no diretório;
- Abra um terminal e inicialize o servidor: `python servidor.py`;
- Abra um novo terminal e inicialize o primeiro cliente: `python cliente.py`;
- Abra um novo terminal e inicialize o segundo cliente: `python cliente.py`;
- Abra um novo terminal e inicialize o terceiro cliente: `python cliente.py`;

Caso deseje alterar o número de jogadores, entre no código do servidor e atualize a variável numJogadores (lembre-se que cada jogador deve ser inicializado em um novo terminal).

### :family: Como contribuir

- Faça um fork desse repositório;
- Cria uma branch com a sua feature: `git checkout -b minha-feature`;
- Faça commit das suas alterações: `git commit -m 'feat: Minha nova feature'`;
- Faça push para a sua branch: `git push origin minha-feature`.

Depois que o merge da sua pull request for feito, você pode deletar a sua branch.

### :memo: Licença

Esse projeto está sob a licença MIT. Veja o arquivo [LICENSE](https://github.com/maykew/RockPaperScissorsGame/blob/master/LICENSE.md) para mais detalhes.
_________

<h4 align="center"> ♥ by Mayke Willans ♥ </h4>
