import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# 1. Configuration and Data Loading
st.set_page_config(layout="wide", page_title="Spanish wikipedia sport articles data analyisis")

#Read dataframe Data

data_url1 = 'figure1_finaldata.csv'
df1 = pd.read_csv(data_url1,index_col=False)
data_url2='figure2_finaldata.csv'
df2=pd.read_csv(data_url2,index_col=False)
df2['month'] = pd.to_datetime(df2['month'], format="%Y-%m-%d").dt.date
data_url3='figure3_finaldata.csv'
df3=pd.read_csv(data_url3,index_col=False)
img1= Image.open('df1.png')
img3= Image.open('df3.png')


# 2. Sidebar Menu Setup
st.sidebar.title("Select Analysis")
analysis_options = {
    "1":"Main Page",
    "2": "Percentage of Sports Articles by Country",
    "3": "Views of Sports vs. Not sports spanish wikipedia articles between 2023-2024 months",
    "4":  "Number of Sports articles related to humans"
}

option_key = st.sidebar.radio(
    "Choose an exploratory view:",
    list(analysis_options.keys()),
    format_func=lambda x: analysis_options[x]
)

st.title(f"Spanish wikipedia articles: {analysis_options[option_key]}")


# 3. Main Page Logic based on Selection
if option_key=="1":
    st.write('## Research questions:')
    st.write('How many Spanish articles from es.wikipedia are related to Sports?')

    st.write('## Hypothesis:')
    st.write('**We hypothesize that spanish articles for spanish speaking countries will have more sports related articles than other countries.')

    st.write('## Data')
    st.write('We worked with spanish articles in the es.wikpedia from the months of 2023-2024 using their means and sums to generate our figures.' \
    '')

    st.write('## Steps taken:')
    st.write("""
    1. **We first seperated rows bewtween  dataframes containing humans and non humans articles. This was determined through , the instance of:, attribute.**
    2. **Then we created a column that would contain teh text we would classify by, either a description or title for those missing a description.**
    3. **Then we cleaned up the teh data in these columns by removing special characters, stopwords, and spaces of the items you are looking at.**
    4. **Finally we did naive bayes classification on both dataframes to classify them as sports and not sports**
    [The latter was attempted after failing to categorize articles with zero-shot classification]""")
    st.write('## Key Takeaways')
    st.write("""Categorizing data with small text samples in dfferent languages can prove difficult due to the high variation of vocabulary
    and also grammar that varies across languages. In addition the categorical information provided by online articles can be hard to access 
    and even possible lead to having inaccurate results""")
    st.write('## Gen AI')
    st.write('Generative AI was used to identify models for zero shot classifcation that would be multilingual when applied to a single comlumn containing both english and spanish'
            'additionally, gen AI was also utilize to check if figures where being generated correctly and to understand hwo to make them fit properly on the streamlit app. ')
if option_key == "2":
    # --- Analysis 1: Percentage of Sports Articles by Country (map Chart) ---

    st.header("1. Top article fraction of top 400 viewed article in 2024-2023 months per country in 2023-02")
    st.markdown("Examine the fraction of categories of spanish articles read across different countries with the most views.")
    st.write('Data was categorized using the descriptions components and each article and then performing naive bayes classification. ')

    fig1= px.choropleth(
    df1,
    locations='country',
    locationmode='country names',
    color= 'sports_percentage',
    color_continuous_scale='Blues',
    title='Percentage of Sports Articles by Country',
    labels={"sports_percentage": "% Sports Articles"},
    width=800,
    height=600)

    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("Snippet of data used to represent categories")
    
    st.dataframe(df1.head(10))
    st.image(img1, caption="Confussion matrix for categorizing dataframe for figure 1 and 2", use_column_width=True)

if option_key=='3':
    st.header("2. Views of Sports vs. Not sports spanish wikipedia articles between 2023-2024 months")
    st.markdown("Compare the views between spanish article in 2024-2023 months.")
    st.write('Data was categorized using the descriptions components and each article and then performing naive bayes classification.')

    months = st.slider('Select month range', min_value=df2['month'].min(), max_value=df2['month'].max(), value=(df2['month'].min(), df2['month'].max()))
    filtered = df2[(df2['month'] >= months[0]) & (df2['month'] <= months[1])]

    fig2= px.line(
    filtered,
    x='month',
    y='views',
    color='categories_generated',
    title='Monthly Views: Sports vs Not Sports',
    markers=True)

    fig2.update_layout(
    xaxis_title='Month',
    yaxis_title='Total Views',
    legend_title='Category'
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("Snippet of data used to represent categories")
    
    st.dataframe(df2.head(10))


if option_key=='4':
    st.header("3. Category counts of sports articles for humans")
    st.markdown("Comapre the spanish articles about humans related to sports in 2024-2023 months.")
    st.write('Data was categorized using the descriptions components and each article and then performing naive bayes classification ')
    
    fig3 = px.bar(
    df3,
    x='category',
    y='count',
    color='category',
    title='Number of Sports articles related to humans',
    text='count')

    st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("Snippet of data used to represent categories")
    
    st.dataframe(df3.head(10))
    st.image(img3, caption="Confussion matrix for categorizing dataframe for figure 3", use_column_width=True)
    