from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
import datetime

app = Flask(__name__)
api = Api(app)

file = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/flower_color_symbolism.csv"
df = pd.read_csv(file)
df['Color'] = df['Flower Color '].str.split().str[0]
colors = df['Color'].to_list()

# We add the parameter "forname" to the get function. 
# Then we use this parameter to return a custom phrase
class my_API_class(Resource):
    def get(self, forname):
        sentence = 'Hi ' + forname + ', welcome in my API'
        return {'hello': sentence}

# We need to indicate how the query will be performed.
# Concretely, what will follow the request URL will be a string that we will name as a "forname" variable.
api.add_resource(my_API_class, '/<string:forname>')

class get_meaning_class(Resource):
    def get(self, color): 


        if color in colors:

            current_date = datetime.date.today().strftime('%Y-%m-%d')
            meaning = df[df['Color'] == color]['Meaning'].values[0]

            return {
                color: meaning,
                "current_date": current_date
                }
        
        else:

            return {'Not found' : 'Please pick a color from the following : ' + ', '.join(colors)}

api.add_resource(get_meaning_class, '/flowers/<string:color>')
        

if __name__ == '__main__':
    app.run(debug=True)
