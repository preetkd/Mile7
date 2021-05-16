from flask import Flask,render_template, request, flash, redirect, url_for, send_file

import sys
import threading
import asyncio

from FuncMile36 import main7

print("In flask global level: {threading.current_thread().name}")
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
            print("Inside flask function: {threading.current_thread().name}")
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            file_nm = loop.run_until_complete(main7(url))
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
