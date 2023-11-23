from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db

bp = Blueprint('Album', __name__, url_prefix="/albumes")

@bp.route('/')
def index():
    db = get_db()
    album = db.execute(
        """SELECT title AS Album, ar.name AS Artista, AlbumId, ar.ArtistId
        FROM albums a 
        JOIN artists ar ON ar.ArtistId = a.ArtistId
        GROUP BY Album
        ORDER BY Artista ASC"""   
    ).fetchall()

    return render_template('Album/index.html', album=album)

@bp.route('/<int:id>')
def detalle(id):
    db = get_db()
    canciones = db.execute(
        """SELECT t.name AS Cancion, Milliseconds AS Duracion, title AS Album, a.AlbumId
            FROM tracks t JOIN albums a ON t.AlbumId = a.AlbumId
            WHERE a.AlbumId = ?
            ORDER BY Cancion ASC"""  ,
        (id,)
    ).fetchall()

    return render_template('Album/detalle.html', canciones=canciones)