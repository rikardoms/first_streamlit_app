import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
from pymongo import MongoClient

# Initialize connection.
# Uses st.experimental_singleton to only run once.
def init_connection():
    print(streamlit.secrets["mongo"])
    #return pymongo.MongoClient(st.secrets["mongo"])

# Pull data from the collection.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.


  
client = init_connection()
#items = get_data()
  
streamlit.header('HUNTER TRADER')
streamlit.header('MULT-CORRETORA - ANALISE')

# Print results.
#for item in items:
#    st.write(f"{item['date']} | {item['type']} | {item['result']} | {item['timeframe']} | {item['active']}")


streamlit.stop()



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


def get_fruityvice_data(this_fruit_choice):
  fruitvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruitvice_response.json())
  return fruityvice_normalized

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
    return "Thanks for adding" + new_fruit

 
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()



#streamlit.stop()

#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchall()
#streamlit.header("the fruit load list contains:")
#streamlit.dataframe(my_data_row)

streamlit.header('The fruit load list contains:')
fruit_to_add = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(fruit_to_add)
  streamlit.text(back_from_function)

#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)
