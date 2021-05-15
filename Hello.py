from flask import Flask,render_template, request, flash, redirect, url_for, send_file

import sys
from FuncMile36 import main7

app = Flask(__name__)

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
            file_nm = main7(url)
            print('called function return_csv - check for created csv file', file_nm)
            redirect_url=file_nm+"/getCSV"
            return redirect(redirect_url)

    return render_template('index.html')  #variable=usernames_list

@app.route("/<int:ofile>/getCSV")
def getPlotCSV(ofile):
    outfile = str(ofile) +".csv"
    with open(outfile) as fp:  #outputs/Adjacency.csv
        csv = fp.read()
    return render_template('excel.html', inp_url = " ", csv = ofile )


@app.route("/<int:ofile>/downloadCSV")
def downloadCSV(ofile):
    outfile = str(ofile)+ ".csv"
    return send_file(outfile,
                     mimetype='text/csv',
                     attachment_filename=outfile,
                     as_attachment=True)
