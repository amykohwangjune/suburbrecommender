import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from io import StringIO

plt.style.use('ggplot')


def generate_population_pyramid_chart(postcode=3177):

    #read file containing population data by suburb
    file_path = os.path.dirname(os.path.abspath(
        __file__))+f"\chart_suburb_information\population_pyramid.csv"
    df_chart = pd.read_csv(file_path)

    #try clause incase suburb data is not present
    try:

        #select suburb using postcode
        df_chart = df_chart[df_chart.iloc[:, 0] == ("POA" + str(postcode))]

        #remove useless columns
        df_chart = df_chart.iloc[:, 4:]

        #extract clolumns specific for males and females
        df_Females = df_chart.iloc[:, [i[-1] == "F" for i in df_chart.columns]]
        df_Males = df_chart.iloc[:, [i[-1] == "M" for i in df_chart.columns]]

        #define age brackets
        AgeClass = ["0-4", "5-14", "15-19", "20-24", "25-34", "35-44", "45-54", "55-64",
                    "65-74", "75-84", "85+"]

        #construct df of values we want to plot
        df = pd.DataFrame({"Age": ["0-4", "5-14", "15-19", "20-24", "25-34",
                                   "35-44", "45-54", "55-64", "65-74", "75-84",
                                   "85+"],

                           "Male": [i for i in df_Males.iloc[0, :]],
                           "Female": [i for i in df_Females.iloc[0, :]]
                           })

        ##PLOT POULATION PYRAMID

        #define x and y limits
        y = range(0, len(df))
        x_male = df['Male']
        x_female = df['Female']

        #define plot parameters
        fig, axes = plt.subplots(ncols=2, sharey=True, figsize=(5, 5))

        #specify background color and plot title
        #fig.patch.set_facecolor('xkcd:light grey')
        # plt.figtext(.5,.9,"Population Pyramid ", fontsize=15, ha='center')

        #define male and female bars
        axes[0].barh(y, x_male, align='center',
                     color=(1.0, 74/255.0, 51/255.0))
        axes[0].set(title='Males')
        axes[1].barh(y, x_female, align='center',
                     color=(52/255.0, 138/255.0, 189/255.0))
        axes[1].set(title='Females')

        #adjust grid parameters and specify labels for y-axis
        # axes[1].grid()
        axes[0].set(yticks=y, yticklabels=df['Age'])
        axes[0].invert_xaxis()
        # axes[0].grid()

        #display plot
        # save_path = os.path.dirname(os.path.abspath(__file__))+f"\charts\population_pyramid.jpg"
        # plt.savefig(save_path, bbox_inches='tight')

        imgdata = StringIO()
        plt.savefig(imgdata, format='svg', bbox_inches='tight')
        imgdata.seek(0)
        data = imgdata.getvalue()

        return data

    except:
        return "No Detailed Statistis available for this suburb"


def generate_donut_chart(postcode=3177):

    #get dataset containing total Male and Female population
    file_path = os.path.dirname(os.path.abspath(
        __file__))+f"\chart_suburb_information\population_pyramid.csv"
    df_chart = pd.read_csv(file_path)

    df_chart = df_chart.iloc[:, [0, 1, 2]]

    #try clause incase suburb data is not present
    try:

        #select suburb using postcode
        df_chart = df_chart[df_chart.iloc[:, 0] == ("POA" + str(postcode))]

        ##CREATE DONUT CHART
        plt.figure(figsize=(5, 5))

        #add circle to make a donut
        my_circle = plt.Circle((0, 0), 0.7, color='white')

        plt.title('Total Population Of Males and Females')

        # add pie chart
        plt.pie(np.squeeze(df_chart.iloc[:, [1, 2]]), labels=[
                "Male", "Female"])
        p = plt.gcf()
        p.gca().add_artist(my_circle)

        #save file
        # save_path = os.path.dirname(os.path.abspath(__file__))+f"\charts\population_donut_chart.jpg"
        # plt.savefig(save_path, bbox_inches='tight')

        imgdata = StringIO()
        plt.savefig(imgdata, format='svg', bbox_inches='tight')
        imgdata.seek(0)
        data = imgdata.getvalue()
        return data

    except:
        return ""


def generate_diversity_chart(postcode=3177):

    #get dataset containing relevant information
    file_path = os.path.dirname(os.path.abspath(
        __file__))+f"\chart_suburb_information/nationalities.csv"
    df_chart = pd.read_csv(file_path)

    #try clause incase suburb data is not present
    try:

        #select suburb using postcode
        df_chart = df_chart[df_chart.iloc[:, 0] == ("POA" + str(postcode))]

        #get information about selected nationalities
        nationalities = ['Chinese', 'English', 'Filipino', 'German',
                         'Greek', 'Indian', 'Lebanese', 'Australian']

        population = [i for i in df_chart.iloc[0, 1:]]

        ##CREATE BAR CHART
        plt.figure(figsize=(6, 3))

        plt.bar(nationalities, population)
        plt.title('Diversity Among The Suburb')
        plt.xlabel('Nationality')
        plt.ylabel('Number of People')
        plt.xticks(rotation=45)

        #save file
        # save_path = os.path.dirname(os.path.abspath(__file__))+f"\charts\diversity_chart.jpg"
        # plt.savefig(save_path, bbox_inches='tight')

        imgdata = StringIO()
        plt.savefig(imgdata, format='svg', bbox_inches='tight')
        imgdata.seek(0)
        data = imgdata.getvalue()
        return data

    except:
        return ""


def generate_transport_chart(postcode=3177):

    #get dataset containing relevant information
    file_path = os.path.dirname(os.path.abspath(
        __file__))+f"\chart_suburb_information\method_transport.csv"
    df_chart = pd.read_csv(file_path)

    #try clause incase suburb data is not present
    try:

        #select suburb using postcode
        df_chart = df_chart[df_chart.iloc[:, 0] == ("POA" + str(postcode))]

        #get information about selected transport methods
        transport = ["Train", "Bus", "Ferry", "Tram", "Taxi/Rideshare",
                     "Car Driver", "Car Passenger", "Motorbike", "Bicycle"]

        population = [i for i in df_chart.iloc[0, 1:]]

        ##CREATE BAR CHART
        plt.figure(figsize=(6, 3))

        plt.bar(transport, population)
        plt.title('Transport Methods Used By People')
        plt.ylabel('Number of People')
        plt.xticks(rotation=45)

        #save file
        # save_path = os.path.dirname(os.path.abspath(__file__))+f"\charts/transport_chart.jpg"
        # plt.savefig(save_path, bbox_inches='tight')

        imgdata = StringIO()
        plt.savefig(imgdata, format='svg', bbox_inches='tight')
        imgdata.seek(0)
        data = imgdata.getvalue()
        return data

    except:
        return ""


def generate_religion_chart(postcode=3177):

    #get dataset containing relevant information
    file_path = os.path.dirname(os.path.abspath(
        __file__))+f"\chart_suburb_information/religion.csv"
    df_chart = pd.read_csv(file_path)

    #try clause incase suburb data is not present
    try:

        #select suburb using postcode
        df_chart = df_chart[df_chart.iloc[:, 0] == ("POA" + str(postcode))]

        #get information about selected transport methods
        religions = ["Buddhism", "Anglican", "Baptist", "Catholic",
                     "Hinduism", "Islam", "Judaism"]

        population = [i for i in df_chart.iloc[0, 1:]]

        ##CREATE BAR CHART
        plt.figure(figsize=(6, 3))

        plt.bar(religions, population)
        plt.title('Religions of the People')
        plt.ylabel('Number of People')
        plt.xticks(rotation=45)

        #save file
        # save_path = os.path.dirname(os.path.abspath(__file__))+f"\charts/religion_chart.jpg"
        # plt.savefig(save_path, bbox_inches='tight')

        imgdata = StringIO()
        plt.savefig(imgdata, format='svg', bbox_inches='tight')
        imgdata.seek(0)
        data = imgdata.getvalue()
        return data

    except:
        return ""
