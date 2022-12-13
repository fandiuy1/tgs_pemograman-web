import os
import mysql.connector
from auth import login
from flask import Flask, redirect, render_template, request, session, url_for, jsonify

application = Flask(__name__, template_folder='templates', static_folder='static')
UPLOAD_FOLDER = os.path.join('static', 'uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
 
application.config['UPLOAD_FOLDER'] = 'static/uploads/'

def getMysqlConnection():
    #  return mariadb.connect(user='root', host='localhost', port='3306', password='', database='table_mhs')
    return mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='perpustakaan_web')
@application.route('/')
@application.route('/landing')
def landing():
    return render_template('landing.html')
@application.route('/isi', methods=['GET', 'POST'])
@application.route('/latihan1', methods=['GET','POST'])
def latihan1():
    print(request.method)
    if request.method == 'GET':
        return render_template(
            'insert.html',
        )
    elif request.method == 'POST':
        id_rak = request.form['id_rak']
        nama_rak = request.form['nama_rak']
        lokasi_rak = request.form['lokasi_rak']
        id_buku = request.form['id_buku']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "✔ Data berhasil diupload"
            sqlstr = "INSERT INTO `rak` (`id_rak`, `nama_rak`, `lokasi_rak`, `id_buku`) VALUES ('"+id_rak+"', '"+nama_rak+"', '"+lokasi_rak+"', '"+id_buku+"');"
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template('insert.html',id_rak=id_rak,nama_rak=nama_rak, lokasi_rak=lokasi_rak, id_buku=id_buku )
@application.route('/latihan3', methods=['POST'])
def latihan3():
    print(request.method)
    all_data = request.get("http://127.0.0.1:5000/database/")
    id_rak = request.form['id_rak']
    nama_rak = request.form['nama_rak']
    lokasi_rak = request.form['lokasi_rak']
    id_buku = request.form['id_buku']
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        sukses = "✔ Data berhasil diupload"
        sqlstr = "INSERT INTO `rak` (`id_rak`, `nama_rak`, `lokasi_rak`, `id_buku`) VALUES ('"+id_rak+"', '"+nama_rak+"', '"+lokasi_rak+"', '"+id_buku+"');"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return jsonify({'msg':'success',
            'kode':'001'})
@application.route('/dashboard')
def dashboard():
    all_data = request.get("http://127.0.0.1:5000/database/")
    anggota = all_data.json()["anggota"]
    buku = all_data.json()["buku"]
    peminjaman = all_data.json()["peminjaman"]
    pengembalian = all_data.json()["pengembalian"]
    petugas = all_data.json()["petugas"]
    rak = all_data.json()["rak"]
    return render_template(
        'dashboard.html',
        anggota=anggota,
        buku=buku,
        peminjaman=peminjaman,
        pengembalian=pengembalian,
        petugas=petugas,
        rak=rak
    )
@application.route('/api')
def api():
    all_data = request.get("http://127.0.0.1:5000/database/")
    anggota = all_data.json()["anggota"]
    buku = all_data.json()["buku"]
    return render_template('api.html',anggota=anggota, buku=buku)

@application.route('/database/')
def database():
    # ambil data-data
    anggota = get_anggota()
    buku = get_buku()
    peminjaman = get_peminjaman()
    pengembalian = get_pengembalian()
    petugas = get_petugas()
    rak = get_rak()
    # convert data ke bentuk objek
    list_anggota = create_dict()
    for row in anggota:
        list_anggota.add(row[0],({"kode_anggota":row[1],"nama_anggota":row[2],"jk_anggota":row[3],"jurusan_anggota":row[4],"no_telp_anggota":row[5],"alamat_anggota":row[6]}))
    list_buku = create_dict()
    for row in buku:
        list_buku.add(row[0],({"kode_buku":row[1],"judul_buku":row[2],"penulis_buku":row[3],"penerbit_buku":row[4],"tahun_penerbit":row[5],"stock":row[6]}))
    list_peminjaman = create_dict()
    for row in peminjaman:
        list_peminjaman.add(row[0],({"tanggal_pinjam":str(row[1]),"tanggal_kembali":str(row[2])}))
    list_petugas = create_dict()
    for row in petugas:
        list_petugas.add(row[0],({"nama_petugas":row[1],"jabatan_petugas":row[2],"no_telp_petugas":row[3],"alamat_petugas":row[4]}))
    list_pengembalian = create_dict()
    for row in pengembalian:
        list_pengembalian.add(row[0],({"tanggal_pinjam":str(row[1]),"denda":row[2]}))
    list_rak = create_dict()
    for row in rak:
        list_rak.add(row[0],({"nama_rak":row[1],"lokasi_rak":row[3]}))
    return jsonify(
        anggota=list_anggota,
        buku=list_buku,
        peminjaman=list_peminjaman,
        pengembalian=list_pengembalian,
        petugas=list_petugas,
        rak=list_rak
    )
class create_dict(dict): 
    def __init__(self): 
        self = dict()
    def add(self, key, value): 
        self[key] = value
    
@application.route('/profile')
def index2():
    return render_template('profile.html')

# untuk daftar member

# untuk dashboard

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        if (username != '' and password !=''):
            db = getMysqlConnection()
            cur = db.cursor()
            cur.execute ("SELECT * from `login` WHERE `username`='"+username+"'") 
            data= cur.fetchone()
            if data == None:
                notif = "Username Salah"
                return redirect('login')
            elif data[1]=='admin'== password:
                return redirect ('tambah')
            else:
                if data[1]==password:
                    notif = "Masukan username dan password"
                    return redirect('anggota')
                else:
                    notif = "Password salah"
                    return redirect('login')
        else:
            return redirect('login')
# untuk yournews
@application.route('/sign-up', methods=['GET', 'POST'])
def daftaranggota():
    print(request.method)
    if request.method == 'GET':
        return render_template(
            'sign-up.html',
        )
    elif request.method == 'POST':
        
        id_anggota = request.form['id_anggota']
        kode_anggota = request.form['kode_anggota']
        nama_anggota = request.form['nama_anggota']
        jk_anggota = request.form['jk_anggota']
        jurusan_anggota = request.form['jurusan_anggota']
        no_telp_anggota = request.form['no_telp_anggota']
        alamat_anggota = request.form['alamat_anggota']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "✔ Data berhasil diupload"
            sqlstr = "INSERT INTO `anggota`(`id_anggota`, `kode_anggota`, `nama_anggota`, `jk_anggota`, `jurusan_anggota`, `no_telp_anggota`, `alamat_anggota`) VALUES ('"+id_anggota+"', '"+kode_anggota+"', '"+nama_anggota+"', '"+jk_anggota+"','"+jurusan_anggota+"','"+no_telp_anggota+"', '"+alamat_anggota+"');"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(
            'register',
            
        )
@application.route('/register', methods=['GET', 'POST'])
def register():
    print(request.method)
    if request.method == 'GET':
        return render_template(
            'register.html',
        )
    elif request.method == 'POST':
        
        username = request.form['username']
        password = request.form['password']
        id_anggota = request.form['id_anggota']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sqlstr = "INSERT INTO `login`(`username`, `password`, `id_anggota`) VALUES ('"+username+"', '"+password+"', '"+id_anggota+"');"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return redirect(
            'login',
        )      
@application.route('/tambah', methods=['GET', 'POST'])
def tambah():
    print(request.method)
    if request.method == 'GET':
        return render_template(
            'tambah_buku.html',
        )
    elif request.method == 'POST':
        id_buku = request.form['id_buku']
        kode_buku = request.form['kode_buku']
        judul_buku = request.form['judul_buku']
        penulis_buku = request.form['penulis_buku']
        penerbit_buku = request.form['penerbit_buku']
        tahun_penerbit = request.form['tahun_penerbit']
        stock = request.form['stock']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "✔ Data berhasil diupload"
            sqlstr = "INSERT INTO `buku`(`id_buku`, `kode_buku`, `judul_buku`, `penulis_buku`, `penerbit_buku`, `tahun_penerbit`, `stock`) VALUES ('"+id_buku+"', '"+kode_buku+"', '"+judul_buku+"', '"+penulis_buku+"','"+penerbit_buku+"', '"+tahun_penerbit+"', '"+stock+"');"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template(
            'tambah_buku.html',
            sukses=sukses
        ) 
@application.route('/pinjam', methods=['GET', 'POST'])
def pinjam():
    print(request.method)
    if request.method == 'GET':
        return render_template(
            'pinjam.html',
        )
    elif request.method == 'POST':
        id_peminjaman = request.form['id_peminjaman']
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "✔ Data berhasil diupload"
            sqlstr = "INSERT INTO `peminjaman` (`id_peminjaman`, `tanggal_pinjam`, `tanggal_kembali`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ('"+id_peminjaman+"', current_timestamp(), current_timestamp(), '"+id_buku+"', '"+id_anggota+"', '"+id_petugas+"');"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template(
            'pinjam.html',
            sukses=sukses
        ) 
@application.route('/kembali', methods=['GET', 'POST'])
def kembali():
    print(request.method)
    if request.method == 'GET':
        return render_template(
            'kembali.html',
        )
    elif request.method == 'POST':
        id_pengembalian = request.form['id_pengembalian']
        denda = request.form['denda']
        id_buku = request.form['id_buku']
        id_anggota = request.form['id_anggota']
        id_petugas = request.form['id_petugas']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "✔ Data berhasil diupload"
            sqlstr = "INSERT INTO `pengembalian` (`id_pengembalian`, `tanggal_pengembalian`, `denda`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ('"+id_pengembalian+"', current_timestamp(),'"+denda+"' '"+id_buku+"', '"+id_anggota+"', '"+id_petugas+"');"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template(
            'kembali.html',
            sukses=sukses
        )
@application.route('/daftar_petugas', methods=['GET', 'POST'])
def daftar_petugas():
    print(request.method)
    if request.method == 'GET':
        return render_template(
            'daftar_petugas.html',
        )
    elif request.method == 'POST':
        id_petugas = request.form['id_petugas']
        nama_petugas = request.form['nama_petugas']
        jabatan_petugas = request.form['jabatan_petugas']
        no_telp_petugas = request.form['no_telp_petugas']
        alamat_petugas = request.form['alamat_petugas']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "✔ Data berhasil diupload"
            sqlstr = "INSERT INTO `petugas` (`id_petugas`, `nama_petugas`, `jabatan_petugas`, `id_buku`, `id_anggota`, `id_petugas`) VALUES ('"+id_petugas+"', '"+nama_petugas+"', '"+jabatan_petugas+"', '"+no_telp_petugas+"', '"+alamat_petugas+"');"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template(
            'daftar_petugas.html',
            sukses=sukses
        )

@application.route('/isi', methods=['GET', 'POST'])
def isi():
    print(request.method)
    if request.method == 'GET':
        return render_template(
            'isi_rak.html',
        )
    elif request.method == 'POST':
        id_rak = request.form['id_rak']
        nama_rak = request.form['nama_rak']
        lokasi_rak = request.form['lokasi_rak']
        id_buku = request.form['id_buku']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "✔ Data berhasil diupload"
            sqlstr = "INSERT INTO `rak` (`id_rak`, `nama_rak`, `lokasi_rak`, `id_buku`) VALUES ('"+id_rak+"', '"+nama_rak+"', '"+lokasi_rak+"', '"+id_buku+"');"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template(
            'isi_rak.html',
            sukses=sukses
        )
@application.route('/status', methods=['GET', 'POST'])
def status():
    print(request.method)
    if request.method == 'GET':
        return render_template(
            'profile.html',
        )
    elif request.method == 'POST':
        id_status = request.form['id_status']
        email = request.form['email']
        isi = request.form['isi']
        id_anggota = request.form['id_anggota']
        db = getMysqlConnection()
        try:
            cur = db.cursor()
            sukses = "✔ Data berhasil diupload"
            sqlstr = "INSERT INTO `status` (`id_status`, `email`, `isi`, `id_anggota`) VALUES ('"+id_status+"', '"+email+"', '"+isi+"', '"+id_anggota+"');"
            print(sqlstr)
            cur.execute(sqlstr)
            db.commit()
            cur.close()
        except Exception as e:
            print("Error in SQL:\n", e)
        finally:
            db.close()
        return render_template(
            'profile.html',
            sukses=sukses
        )
@application.route('/anggota')
def anggota():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from anggota"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('anggota.html', anggota=output_json)
@application.route('/buku')
def buku():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from buku"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('buku.html', buku=output_json)
@application.route('/peminjaman')
def peminjaman():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from peminjaman"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('daftar_pinjam.html', peminjaman=output_json)
@application.route('/pengembalian')
def pengembalian():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from pengembalian"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('daftar_kembali.html', pengembalian=output_json)
@application.route('/petugas')
def petugas():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from petugas"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('petugas.html', petugas=output_json)

@application.route('/rak')
def rak():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from rak"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('isi_rak.html', rak=output_json)


def get_anggota():
    db = getMysqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from anggota")
    anggota = cur.fetchall()
    db.close()
    return anggota
def get_buku():
    db = getMysqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from buku")
    buku = cur.fetchall()
    db.close()
    return buku
def get_peminjaman():
    db = getMysqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from peminjaman")
    peminjaman = cur.fetchall()
    db.close()
    return peminjaman
def get_pengembalian():
    db = getMysqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from pengembalian")
    pengembalian = cur.fetchall()
    db.close()
    return pengembalian
def get_petugas():
    db = getMysqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from petugas")
    petugas = cur.fetchall()
    db.close()
    return petugas

def get_rak():
    db = getMysqlConnection()
    cur = db.cursor()
    cur.execute("SELECT * from rak")
    rak = cur.fetchall()
    db.close()
    return rak

@application.route('/lstatus')
def lstatus():
    db = getMysqlConnection()
    try:
        sqlstr = "SELECT * from status"
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
    except Exception as e:
        print("Error in SQL:\n", e)
    finally:
        db.close()
    return render_template('isi_rak.html', status=output_json)
   
   
@application.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    db = getMysqlConnection()
    cur = db.cursor()
    x = str(id)
    cur.execute('SELECT * FROM karyawan WHERE NIM='+x+'')
    item = cur.fetchone()
    if request.method == 'POST':
        NIM = request.form['NIM']
        Nama = request.form['Nama']
        Asal_Kota = request.form['Asal_Kota']
        Jenis_Kelamin = request.form['Jenis_Kelamin']
        Alasan = request.form['Alasan']
        sqlstr = "UPDATE `karyawan` SET `NIM`='"+NIM+"', `Nama`='"+Nama+"',`Asal_Kota`='"+Asal_Kota+"',`Jenis_Kelamin`='"+Jenis_Kelamin+"',`Alasan`='"+Alasan+"' WHERE `NIM`='"+item[0]+"'"
        cur.execute(sqlstr)
        db.commit()
        cur.close()
        db.close()
        sukses = "✔ Data berhasil diedit"
        disabled='disabled'
        return render_template(
            'edit.html', 
            item=item,
            sukses=sukses, 
            disabled=disabled
        )
    else:
        cur.close()
        db.close()
        return render_template(
            'edit.html',
            item=item, 
            disabled=''
        ) 
 
# Define secret key to enable session

@application.route('/hapusbuku/<int:id>')
def hapusbuku(id):
    db = getMysqlConnection()
    cur = db.cursor()
    x = str(id)
    cur.execute('DELETE FROM `buku` WHERE id_buku='+x+'')
    db.commit()
    db.close()

    return redirect(
        '../tables'
    )
@application.route('/hapuspetugas/<int:id>')
def hapuspetugas(id):
    db = getMysqlConnection()
    cur = db.cursor()
    x = str(id)
    cur.execute('DELETE FROM `petugas` WHERE id_petugas='+x+'')
    db.commit()
    db.close()

    return redirect(
        '../tables'
    )
@application.route('/hapusanggota/<int:id>')
def hapusanggota(id):
    db = getMysqlConnection()
    cur = db.cursor()
    x = str(id)
    cur.execute('DELETE FROM `anggota` WHERE id_anggota='+x+'')
    db.commit()
    db.close()

    return redirect(
        '../tables'
    )
@application.route('/hapuspeminjaman/<int:id>')
def hapuspeminjaman(id):
    db = getMysqlConnection()
    cur = db.cursor()
    x = str(id)
    cur.execute('DELETE FROM `peminjaman` WHERE id_peminjaman='+x+'')
    db.commit()
    db.close()
@application.route('/hapuspengembalian/<int:id>')
def hapuspengembalian(id):
    db = getMysqlConnection()
    cur = db.cursor()
    x = str(id)
    cur.execute('DELETE FROM `pengembalian` WHERE id_pengembalian='+x+'')
    db.commit()
    db.close()

    return redirect(
        '../tables'
    )
@application.route('/hapusrak/<int:id>')
def hapusrak(id):
    db = getMysqlConnection()
    cur = db.cursor()
    x = str(id)
    cur.execute('DELETE FROM `rak` WHERE id_rak='+x+'')
    db.commit()
    db.close()
@application.route('/hapusstatus/<int:id>')
def hapusstatus(id):
    db = getMysqlConnection()
    cur = db.cursor()
    x = str(id)
    cur.execute('DELETE FROM `status` WHERE id_status='+x+'')
    db.commit()
    db.close()
if __name__ == '__main__':
    application.run(debug=True)