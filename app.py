from flask import Flask,render_template,Response, request
import pymongo 
import json
from bson.objectid import ObjectId
app = Flask(__name__)

try:
    myclient = pymongo.MongoClient(host="localhost",port=27017,serverSelectionTimeoutMS=1000)
    db = myclient.companyPy
    myclient.server_info()
    
except:
    print("Error")
@app.route("/users", methods=["POST"])
def create_user( ):
    try:
        user ={
            "name":request.form["name"] ,
            "lastName":request.form["lname"]
        }
        dbResponse = db.users.insert_one(user)
        # for attr in dir(dbResponse):
        #     print(attr)
        return Response(
            response=json.dumps(
                {
                    "message":"user Created","id":f"{dbResponse.inserted_id}"}
                ),
            status=200,
            mimetype="application/json" 
        )
    except Exception as ex:
        return Response(
            response=json.dumps(
                {"message":"Error While getting "}
                ),
            status=500,
            mimetype="application/json" 
        )
  
@app.route("/getUsers", methods=["GET"])
def get_user( ):
    try:
        data = list(db.users.find())
        print(data)
        for user in data:
            user["_id"] = str(user["_id"])
        return Response(
            response=json.dumps(
                data
                ),
            status=200,
            mimetype="application/json" 
        )
    except Exception as ex:
       return Response(
            response=json.dumps(
                {"message":"Error While getting Records "}
                ),
            status=500,
            mimetype="application/json" 
        )
    


@app.route("/updateUsers/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"name":request.form["name"]}}
            )
        return Response(
            response=json.dumps(
                {"message":f"{dbResponse.modified_count } user update"}
                ),
            status=200,
            mimetype="application/json" 
        )

    except Exception as ex:
        return Response(
            response=json.dumps(
                {"message":"Error While  Updateing "}
                ),
            status=500,
            mimetype="application/json" 
        )

@app.route("/deleteUsers/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one(
            {"_id":ObjectId(id)},
            
            )
        return Response(
            response=json.dumps(
                {"message":f"{id} is deleted. only {dbResponse.deleted_count} deleted."}
                ),
            status=200,
            mimetype="application/json" 
        )

    except Exception as ex:
        return Response(
            response=json.dumps(
                {"message":"Error While  deleteing "}
                ),
            status=500,
            mimetype="application/json" 
        )


'''
@app.route("/about")
def about():
    return render_template("index.html");
'''

if __name__ =="__main__":
    app.run(debug=True,port=8000)
    #app.run(debug=True) #default is 5000