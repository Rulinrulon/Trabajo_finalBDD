from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db

bp = Blueprint('Canción', __name__)

@bp.route('/canciones')
def index():
    db = get_db()
    canciones = db.execute(
        """SELECT t.name AS Cancion, title AS Album, ar.name AS Artista, g.name AS Genero
        FROM  tracks t JOIN albums a ON t.AlbumId = a.AlbumId
        JOIN artists ar ON ar.ArtistId = a.ArtistId
        JOIN genres g ON g.GenreId = t.GenreId
        ORDER BY t.name DESC"""
    ).fetchall()
    return render_template('Canción/index.html', canciones=canciones)