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
