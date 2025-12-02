import streamlit as st
import mysql.connector as sql
import pandas as pd

#connection func.
def get_connection():
    return sql.connect(
        host="172.21.144.1",
        user="py_user",
        password="qwe123QWE",
        database="ncaafb_db",
       )

def fetch_table(query):
    conn=get_connection()
    df=pd.read_sql(query,conn)
    conn.close()
    return df

#load Data
teams_df=fetch_table("SELECT * FROM teams;")
players_df=fetch_table("SELECT * FROM players;")
stats_df=fetch_table("select * from stats;")
season_sch_df=fetch_table("select * from seasons;")
rankings_df=fetch_table("select * from rankings;")
venue_df=fetch_table("select * from venue;")
coaches_df=fetch_table("select * from coaches")

st.sidebar.title("Data Analysis")
option=st.sidebar.radio(
    "Navigate",("Home","Team", "Players","Statistics","Seasons and Schedule", "Rankings", "Venue", "Coaches","Analysis")
)

if option=="Home":
        st.markdown("<h1 style='font-size:40px;'>Welcome to NCAAFB Data - Kickoff ⚽</h1>",
    unsafe_allow_html=True
)
        st.header("Data Analysis Home page")

elif option=="Team":
        st.title("Teams overview")
        st.write("All Teams data")
        st.dataframe(teams_df)
        
elif option=="Players":
      st.title("Players Overview")
      st.write("All Players data")
      

      # Text input for search
      search_term = st.text_input("🔍 Search by name (first_name / last_name):", "")

      if search_term:
        # Case-insensitive search across first_name and last_name
        query_filtered = """
            SELECT * 
            FROM players
            WHERE LOWER(first_name) LIKE LOWER(%s)
               OR LOWER(last_name) LIKE LOWER(%s);
        """
        params = [f"%{search_term}%", f"%{search_term}%"]
        conn = get_connection()
        players_df = pd.read_sql(query_filtered, conn, params=params)
        conn.close()
      else:
        # Default: fetch all players
        query_all = "SELECT * FROM players;"
        players_df = fetch_table(query_all)

      # Display results
      st.dataframe(players_df.reset_index(drop=True))

      # sidebar Filters
      category=st.sidebar.selectbox("Select your Category", ["Position", "Status", "Eligibility"])

      # Get values from chosen Category from SQL
      query_distinct = f"SELECT DISTINCT {category} FROM players;"
      distinct_values_df = fetch_table(query_distinct)
      distinct_values = distinct_values_df[category].tolist()

      sub_filter = st.sidebar.selectbox(f"Select {category}", distinct_values)

    # Filtered query
      query_filtered = f"""
        SELECT * 
        FROM players
        WHERE {category} = '{sub_filter}';
       """
      filtered_df = fetch_table(query_filtered)

      st.write(f"Players filtered by '{category}': '{sub_filter}'")
      st.dataframe(filtered_df)

elif option=="Statistics":
      st.title("Statistics Overview")
      st.write("Statistic data")
      st.dataframe(stats_df)
      
      # Sidebar filter 
      category=st.sidebar.selectbox("Select your category", ["season_id"])

      # Get Values from chosen category from SQL
      query_distinct = f"SELECT DISTINCT {category} FROM stats;"
      distinct_values_df = fetch_table(query_distinct)
      distinct_values = distinct_values_df[category].tolist()

      sub_filter = st.sidebar.selectbox(f"Select {category}", distinct_values)

    # Filtered query
      query_filtered = f"""
        SELECT * 
        FROM stats
        WHERE {category} = '{sub_filter}';
      """
      filtered_df = fetch_table(query_filtered)

      st.write(f"Statistics filtered by '{category}': '{sub_filter}'")
      st.dataframe(filtered_df)

elif option=="Seasons and Schedule":
      st.title("Seasons Overview")
      st.write("Seasons & Schedules Information")
      st.dataframe(season_sch_df)

      #Sidebar Filter
      category=st.sidebar.selectbox("Select your Category",["year","status"])

      #Get values for chosen category
      query_distinct = f"SELECT DISTINCT {category} FROM seasons;"
      distinct_values_df = fetch_table(query_distinct)
      distinct_values = distinct_values_df[category].tolist()

      sub_filter = st.sidebar.selectbox(f"Select {category}", distinct_values)

    # Filtered query
      query_filtered = f"""
        SELECT * 
        FROM seasons
        WHERE {category} = '{sub_filter}';
      """
      filtered_df = fetch_table(query_filtered)

      st.write(f"Seasons filtered by '{category}': '{sub_filter}'")
      st.dataframe(filtered_df)

elif option=="Rankings":
      st.title("Ranking Overview")
      st.write("Ranking Information")
      st.dataframe(rankings_df)
      
      #Sidebar Filters
      category=st.sidebar.selectbox("select your category",["season", "week","rank"])

      if category=="rank":
            rank_groups={
                        "0-5":(0,5),
                        "6-10":(6,10),
                        "11-15":(11,15),
                        "16-20":(16,20),
                        "21-25":(21,25),
                        "26-30":(26,30)
                  }
            selected_group = st.sidebar.selectbox("Select rank group", list(rank_groups.keys()))
            low, high = rank_groups[selected_group]

        # SQL query for rank range
            query_filtered = f"""
            SELECT * 
            FROM rankings
            WHERE `rank` BETWEEN {low} AND {high};"""
            filtered_df = fetch_table(query_filtered)
            st.write(f"Rankings filtered by rank group: '{selected_group}'")
            st.dataframe(filtered_df)

        # Chart and output
            st.bar_chart(filtered_df, x="rank", y="points", x_label="Team")        

      else:
        # Get values for season or week
            query_distinct = f"SELECT DISTINCT {category} FROM rankings;"
            distinct_values_df = fetch_table(query_distinct)
            distinct_values = distinct_values_df[category].tolist()

            sub_filter = st.sidebar.selectbox(f"Select {category}", distinct_values)

        # SQL query for exact match
            query_filtered = f"""
            SELECT * 
            FROM rankings
            WHERE {category} = '{sub_filter}';
        """
            filtered_df = fetch_table(query_filtered)

            st.write(f"Rankings filtered by '{category}': '{sub_filter}'")

            st.dataframe(filtered_df)

      
elif option=="Venue":
      st.title("Venue Overview")
      st.write("Venue Information")
      st.dataframe(venue_df)
      #Sidebar filter
      category=st.sidebar.selectbox("select your category",["state", "roof_type"])

      #Get values for chosen category
      query_distinct = f"SELECT DISTINCT {category} FROM venue;"
      distinct_values_df = fetch_table(query_distinct)
      distinct_values = distinct_values_df[category].tolist()

      sub_filter = st.sidebar.selectbox(f"Select {category}", distinct_values)

    # Filtered query
      query_filtered = f"""
        SELECT * 
        FROM venue
        WHERE {category} = '{sub_filter}';
      """
      filtered_df = fetch_table(query_filtered)

      st.write(f"Venue filtered by '{category}': '{sub_filter}'")
      st.dataframe(filtered_df)

elif option=="Coaches":
      st.title("coaches Overview")
      st.header("coaches Information")
      st.dataframe(coaches_df)
    
elif option=="Analysis":
      st.title("Data Analysis")
      #Define questions
      quest1="Which teams have maintained Top 5 rankings across multiple seasons"
      quest2="What are the average ranking points per team by season"
      quest3="How many first-place votes did each team receive across weeks"
      quest4="Which players have appeared in multiple seasons for the same team"
      quest5="What are the most common player positions and their distribution across teams"
      quest6="Which venues hosted the most games across all seasons"
      quest7="How does ranking improvement correlate with game performance (points scored)"
      quest8="What is the first and last season year played in this Data"
      quest = st.radio(
            "Choose Analysis question",
            [
            quest1,
            quest2,
            quest3,
            quest4,
            quest5,
            quest6,
            quest7,
            quest8
            ],
            index=None,
            )
      #Logic
      if quest==quest1:
            st.subheader("teams maintained Top 5 rankings across multiple seasons:")
            filtered_df = rankings_df[
            (rankings_df["rank"] >= 0) & (rankings_df["rank"] <= 5)
            ]
            st.dataframe(filtered_df)
      elif quest==quest2:
            st.subheader("Average ranking points per team by season")
            filtered_df=rankings_df[["name","market","points"]].sort_values(by="points",ascending=True)
            st.dataframe(filtered_df)
      elif quest==quest3:
            st.write(f"first-place votes receive by Each Team in ascending order")
            filtered_df=rankings_df[["name","market","fp_votes"]].sort_values(by="fp_votes",ascending=True)
            st.dataframe(filtered_df)
      elif quest==quest4:
            #SQL query
            #query=("select p.first_name, p.last_name,t.team_id, from players p join teams t on p.team_id= t.team_id;")
            #load Dataframe
            df1=fetch_table("select p.first_name, p.last_name, t.team_id " \
            "from players p " \
            "left join teams t on p.team_id= t.team_id;"
            )
            #Diplay df
            #st.dataframe(df1)
      elif quest==quest6:
            df2=pd.DataFrame(venue_df)
            #count venues per city
            city_counts=df2["city"].value_counts()
            #find city with most games
            top_city=city_counts.idxmax()
            top_count=city_counts.max()
            #Display in streamlit
            st.header("City with Most Hosted Games")
            st.write(f"🏟️ **{top_city}** hosted the most games with **{top_count} venues**.")
            st.bar_chart(city_counts)
      elif quest==quest7:
            df3=pd.DataFrame(rankings_df)
            #max rankiing and Points
            players_rank=df3["rank"].min()
            players_points=df3["points"].max()
            #Display in Streamlit
            st.subheader("Maximum points scored in all the games will have the highest Rank")
            st.write(f"Max points scored by any players is {players_points}. Hence the player has the Highest rank i.e {players_rank}")
      elif quest==quest8:
            df4=pd.DataFrame(season_sch_df)
            #First and Last season played
            first_year=df4["year"].min()
            last_year=df4["year"].max()
            #Display in Streamlit
            st.write(f"First season played in year {first_year}. Last season played in year {last_year}")


