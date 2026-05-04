from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ------------------- TABLES -------------------

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    purchase_dt = db.Column(db.String(50))
    cost = db.Column(db.Float)

class InventoryDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer)
    inventory_details = db.Column(db.String(200))

class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_ip = db.Column(db.String(50))
    device_details = db.Column(db.String(200))
    config_changed = db.Column(db.Boolean)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_by = db.Column(db.String(50))
    post_dt = db.Column(db.String(50))
    post_details = db.Column(db.String(200))

# Create database
with app.app_context():
    db.create_all()

# ------------------- Q1 API -------------------

@app.route('/getInventoryDetails', methods=['GET'])
def get_inventory():
    start = request.args.get('start_date')
    end = request.args.get('end_date')

    data = Inventory.query.filter(
        Inventory.purchase_dt >= start,
        Inventory.purchase_dt <= end
    ).all()

    result = []
    for item in data:
        details = InventoryDetails.query.filter_by(inventory_id=item.id).all()
        result.append({
            "id": item.id,
            "date": item.purchase_dt,
            "cost": item.cost,
            "details": [d.inventory_details for d in details]
        })

    return jsonify(result)

# ------------------- Q2 API -------------------

@app.route('/deviceConfigNotification', methods=['GET'])
def notify():
    devices = Devices.query.filter_by(config_changed=True).all()

    result = []
    for d in devices:
        result.append({
            "device_id": d.id,
            "message": "Configuration changed!"
        })

    return jsonify(result)

# ------------------- Q3 API -------------------

@app.route('/getPostsUploaded', methods=['GET'])
def get_posts():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 5))

    posts = Posts.query.offset((page-1)*limit).limit(limit).all()

    result = []
    for p in posts:
        result.append({
            "id": p.id,
            "post_by": p.post_by,
            "date": p.post_dt,
            "details": p.post_details
        })

    return jsonify(result)

# ------------------- RUN APP -------------------


with app.app_context():
    if not Inventory.query.first():
        i1 = Inventory(purchase_dt="2023-05-10", cost=1000)
        i2 = Inventory(purchase_dt="2023-08-15", cost=2000)

        db.session.add_all([i1, i2])
        db.session.commit()

        d1 = InventoryDetails(inventory_id=i1.id, inventory_details="Keyboard")
        d2 = InventoryDetails(inventory_id=i2.id, inventory_details="Mouse")

        db.session.add_all([d1, d2])

        dev1 = Devices(device_ip="192.168.1.1", device_details="Router", config_changed=True)
        dev2 = Devices(device_ip="192.168.1.2", device_details="Switch", config_changed=False)

        db.session.add_all([dev1, dev2])

        p1 = Posts(post_by="Alice", post_dt="2023-01-01", post_details="Post 1")
        p2 = Posts(post_by="Bob", post_dt="2023-01-02", post_details="Post 2")

        db.session.add_all([p1, p2])

        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)



# http://127.0.0.1:5000/getInventoryDetails?start_date=2023-01-01&end_date=2023-12-31
# http://127.0.0.1:5000/deviceConfigNotification
# http://127.0.0.1:5000/getPostsUploaded?page=1&limit=1

