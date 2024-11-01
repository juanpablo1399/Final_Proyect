from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class TeamCreate(BaseModel):
    team_name: str = Field(..., description="Nombre del equipo (campo requerido)")
    city: str = Field(..., description="Ciudad del equipo (campo requerido)")
    stadium: str = Field(..., description="Estadio del equipo (campo requerido)")
    founded_year: int = Field(..., description="Año de fundación del equipo (campo requerido)")

class Team(TeamCreate):
    team_id: int

class PlayerCreate(BaseModel):
    first_name: str = Field(..., description="Nombre del jugador (campo requerido)")
    last_name: str = Field(..., description="Apellido del jugador (campo requerido)")
    position: str = Field(..., description="Posición del jugador (campo requerido)")
    jersey_number: int = Field(..., description="Número de camiseta del jugador (campo requerido)")
    team_id: Optional[int] = Field(None, description="ID del equipo del jugador (opcional)")

class Player(PlayerCreate):
    player_id: int

class CoachCreate(BaseModel):
    first_name: str = Field(..., description="Nombre del entrenador (campo requerido)")
    last_name: str = Field(..., description="Apellido del entrenador (campo requerido)")
    role: str = Field(..., description="Rol del entrenador (campo requerido)")
    team_id: Optional[int] = Field(None, description="ID del equipo del entrenador (opcional)")

class Coach(CoachCreate):
    coach_id: int

class GameCreate(BaseModel):
    home_team_id: int = Field(..., description="ID del equipo local (campo requerido)")
    away_team_id: int = Field(..., description="ID del equipo visitante (campo requerido)")
    game_date: date = Field(..., description="Fecha del juego (campo requerido)")
    home_team_score: int = Field(..., description="Puntuación del equipo local (campo requerido)")
    away_team_score: int = Field(..., description="Puntuación del equipo visitante (campo requerido)")

class Game(GameCreate):
    game_id: int

class PlayerStatCreate(BaseModel):
    player_id: int = Field(..., description="ID del jugador (campo requerido)")
    game_id: int = Field(..., description="ID del juego (campo requerido)")
    touchdowns: int = Field(..., description="Número de touchdowns (campo requerido)")
    passing_yards: int = Field(..., description="Yardas de pase (campo requerido)")
    rushing_yards: int = Field(..., description="Yardas de carrera (campo requerido)")

class PlayerStat(PlayerStatCreate):
    stat_id: int

class TeamStatCreate(BaseModel):
    team_id: int = Field(..., description="ID del equipo (campo requerido)")
    game_id: int = Field(..., description="ID del juego (campo requerido)")
    total_yards: int = Field(..., description="Total de yardas (campo requerido)")
    total_touchdowns: int = Field(..., description="Total de touchdowns (campo requerido)")
    penalties: int = Field(..., description="Número de penalizaciones (campo requerido)")

class TeamStat(TeamStatCreate):
    team_stat_id: int