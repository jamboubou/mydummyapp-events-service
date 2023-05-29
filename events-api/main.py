import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
from ddtrace.runtime import RuntimeMetrics
RuntimeMetrics.enable()


@app.route('/create', methods=['POST'])
def create_event():
    try:        
        _json = request.json
        _name = _json['name']
        _description = _json['description']
        _location = _json['location']
        _type = _json['type']	
        if _name and _description and _location and _type and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)		
            sqlQuery = "INSERT INTO event(name, description, location, type) VALUES(%s, %s, %s, %s)"
            bindData = (_name, _description, _location, _type)            
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Event added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()          
     
@app.route('/event')
def event():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, description, location, type FROM event")
        eventRows = cursor.fetchall()
        respone = jsonify(eventRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/event/')
def event_details(event_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, description, location, type FROM event WHERE id =%s", event_id)
        eventRow = cursor.fetchone()
        respone = jsonify(eventRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/update', methods=['PUT'])
def update_event():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _description = _json['description']
        _location = _json['location']
        _type = _json['type']
        if _name and _description and _location and _type and _id and request.method == 'PUT':			
            sqlQuery = "UPDATE event SET name=%s, description=%s, location=%s, type=%s WHERE id=%s"
            bindData = (_name, _description, _location, _type, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Event updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/delete/', methods=['DELETE'])
def delete_event(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM event WHERE id =%s", (id,))
		conn.commit()
		respone = jsonify('Event deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/', methods=['GET'])
def health_check():   
    message = {
        'status': 200,
        'message': 'Alive',
    }
    respone = jsonify(message)
    respone.status_code = 200
    return respone


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)