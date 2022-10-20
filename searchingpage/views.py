from asyncio.windows_events import NULL
from django.shortcuts import render
import pymongo
from .modules import wsm
from .modules import charts

server = "localhost"
port = 27017
#Establish a connection with mongo instance.
conn = pymongo.MongoClient(server, port)

# First define the database name
dbname = conn['fit3164_fyp']

# Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection)
uni_name = dbname["university_name"]

#get collection with suburb scores and related data
suburb_scores_collection = dbname["suburb_scores"]

# Get the rental cost
rent_cost = dbname["rent_cost"]


# Create your views here.
def searchingpage(request):
    universities = uni_name.find({})
    rent = rent_cost.aggregate([
        {"$group": {"_id": NULL,
                    "maxValue": {"$max": "$rent"},
                    "minValue": {"$min": "$rent"}}
         }
    ])
    rentcost = []
    for result in rent:
        rentcost.append(result)
    # Sample Output : [{'_id': 0, 'maxValue': '$400 ', 'minValue': '$0'}]

    rentMax = rentcost[0]['maxValue']
    rentMin = rentcost[0]['minValue']

    return render(request, 'searchingpage/searching.html', {"uni": universities, "rentMax": rentMax, "rentMin": rentMin})


#integrate so that this runs after submit is pressed
def resultpage_view(request):
    if request.method == 'POST':
        university = request.POST['university']
        rent = int(request.POST['avg_rent'])
        distance = int(request.POST['city_distance'])
        # rent, distance, safety, early_trans, night_trans, uni drive distance
        importance_variables = []
        rental_importance = int(request.POST['rental_importance'])
        distance_importance = int(request.POST['distance_importance'])
        safety = int(request.POST['safety'])
        transit_importance = int(request.POST['transit_importance'])
        night_importance = int(request.POST['night_importance'])
        city_importance = int(request.POST['city_importance'])
        importance_variables.append(rental_importance)
        importance_variables.append(distance_importance)
        importance_variables.append(safety)
        importance_variables.append(transit_importance)
        importance_variables.append(night_importance)
        importance_variables.append(city_importance)
        for i in range(3):
            importance_variables.append(0)

        model = wsm.WSM(university, importance_variables, distance, rent)

        model = sorted(model, key=lambda d: d['suburb_score'], reverse=True)

        # print(model)

    #remove previous results from mongodb collection
    suburb_scores_collection.remove({})

    #save all the current results into mongodb collection so it can be used for individual suburb details later
    if len(model) > 1:
        suburb_scores_collection.insert_many(model)

    elif len(model) == 1:
        model[0]["suburb_score"] = float(model[0]["suburb_score"])
        suburb_scores_collection.insert_one(model[0])

    #send to error page if no recommendations generated
    if len(model) == 0:
        return render(request, 'searchingpage/error.html')

    #send to regular site if there are suburb recommendations
    else:
        return render(request, 'searchingpage/results.html', {"suburbs": model})


def detail_view(request, suburb_name_postcode, *args, **kwargs):
    suburb_cursor = suburb_scores_collection.find(
        {"suburb_name_postcode": suburb_name_postcode})

    #get object (there should only be one suburb returned in the cursor)
    for suburb_details in suburb_cursor:
        suburb_object = suburb_details

    pyramid_chart = charts.generate_population_pyramid_chart(
        int(suburb_object["postcode"]))
    donut_chart = charts.generate_donut_chart(int(suburb_object["postcode"]))
    diversity_chart = charts.generate_diversity_chart(
        int(suburb_object["postcode"]))
    transport_chart = charts.generate_transport_chart(
        int(suburb_object["postcode"]))
    religion_chart = charts.generate_religion_chart(
        int(suburb_object["postcode"]))

    return render(request, "searchingpage/detail.html", {"suburb": suburb_object, "pyramid_chart": pyramid_chart,
                                                         "donut_chart": donut_chart, "diversity_chart": diversity_chart, "transport_chart": transport_chart, "religion_chart": religion_chart})
