from flask import Flask, render_template, redirect, url_for, Blueprint, flash, request
from sik.models import User, Tsk_belumnikah, Tsk_tidakmampu, Tpermohonan, Tpenduduk, Tinformasi
from sik import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from sik import app
from PIL import Image
# ==============================================================================================
from sik.forms import Registrasi_F, Login_F, Sk_belumnikah_F, Sk_tidakmampu_F, Kategorisurat_F, Penduduk_F, Update_Account_F, Informasi_F
# ==============================================================================================

vmahasiswa = Blueprint('vmahasiswa', __name__)


@vmahasiswa.route("/")
def landing():
	penduduk = Tpenduduk.query.all()
	informasi = Tinformasi.query.all()
	return render_template("landing_page.html", title='Home', penduduk=penduduk, informasi=informasi)

@vmahasiswa.route("/surat/permohonan", methods=['GET','POST'])
@login_required
def suratpermohonan():
	form=Kategorisurat_F()
	if form.validate_on_submit():
		kategorisurat = Tpermohonan(nama=form.nama.data, no_hp=form.no_hp.data, kategori=form.kategori.data, pemohon=current_user)
		db.session.add(kategorisurat)
		db.session.commit()
		flash('Data berhasil ditambahkan','success')
		return redirect(url_for('vmahasiswa.pilihkategori'))
	return render_template("surat_permohonan.html", title="Surat Permohonan", form=form, Legend='Surat Permohonan', kategorisurat='kategorisurat')


@vmahasiswa.route("/pilih/kategori/surat")
def pilihkategori():
	return render_template("pilih_kategori.html")

# ============================================================================================
@vmahasiswa.route("/registrasi", methods=['GET', 'POST'])
def registrasi():
	if current_user.is_authenticated:
		return redirect(url_for('vmahasiswa.landing'))
	form = Registrasi_F()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Akun {form.username.data} Berhasil di Tambahkan, Silahkan Login', 'success')
		return redirect(url_for('vmahasiswa.loginuser'))
	return render_template("daftar.html", title="Registrasi", form=form)

# ==============================================================================================
@vmahasiswa.route("/loginuser", methods=['GET', 'POST'])
def loginuser():
	if current_user.is_authenticated:
		return redirect(url_for('vmahasiswa.base'))
	form = Login_F()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page= request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('vmahasiswa.landing'))
		else:
			flash('Login failed...!!!, Periksa Kembali Email dan Password Anda', 'warning')
	return render_template("login.html", title="Login", form=form)

# ===============================================================================================
@vmahasiswa.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('vmahasiswa.landing'))

# =============================================================================================
@vmahasiswa.route("/sk_belumnikah", methods=['GET','POST'])
@login_required
def sk_belumnikah():
	form=Sk_belumnikah_F()
	if form.validate_on_submit():
		sk_belumnikah = Tsk_belumnikah(nama=form.nama.data, ttl=form.ttl.data, jenis_kelamin=form.jenis_kelamin.data, status_perkawinan=form.status_perkawinan.data, 
        	agama=form.agama.data, kewarganegaraan=form.kewarganegaraan.data, pekerjaan=form.pekerjaan.data, alamat=form.alamat.data)
		db.session.add(sk_belumnikah)
		db.session.commit()
		flash('Data berhasil ditambahkan','Sukses')
		return redirect(url_for('vmahasiswa.suratpermohonan'))
	return render_template("sk_belumnikah.html",  form=form, sk_belumnikah='sk_belumnikah')

# =============================================================================================
@vmahasiswa.route("/sk_tidakmampu", methods=['GET','POST'])
@login_required
def sk_tidakmampu():
	form=Sk_tidakmampu_F()
	if form.validate_on_submit():
		sk_tidakmampu = Tsk_tidakmampu(nama=form.nama.data, nik=form.nik.data, ttl=form.ttl.data, jenis_kelamin=form.jenis_kelamin.data, agama=form.agama.data, 
			pekerjaan=form.pekerjaan.data, kewarganegaraan=form.kewarganegaraan.data, alamat=form.alamat.data)
		db.session.add(sk_tidakmampu)
		db.session.commit()
		flash('Data berhasil ditambahkan','Sukses')
		return redirect(url_for('vmahasiswa.suratpermohonan'))
	return render_template("sk_tidakmampu.html",  form=form, sk_tidakmampu='sk_tidakmampu')

# =============================================================================================
def simpan_foto(form_foto):
	random_hex = secrets.token_hex(8)
	f_name, f_ext = os.path.splitext(form_foto.filename)
	foto_fn = random_hex + f_ext
	foto_path = os.path.join(app.root_path, 'sik/static/foto', foto_fn)
	form_foto.save(foto_path)
	return foto_fn
	
	output_size =(125,125)
	j = Image.open(form_foto)
	j.thumbnail(output_size)
	j.save(foto_path)
	return foto_fn

@vmahasiswa.route("/account", methods=['GET','POST'])
@login_required
def akun():
	form=Update_Account_F()
	if form.validate_on_submit():
		# save foto profil
		if form.foto.data:
			file_foto = simpan_foto(form.foto.data)
			current_user.img = file_foto
		# save db
		current_user.username=form.username.data
		current_user.email=form.email.data
		db.session.commit()
		flash('Akun ini berhasil di update!','success')
		return redirect(url_for('vmahasiswa.akun'))
	elif request.method == 'GET':
		form.username.data=current_user.username
		form.email.data=current_user.email

	img = url_for('static', filename='foto/' + current_user.img)
	return render_template("akun.html", title="Account", img=img, form=form)

@vmahasiswa.route("/delete/<id>", methods=['GET', 'POST'])
def delete(id):
        my_data=Tpermohonan.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        flash('Data Anda Berhasil di Hapus', 'warning')
        return redirect(url_for('vmahasiswa.permohonan'))