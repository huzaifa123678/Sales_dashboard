import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.set_page_config(page_title="Sales Dashboard",layout="wide")
@st.cache_data
def load_data():
  df=pd.read_csv("cleaned_sales_data.csv")
  df["ORDERDATE"]=pd.to_datetime(df["ORDERDATE"])
  return df
df = load_data()

st.sidebar.header("Filters")
year=st.sidebar.multiselect("select year",df['YEAR_ID'].unique(),default=df['YEAR_ID'].unique(), max_selections=3)
product=st.sidebar.multiselect("select product",df['PRODUCTLINE'].unique(),default=df['PRODUCTLINE'].unique(), max_selections=7)
df_filtered = df[(df['YEAR_ID'].isin(year)) & (df['PRODUCTLINE'].isin(product))]

st.title("SALES DASHBOARD")
col1,col2,col3,col4=st.columns(4)
col1.metric("Total sale",f"{df_filtered['SALES'].sum():,.0f}")
col2.metric("Avg sale",f"{df_filtered['SALES'].mean():,.0f}")
col3.metric("Customers",df_filtered['CUSTOMERNAME'].nunique())
col4.metric("Top product line",df_filtered.groupby('PRODUCTLINE')['SALES'].sum().idxmax())

st.subheader("Monthly sales trend")
monthly_sales = df_filtered.groupby('month_year')['SALES'].sum()
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot( monthly_sales.values, marker='o')
ax.set_xlabel('Month-Year')
ax.set_ylabel('Total Sales')
ax.set_title('Monthly Sales Trend')
ax.grid(True)
st.pyplot(fig)

st.subheader("Order Status Distribution")
fig, ax = plt.subplots(figsize=(5,5))
df_filtered['STATUS'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
ax.set_ylabel("")
st.pyplot(fig)

st.subheader("Top 10 Countries by Sales")
country_sales = df_filtered.groupby('COUNTRY')['SALES'].sum().nlargest(10)
fig, ax = plt.subplots(figsize=(8,4))
country_sales.plot(kind='barh', ax=ax, color="skyblue")
st.pyplot(fig)

with st.expander("See Dataset"):
  st.dataframe(df_filtered)

