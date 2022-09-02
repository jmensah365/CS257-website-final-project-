'''
A simple sample web application using Flask. Demonstrates the basics of routes, as well
as how to use forms with Flask.
author: AJ LeSure, Devin Lewis, Jeremiah Mensah, & Amy Czismar Dalal
CS 257, Winter 2022
'''

import flask
from flask import render_template, request
import json
import sys
import datasource
from datasource import DataSource
import math


app = flask.Flask(__name__)

# This line tells the web browser to *not* cache any of the files.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def home():
    '''
    Simple route to go to our main page.
    '''
    return render_template('data.html')

@app.route('/about.html')
def aboutPage():
    '''
    Simple route to go to our about page.
    '''
    return render_template('about.html')


@app.route('/data.html')
def backHome():
    '''
    Similar to the home function, this takes us back to the home page from every other page.
    '''
    return render_template('data.html')

@app.route('/search.html', methods=['GET', 'POST'])
def searchOptions():
    
    
    # This method is executed once you submit the search from the home page. It embeds the responses
    # into a web page.
    
    if request.method == 'POST':
        result = request.form
   
        # Here is where you would call one or more database methods with the form data.
        data = DataSource()
        
        user_input = result.get('keyword')
        print(user_input)
        actual_data = data.getFilmsByTitle(user_input)
       
        
        # This section filters results based on those selected by the user (year released, age, and streaming platform)
        year = result.get('year')
        age = result.get('age')
        streaming_platform = result.get('streaming_platform')
        
        filtered_data = data.filterYear(actual_data, year)
        filtered_data = data.filterAge(filtered_data, age)
        filtered_data = data.filterStreamingPlatform(filtered_data, str(streaming_platform))
                
        num_results = len(filtered_data)
        num_pages = int(math.ceil(num_results / 10))
        page_number = int(result.get('page_number'))
        total_num_pages = num_pages

        display_data = []
        if num_pages > 1:
            for i in range(10):
                if i + ((page_number - 1) * 10) < len(filtered_data):
                    display_data.append(filtered_data[i + ((page_number - 1) * 10)])
        else:
            display_data = filtered_data
            
        data.connection.close()
        
    return render_template('results.html', results=display_data, length=num_results, page_number=page_number, keyword=user_input, total_pages=total_num_pages, year=year, age=age, streaming_platform=streaming_platform)
     
@app.route('/results.html', methods=['GET', 'POST'])
def searchResult():
    
    
    # This method is executed once you submit the search from the home page. It embeds the responses
    # into a web page.
    
    if request.method == 'POST':
        result = request.form
   
        # Here is where you would call one or more database methods with the form data.
        data = DataSource()
        
        user_input = result.get('keyword')
        print(user_input)
        actual_data = data.getFilmsByTitle(user_input)
       
        
        # This section filters results based on those selected by the user (year released, age, and streaming platform)
        year = result.get('year')
        age = result.get('age')
        streaming_platform = result.get('streaming_platform')
        
        filtered_data = data.filterYear(actual_data, year)
        filtered_data = data.filterAge(filtered_data, age)
        filtered_data = data.filterStreamingPlatform(filtered_data, str(streaming_platform))
                
        num_results = len(filtered_data)
        num_pages = int(math.ceil(num_results / 10))
        page_number = int(result.get('page_number'))
        total_num_pages = num_pages

        display_data = []
        if num_pages > 1:
            for i in range(10):
                if i + ((page_number - 1) * 10) < len(filtered_data):
                    display_data.append(filtered_data[i + ((page_number - 1) * 10)])
        else:
            display_data = filtered_data
            
        data.connection.close()
        
    return render_template('results.html', results=display_data, length=num_results, page_number=page_number, keyword=user_input, total_pages=total_num_pages, year=year, age=age, streaming_platform=streaming_platform)
     

'''
Run the program by typing 'python3 localhost [port]', where [port] is one of 
the port numbers you were sent by my earlier this term.
'''
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = sys.argv[2]
    app.run(host=host, port=port)
