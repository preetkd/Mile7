from flask import Flask,render_template, request, flash, redirect, url_for, send_file, jsonify

import sys
from FuncMile36 import main8
from multiprocessing import Process,Manager,Value
from ctypes import c_char_p

app = Flask(__name__)
manager = Manager()
file_name = manager.Value(c_char_p, "1234")
@app.route('/test')
def hello_world():
    return 'Hello, World!'

@app.route("/",  methods=('GET', 'POST'))
def viewentries():
     #url =''
    if request.method == 'POST':
        url = request.form['inp_url']

        if not url:
            flash('URL is required!')
        else:
            print('url entered is ', url)
            inp_arg = (url,file_name)
            heavy_process = Process(target=main8, args=(inp_arg,))
            heavy_process.start()
            #file_nm = main7(url)
            print('called function return_csv - check for created csv file', file_name)
            redirect_url = file_name.value+"/getCSV"
            return redirect(redirect_url)

    return render_template('index.html')  #variable=usernames_list

@app.route("/<int:ofile>/getCSV")
def getPlotCSV(ofile):
    return render_template('excel.html', inp_url = " ", csv = ofile )

@app.route("/getFilename")
def getFileName():
    print(file_name.value)
    return jsonify(filenm=file_name.value)

@app.route("/<int:ofile>/downloadCSV")
def downloadCSV(ofile):
    outfile = str(ofile)+ ".csv"
    return send_file(outfile,
                     mimetype='text/csv',
                     attachment_filename=outfile,
                     as_attachment=True)
