README - SkillCraft

Requisitos

- Python instalado
- Git (para clonar o repositório)
- Ambiente virtual (recomendado)

2. Criar e ativar o ambiente virtual:

Windows:
python -m venv venv
.env\Scriptsctivate

Mac/Linux:
python3 -m venv venv
source venv/bin/activate

3. Instalar as dependências que estão no ficheiro "requirements.txt":

pip install -r requirements.txt

4. Aplicar as migrações da base de dados:

python manage.py migrate


4. Como executar o projeto:

Passo 1: Iniciar o servidor HTTP

python manage.py runserver

Passo 2: Iniciar o servidor WebSocket (para o chat)

Numa outra shell copiar o código que está em baixo, com o mesmo ambiente virtual ativado:

daphne -p 8001 skillcraft.asgi:application


Notas

- O projeto usa ImageField, por isso é necessário o pacote Pillow.
- O chat em tempo real funciona via WebSocket, através de Django Channels.
- Não é necessário Redis, pois está a usar InMemoryChannelLayer.

Suporte

Este projeto foi desenvolvido para fins académicos.
Em caso de dúvidas, contactar: skillcraft.suporte.staff@gmail.com
