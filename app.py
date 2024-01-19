import pandas as pd
import json
import streamlit as st
import mysql.connector
from PIL import Image
import plotly.express as px

#Configuring streamlit header
im = Image.open("phonepe-logo.png")
st.set_page_config(page_title="PhonePe Pulse Data Visualization", page_icon=im, layout='wide')

# header section
st.title(":violet[PhonePe Pulse Data Visualization:]")
row_input = st.columns((2,1,2,1))

# adding a selectbox for transactions and user
with row_input[0]:
    selected_option = st.selectbox('select...',('Transactional', 'User'),placeholder='Select',label_visibility='hidden')

# if trasanctional is selected:
if selected_option == 'Transactional':
    col1, col2 = st.columns(2)
    with col1:
        row_input = st.columns((1,0.5,0.5,0.5))
        with row_input[0]:
            selected_year = st.selectbox(
                        'Year:',('2018', '2019','2020', '2021', '2022'),index=4,placeholder='Select')
        with row_input[1]:
            selected_quater = st.selectbox(
                        label='Quater:',index=3, options=('Q1', 'Q2','Q3', 'Q4'))

        #loading the geojson
        indian_states = json.load(open("states_india.geojson",'r'))
        
        #mysql connection
        myslq_engine = mysql.connector.connect(user='root', 
                                            password='admin', 
                                            host='localhost', 
                                            port='3306', 
                                            database = 'phonepe')

        crsr = myslq_engine.cursor()
                
        # SQL query to be executed in the database
        sql_command = f"""SELECT * from aggregate_transaction
                        where year = {selected_year} and quater = {selected_quater[1]};
        """

        # execute the statement
        crsr.execute(sql_command)
        queryResult = crsr.fetchall()

        # adding result to the dataframe
        i = [i for i in range(1, len(queryResult)+1)]
        df = pd.DataFrame(queryResult, columns=['S.No',
                                                'State', 
                                                'Year', 
                                                'Quater', 
                                                'Transaction_type', 
                                                'Transaction_count', 
                                                'Transaction_amount', 
                                                'ID',
                                                'Transaction_amountScale' 
                                                ], index=i)
        myslq_engine.close()

        #deleting first column
        df = df.iloc[: , 1:]
        df = df.rename_axis('S.No')
        
        fig = px.choropleth_mapbox(
                            df, 
                            locations = 'ID', 
                            geojson=indian_states, 
                            color='Transaction_amountScale',
                            hover_name = 'State',
                            featureidkey='properties.state_code',
                            hover_data=['Transaction_amount'],
                            mapbox_style='carto-positron',
                            center={'lat':24, 'lon':78},    
                            zoom = 3.2,
                            color_continuous_scale="Viridis",
                            
                            )
        fig.layout.coloraxis.colorbar.title = 'Transaction Amount (in log10)'
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        #Function to get total number transactions
        def total_trans():
            myslq_engine = mysql.connector.connect(user='root', 
                                                password='admin', 
                                                host='localhost', 
                                                port='3306', 
                                                database = 'phonepe')

            crsr = myslq_engine.cursor()
                    
            # SQL query to be executed in the database
            sql_command = """SELECT sum(Transaction_count) FROM aggregate_transaction;
            """

            # execute the statement
            crsr.execute(sql_command)
            queryResult = crsr.fetchall()

            # adding result to the dataframe
            i = [i for i in range(1, len(queryResult)+1)]
            df = pd.DataFrame(queryResult, columns=['Transaction_count'
                                                    ], index=i)
            myslq_engine.close()

            #deleting first column
            df = df.rename_axis('S.No')
            return ('{:,}'.format(df['Transaction_count'].iloc[0]))
        
        #function to get total payment
        def total_payment():
            myslq_engine = mysql.connector.connect(user='root', 
                                                password='admin', 
                                                host='localhost', 
                                                port='3306', 
                                                database = 'phonepe')

            crsr = myslq_engine.cursor()
                    
            # SQL query to be executed in the database
            sql_command = """SELECT sum(Transaction_amount) FROM aggregate_transaction;
            """

            # execute the statement
            crsr.execute(sql_command)
            queryResult = crsr.fetchall()

            # adding result to the dataframe
            i = [i for i in range(1, len(queryResult)+1)]
            df = pd.DataFrame(queryResult, columns=['Transaction_amount'
                                                    ], index=i)
            myslq_engine.close()

            #deleting first column
            df = df.rename_axis('S.No')
            return ('{:,}'.format(df['Transaction_amount'].iloc[0]))
        
        #function to get the avg transaction value
        def avg_transaction():
            myslq_engine = mysql.connector.connect(user='root', 
                                                password='admin', 
                                                host='localhost', 
                                                port='3306', 
                                                database = 'phonepe')

            crsr = myslq_engine.cursor()
                    
            # SQL query to be executed in the database
            sql_command = """SELECT avg(Transaction_amount) FROM aggregate_transaction;
            """

            # execute the statement
            crsr.execute(sql_command)
            queryResult = crsr.fetchall()

            # adding result to the dataframe
            i = [i for i in range(1, len(queryResult)+1)]
            df = pd.DataFrame(queryResult, columns=['Transaction_amount'
                                                    ], index=i)
            myslq_engine.close()

            #deleting first column
            df = df.rename_axis('S.No')
            return ('{:,}'.format(df['Transaction_amount'].iloc[0]))
        
        #to get the total transaction per category
        def total_trans_category(x):
            myslq_engine = mysql.connector.connect(user='root', 
                                                password='admin', 
                                                host='localhost', 
                                                port='3306', 
                                                database = 'phonepe')

            crsr = myslq_engine.cursor()       

            if x == 'Merchant payments':
                # SQL query to be executed in the database
                sql_command = f"""SELECT sum(Transaction_count) 
                                FROM aggregate_transaction 
                                where Transaction_type = 'Merchant payments';
                                """
            elif x == 'Peer-to-peer payments':
                # SQL query to be executed in the database
                sql_command = f"""SELECT sum(Transaction_count) 
                                FROM aggregate_transaction 
                                where Transaction_type = 'Peer-to-peer payments';
                                """
            elif x == 'Recharge & bill payments':
                # SQL query to be executed in the database
                sql_command = f"""SELECT sum(Transaction_count) 
                                FROM aggregate_transaction 
                                where Transaction_type = 'Recharge & bill payments';
                                """
            elif x == 'Financial Services':
                # SQL query to be executed in the database
                sql_command = f"""SELECT sum(Transaction_count) 
                                FROM aggregate_transaction 
                                where Transaction_type = 'Financial Services';
                                """
            else:
                # SQL query to be executed in the database
                sql_command = f"""SELECT sum(Transaction_count) 
                                FROM aggregate_transaction 
                                where Transaction_type = 'Others';
                                """

            # execute the statement
            crsr.execute(sql_command)
            queryResult = crsr.fetchall()

            # adding result to the dataframe
            i = [i for i in range(1, len(queryResult)+1)]
            df = pd.DataFrame(queryResult, columns=['Transaction_count'
                                                    ], index=i)
            myslq_engine.close()

            #deleting first column
            df = df.rename_axis('S.No')
            return ('{:,}'.format(df['Transaction_count'].iloc[0]))

        #to get the top ten states in transactions
        def top_ten_states():
            myslq_engine = mysql.connector.connect(user='root', 
                                                password='admin', 
                                                host='localhost', 
                                                port='3306', 
                                                database = 'phonepe')

            crsr = myslq_engine.cursor()       

            # SQL query to be executed in the database
            sql_command = """SELECT State, sum(Transaction_count) as "Transaction Count"
                            FROM aggregate_transaction
                            group by State
                            order by sum(Transaction_count) desc
                            limit 10;
                            """
            
            # execute the statement
            crsr.execute(sql_command)
            queryResult = crsr.fetchall()

            # adding result to the dataframe
            i = [i for i in range(1, len(queryResult)+1)]
            df = pd.DataFrame(queryResult, columns=['State', 'Transaction Count'
                                                    ], index=i)
            myslq_engine.close()

            #deleting first column
            df = df.rename_axis('S.No')
            return df
        
        #to get the top ten districts in transactions
        def top_ten_districts():
            myslq_engine = mysql.connector.connect(user='root', 
                                                password='admin', 
                                                host='localhost', 
                                                port='3306', 
                                                database = 'phonepe')

            crsr = myslq_engine.cursor()       

            # SQL query to be executed in the database
            sql_command = """SELECT District, sum(Transaction_count) as "Transaction Count"
                            FROM map_transaction
                            group by District
                            order by sum(Transaction_count) desc
                            limit 10;
                            """
            
            # execute the statement
            crsr.execute(sql_command)
            queryResult = crsr.fetchall()

            # adding result to the dataframe
            i = [i for i in range(1, len(queryResult)+1)]
            df = pd.DataFrame(queryResult, columns=['District', 'Transaction Count'
                                                    ], index=i)
            myslq_engine.close()

            #deleting first column
            df = df.rename_axis('S.No')
            df['District'] = df['District'].str.title()
            return df

        #to get the top ten districts in pincodes
        def top_ten_pincodes():
            myslq_engine = mysql.connector.connect(user='root', 
                                                password='admin', 
                                                host='localhost', 
                                                port='3306', 
                                                database = 'phonepe')

            crsr = myslq_engine.cursor()       

            # SQL query to be executed in the database
            sql_command = """SELECT Pincode, sum(Transaction_count) as "Transaction Count"
                            FROM top_transaction
                            group by Pincode
                            order by sum(Transaction_count) desc
                            limit 10;
                            """
            
            # execute the statement
            crsr.execute(sql_command)
            queryResult = crsr.fetchall()

            # adding result to the dataframe
            i = [i for i in range(1, len(queryResult)+1)]
            df = pd.DataFrame(queryResult, columns=['Pincode', 'Transaction Count'
                                                    ], index=i)
            myslq_engine.close()

            #deleting first column
            df = df.rename_axis('S.No')
            return df

        st.markdown("""
        <style>
        .smaller-font {
            font-size:15px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <style>
        .small-font {
            font-size:20px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <style>
        .bigger-font {
            font-size:40px;
            color: rgb(96, 180, 255);
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <style>
        .big-font {
            font-size:25px;
            color: rgb(96, 180, 255);
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        st.title(":blue[Transactions:]")
        st.markdown('<p class="small-font">All PhonePe transactions (UPI + Cards + Wallets)</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="bigger-font">{total_trans()}</p>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="small-font">Total Payment Value</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="big-font">₹{total_payment()}</p>', unsafe_allow_html=True)
        with col2:
            st.markdown('<p class="small-font">Avg. Transaction value in all payment categories</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="big-font">₹{avg_transaction()}</p>', unsafe_allow_html=True)
        st.subheader('',divider='rainbow',)
        
        
        st.subheader('Categories')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="small-font">Merchant payments:</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p class="big-font">{total_trans_category("Merchant payments")}</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="small-font">Peer-to-peer payments</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p class="big-font">{total_trans_category("Peer-to-peer payments")}</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="small-font">Recharge & bill payments</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p class="big-font">{total_trans_category("Recharge & bill payments")}</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="small-font">Financial Services</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p class="big-font">{total_trans_category("Financial Services")}</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p class="small-font">Others</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p class="big-font">{total_trans_category("Others")}</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        selected_option_SDP = st.selectbox(
        "Select Region: ",
        ("State", "District", "Pincode"),
        index=0,
        placeholder="Select...")

        if selected_option_SDP == 'State':
            st.markdown('<p class="small-font">Top 10 states:</p>', unsafe_allow_html=True)
            st.dataframe(top_ten_states(), width=1000)
        elif selected_option_SDP == 'District':
            st.markdown('<p class="small-font">Top 10 Disctricts :</p>', unsafe_allow_html=True)
            st.dataframe(top_ten_districts(), width=1000)        
        elif selected_option_SDP == 'Pincode':
            st.markdown('<p class="small-font">Top 10 Pincodes :</p>', unsafe_allow_html=True)
            st.dataframe(top_ten_pincodes(), width=1000)

# if user is selected:
elif selected_option == 'User':
    col1, col2 = st.columns(2)
    with col1:
        row_input = st.columns((1,0.5,0.5,0.5))
        with row_input[0]:
            
            selected_userYear = st.selectbox(
                        'Year:',(2018, 2019,2020, 2021, 2022), index=0,placeholder='Select')
            
        with row_input[1]:
            if selected_userYear == 2022:
                selected_userQuater = st.selectbox(
                        label='Quater:', options=('Q1',))
            else:
                selected_userQuater = st.selectbox(
                        label='Quater:',index=3, options=('Q1', 'Q2', 'Q3', 'Q4'),placeholder='Select')

        #loading the geojson
        indian_states = json.load(open("states_india.geojson",'r'))

        # connecting mysql
        myslq_engine = mysql.connector.connect(user='root', 
                                            password='admin', 
                                            host='localhost', 
                                            port='3306', 
                                            database = 'phonepe')

        crsr = myslq_engine.cursor()
                
        # SQL query to be executed in the database
        sql_command = f"""SELECT * from aggregate_user
                        where year = 2022 and quater = 1;
        """

        # execute the statement
        crsr.execute(sql_command)
        queryResult = crsr.fetchall()

        # adding result to the dataframe
        i = [i for i in range(1, len(queryResult)+1)]
        df = pd.DataFrame(queryResult, columns=['S.No',
                                                'State', 
                                                'Year', 
                                                'Quater', 
                                                'Brands', 
                                                'User_Count', 
                                                'Percentage', 
                                                'ID',
                                                'PercentageScale'
                                                ], index=i)
        myslq_engine.close()

        #deleting first column
        df = df.iloc[: , 1:]
        df = df.rename_axis('S.No')
        
        fig = px.choropleth_mapbox(
                            df, 
                            locations = 'ID', 
                            geojson=indian_states, 
                            color='PercentageScale',
                            hover_name = 'State',
                            featureidkey='properties.state_code',
                            hover_data=['User_Count'],
                            mapbox_style='carto-positron',
                            center={'lat':24, 'lon':78},    
                            zoom = 3.2,
                            color_continuous_scale="Viridis"
                            )
        fig.layout.coloraxis.colorbar.title = 'User Percentage (in log10)'
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        #Function to get total number users
        def total_users():
            myslq_engine = mysql.connector.connect(user='root', 
                                                password='admin', 
                                                host='localhost', 
                                                port='3306', 
                                                database = 'phonepe')

            crsr = myslq_engine.cursor()
                    
            # SQL query to be executed in the database
            sql_command = """SELECT sum(User_count) FROM aggregate_user;
            """

            # execute the statement
            crsr.execute(sql_command)
            queryResult = crsr.fetchall()

            # adding result to the dataframe
            i = [i for i in range(1, len(queryResult)+1)]
            df = pd.DataFrame(queryResult, columns=['User_count'
                                                    ], index=i)
            myslq_engine.close()

            #deleting first column
            df = df.rename_axis('S.No')
            return ('{:,}'.format(df['User_count'].iloc[0]))
        
        #to get the top ten states in transactions
        def top_ten_states():
            myslq_engine = mysql.connector.connect(user='root', 
                                                password='admin', 
                                                host='localhost', 
                                                port='3306', 
                                                database = 'phonepe')

            crsr = myslq_engine.cursor()       

            # SQL query to be executed in the database
            sql_command = """SELECT State, sum(User_count) as "user Count"
                            FROM aggregate_user
                            group by State
                            order by sum(User_count) desc
                            limit 10;
                            """
            
            # execute the statement
            crsr.execute(sql_command)
            queryResult = crsr.fetchall()

            # adding result to the dataframe
            i = [i for i in range(1, len(queryResult)+1)]
            df = pd.DataFrame(queryResult, columns=['State', 'User Count'
                                                    ], index=i)
            myslq_engine.close()

            #deleting first column
            df = df.rename_axis('S.No')
            return df

        #to get the top ten districts in transactions
        def top_ten_districts():
            myslq_engine = mysql.connector.connect(user='root', 
                                                password='admin', 
                                                host='localhost', 
                                                port='3306', 
                                                database = 'phonepe')

            crsr = myslq_engine.cursor()       

            # SQL query to be executed in the database
            sql_command = """SELECT District, sum(Registered_Users) as "User Count"
                            FROM map_user
                            group by District
                            order by sum(Registered_Users) desc
                            limit 10;
                            """
            
            # execute the statement
            crsr.execute(sql_command)
            queryResult = crsr.fetchall()

            # adding result to the dataframe
            i = [i for i in range(1, len(queryResult)+1)]
            df = pd.DataFrame(queryResult, columns=['District', 'Registered Users'
                                                    ], index=i)
            myslq_engine.close()

            #deleting first column
            df = df.rename_axis('S.No')
            df['District'] = df['District'].str.title()
            return df

        #to get the top ten districts in pincodes
        def top_ten_pincodes():
            myslq_engine = mysql.connector.connect(user='root', 
                                                password='admin', 
                                                host='localhost', 
                                                port='3306', 
                                                database = 'phonepe')

            crsr = myslq_engine.cursor()       

            # SQL query to be executed in the database
            sql_command = """SELECT Pincode, sum(Registered_Users) as "User Count"
                            FROM top_user
                            group by Pincode
                            order by sum(Registered_Users) desc
                            limit 10;
                            """
            
            # execute the statement
            crsr.execute(sql_command)
            queryResult = crsr.fetchall()

            # adding result to the dataframe
            i = [i for i in range(1, len(queryResult)+1)]
            df = pd.DataFrame(queryResult, columns=['Pincode', 'Registered Users'
                                                    ], index=i)
            myslq_engine.close()

            #deleting first column
            df = df.rename_axis('S.No')
            return df

        st.markdown("""
        <style>
        .smaller-font {
            font-size:15px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <style>
        .small-font {
            font-size:20px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <style>
        .bigger-font {
            font-size:40px;
            color: rgb(178, 126, 255);
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <style>
        .big-font {
            font-size:25px;
            color: rgb(178, 126, 255);
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
        st.title(":violet[Users:]")
        st.markdown('<p class="small-font">Total Registered PhonePe Users till Q1 2022</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="bigger-font">{total_users()}</p>', unsafe_allow_html=True)


    col1, col2 = st.columns(2)
    with col1:
        selected_option_SDP = st.selectbox(
        "Select Region: ",
        ("State", "District", "Pincode"),
        index=0,
        placeholder="Select...")

        if selected_option_SDP == 'State':
            st.markdown('<p class="small-font">Top 10 states:</p>', unsafe_allow_html=True)
            st.dataframe(top_ten_states(), width=1000)
        elif selected_option_SDP == 'District':
            st.markdown('<p class="small-font">Top 10 Disctricts :</p>', unsafe_allow_html=True)
            st.dataframe(top_ten_districts(), width=1000)        
        elif selected_option_SDP == 'Pincode':
            st.markdown('<p class="small-font">Top 10 Pincodes :</p>', unsafe_allow_html=True)
            st.dataframe(top_ten_pincodes(), width=1000)