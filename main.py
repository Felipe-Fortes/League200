import requests
from datetime import datetime

# Configurações
SOLOQ = 420
FLEX = 440
NORMAL = 430

RIOT_API = "RGAPI-7840be6d-e40b-4f07-a200-c769b48fb0c9"

# Variáveis globais para armazenar dados
current_stats = {
    "top": 0,
    "jungle": 0,
    "mid": 0,
    "adc": 0,
    "support": 0,
    "last_update": None
}

dicionariopartidas = {}


def fetch_challenger_players(queue_type=SOLOQ):
    """Busca os 40 jogadores challenger no BR."""
    API_URL = f"https://br1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={RIOT_API}"
    
    try:
        resp = requests.get(API_URL, timeout=10)
        resp.raise_for_status()
        challinform = resp.json()
        
        dicionariolol = {}
        lista_chall = []
        
        for i in range(min(40, len(challinform.get('entries', [])))):
            puuid = challinform['entries'][i]['puuid']
            lista_chall.append(puuid)
            dicionariolol[puuid] = i + 1
        
        return dicionariolol, sorted(lista_chall)
    except Exception as e:
        print(f"Erro ao buscar jogadores challenger: {e}")
        return {}, []


def analyze_matches(dicionariolol, sorted_lista_chall, queue_type=SOLOQ, match_count=20):
    """Analisa as partidas dos jogadores challenger e calcula pontos por lane."""
    
    stats = {
        "top": 0,
        "jungle": 0,
        "mid": 0,
        "adc": 0,
        "support": 0
    }
    
    if not dicionariolol:
        return stats
    
    # Pega PUUIDs de alguns jogadores para buscar partidas
    first_players = list(dicionariolol.keys())[:5]
    
    for player_puuid in first_players:
        try:
            API_URL_MATCH = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{player_puuid}/ids?queue={queue_type}&start=0&count={match_count}&api_key={RIOT_API}"
            resp = requests.get(API_URL_MATCH, timeout=10)
            resp.raise_for_status()
            matchinfo = resp.json()
            
            for matchid in matchinfo:
                if matchid in dicionariopartidas:
                    continue
                
                dicionariopartidas[matchid] = True
                
                try:
                    API_URL_DETAIL = f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={RIOT_API}"
                    resp_detail = requests.get(API_URL_DETAIL, timeout=10)
                    resp_detail.raise_for_status()
                    matchdetail = resp_detail.json()
                    
                    # Processa participantes
                    for i in range(min(10, len(matchdetail.get('info', {}).get('participants', [])))):
                        participant = matchdetail['info']['participants'][i]
                        puuid = participant['puuid']
                        
                        if puuid in sorted_lista_chall:
                            position = participant.get('teamPosition', '')
                            rank = dicionariolol[puuid]
                            points = 201 - rank
                            
                            # Mapear posições para lanes
                            if position == 'TOP':
                                stats['top'] += points
                            elif position == 'JUNGLE':
                                stats['jungle'] += points
                            elif position == 'MIDDLE':
                                stats['mid'] += points
                            elif position == 'BOTTOM':
                                stats['adc'] += points
                            elif position == 'UTILITY':
                                stats['support'] += points
                
                except Exception as e:
                    print(f"Erro ao processar partida {matchid}: {e}")
                    continue
        
        except Exception as e:
            print(f"Erro ao buscar partidas do jogador {player_puuid}: {e}")
            continue
    
    return stats


def update_stats():
    """Executa a análise completa e atualiza as estatísticas."""
    global current_stats
    
    print(f"[{datetime.now()}] Iniciando atualização de estatísticas...")
    
    try:
        # Busca jogadores challenger
        dicionariolol, sorted_lista_chall = fetch_challenger_players()
        
        if not dicionariolol:
            print("Falha ao buscar jogadores challenger")
            return
        
        # Analisa partidas
        stats = analyze_matches(dicionariolol, sorted_lista_chall)
        
        # Atualiza dados globais
        current_stats = {
            "top": stats['top'],
            "jungle": stats['jungle'],
            "mid": stats['mid'],
            "adc": stats['adc'],
            "support": stats['support'],
            "last_update": datetime.now().isoformat()
        }
        
        print(f"Estatísticas atualizadas:")
        print(f"Top: {stats['top']}")
        print(f"Jungle: {stats['jungle']}")
        print(f"Mid: {stats['mid']}")
        print(f"ADC: {stats['adc']}")
        print(f"Support: {stats['support']}")
    
    except Exception as e:
        print(f"Erro ao atualizar estatísticas: {e}")


def get_stats():
    """Retorna as estatísticas atuais."""
    return current_stats


