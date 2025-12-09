from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from main import update_stats
import atexit

app = Flask(__name__)

# Configurar scheduler para atualizar estatísticas diariamente
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=update_stats,
    trigger="cron",
    hour=0,  # Executa à meia-noite (00:00)
    minute=0,
    id='daily_update',
    name='Atualização diária de estatísticas'
)
scheduler.start()

# Garante que o scheduler seja parado quando a aplicação fechar
atexit.register(lambda: scheduler.shutdown())

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
