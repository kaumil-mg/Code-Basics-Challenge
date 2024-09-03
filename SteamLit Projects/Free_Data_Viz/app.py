import streamlit as st
import json
from streamlit_lottie import st_lottie
import requests

st.set_page_config(page_title='Kaumil Mistry - Data Scientist', page_icon=':smile:', layout='wide')



col1, col2, col3 = st.columns((3))

# Set the title and header
with col1:
    st.header("Resume")

# load animation 
def load_lottie(url: str):
    r= requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()



# Contact Information
with col1:
    st.subheader("Contact Information")
    st.write("""
    **Email:** kaumil09@gmail.com  
    **Phone:** 6354162751  
    **Portfolio:** [Kaumilmg Portfolio](https://kaumil-mg.github.io/Portfolio-web)  
    **LinkedIn:** [Kaumil Mistry](https://www.linkedin.com/in/kaumilmg/)  
    **GitHub:** [Kaumil Mistry](https://github.com/kaumil-mg)
    """)
with col3:
    lottie_hello = load_lottie('https://lottie.host/03f63272-ebfd-421f-a05d-d5a115ea834d/MNRX76Zr4S.json')
    st_lottie(
        lottie_hello,
        key='Hello Buddy',
        quality='high',
        height=300,
        width=300,
        speed=1,
        loop=2
    )

# Profile
st.subheader("Profile")
st.write("""
Data Scientist with Let's Enkindle and over 4 years of experience in extracting, analyzing, predicting, and visualizing data to drive business decisions. Proficient in Power BI, SQL, Python, and Tableau, with a proven track record of building data pipelines, performing statistical analysis, and creating interactive dashboards. Adept at working with large datasets, identifying trends, and delivering actionable insights.
""")

# Professional Experience
st.subheader("Professional Experience")

st.write("**Let's Enkindle - Data Scientist**")
st.write("""
- Analyzing and visualizing data using Power BI and Python (matplotlib, plotly, seaborn).
- Implementing machine learning models like LSTM, XGBoost, and others to train chemical trend datasets.
- Learning and applying deep learning models in practical scenarios.
""")

st.write("**Value Score Business Solution LLP - ERP Technical Consultant and Analyst**")
st.write("""
- Proficient in designing and optimizing SQL databases and creating data pipelines for integrating various sources.
- Excel in Tableau for interactive dashboard creation and possess strong data analysis skills supporting decision-making.
- Hands-on experience in SQL database design, Epicor ERP system configuration, and data visualization with Tableau.
""")

st.write("**Parentheses System PVT. LTD. - Intern Data Analyst**")
st.write("""
- Skilled in using Python (Pandas, NumPy) for data analysis, and creating impactful data visualizations using Matplotlib and Seaborn.
- Develop ETL pipelines and collaborate with cross-functional teams to deliver data-driven insights.
- Present complex analytical findings to business teams and bridge the gap between technical and non-technical stakeholders.
""")

st.write("**Dotmg Studio - Web Developer and Digital Marketer**")
st.write("""
- Increased website traffic by 25% through data-driven SEO initiatives.
- Developed visually appealing websites using frontend technologies like HTML, CSS, JS, and Django.
- Created robust web applications using backend technologies such as PHP, SQL, DBMS, and PostgreSQL.
""")

# Education
st.subheader("Education")

st.write("**M.Sc. Data Science** - Symbiosis Skills and Professional University (2021 - 2023) Pune")
st.write("**B.Sc. IT** - Indus University (2018 - 2021) Ahmedabad")

# Skills
st.subheader("Skills")
st.write("""
- **Data Analyst:** Power BI, Tableau, AWS Glue, ETL, Python (Matplotlib, Seaborn, Plotly)
- **Data Mining:** SQL, NoSQL, MongoDB, Cloud extraction, PostgreSQL
- **Cloud Computing:** AWS, GCP, Azure
- **Web Development:** HTML, CSS, Django, Bootstrap, SQL, DBMS, JavaScript, PHP
- **Documentation:** Excel, Word, PowerPoint
- **DevOps:** Git, GitHub, Docker, Unix
""")

# Certifications
st.subheader("Certifications")
st.write("""
- **Data Science Master** - Physics Wallah
- **Build a Data Science Web App with Streamlit and Python** - Coursera
- **Data Analytics Part 2: Extending and Applying Core Knowledge**
""")

# Projects
st.subheader("Projects")

st.write("**[Data Visualization - Power BI](https://linktr.ee/Kaumilmg)**")
st.write("""
- Conducted in-depth analysis across different fields using Power BI for data visualization.
- Strong grasp of live data, SQL, Python, and various dataset formats such as JSON, CSV, Excel, and SQL.
- Utilized Python packages like pandas, numpy, matplotlib, seaborn, and plotly for visualization.
""")

st.write("**[Flipkart Product Review Using Python - AWS (Code pipeline, Beanstalk), MongoDB](https://github.com/kaumil-mg/web-scrap)**")
st.write("""
- Web scraped product reviews using BeautifulSoup and Selenium, stored data in MongoDB, and automated deployment with AWS services.
""")

st.write("**[E-commerce Website - HTML & CSS, PHP, JS](https://www.youtube.com/watch?v=6TDlgTe8gEQ)**")
st.write("""
- Built a dynamic e-commerce website with essential features such as product catalog, shopping cart, secure checkout, and showcased skills in database management and user authentication.
""")

# Footer
st.write("For more details, visit my [LinkedIn](https://www.linkedin.com/in/kaumilmg/) or [GitHub](https://github.com/kaumil-mg).")