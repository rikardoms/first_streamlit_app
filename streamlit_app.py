import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header('Fruityvice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
fruitvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruitvice_response.json())

fruityvice_normalized = pandas.json_normalize(fruitvice_response.json())
streamlit.dataframe(fruityvice_normalized)


streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("the fruit load list contains:")
streamlit.dataframe(my_data_row)

fruit_to_add = streamlit.text_input('What fruit would you like to add?', 'Kiwi')
my_cur.execute("INSERT INTO fruit_load_list VALUES('"+fruit_to_add+"')")
streamlit.text("Thanks for adding " + fruit_to_add )

#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)
