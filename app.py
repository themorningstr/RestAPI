from flask import Flask


app = Flask(__name__)


stores  = [
    {
        "name" : "My Store",
        "item" : [
            {
                "name": "chair", 
                "price": 12.00

            }
        ]
    }

]




@app.get("/store")
def get_store():
    return {"store" : stores}