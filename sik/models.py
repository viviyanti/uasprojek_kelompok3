from datetime import datetime
from sik import db, login_manager, app
from flask_login import UserMixin
from flask_admin import Admin
# ======================================================================================
from flask_admin.contrib.sqla import ModelView
# ======================================================================================

admin = Admin(app)

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    img = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    permohonan = db.relationship('Tpermohonan', backref='pemohon', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.img}','{self.password}')"

class Tsk_belumnikah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    ttl = db.Column(db.String(50), nullable=False)
    jenis_kelamin = db.Column(db.String(15), nullable=False)
    status_perkawinan = db.Column(db.String(20), nullable=False)
    agama = db.Column(db.String(15), nullable=False)
    kewarganegaraan = db.Column(db.String(30), nullable=False)
    pekerjaan = db.Column(db.String(30), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Tsk_belumnikah('{self.nama}','{self.ttl}','{self.jenis_kelamin}','{self.status_perkawinan}','{self.agama}','{self.kewarganegaraan}','{self.pekerjaan}','{self.alamat}')"

class Tsk_tidakmampu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nik = db.Column(db.String(50), unique=True, nullable=False)
    ttl = db.Column(db.String(50), nullable=False)
    jenis_kelamin = db.Column(db.String(15), nullable=False)
    agama = db.Column(db.String(15), nullable=False)
    pekerjaan = db.Column(db.String(30), nullable=False)
    kewarganegaraan = db.Column(db.String(30), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"Tsk('{self.nama}','{self.nik}','{self.ttl}','{self.jenis_kelamin}','{self.agama}','{self.pekerjaan}','{self.kewarganegaraan}','{self.alamat}')"

class Tpermohonan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    no_hp = db.Column(db.String(120), unique=False, nullable=False)
    kategori = db.Column(db.String(30), nullable=False)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column (db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Tpermohonan('{self.kategori}','{self.tgl_post}')"

class Tpenduduk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bulan = db.Column(db.String(100), nullable=False)
    tahun = db.Column(db.String(100), nullable=False)
    pria = db.Column(db.String(100), nullable=False)
    wanita = db.Column(db.String(100), nullable=False)
    lahir = db.Column(db.String(100), nullable=False)
    datang = db.Column(db.String(100), nullable=False)
    mati = db.Column(db.String(100), nullable=False)
    pindah = db.Column(db.String(100), nullable=False)
    kk = db.Column(db.String(100), nullable=False)
    jj = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Tpenduduk('{self.bulan}','{self.tahun}','{self.pria}','{self.wanita}','{self.lahir}','{self.mati}','{self.pindah}')"

class Tinformasi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.String(100), nullable=False)
    konten = db.Column(db.Text, nullable=False)
    ttd =db.Column(db.String(100), nullable=True)




# =========================================================================================
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Tsk_belumnikah, db.session))
admin.add_view(ModelView(Tsk_tidakmampu, db.session))
admin.add_view(ModelView(Tpermohonan, db.session))
admin.add_view(ModelView(Tpenduduk, db.session))
admin.add_view(ModelView(Tinformasi, db.session))
# =========================================================================================