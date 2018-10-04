from flask import Blueprint, render_template, redirect, flash, url_for
from flaskr import app, db
from flaskr.forms.companies import CompanyForm
from flaskr.models import Company
from flaskr.utils.roles import login_required_staff

bp = Blueprint('companies', __name__, url_prefix='/companies')

@bp.route('/')
@login_required_staff
def index():
    items = Company.query.order_by(
        Company.name
    ).all()
    return render_template('companies/index.pug', items=items)

@bp.route('/create', methods=['GET', 'POST'])
@login_required_staff
def create():
    form = CompanyForm()
    if form.validate_on_submit():
        item = Company()
        form.populate_obj(item)
        db.session.add(item)
        try:
            db.session.commit()
            flash('就労先企業の登録ができました','success')
            return redirect(url_for('companies.index'))
        except Exception as e:
            db.session.rollback()
            flash('就労先企業の登録でエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('companies/edit.pug', form=form)

@bp.route('/<id>/edit', methods=['GET', 'POST'])
@login_required_staff
def edit(id):
    item = Company.get_or_404(id)
    form = CompanyForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        try:
            db.session.commit()
            flash('就労先企業の変更ができました','success')
            return redirect(url_for('companies.index'))
        except Exception as e:
            db.session.rollback()
            flash('就労先企業の変更でエラーが発生しました {}'.format(e), 'danger')
            app.logger.exception(e)
    return render_template('companies/edit.pug', id=id, form=form)

@bp.route('/<id>/destroy')
@login_required_staff
def destroy(id):
    item = Company.get_or_404(id)
    db.session.delete(item)
    try:
        db.session.commit()
        flash('就労先企業の削除ができました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('就労先企業の削除でエラーが発生しました {}'.format(e), 'danger')
        app.logger.exception(e)
    return redirect(url_for('companies.index'))
