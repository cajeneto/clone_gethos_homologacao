from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Configura o ambiente do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gethosapp.settings')

# Cria a instância do Celery
app = Celery('gethosapp')

# Lê as configurações do Celery do arquivo settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['gethos_home', 'cadastros', 'processos'])

# Autodiscovery para localizar tarefas definidas em 'tasks.py'
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
