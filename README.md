# Desafio Tecnico

Sistema que simula uma conta bancaria com transação de Debito e Credito
Sistema de debito funcionando por Deposito e Compra no Debito
Sistema de credito funcionando com base na fatura, fatura que vence a cada 20 minutos controlada por um task schedule, com bloqueio do limite e limite de credito. E pagamento da fatura realizado a partir do Saldo da conta.

## Instalação

```bash
# Clone o repositorio:
git clone https://github.com/MauroTony/backend-bancoapi.git

# Entre na pasta
cd backend-bancoapi

# Instale as dependências
pip install -r requirements.txt


OBS: Projeto feito utilizando o Banco de dados PostgreSQL, preferencialmente utilize o mesmo se possivel.
# Configurar a .env
Criar .env no mesmo diretorio em que se encontra o settings.py
Adicionar na .env as seguintes variaveis:

DATABASE_NAME=<database>
DATABASE_USER=<username>
DATABASE_PASS=<password>
DATABASE_HOST=<host_or_ip
DATABASE_PORT=<port>

# Realizar migrações
python manage.py makemigrations
python manage.py migrate

# Criar registros pre definidos
Executar no terminal o comando python manage.py shell

from banco_api.models import StatusFatura
StatusFatura.objects.create(status_id=1, descricao="Fatura fechada")
StatusFatura.objects.create(status_id=2, descricao="Fatura aberta")
StatusFatura.objects.create(status_id=3, descricao="Fatura vencida")
from banco_api.models import TipoTransacao
TipoTransacao.objects.create(codigo_tipo=1, descricao="Debito")
TipoTransacao.objects.create(codigo_tipo=2, descricao="Deposito")
TipoTransacao.objects.create(codigo_tipo=3, descricao="Credito")
TipoTransacao.objects.create(codigo_tipo=4, descricao="Pagamento da Fatura")
from django_q.models import Schedule
Schedule.objects.create(func="banco_api.schedules.faturas", minutes=1, repeats=-1, schedule_type="I")

# Execute o servidor
python manage.py runserver
# Em outro terminal executar (Essencial)
 python manage.py qcluster
 
```
Documentação da api explicada no link abaixo
https://documenter.getpostman.com/view/19154738/VUjLM7PJ
