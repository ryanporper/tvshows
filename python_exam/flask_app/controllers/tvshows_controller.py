from pyexpat import model
from flask import render_template, session, redirect, request, flash
from flask_app import app
from flask_app.models.tvshows import Tvshow
from flask_app.models.user import User

@app.route('/tvshows/new')
def tvshow_new():
    if 'id' not in session:
        flash('Log in before trying to view the dashboard.')
        return redirect('/')
    return render_template("new_tvshow.html")

@app.route('/tvshows/create', methods=['POST'])
def tvshow_create():
    if not Tvshow.is_valid(request.form):
        return redirect('/tvshows/new')
    if "under" not in request.form:
        data = {
             **request.form,
            "id": id,
            "under": '0'
        }
    else:
        data = {
            **request.form,
            'id': session['id']
        }
    Tvshow.save(data)
    return redirect('/dashboard')

@app.route('/tvshows/<int:id>/view')
def show_one_tvshow(id):
    if 'id' not in session:
        flash('Log in before trying to view the dashboard.')
        return redirect('/')
    data = {'id': id}
    tvshow = Tvshow.get_one_by_id(data)
    return render_template("show_tvshow.html", tvshow=tvshow)

@app.route('/tvshows/<int:id>/delete')
def delete_tvshow(id):
    data = {
        'id': id
    }
    tvshow = Tvshow.get_one_by_id(data)
    if tvshow.user_id != session['id']:
        flash('Nice try bucko.')
        return redirect('/dashboard')
    Tvshow.delete_by_id(data)
    return redirect('/dashboard')

@app.route('/tvshows/<int:id>/edit')
def edit_tvshow(id):
    data = {
        'id': id
    }
    tvshow = Tvshow.get_one_by_id(data)
    if tvshow.user_id != session['id']:
        flash('Nice try bucko.')
        return redirect('/dashboard')
    return render_template('edit_tvshow.html', tvshow=tvshow)

@app.route('/tvshows/<int:id>/update', methods=['POST'])
def update_tvshow(id):
    if "under" not in request.form:
        updated_info = {
             **request.form,
            "id": id,
            "under": '0'
        }
    else:
        updated_info = {
            **request.form,
            'id': id
        }
    tvshow = Tvshow.get_one_by_id(updated_info)
    if tvshow.user_id != session['id']:
        flash('Nice try bucko.')
        return redirect('/dashboard')

    if not Tvshow.is_valid(updated_info):
        return redirect(f'/tvshows/{id}/edit')

    Tvshow.update(updated_info)
    return redirect('/dashboard')