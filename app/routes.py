from fastapi import APIRouter, HTTPException, status
from app.models import (
    TeamCreate, Team, TeamResponse, PlayerCreate, Player, PlayerResponse,
    CoachCreate, Coach, CoachResponse, GameCreate, Game, GameSummaryResponse,
    PlayerStatCreate, PlayerStat, TeamStatCreate, TeamStat
)
from app.database import get_db_connection
from typing import List
import mysql.connector

router = APIRouter()

# Team Endpoints
@router.post("/teams/", response_model=Team, tags=["Teams"])
def create_team(team: TeamCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO teams (team_name, city, stadium, founded_year)
        VALUES (%s, %s, %s, %s)
        """
        values = (team.team_name, team.city, team.stadium, team.founded_year)
        cursor.execute(query, values)
        conn.commit()
        team_id = cursor.lastrowid
        return Team(team_id=team_id, **team.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/teams/", response_model=List[TeamResponse], tags=["Teams"])
def list_teams():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT team_name, city FROM teams"
        cursor.execute(query)
        teams = cursor.fetchall()
        return teams
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/teams/bulk/", response_model=List[Team], tags=["Teams"])
def create_teams_bulk(teams: List[TeamCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO teams (team_name, city, stadium, founded_year)
        VALUES (%s, %s, %s, %s)
        """
        values = [(t.team_name, t.city, t.stadium, t.founded_year) for t in teams]
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        team_ids = range(last_id - len(teams) + 1, last_id + 1)
        
        return [Team(team_id=tid, **t.dict()) for tid, t in zip(team_ids, teams)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Player Endpoints
@router.post("/players/", response_model=Player, tags=["Players"])
def create_player(player: PlayerCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO players (first_name, last_name, position, jersey_number, team_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (player.first_name, player.last_name, player.position, player.jersey_number, player.team_id)
        cursor.execute(query, values)
        conn.commit()
        player_id = cursor.lastrowid
        return Player(player_id=player_id, **player.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/players/", response_model=List[PlayerResponse], tags=["Players"])
def list_players():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT first_name, last_name, position FROM players"
        cursor.execute(query)
        players = cursor.fetchall()
        return players
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/players/bulk/", response_model=List[Player], tags=["Players"])
def create_players_bulk(players: List[PlayerCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO players (first_name, last_name, position, jersey_number, team_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = [(p.first_name, p.last_name, p.position, p.jersey_number, p.team_id) for p in players]
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        player_ids = range(last_id - len(players) + 1, last_id + 1)
        
        return [Player(player_id=pid, **p.dict()) for pid, p in zip(player_ids, players)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Coach Endpoints
@router.post("/coaches/", response_model=Coach, tags=["Coaches"])
def create_coach(coach: CoachCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO coaches (first_name, last_name, role, team_id)
        VALUES (%s, %s, %s, %s)
        """
        values = (coach.first_name, coach.last_name, coach.role, coach.team_id)
        cursor.execute(query, values)
        conn.commit()
        coach_id = cursor.lastrowid
        return Coach(coach_id=coach_id, **coach.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/coaches/", response_model=List[CoachResponse], tags=["Coaches"])
def list_coaches():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT first_name, last_name, role FROM coaches"
        cursor.execute(query)
        coaches = cursor.fetchall()
        return coaches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/coaches/bulk/", response_model=List[Coach], tags=["Coaches"])
def create_coaches_bulk(coaches: List[CoachCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO coaches (first_name, last_name, role, team_id)
        VALUES (%s, %s, %s, %s)
        """
        values = [(c.first_name, c.last_name, c.role, c.team_id) for c in coaches]
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        coach_ids = range(last_id - len(coaches) + 1, last_id + 1)
        
        return [Coach(coach_id=cid, **c.dict()) for cid, c in zip(coach_ids, coaches)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Game Endpoints
@router.post("/games/", response_model=Game, tags=["Games"])
def create_game(game: GameCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO games (home_team_id, away_team_id, game_date, home_team_score, away_team_score)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (game.home_team_id, game.away_team_id, game.game_date, game.home_team_score, game.away_team_score)
        cursor.execute(query, values)
        conn.commit()
        game_id = cursor.lastrowid
        return Game(game_id=game_id, **game.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/games/", response_model=List[GameSummaryResponse], tags=["Games"])
def list_games():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT game_date, home_team_score, away_team_score FROM games"
        cursor.execute(query)
        games = cursor.fetchall()
        return games
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.post("/games/bulk/", response_model=List[Game], tags=["Games"])
def create_games_bulk(games: List[GameCreate]):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO games (home_team_id, away_team_id, game_date, home_team_score, away_team_score)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = [(g.home_team_id, g.away_team_id, g.game_date, g.home_team_score, g.away_team_score) for g in games]
        cursor.executemany(query, values)
        conn.commit()
        
        cursor.execute("SELECT LAST_INSERT_ID()")
        last_id = cursor.fetchone()[0]
        game_ids = range(last_id - len(games) + 1, last_id + 1)
        
        return [Game(game_id=gid, **g.dict()) for gid, g in zip(game_ids, games)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# 1. Obtener todos los jugadores de un equipo específico
@router.get("/Query1/", tags=["Query1: Get all players by team id"], response_model=List[Player])
def get_all_players_by_team_id(team_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM players WHERE team_id = %s"
        cursor.execute(query, (team_id,))
        players = cursor.fetchall()
        return [Player(**player) for player in players]
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail="Error al acceder a la base de datos: " + str(e))
    finally:
        cursor.close()
        conn.close()

# 2. Obtener todos los equipos junto con su entrenador (LEFT JOIN)
@router.get("/Query2/", tags=["Query2: Get all teams with their coaches"], response_model=List[dict])
def get_all_teams_with_coaches():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT teams.team_name, coaches.first_name, coaches.last_name, coaches.role
        FROM teams
        LEFT JOIN coaches ON teams.team_id = coaches.team_id
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# 3. Obtener todos los juegos y resultados (INNER JOIN entre equipos)
@router.get("/Query3/", tags=["Query3: Get all games and scores"], response_model=List[dict])
def get_all_games_and_scores():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT g.game_date, ht.team_name AS home_team, g.home_team_score, 
               at.team_name AS away_team, g.away_team_score
        FROM games g
        INNER JOIN teams ht ON g.home_team_id = ht.team_id
        INNER JOIN teams at ON g.away_team_id = at.team_id
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# 4. Obtener el jugador con el máximo número de touchdowns
@router.get("/Query4/", tags=["Query4: Get player with max touchdowns"], response_model=dict)
def get_player_with_max_touchdowns():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT p.first_name, p.last_name, ps.touchdowns
        FROM players p
        INNER JOIN player_stats ps ON p.player_id = ps.player_id
        ORDER BY ps.touchdowns DESC
        LIMIT 1
        """
        cursor.execute(query)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# 5. Obtener el equipo con más touchdowns totales en un juego
@router.get("/Query5/", tags=["Query5: Get team with max touchdowns in a game"], response_model=dict)
def get_team_with_max_touchdowns():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT t.team_name, ts.total_touchdowns
        FROM teams t
        INNER JOIN team_stats ts ON t.team_id = ts.team_id
        ORDER BY ts.total_touchdowns DESC
        LIMIT 1
        """
        cursor.execute(query)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# 6. Obtener el promedio de yardas por jugador en un juego
@router.get("/Query6/", tags=["Query6: Get average yards per player per game"], response_model=List[dict])
def get_avg_yards_per_player():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT p.first_name, p.last_name, AVG(ps.passing_yards + ps.rushing_yards) AS avg_yards
        FROM players p
        INNER JOIN player_stats ps ON p.player_id = ps.player_id
        GROUP BY p.player_id
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# 7. Obtener el equipo con la menor cantidad de penalizaciones en un juego
@router.get("/Query7/", tags=["Query7: Get team with min penalties in a game"], response_model=dict)
def get_team_with_min_penalties():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT t.team_name, ts.penalties
        FROM teams t
        INNER JOIN team_stats ts ON t.team_id = ts.team_id
        ORDER BY ts.penalties ASC
        LIMIT 1
        """
        cursor.execute(query)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# 8. Obtener la lista de juegos en los que un jugador específico ha participado
@router.get("/Query8/", tags=["Query8: Get games by player id"], response_model=List[dict])
def get_games_by_player_id(player_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT g.game_date, ht.team_name AS home_team, at.team_name AS away_team
        FROM games g
        INNER JOIN player_stats ps ON g.game_id = ps.game_id
        INNER JOIN teams ht ON g.home_team_id = ht.team_id
        INNER JOIN teams at ON g.away_team_id = at.team_id
        WHERE ps.player_id = %s
        """
        cursor.execute(query, (player_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# 9. Obtener la cantidad total de jugadores en cada equipo
@router.get("/Query9/", tags=["Query9: Get total players per team"], response_model=List[dict])
def get_total_players_per_team():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT t.team_name, COUNT(p.player_id) AS total_players
        FROM teams t
        LEFT JOIN players p ON t.team_id = p.team_id
        GROUP BY t.team_id
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# 10. Obtener el equipo con el mayor número de juegos ganados (considerando el score)
@router.get("/Query10/", tags=["Query10: Get team with most wins"], response_model=dict)
def get_team_with_most_wins():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT t.team_name, COUNT(*) AS wins
        FROM games g
        INNER JOIN teams t ON g.home_team_id = t.team_id AND g.home_team_score > g.away_team_score
        OR g.away_team_id = t.team_id AND g.away_team_score > g.home_team_score
        GROUP BY t.team_id
        ORDER BY wins DESC
        LIMIT 1
        """
        cursor.execute(query)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# 11. Obtener la cantidad total de touchdowns de cada jugador
@router.get("/Query11/", tags=["Query11: Get total touchdowns per player"], response_model=List[dict])
def get_total_touchdowns_per_player():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT p.first_name, p.last_name, SUM(ps.touchdowns) AS total_touchdowns
        FROM players p
        INNER JOIN player_stats ps ON p.player_id = ps.player_id
        GROUP BY p.player_id
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# 12. Obtener el promedio de penalizaciones por equipo en todos sus juegos
@router.get("/Query12/", tags=["Query12: Get average penalties per team"], response_model=List[dict])
def get_avg_penalties_per_team():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT t.team_name, AVG(ts.penalties) AS avg_penalties
        FROM teams t
        INNER JOIN team_stats ts ON t.team_id = ts.team_id
        GROUP BY t.team_id
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

# 13. Obtener el juego con el total de yardas más alto (sumando ambos equipos)
@router.get("/Query13/", tags=["Query13: Get game with highest total yards"], response_model=dict)
def get_game_with_highest_total_yards():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT g.game_date, ht.team_name AS home_team, at.team_name AS away_team, 
               (home_team_stats.total_yards + away_team_stats.total_yards) AS total_yards
        FROM games g
        INNER JOIN team_stats home_team_stats ON g.home_team_id = home_team_stats.team_id AND g.game_id = home_team_stats.game_id
        INNER JOIN team_stats away_team_stats ON g.away_team_id = away_team_stats.team_id AND g.game_id = away_team_stats.game_id
        INNER JOIN teams ht ON g.home_team_id = ht.team_id
        INNER JOIN teams at ON g.away_team_id = at.team_id
        ORDER BY total_yards DESC
        LIMIT 1
        """
        cursor.execute(query)
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# 14. Obtener el jugador con el máximo de yardas en un juego específico
@router.get("/Query14/", tags=["Query14: Get player with max yards in a game"], response_model=dict)
def get_player_with_max_yards_in_game(game_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT p.first_name, p.last_name, (ps.passing_yards + ps.rushing_yards) AS total_yards
        FROM players p
        INNER JOIN player_stats ps ON p.player_id = ps.player_id
        WHERE ps.game_id = %s
        ORDER BY total_yards DESC
        LIMIT 1
        """
        cursor.execute(query, (game_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

# 15. Obtener la lista de entrenadores y su equipo correspondiente
@router.get("/Query15/", tags=["Query15: Get list of coaches and their teams"], response_model=List[dict])
def get_list_of_coaches_and_teams():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT c.first_name, c.last_name, c.role, t.team_name
        FROM coaches c
        INNER JOIN teams t ON c.team_id = t.team_id
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()