import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Salary Dashboard",
                   page_icon=':bar_chart:',
                   layout='wide')

df = pd.read_csv('Salary_Data.csv').dropna()
df['Education_Level'] = df['Education_Level'].replace([r"Bachelor's"],r"Bachelor's Degree")
df['Education_Level'] = df['Education_Level'].replace([r"Master's"],r"Master's Degree")
df['Education_Level'] = df['Education_Level'].replace([r"phD"],r"PhD")
# SIDEBAR
st.sidebar.header("Filter Here")
gender = st.sidebar.multiselect("Select the Gender",options=df['Gender'].unique(),default=df['Gender'].unique())
education = st.sidebar.multiselect("Select the Education",options=df['Education_Level'].unique(),default=df['Education_Level'].unique())
job = st.sidebar.multiselect("Select the Job Title",options=df['Job_Title'].unique(),default=df['Job_Title'].unique())

df_selection = df.query(
    "Gender == @gender & Education_Level == @education & Job_Title == @job"
)

#st.dataframe(df_selection)

# MAINPAGE
st.title(":bar_chart: Salary Dashboard")
st.markdown("##")

col1,col2 = st.columns(2)
genders_count = df_selection['Gender'].value_counts()
fig_genders = px.pie(genders_count,values=genders_count,names=df_selection['Gender'].unique(),title='Gender Counts')

#KPI
average_salary = int(df_selection["Salary"].mean())
total_salary = df_selection["Salary"].sum()
with col1:
    st.subheader("Average Salary")
    st.subheader(f'US $ {average_salary:,}')
with col2:
    st.plotly_chart(fig_genders,use_container_width=True)
st.markdown("---")

#BARCHART

#salary by education level

salary_by_education =df_selection.groupby(by=["Education_Level"])['Salary'].mean()

fig_salary_education = px.bar(
    salary_by_education,
    x = "Salary",
    y = salary_by_education.index,
    orientation="h",
    color_discrete_sequence=["#0083B8"]*len(salary_by_education),
    template="plotly_white",
    title="Salary by Education"

)


#salary by gender
salary_by_gender = df_selection.groupby(by=["Gender"])["Salary"].mean()
fig_salary_gender = px.bar(salary_by_gender,
                           x = "Salary",
                           y=salary_by_gender.index,
                           orientation="h",
                           color_discrete_sequence=["#0083B8"]*len(salary_by_gender),
                           template="plotly_white",
                           title="Salary by Gender",
                           )

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_salary_education,use_container_width=True)
right_column.plotly_chart(fig_salary_gender,use_container_width=True)

#Regression
st.markdown("---")
fig = px.scatter(df_selection,
                 x="Age",y="Salary",
                 color='Education_Level',
                 opacity=0,
                 trendline="ols",
                 title="Salary Regression by Age")
st.plotly_chart(fig,use_container_width=True)

