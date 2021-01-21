from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# ====================================================================================
from sik.models import User, Tsk_belumnikah, Tsk_tidakmampu, Tpermohonan, Tpenduduk, Tinformasi
from flask_wtf.file import FileField, FileAllowed
# =======================================================================================
from flask_login import current_user
from flask_ckeditor import CKEditorField

class Registrasi_F(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    konfirmasi_password = PasswordField('Konfirmasi_Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField ('Daftar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Sudah Terdaftar, Gunakan Username Yang Lain')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email Sudah Terdaftar, Gunakan Email Yang Lain')
            
    def validate_password(self, password):
        user = User.query.filter_by(password=password.data).first()
        if user:
            raise ValidationError('Password Sudah Terdaftar, Gunakan Password Yang Lain')

# ===================BATAS login==========================================================
class Login_F(FlaskForm):
    email = StringField ('Email', validators=[DataRequired(), Email()])
    password = PasswordField ('Password', validators=[DataRequired()])
    # ====================================================================================
    remember = BooleanField('Remember Me')
    # ====================================================================================
    submit = SubmitField ('Login')

class Update_Account_F(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    foto = FileField('Update Foto Profil', validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
        # if username.data !=current_user.emaildbw:
            user = User.query.filter_by(username=username.data). first()
            if user:
                raise ValidationError('Username yang anda masukan sudah digunakan, cobalah menggunakan username yang berbeda')

    def validate_emial(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data). first()
            if user:
                raise ValidationError('Email yang anda masukan sudah digunakan, cobalah menggunakan email yang berbeda')

# ===================BATAS Sk Belum Nikah===================================================
class Sk_belumnikah_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    ttl = StringField('TTL', validators=[DataRequired()])
    jenis_kelamin = StringField('Jenis Kelamin', validators=[DataRequired()])
    status_perkawinan = StringField('Status Perkawinan', validators=[DataRequired()])
    agama = StringField('Agama', validators=[DataRequired()])
    kewarganegaraan = StringField('Kewarga Negaraan', validators=[DataRequired()])
    pekerjaan = StringField('Pekerjaan', validators=[DataRequired()])
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    submit = SubmitField ('Kirim')

# ===================BATAS sk Tidak Mampu===================================================
class Sk_tidakmampu_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    nik = StringField('NIK', validators=[DataRequired()])
    ttl = StringField('TTL', validators=[DataRequired()])
    jenis_kelamin = StringField('Jenis Kelamin', validators=[DataRequired()])
    agama = StringField('Agama', validators=[DataRequired()])
    pekerjaan = StringField('Pekerjaan', validators=[DataRequired()])
    kewarganegaraan = StringField('Kewarga Negaraan', validators=[DataRequired()])
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    submit = SubmitField ('Kirim')

# ===========================================================================================
class Kategorisurat_F(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired()])
    no_hp = IntegerField ('No Hp', validators=[DataRequired()])
    kategori = StringField('Kategori Surat', validators=[DataRequired()])
    submit = SubmitField ('Kirim')

# ===========================================================================================
class Penduduk_F(FlaskForm):
    bulan = StringField('Bulan', validators=[DataRequired()])
    tahun = StringField('Tahun', validators=[DataRequired()])
    pria = StringField('Pria', validators=[DataRequired()])
    wanita = StringField('Wanita', validators=[DataRequired()])
    lahir = StringField('Lahir', validators=[DataRequired()])
    datang = StringField('Datang', validators=[DataRequired()])
    mati = StringField('Meninggal', validators=[DataRequired()])
    pindah = StringField('Pindah', validators=[DataRequired()])
    kk = StringField('Jumlah KK', validators=[DataRequired()])
    jj = StringField('Jumlah Jiwa', validators=[DataRequired()])

# ===========================================================================================
class Informasi_F(FlaskForm):
    title =StringField('Title', validators=[DataRequired()])
    konten = CKEditorField('Konten', validators=[DataRequired()])
    title =StringField('Title', validators=[DataRequired()])
    ttd =StringField('Tanda Tangan', validators=[DataRequired()])
    submit=SubmitField('Save')