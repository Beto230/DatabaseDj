from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""
    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    if playlist_id in playlists:
        playlist = playlists[playlist_id]
        return render_template('playlist_details.html', playlist=playlist)
    else:
        return "Playlist not found", 404
    
    
@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    if request.method == "POST":
        
        playlist_name = request.form.get('name')
        playlist_description = request.form.get('description')

        if not playlist_name:
            error = "Please enter a playlist name."
            return render_template('add_playlist.html', error=error)

        new_playlist = Playlist(name=playlist_name, description=playlist_description)
        db.session.add(new_playlist)
        db.session.commit()

        return redirect('playlists.html')

    return render_template('add_playlist.html')

##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """return a specific song"""

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    if song_id in songs:
        song = songs[song_id]
        return render_template('song_details.html', song=song)
    else:
        return "Song not found", 404

@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """

    # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
    if request.method == "POST":
        # Check if the form is filled out and valid
        song_title = request.form.get('title')
        song_artist = request.form.get('artist')
        song_duration = request.form.get('duration')

        if not song_title or not song_artist or not song_duration:
            # Form not filled out or invalid, show the form again
            error_message = "Please fill out all fields."
            return render_template('add_song_form.html', error=error_message)

        # If the form is valid, add the song to the database
        new_song = Song(title=song_title, artist=song_artist, duration=song_duration)
        db.session.add(new_song)
        db.session.commit()

        # Redirect to the list of songs
        return redirect('songs.html')

@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a playlist and redirect to list."""

    # BONUS - ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK

    # THE SOLUTION TO THIS IS IN A HINT IN THE ASSESSMENT INSTRUCTIONS

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Restrict form to songs not already on this playlist

    curr_on_playlist = ...
    form.song.choices = ...

    if form.validate_on_submit():

          # ADD THE NECESSARY CODE HERE FOR THIS ROUTE TO WORK
        song_id = form.song.data

        # Get the song object from the database
        song = Song.query.get(song_id)

        if song:
            # Add the selected song to the playlist
            playlist.songs.append(song)
            db.session.commit()

            # Redirect to the playlist details page
            return redirect('playlist.html', playlist_id=playlist_id)

        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                             playlist=playlist,
                             form=form)
