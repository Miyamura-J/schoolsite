from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Major
from . import db
import json

views = Blueprint('views', __name__)

@views.route("/")
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/ressources")
@login_required
def ressources():
    majors = Major.query.filter_by()
    return render_template("ressources.html", user=current_user, majors=majors)

@views.route("/notes", methods=["GET","POST"])
@login_required
def notes():
    if request.method == "POST":
        data = request.form.get("note")
        new_note = Note(data = data, user_id=current_user.id)

        db.session.add(new_note)
        db.session.commit()
        
    return render_template("notes.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    data = json.loads(request.data)
    noteId = data["noteId"]
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note deleted", categoty="success")
    return jsonify({})