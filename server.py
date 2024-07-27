from flask import Flask, render_template, jsonify, request
from flask import Response
import json
from flask import redirect, url_for
import re 


app = Flask(__name__)

current_id = "10"
data = {
    "1": {
        "id": "1",
        "restaurant": "Mokyo",
        "image": "https://cdn.vox-cdn.com/thumbor/ptBaKm64tYZFqdPHrFGFJWOGqIQ=/0x0:5760x3840/1200x675/filters:focal(2523x1659:3443x2579)/cdn.vox-cdn.com/uploads/chorus_image/image/66250788/Mokyo_44.0.jpg",
        "alt": "Dining table with plates of lobster rolls, cauliflower, and meat.",
        "rating": "9.7",
        "helpfulReview": "This place is soooo good. Small plate restaurant, literally have taken three of my dates here just so I could eat the delicious food for free. It’s an Asian fusion place, so they have interesting dishes. Would definitely come here again. Drinks were kinda mid tho ngl.",
        "cuisine": ["Korean", "Asian Fusion"],
        "priceRange": "$$$",
        "popularDishes": ["Lobster Rolls", "Beef Tartare", "Octopus Congee"],
        "location": "East Village",
        "similarRestaurants": ["2"]
    },
    "2": {
        "id": "2",
        "restaurant": "C as in Charlie",
        "image": "https://assets-global.website-files.com/62ee0bbe0c783a903ecc0ddb/64516dd0d4af4fce01e3afe0_C%20as%20in%20Charlie%20tablescape%201.jpg",
        "alt": "Table with a nice spread of plates of various foods, forks and knives, and drinks.",
        "rating": "9.7",
        "helpfulReview": "A small plate restaurant. Went here with my sisters, and they offered us free drinks. I like how the food is inspired by Korean and Southern cuisines. The presentation of the food was very interesting. Would come again.",
        "cuisine": ["Korean", "Southern"],
        "priceRange": "$$",
        "popularDishes": ["Toast Roll", "Popcorn Chicken", "Mushroom Bibimbap"],
        "location": "Noho",
        "similarRestaurants": ["1"]
    },
    "3": {
        "id": "3",
        "restaurant": "DOMODOMO New York",
        "image": "https://images.getbento.com/accounts/59c8fb620c14dfe9bfe0d8a319bfed55/media/images/2812DOMOKASE_DOMODOMO.jpeg?w=1200&fit=crop&auto=compress,format&h=600",
        "alt": "Table with plates of sushi and pasta.",
        "rating": "9.8",
        "helpfulReview": "A date took me here so I didn't have to pay anything. That's a good thing because this place is lowkey expensive. The food is amazing though. I got one of the omakase sets, and each dish was impeccable. Come here with a date for sure.",
        "cuisine": ["Japanese", "Sushi", "Omakase"],
        "priceRange": "$$$",
        "popularDishes": ["Spicy Tuna Cones", "Yellowfish Carpaccio", "Miso Black Cod"],
        "location": "South Village",
        "similarRestaurants": ["4", "5", "10"]
    },
    "4": {
        "id": "4",
        "restaurant": "Nami Nori",
        "image": "https://img.cdn4dd.com/cdn-cgi/image/fit=contain,width=1200,height=672,format=auto/https://doordash-static.s3.amazonaws.com/media/store/header/463596.jpg",
        "alt": "Five handrolls with different toppings",
        "rating": "9.7",
        "helpfulReview": "A small plate restaurant. Went here with my sisters, and they offered us free drinks. I like how the food is inspired by Korean and Southern cuisines. The presentation of the food was very interesting. Would come again.",
        "cuisine": ["Japanese", "Sushi"],
        "priceRange": "$$$",
        "popularDishes": ["Coconut Shrimp", "Spicy Tuna Dip", "Scallop"],
        "location": "South Village",
        "similarRestaurants": ["3", "5", "10"]
    },
    "5": {
        "id": "5",
        "restaurant": "Temakase",
        "image": "https://irp.cdn-website.com/62f27e3a/dms3rep/multi/Temakase-34.jpg",
        "alt": "Two crispy rice pieces with crab on top.",
        "rating": "9.5",
        "helpfulReview": "Went here once with my ex, and another time with my suitemates. The atmosphere is very nice and usually quiet. The crispy rice dishes are sooo good and unique. I wish they gave more handrolls for the price. Solid place for a first date.",
        "cuisine": ["Japanese", "Sushi"],
        "priceRange": "$$",
        "popularDishes": ["Crispy Rice", "Spicy Tuna Crunch", "Spicy Scallop"],
        "location": "Ukrainian Village",
        "similarRestaurants": ["3", "4", "10"]
    },
    "6": {
        "id": "6",
        "restaurant": "Pho Bang",
        "image": "https://tastet.ca/wp-content/uploads/2018/11/pho-bang-restaurant-pho-montreal-16.jpg",
        "alt": "A person using chopsticks to hold up food from a bowl of pho.",
        "rating": "9.5",
        "helpfulReview": "My family has been going here for at least two decades. This place is very authentic, and you can tell just by the way it looks. The food is very cheap and flavorful. I've brought so many friends and dates to this place.",
        "cuisine": ["Vietnamese"],
        "priceRange": "$",
        "popularDishes": ["Pho", "Banh Mi", "Spring Rolls"],
        "location": "Chinatown",
        "similarRestaurants": ["7"]
    },
    "7": {
        "id": "7",
        "restaurant": "Little Kirin",
        "image": "https://images.squarespace-cdn.com/content/v1/64f1fad7f23a197b95107614/44b6b42b-4d67-4adc-a5a8-bb4513105383/P1400472.jpeg",
        "rating": "9.8",
        "helpfulReview": "Oh, man. I blasted a nut when I dipped that sandwich into the pho broth. The crust of the bread soaked in that scrumptious, delectable liquid -- chef's kiss. I wish my fingers would turn into Little Kirin's sandwiches so I could eat them at any time. A nut to remember.",
        "alt": "A table with a large spread of different food including sandwiches.",
        "cuisine": ["Vietnamese", "Sandwiches"],
        "priceRange": "$$",
        "popularDishes": ["Pho Sandwich", "Grandma's Pork Sandwich", "Pho Broth"],
        "location": "Ukranian Village",
        "similarRestaurants": ["6"]
    },
    "8": {
        "id": "8",
        "restaurant": "TabeTomo",
        "image": "https://assets3.thrillist.com/v1/image/2934572/1200x630",
        "alt": "A table with bowls of ramen and plates of karaage and gyoza.",
        "rating": "9.6",
        "helpfulReview": "Portions are HUGEE. A date brought me here since his family owns the restaurant. Very intimate lighting, but people were really loud. This place literally piles your bowls with so much food. Very good food, sad I didn't finish it.",
        "cuisine": ["Japanese", "Ramen"],
        "priceRange": "$$",
        "popularDishes": ["Tsukemen", "Takoyaki", "Karaage"],
        "location": "Ukranian Village",
        "similarRestaurants": ["9"]
    },
    "9": {
        "id": "9",
        "restaurant": "Ramen Ishida",
        "image": "https://images.happycow.net/venues/1024/16/18/hcmp161885_599700.jpeg",
        "alt": "A bowl of ramen with corn and herbs on the top.",
        "rating": "9.8",
        "helpfulReview": "The best ramen I've ever had. Literally nothing can beat it. However, the place is very small so the wait to get seated is long. Also it's in the sketchy part of the LES.",
        "cuisine": ["Japanese", "Ramen"],
        "priceRange": "$",
        "popularDishes": ["Tokyo Style Shoyu Ramen", "Pork Buns", "Truffle Ramen"],
        "location": "Lower East Side",
        "similarRestaurants": ["8"]
    },
    "10": {
        "id": "10",
        "restaurant": "SUGARFISH by sushi nozawa",
        "image": "https://sugarfishsushi.com/wp-content/uploads/2019/09/SFxsn_HmPg-05.jpg",
        "alt": "A plate of raw fish.",
        "rating": "9.8",
        "helpfulReview": "The sets are pretty affordable considering how many dishes you get. The lighting is very dim, so it makes the atmosphere intimate. I'd come here again if I hadn't already been to this place twice already. Def recommend.",
        "cuisine": ["Japanese", "Sushi"],
        "priceRange": "$$$",
        "popularDishes": ["Tuna Sashimi", "Toro Hand Roll", "Albacore"],
        "location": "Flatiron District",
        "similarRestaurants": ["3", "4", "5"]
    }
}

@app.route('/')
def index():
    # Show the three popular items (as an example)
    popular_items = list(data.values())[:3]
    return render_template('index.html', popular_items=popular_items)

def highlight_query_in_list(query, list_items):
    highlighted_items = []
    query_regex = re.compile(re.escape(query), re.IGNORECASE)
    for item in list_items:
        highlighted_item = query_regex.sub(lambda match: f"<strong>{match.group(0)}</strong>", item)
        highlighted_items.append(highlighted_item)
    return highlighted_items

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = ""
    if request.method == "POST":
        query = request.form.get('query', '').lower()
    else:
        query = request.args.get('query', '').lower()

    restaurant_results = {}
    cuisine_results = {}
    dish_results = {}

    for id, details in data.items():
        if query in details['restaurant'].lower():
            highlighted_name = highlight_query_in_list(query, [details['restaurant']])[0]
            restaurant_results[id] = {**details, 'restaurant': highlighted_name}

        if any(query in cuisine.lower() for cuisine in details['cuisine']):
            highlighted_cuisines = highlight_query_in_list(query, details['cuisine'])
            cuisine_results[id] = {**details, 'cuisine': highlighted_cuisines}

        if any(query in dish.lower() for dish in details['popularDishes']):
            highlighted_dishes = highlight_query_in_list(query, details['popularDishes'])
            dish_results[id] = {**details, 'popularDishes': highlighted_dishes}

    results_count = len(restaurant_results) + len(cuisine_results) + len(dish_results)

    return render_template('search_results.html', query=query, 
                           restaurantResults=restaurant_results, 
                           cuisineResults=cuisine_results, 
                           dishResults=dish_results, 
                           results_count=results_count)
# def highlight_query_in_list(query, list_items):
#     highlighted_items = []
#     # Compiling regex for case-insensitive partial match
#     query_regex = re.compile(re.escape(query), re.IGNORECASE)
#     for item in list_items:
#         # Using regex sub() method to replace the matched query with a bold tag
#         highlighted_item = query_regex.sub(lambda match: f"<strong>{match.group(0)}</strong>", item)
#         highlighted_items.append(highlighted_item)
#     return highlighted_items

# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == "POST":
#         query = request.form.get('query').lower()
        
#     else:  # Handle GET requests
#         query = request.args.get('query', '').lower()

#     filtered_restaurant_results = {}
#     for id, details in data.items():
#         restaurant_name = details['restaurant']
#         # Check if the query is in the restaurant name (case-insensitive)
#         if query.lower() in restaurant_name.lower():
#             # Highlight the query in the restaurant name for display
#             highlighted_name = restaurant_name.replace(query, f"<strong>{query}</strong>")
#             # Make a shallow copy of details to avoid altering original data
#             restaurant_details = details.copy()
#             restaurant_details['restaurant'] = highlighted_name
#             filtered_restaurant_results[id] = restaurant_details
    
#     # restaurantResults = {k: v for k, v in data.items() if query in v['restaurant'].lower()}
#     cuisineResults = {k: v for k, v in data.items() if any(query in cuisine.lower() for cuisine in v['cuisine'])}
#     dishResults = {k: v for k, v in data.items() if any(query in dish.lower() for dish in v['popularDishes'])}

#     for k, v in cuisineResults.items():
#         v['cuisine'] = highlight_query_in_list(query, v['cuisine'])

#     for k, v in dishResults.items():
#         v['popularDishes'] = highlight_query_in_list(query, v['popularDishes'])

#     if query:
#         highlighted_cuisines = highlight_query_in_list(query, cuisineResults)
#         highlighted_dishes = highlight_query_in_list(query, dishResults)
#         # Pass the highlighted results to the template
#     else:
#         # Regular, non-highlighted lists
#         highlighted_cuisines = cuisineResults
#         highlighted_dishes = dishResults

#     results_count = len(filtered_restaurant_results) + len(cuisineResults) + len(dishResults)


#     return render_template('search_results.html', query=query, 
#                            restaurantResults=filtered_restaurant_results, 
#                            cuisineResults=cuisineResults, 
#                            dishResults=dishResults, 
#                            results_count=results_count)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        # Extracting comma-separated string and converting to a list after stripping unwanted characters
        cuisine_string = request.form.get('cuisine')
        popular_dishes_string = request.form.get('popularDishes')
        
        # Splitting by comma and creating a list, ensuring to strip away brackets and quotes if present
        cuisine_list = [c.strip(" '[]") for c in cuisine_string.split(',')]
        popular_dishes_list = [d.strip(" '[]") for d in popular_dishes_string.split(',')]

        data[id]['helpfulReview'] = request.form.get('helpfulReview')
        data[id]['cuisine'] = cuisine_list
        data[id]['popularDishes'] = popular_dishes_list
        # Add or update other fields as necessary

        # Redirect to the view page to see changes
        return redirect(url_for('view', id=id))
    else:
        # Fetch the current restaurant data
        item = data.get(id)
        # Render the edit template with pre-populated data
        if item:
            return render_template('edit.html', item=item, id=id)  # Ensure 'id' is also passed to the template
        else:
            return "Restaurant not found", 404

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    global data
    global current_id

    if request.method == 'POST':
        current_id_int = int(current_id)
        current_id_int += 1
        current_id = str(current_id_int)
        entry = request.get_json()

        # Error handling
        errors = {}
       
        if not entry.get('restaurant'):
            errors['restaurant'] = 'Restaurant name cannot be blank.'
        if not entry.get('image'):
            errors['image'] = 'Image URL cannot be blank.'
        if not entry.get('alt'):
            errors['alt'] = 'Alt text cannot be blank.'
        # if not re.match(r'^\d+(\.\d{1})?$', entry.get('rating', '')):  # Correctly use the .get() method to provide a default value
        #     errors['rating'] = 'Rating must be a number with at most one decimal place.'
        if entry.get('rating'):
            try:
                rating = float(entry['rating'])
                if not (0.0 <= rating <= 10.0):
                    errors['rating'] = 'Rating must be between 0.0 and 10.0.'
            except ValueError:
                errors['rating'] = 'Rating must be a number.'
        if not entry.get('helpfulReview'):
            errors['helpfulReview'] = 'Helpful review cannot be blank.'
        if not entry.get('cuisine'):
            errors['cuisine'] = 'At least one cuisine must be specified.'
        if not entry.get('priceRange'):
            errors['priceRange'] = 'Price range cannot be blank.'
        if not entry.get('popularDishes'):
            errors['popularDishes'] = 'At least one popular dish must be specified.'
        if not entry.get('location'):
            errors['location'] = 'Location cannot be blank.'

        if errors:
            return jsonify({'success': False, 'errors': errors}), 400

        # Logic to save data to the server/database
        # new_id = str(max([int(x) for x in data.keys()]) + 1)  # Generate a new ID
        entry['id'] = current_id
        data[current_id] = entry

        # After saving the new item in the add_item() route
        return jsonify({'success': True, 'message': 'New item successfully created.', 'id': current_id})


    else:
        return render_template('add.html')



@app.route('/view/<id>')
def view(id):
    item = data.get(id)
    similar_restaurants = [data[sim_id] for sim_id in item['similarRestaurants'] if sim_id in data]
    # Pass the similar restaurants' details to the template without highlighting
    return render_template('view.html', item=item, similar_restaurants=similar_restaurants)




if __name__ == '__main__':
    app.run(debug=True)
