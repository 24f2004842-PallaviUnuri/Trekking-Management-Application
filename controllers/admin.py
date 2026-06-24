from flask import Blueprint, render_template, url_for, redirect, request, flash
from models import db, User, Trek

admin_bp = Blueprint('admin',__name__)

@admin_bp.route('/dashboard',methods=['GET', 'POST'])
def dashboard():
    recent_treks = Trek.query.order_by(Trek.id.desc()).limit(5).all()
    return render_template('admin/admin_dashboard.html',recent_treks = recent_treks)

@admin_bp.route('/treks')
def manage_treks():
    treks = Trek.query.all()
    return render_template('admin/manage_trek.html',treks=treks)



@admin_bp.route('/add_trek',methods=['GET', 'POST'])
def add_trek():
    if request.method == "POST":
        name = request.form.get('name')
        location = request.form.get('location')
        difficulty = request.form.get('difficulty')
        duration  = request.form.get('duration')
        available_slots = request.form.get('available_slots')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        if not name and not location and not available_slots and not start_date and not end_date:
            flash("Please fill all required fields.","danger")
            return redirect(url_for('admin.add_trek'))
        
        new_trek = Trek(
            name = name,
            location = location,
            difficulty = difficulty,
            duration  = int(duration),
            available_slots = int(available_slots),
            start_date = start_date,
            end_date = end_date
        )
        db.session.add(new_trek)
        db.session.commit()
    return render_template('admin/add_trek.html')


@admin_bp.route('/treks/edits/<int:trek_id>',methods=['GET','POST'])
def edit_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    if request.method == 'POST':
        trek.name = request.form.get('name')
        trek.location = request.form.get('location')
        trek.difficulty = request.form.get('difficulty')
        trek.duration  = request.form.get('duration')
        trek.available_slots = request.form.get('available_slots')
        trek.start_date = request.form.get('start_date')
        trek.end_date = request.form.get('end_date')
        db.session.commit()
        flash('Trek Updated successfully.','success')
        return redirect(url_for('admin.manage_trek'))
    return render_template('admin/edit_trek.html',trek=trek)

@admin_bp.route('/treks/delete/<int:trek_id>')
def delete_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    flash('Trek deleted.','info')
    return redirect(url_for('admin.manage_treks'))
