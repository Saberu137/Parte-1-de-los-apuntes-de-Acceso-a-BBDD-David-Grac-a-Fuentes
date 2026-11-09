import sqlite3

from fastapi import Depends, FastAPI, HTTPException

import schemas
from database import crear_tablas, get_connection

# Crea la tabla si no existe
crear_tablas()

app = FastAPI()


def get_db():
    db = get_connection()
    try:
        yield db
    finally:
        db.close()


@app.post("/tareas", response_model=schemas.TareaLeer, status_code=201)
def crear_tarea(datos: schemas.TareaCrear, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute("INSERT INTO tareas (titulo) VALUES (?)", (datos.titulo,))
    db.commit()
    fila = db.execute("SELECT * FROM tareas WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return dict(fila)


@app.get("/tareas", response_model=list[schemas.TareaLeer])
def listar_tareas(db: sqlite3.Connection = Depends(get_db)):
    filas = db.execute("SELECT * FROM tareas").fetchall()
    return [dict(f) for f in filas]


@app.put("/tareas/{tarea_id}/completar", response_model=schemas.TareaLeer)
def completar_tarea(tarea_id: int, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.execute("UPDATE tareas SET completada = 1 WHERE id = ?", (tarea_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    fila = db.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()
    return dict(fila)