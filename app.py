# Nhập các thư viện
from flask import Flask, render_template
from flask import jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField , SelectMultipleField, IntegerField
from wtforms.validators import DataRequired
from flask import render_template, flash, redirect
import pickle
import numpy as np
import os 
import codecs

# Mở các file model
file = open('templates/runtime.txt', mode="r", encoding='utf-8')
loaded_model = pickle.load(open('trained_model.sav', 'rb'))
model = pickle.load(open('deep_model.sav', 'rb'))
# Định nghĩa key
key_1, key_2, key_3, key_4, key_5, key_6, key_7, key_21, key_8, key_9, key_10, key_11, key_12, key_13, key_14, key_15, key_16, key_17, key_18, key_19, key_20 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

# Khai báo flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'zky_nah'

def stroke_prediction(input_data):
    # Đổi thông tin nhập vào thành dạng Array
    input_data_as_numpy_array = np.asarray(input_data)

    # tái cấu trúc mảng tiền nhập liệu
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    # Tạo tiên đoán bằng model
    prediction = loaded_model.predict_proba(input_data_reshaped)[:, 1][0]
    prediction_proba = loaded_model.predict_proba(input_data_reshaped)
    return prediction_proba, prediction*100

def stroke_prediction_deep(input_data):
   
    # Đổi thông tin nhập vào thành dạng Array
    input_data_as_numpy_array = np.asarray(input_data)

    # tái cấu trúc mảng tiền nhập liệu
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

    # Tạo tiên đoán bằng model
    prediction =  model.predict(input_data_reshaped) 
    prediction_proba =  model.predict(input_data_reshaped)
    return prediction_proba, prediction*100

class  Form(FlaskForm):
    # Tạo form nhập dữ liệu
    age = StringField('Tuổi', validators=[DataRequired()])
    hypertension = BooleanField('Chỉ số Huyết áp')
    heart = BooleanField('Triệu chứng bệnh tim')
    glucozo = StringField('Lượng đường trong máu', validators=[DataRequired()])
    bmi = StringField('Chỉ số khối cơ thể (bmi)', validators=[DataRequired()])
    gender_male = BooleanField('Nam')
    gender_female = BooleanField('Nữ')
    gender_other = BooleanField('Khác')
    married_No = BooleanField('Chưa kết hôn')
    married_Yes= BooleanField('Đã kết hôn')
    Govt_job = BooleanField('Làm việc cho chính phủ')
    Privacy_job = BooleanField('Việc làm cho công ty tư nhân')
    Self_job = BooleanField('Nghề tự do')
    Never_job = BooleanField('Không có việc làm')
    Child_job = BooleanField('Chưa đến tuổi đi làm')
    rural = BooleanField('Sống ở miền quê')
    urban = BooleanField('Sống ở thành thị')
    smoke_unk = BooleanField('Không rõ có hay không hút thuốc')
    smoke_usedto = BooleanField('Đã từng hút thuốc')
    smoke_nev = BooleanField('Không hút thuốc')
    smoke_status = BooleanField('Đang hút thuốc')
    submit = SubmitField('Kiểm tra')
     
# tạo hàm chuyển trang
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='Kiểm tra nguy cơ đột quỵ')
@app.route('/symbol.html')
def symbol():
    return render_template('symbol.html', the_title='Thông tin thêm')
@app.route('/myth.html', methods=["GET", "POST"])
def myth():
    # Lấy dữ liệu từ form
    form =  Form()
    # Nhận dữ liệu từ html
    data_age =  form.age.data
    data_hyper = form.hypertension.data
    data_glu = form.glucozo.data
    data_heart = form.heart.data
    data_bmi = form.bmi.data
    data_gen_male = form.gender_male.data
    data_gen_female = form.gender_female.data
    data_gen_other = form.gender_other.data
    data_marr_Y = form.married_Yes.data
    data_marr_N = form.married_No.data
    data_gvt = form.Govt_job.data
    data_priv = form.Privacy_job.data
    data_self = form.Self_job.data
    data_Nev = form.Never_job.data
    data_Child = form.Child_job.data
    data_rural = form.rural.data
    data_urban = form.urban.data
    data_unk_sm = form.smoke_unk.data
    data_use_sm = form.smoke_usedto.data
    data_nev_sm = form.smoke_nev.data
    data_sta_sm = form.smoke_status.data
    
    # Xử lí dữ liệu thành tham số
    def key(data_age, data_hyper, data_glu ,data_heart, data_bmi,  data_gen_male, data_gen_female, data_gen_other, data_marr_Y, data_marr_N, data_gvt, data_priv,data_self, data_Nev,data_Child, data_rural,data_urban, data_unk_sm, data_use_sm, data_nev_sm , data_sta_sm ):
        key_age = (int(data_age)-43.22661448140902)/(22.61043402711303)
        key_glucozo = (float(data_glu)-106.14767710371795)/(45.27912905705893)
        key_bmi = (float(data_bmi) -28.90337865973328)/(7.698534094073452)

        if data_hyper == True:
            key_hyper = int(1)
        else:
            key_hyper = int(0) 

        if data_heart == True:
            key_heart = int(1)
        else:
            key_heart = int(0) 
        
        if  data_gen_male == True:
            key_gender = 1
        elif data_gen_female == True:
            key_gender = 0
        elif data_gen_other == True:
            key_gender = 2 
      
        if data_marr_N == True:
         
            key_marr = 0  
        elif data_marr_Y == True:
            key_marr = 1 
     
        if data_gvt == True:
            key_job = int(0) 
             
        elif data_Nev == True:
            key_job = int(1)  
             
        elif data_priv == True:
            key_job = int(2)
        elif data_self == True:
            key_job = int(3)
        elif data_Child == True:
            key_job = int(4)
        
        if data_rural == True:
            key_live = int(0)  
        elif data_urban == True:
            key_live = int(1)
    # Tiểu sử hút thuốc
        if data_unk_sm == True:
            key_smoke = int(0)  
              
        elif data_use_sm == True:
            key_smoke = int(1)  
             
        elif data_nev_sm == True:
            key_smoke = int(2)  
             
        elif data_sta_sm == True:
            key_smoke = int(3) 

        # trả về tham số    
        return  [key_gender, key_age, key_hyper, key_heart, key_marr, key_job, key_live, key_glucozo, key_bmi, key_smoke]
    if form.validate_on_submit():
        # Nhận kết quả dự đoán
        setz =  key(data_age , data_hyper , data_glu , data_heart, data_bmi, data_gen_male, data_gen_female, data_gen_other, data_marr_Y, data_marr_N, data_gvt, data_priv, data_self, data_Nev, data_Child, data_rural, data_urban, data_unk_sm, data_use_sm, data_nev_sm, data_sta_sm) 
        prediction_proba, score_predict = stroke_prediction(setz)
        prediction, score_deep  = stroke_prediction_deep(setz)
        round(score_predict, 2)
        # in kết quả dự đoán
        if(score_predict == 0):
            data = "Nhấn nút để nhận dự đoán!"
            return '''<div id="result"><h1>Kết quả: {}</h1> </div>'''.format(data)
        elif(score_predict >= 75 and score_deep == 0):
            data = f'Bạn có {round(score_predict, 2)} % khả năng bị Đột quỵ, tìm bác sĩ để nhận chuẩn đoán chi tiết.'
            return '''<div id="result"><h1>Kết quả: {}</h1> </div>'''.format(data)
        elif(score_predict >= 40 and score_predict < 75 and score_deep == 0):
            data = f'Bạn có {round(score_predict, 2)} % khả năng bị Đột quỵ, nguy cơ này là rất cao.'
            return '''<div id="result"><h1>Kết quả: {}</h1> </div>'''.format(data)
        else:
            data = f'Bạn có {round(score_predict, 2)} % khả năng bị Đột quỵ.'
            return '''<div id="result"><h1>Kết quả: {}</h1> </div>'''.format(data)

         

    return render_template('myth.html', the_title='Bắt đầu', form=form )
def test_db_connection():
    try:
        # google sql cloud database -- ip whitelisting test for heroku app
        from mysql.connector import connect
        cnx = connect(
            host='35.238.34.27',
            database='demo',
            user='nivratti',
            password='nivpoijkldfghcc@@', 
            port=3306
        )
        d = {
            "success": True,
            "message": "Connected to database successfully",
        }
    except Exception as e:
        d = {
            "success": False,
            "message": str(e),
        }
    return jsonify(d)


if __name__ == '__main__':
    app.run(debug=True)
