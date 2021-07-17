import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("pets", "pets", url_prefix="")

def format_date(d):
    if d:
        d = datetime.datetime.strptime(d, '%Y-%m-%d')
        v = d.strftime("%a - %b %d, %Y")
        return v
    else:
        return None

@bp.route("/search/<field>/<value>")
def search(field, value):
    # TBD
    return ""

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor()
    
    oby1 = request.args.get("order_by", "id") # TODO. This is currently not used. 
    order = request.args.get("order", "asc")
    if order == "asc" and oby1=="id":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.id")
    elif oby1 =="id":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.id desc")
    pets = cursor.fetchall()
    
    #order by name
    oby2 = request.args.get("order_by", "name") # TODO. This is currently not used. 
    order = request.args.get("order", "asc")
    if order == "asc" and oby2=="name":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.name")
        pets = cursor.fetchall()
    elif oby2=="name":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.name desc")
        pets = cursor.fetchall()
    
    
    #order by bought
    oby3 = request.args.get("order_by", "bought") # TODO. This is currently not used. 
    order = request.args.get("order", "asc")
    if order == "asc" and oby3=="name":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.bought")
        pets = cursor.fetchall()
    elif oby3=="bought":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.bought desc")
        pets = cursor.fetchall()
    
    #order by sold
    oby4 = request.args.get("order_by", "sold") # TODO. This is currently not used. 
    order = request.args.get("order", "asc")
    if order == "asc" and oby4=="sold":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.sold")
        pets = cursor.fetchall()
    elif oby4=="sold":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.sold desc")
        pets = cursor.fetchall()
    
    #order by species
    oby5 = request.args.get("order_by", "name") # TODO. This is currently not used. 
    order = request.args.get("order", "asc")
    if order == "asc" and oby5=="species":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.species")
        pets = cursor.fetchall()
    elif oby5=="name":
        cursor.execute(f"select p.id, p.name, p.bought, p.sold, s.name from pet p, animal s where p.species = s.id order by p.species desc")
        pets = cursor.fetchall()
    
    return render_template('index.html', pets = pets, order="desc" if order=="asc" else "asc")


@bp.route("/<pid>")
def pet_info(pid): 
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select p.name, p.bought, p.sold, p.description, s.name from pet p, animal s where p.species = s.id and p.id = ?", [pid])
    pet = cursor.fetchone()
    cursor.execute("select t.name from tags_pets tp, tag t where tp.pet = ? and tp.tag = t.id", [pid])
    tags = (x[0] for x in cursor.fetchall())
    name, bought, sold, description, species = pet
    data = dict(id = pid,
                name = name,
                bought = format_date(bought),
                sold = format_date(sold),
                description = description, #TODO Not being displayed
                species = species,
                tags = tags)
    return render_template("petdetail.html", **data)

@bp.route("/<pid>/edit", methods=["GET", "POST"])
def edit(pid):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select p.name, p.bought, p.sold, p.description, s.name from pet p, animal s where p.species = s.id and p.id = ?", [pid])
        pet = cursor.fetchone()
        cursor.execute("select t.name from tags_pets tp, tag t where tp.pet = ? and tp.tag = t.id", [pid])
        tags = (x[0] for x in cursor.fetchall())
        name, bought, sold, description, species = pet
        print(sold)
        data = dict(id = pid,
                    name = name,
                    bought = format_date(bought),
                    sold = format_date(sold),
                    description = description,
                    species = species,
                    tags = tags)
        return render_template("editpet.html", **data)
    elif request.method == "POST":
        description = request.form.get('description')
        sold = request.form.get("sold")
        # TODO Handle sold
        ###########
        cursor.execute("select p.sold from pet p where p.id = ?",[pid])
        pet_sold = cursor.fetchone()
        sold_data, = pet_sold
        sql_update_query = """update pet set description = ?, sold = ? where id = ?"""
        if sold_data!='' and not sold:
        	data = (description, '',pid)
        	cursor.execute(sql_update_query,data)
        	conn.commit()
        if sold_data=='' and sold:
        	today = datetime.data.today().strftime('%Y-%m-%d')
        	data = (description, today,pid)
        	cursor.execute(sql_update_query,data)
        	conn.commit()
        else:
        	sql_update_query = """update pet set description = ? where id = ?"""
        	data = (description,pid)
        	cursor.execute(sql_update_query,data)
        	conn.commit()
        return redirect(url_for("pets.pet_info", pid=pid), 302)
        
    



