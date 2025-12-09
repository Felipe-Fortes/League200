from flask import jsonify, redirect, url_for
from frontend import app
from main import get_stats, update_stats

# rotas
@app.route('/')
def homepage():
    stats = get_stats()
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>League 200 - High Elo Lane Stats</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}
            h1 {{
                text-align: center;
                color: #333;
                margin-bottom: 10px;
            }}
            .subtitle {{
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 14px;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .stat-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }}
            .stat-card h3 {{
                margin: 0 0 10px 0;
                font-size: 14px;
                text-transform: uppercase;
                opacity: 0.9;
            }}
            .stat-card .points {{
                font-size: 32px;
                font-weight: bold;
                margin: 0;
            }}
            .last-update {{
                text-align: center;
                color: #999;
                font-size: 12px;
                margin-top: 20px;
            }}
            .button {{
                display: block;
                width: 200px;
                margin: 20px auto;
                padding: 10px;
                background: #667eea;
                color: white;
                text-align: center;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                text-decoration: none;
            }}
            .button:hover {{
                background: #764ba2;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚔️ League 200</h1>
            <p class="subtitle">High Elo Lane Performance Analysis</p>
            
            <div class="stats-grid">
                <div class="stat-card">
                    <h3>Top Lane</h3>
                    <p class="points">{stats['top']}</p>
                </div>
                <div class="stat-card">
                    <h3>Jungle</h3>
                    <p class="points">{stats['jungle']}</p>
                </div>
                <div class="stat-card">
                    <h3>Mid Lane</h3>
                    <p class="points">{stats['mid']}</p>
                </div>
                <div class="stat-card">
                    <h3>ADC</h3>
                    <p class="points">{stats['adc']}</p>
                </div>
                <div class="stat-card">
                    <h3>Support</h3>
                    <p class="points">{stats['support']}</p>
                </div>
            </div>
            
            <a href="/api/stats" class="button">Ver JSON</a>
            <a href="/update" class="button">Atualizar Agora</a>
            
            <div class="last-update">
                Última atualização: {stats['last_update'] or 'Nunca'}
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/about')
def about():
    return """
    <h1>League 200</h1>
    <p>Análise diária do desempenho de lanes em High Elo (Challenger)</p>
    <p>O site atualiza automaticamente todos os dias para fornecer estatísticas precisas.</p>
    """

@app.route('/api/stats')
def api_stats():
    """Retorna as estatísticas em formato JSON."""
    return jsonify(get_stats())

@app.route('/update')
def manual_update():
    """Permite atualização manual das estatísticas e redireciona para home."""
    try:
        update_stats()
        return redirect(url_for('homepage'))
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

