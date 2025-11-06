#Serve as the UI for my program 
#kyle marasa

from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import json
import os

app = Flask(__name__)
app.secret_key = "planttrackerkey" 

DataFile = os.path.join('data', 'plants.json')

def load_plants():
    if os.path.exists(DataFile):
       with open(DataFile, "r") as f:
           return json.load(f)
    return []


def save_plants(plants):
    os.makedirs(os.path.dirname(DataFile), exist_ok=True)
    with open(DataFile, "w") as f:
        json.dump(plants, f, indent=4)

if not os.path.exists(DataFile):
    with open(DataFile, 'w') as f:
        json.dump([], f)

@app.route('/')
def home():
    plants = load_plants()
    return render_template("home.html", plants=plants)

@app.route('/add', methods=['GET', 'POST'])
def add_plant():
    plants = load_plants()
    if request.method == 'POST':
        name = request.form.get("name")
        species = request.form.get("species")
        last_watered = request.form.get("last_watered")

        plants = load_plants() 
        new_plant = {
            "id": len(plants) + 1,
            "name": name,
            "species": species,
            "last_watered": last_watered if last_watered else None

        }
        plants.append(new_plant)
        save_plants(plants)
        return redirect(url_for('view_plants'))
    return render_template('add_plant.html')

@app.route('/plants')
def view_plants():
    plants = load_plants()
    return render_template('view_plants.html', plants=plants)

@app.route('/update/<int:plant_id>', methods=['GET', 'POST'])
def update_plant(plant_id):
    plants = load_plants()
    plant = next((p for p in plants if p["id"] == plant_id), None)

    if not plant:
        return "Plant not found", 404
    
    if request.method == 'POST':
        new_date = request.form['last_watered']
        plant['last_watered'] = new_date
        save_plants(plants)
        return redirect(url_for('view_plants'))
    return render_template('update_plant.html', plant=plant)

@app.route('/update', methods=['GET', 'POST'])
def update_select():
    plants = load_plants()
    if request.method == 'POST':
        plant_id = int(request.form['plant_id'])
        name = request.form.get('name')
        species=request.form.get('species')
        last_watered = request.form.get('last_watered')

        for plant in plants:
            if plant['id'] == plant_id:
                if name:
                    plant['name'] = name
                if species:
                    plant['species'] = species
                if last_watered:
                    plant['last_watered'] = last_watered
                break
        save_plants(plants)
        return redirect(url_for('view_plants'))
    return render_template('update_select.html', plants=plants)

@app.route('/delete_plant/<int:plant_id>', methods=['POST'])
def delete_plant(plant_id):
    file_path = os.path.join('data', 'plants.json')

   
    if not os.path.exists(file_path):
        flash("No plant data file found to delete from.", "error")
        return redirect(url_for('view_plants'))

   
    with open(file_path, 'r') as f:
        plants = json.load(f)

   
    updated_plants = [plant for plant in plants if plant['id'] != plant_id]

    with open(file_path, 'w') as f:
        json.dump(updated_plants, f, indent=4)

    flash("Plant deleted successfully!", "success")
    return redirect(url_for('view_plants'))

if __name__ == '__main__':
    app.run(debug=True)