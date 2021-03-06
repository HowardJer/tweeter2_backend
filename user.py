from flask import Flask, request, Response
import mariadb
import dbcreds
import json

app = Flask(__name__)
CORS (app)

def connect(): 
    return mariadb.connect(
        host = dbcreds.host,
        port = dbcreds.port,
        user = dbcreds.user,
        password = dbcreds.password,
        database = dbcreds.database 
    )



@app.route("/api/user",methods=["GET", "POST", "PATCH", "DELETE"])
def post():
    if request.method == "GET":
        conn = None
        cursor = None
        results = None
        try:
            conn = mariadb.connect(user=dbcreds.username,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts")
            results = cursor.fetchall()
        except Exception as e:
            print(e)
        finally: 
            if(conn != None):
                conn.rollback() 
                conn.close() 
            if(cursor != None):
                cursor.close()
            if(results != None or results == []):
                posts = []
                for item in results:
                    post ={
                        "id":item[0],
                        "content":item[1]
                    }              
                    posts.append(post)
                return Response(json.dumps(posts, default=str),mimetype="application/json",status=200)
            else: 
                return Response("Failed", mimetype="html/text", status=400)
    if request.method == "POST":
        content = request.json.get("content")
        conn = None
        cursor = None
        results = None
        try:
            conn = mariadb.connect(user=dbcreds.username,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO posts (content) VALUES (?)",[content])
            conn.commit()
            post_id = cursor.lastrowid
        except Exception as e:
            print(e)
        finally: 
            if(conn != None):
                conn.rollback() 
                conn.close() 
            if(cursor != None):
                cursor.close()
            if(post_id != None ):
                
                
                post ={
                    "id":post_id,
                    "content": content
                }              
                    
                return Response(json.dumps(post, default=str),mimetype="application/json",status=201)
            else: 
                return Response("Failed", mimetype="html/text", status=400)            
    if request.method == "PATCH":
        content = request.json.get("content")
        post_id =request.json.get("id")
        conn = None
        cursor = None
        try:
            conn = mariadb.connect(user=dbcreds.username,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("UPDATE posts SET  content =? WHERE id=?",[content, post_id])
            conn.commit()
            post_id = cursor.lastrowid
        except Exception as e:
            print(e)
        finally: 
            if(conn != None):
                conn.rollback() 
                conn.close() 
            if(cursor != None):
                cursor.close()
            if(post_id != None ):
                
                
                post ={
                    "id":post_id,
                    "content": content
                }              
                    
                return Response(json.dumps(post, default=str),mimetype="application/json",status=201)
            else: 
                return Response("Failed", mimetype="html/text", status=400)            
    if request.method == "DELETE":
        post_id =request.json.get("id")
        conn = None
        cursor = None
        try:
            conn = mariadb.connect(user=dbcreds.username,password=dbcreds.password,host=dbcreds.host,port=dbcreds.port,database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM posts WHERE id=?",[post_id])
            rows = cursor.rowcount
            conn.commit()
            post_id = cursor.lastrowid
        except Exception as e:
            print(e)
        finally: 
            if(conn != None):
                conn.rollback() 
                conn.close() 
            if(cursor != None):
                cursor.close()
            if(rows == 1): 
                    
                return Response("Success",mimetype="html/text",status=201)
            else: 
                return Response("Failed", mimetype="html/text", status=400)        