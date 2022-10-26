import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Avaz New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🍓 Build Your Own Smoothie 🍇🥝')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# display the table on the page
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

# create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # streamlit.text(fruityvice_response.json()) # Just writes data to the screen
      # Take the json version of the response and normalize it
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized

# New section to display Fruityvice API response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
      # import requests
      # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
      #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      # streamlit.text(fruityvice_response.json()) # Just writes data to the screen
      # Take the json version of the response and normalize it
      #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      # output it on the screen as a table
      # streamlit.dataframe(fruityvice_normalized)
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()

# don't run anything past here whie we troubleshoot
# streamlit.stop()

streamlit.header("View our fruit list - add your favorites!")
# Snowflake related functions
def get_fruit_load_list():
      with my_cnx.cursor() as my_cur:
            my_cur.execute("select * from fruit_load_list")
            return my_cur.fetchall()
      
# add a button to load the fruit
if streamlit.button('Get Fruit List'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      my_data_rows = get_fruit_load_list()
      my_cnx.close()
      streamlit.dataframe(my_data_rows)
      

# import snowflake.connector
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
# my_data_row = my_cur.fetchone()
# my_data_rows = my_cur.fetchall()
# streamlit.text("Hello from Snowflake:")
# streamlit.text("The Fruit Load List contains:")
# streamlit.header("The Fruit Load List contains:")
# streamlit.text(my_data_row)
# streamlit.dataframe(my_data_row)
# streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
# add_my_fruit = streamlit.text_input('What fruit would you like to add?')

# my_cur.execute("insert into fruit_load_list values ('from Streamlit')");

def insert_row_snowflake(new_fruit):
      with my_cnx.cursor() as my_cur:
            my_cur.execute("insert into fruit_load_list values ('"+ new_fruit + "')");
            return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function = insert_row_snowflake(add_my_fruit)
      my_cnx.close()
      streamlit.text(back_from_function)

      
      
