#List of imports
from flask import Flask
from flask import request
from flask import render_template
import requests
from flask import redirect, url_for
from bson import json_util

app = Flask(__name__)


#Route meant for creating all the records
@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        servingsize = request.form['servingsize']
        calories = request.form['calories']
        protein = request.form['protein']
        carbs = request.form['carbs']
        fat = request.form['fat']
        water = request.form['water']

        req = {"name": name, "servingsize": servingsize, "calories": calories, "protein": protein, "carbs": carbs, "fat": fat, "water": water}
        url = "https://lightenup.azurewebsites.net/api/createrecord"
        
        requests.post(url, json=req)
        return redirect(url_for('records'))

    createURL = url_for('records')
    return render_template('create.html', url=createURL)


#Default route for introductory page
#Route meant for displaying all the records
@app.route("/")
@app.route('/records', methods=['GET', 'POST'])
def records():
    cals = 0
    waterVar = 0
    proteinVar = 0
    carbsVar = 0
    fatVar = 0

    if request.method == 'POST':
        return render_template("records.html")
    else:
        readUrl = "https://lightenup.azurewebsites.net/api/readrecords"
        req = requests.get(readUrl, params={"query":"{}"})
        ret = req.text
    
        try:
            response = json_util.loads(ret)
        except:
            response = {}
            
        for x in response:
            del x["_id"]
            cals += int(x["calories"])
            proteinVar += int(x["protein"])
            carbsVar += int(x["carbs"])
            fatVar += int(x["fat"])
            waterVar += int(x["water"])

        totalCals = cals
        cals = round((cals / 3700) * 100)
        if(cals == 0):
            cals = 1

        #3700 for males, 2700 for females
        totalWater = waterVar
        waterVar = round((waterVar / 3700) * 100)
        if(waterVar == 0):
            waterVar = 1
        
        return render_template('records.html', allCals=totalCals, allWater=totalWater, parent_list=response, calories = cals, water = waterVar, protein = proteinVar, carbs = carbsVar, fat = fatVar)
    

#Route meant for deleting records
@app.route('/delete')
@app.route('/delete/<string:id>')
def delete(id):
    deleteUrl = "https://lightenup.azurewebsites.net/api/deleterecord"
    name = {"name":id}
    requests.delete(deleteUrl, json=name)

    return redirect(url_for('records'))



#Route meant for updating records
@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update(id):
    allRecVar = url_for('records')
    updateUrl = "https://lightenup.azurewebsites.net/api/updaterecord"
    readUrl = "https://lightenup.azurewebsites.net/api/readrecords"
    
    nameVar = ""
    servingSizeVar = ""
    caloriesVar = ""
    proteinVar = ""
    carbsVar = ""
    fatsVar = ""

    id = '"' + id + '"'
    query = '{"name":' + id + '}'
    #'{"title":"test"}'
    param = {"query":f'{{"name":{id}}}'}

    req = requests.get(readUrl, params=param)
    ret = req.text

    try:
        response = json_util.loads(ret)
    except:
        response = {}

    for x in response:
        nameVar = x["name"]
        servingSizeVar = x["servingsize"]
        caloriesVar = x["calories"]
        proteinVar = x["protein"]
        carbsVar = x["carbs"]
        fatsVar = x["fat"]
        waterVar = x["water"]

    #When submitted, delete old record, and create a whole new record

    updateResponse = {"name":nameVar, "servingsize":servingSizeVar, "calories":caloriesVar, "protein": proteinVar, "carbs": carbsVar, "fat":fatsVar}

    if request.method == 'POST':
        name = request.form['name']
        servingsize = request.form['servingsize']
        calories = request.form['calories']
        protein = request.form['protein']
        carbs = request.form['carbs']
        fat = request.form['fat']
        water = request.form['water']

        updateVar = {"name": name, "servingsize": servingsize, "calories": calories, "protein": protein, "carbs": carbs, "fat": fat, "water": water}
        query = {"name": nameVar}
        param3 = [query, updateVar]
        requests.put(updateUrl, json=param3)
        return redirect(url_for('records'))

    return render_template('update.html', name=nameVar, servingsize=servingSizeVar, calories=caloriesVar, protein=proteinVar, carbs=carbsVar, fat=fatsVar, allRec = allRecVar, water=waterVar)


#Route Redirections
@app.route('/<action>')
def choice(action):
    if action == "create":
        return redirect(url_for('create'))
    else:
        return redirect(url_for('records'))

