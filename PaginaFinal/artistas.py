from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db

bp = Blueprint('Artista', __name__, url_prefix="/artistas")

@bp.route('/')
def index():
    db = get_db()
    artistas = db.execute(
        """SELECT ar.name AS Nombre, count(al.AlbumId) AS Albums
         FROM artists ar JOIN albums al ON ar.ArtistId = al.ArtistId
		 GROUP BY Nombre
         ORDER BY Nombre ASC"""   
    ).fetchall()

    return render_template('Artista/index.html', artistas=artistas)

@bp.route('/<int:id>')
def detalle(id):
    db = get_db()
    artista = db.execute(
        """SELECT ar.name AS Nombre, title AS Album, sum(milliseconds), g.name AS Genero
         FROM artists ar JOIN albums a ON ar.ArtistId = a.ArtistId
         JOIN tracks t ON t.AlbumId = a.AlbumId
         JOIN genres g ON t.GenreId = g.GenreId
		 WHERE ar.ArtistId = ?
         ORDER BY Nombre ASC"""   ,
         (id,)
    ).fetchone()

    album = db.execute(
        """SELECT title AS Album, ar.name AS Artista, sum(Milliseconds) AS Duración
        FROM albums a 
        JOIN artists ar ON ar.ArtistId = a.ArtistId
        JOIN tracks t ON t.AlbumId = a.AlbumId
        GROUP BY Album
        ORDER BY Artista ASC"""   
    ).fetchall()

    return render_template('Artista/detalle.html', artista=artista, album=album)
