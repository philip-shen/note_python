#Streamlit pckgs
import streamlit as st
# EDA pckgs
import pandas as pd
import numpy as np
#VIZ pckgs
import plotly.express as px
import plotly.graph_objs as go
col1,col2,col3= st.columns([2,2,2])
data= st.file_uploader("Upload Dataset",type=["csv","xlsx","xls"])

if data is not None:
    #check the type of the file
    if data.type=="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df=pd.read_excel(data)
    elif data.type=="application/vnd.ms-excel":
        df=pd.read_csv(data)
        all_columns_names= df.columns.tolist()
        col= st.selectbox("Choose Column",df.columns.tolist())
        selected_column_names__pyplot= st.multiselect("Select Columns",all_columns_names)
        plot_btn= st.button("Generate Plot")
        #count plot
        with col1:
            #pie chart
            if st.checkbox("Pie Plot"):
                if plot_btn:
                    data_pie= df[col].value_counts().to_frame()
                    labels=data_pie.index.tolist()
                    datavals=data_pie[col].tolist()
                    trace=go.Pie(labels=labels,
                                    values=datavals,
                                    hovertemplate= "%{label}: <br>Value: %{value} ",
                                    showlegend=True,
                                    textposition='inside',
                                    )
                    layout= go.Layout(
                        title= 'Percentage of {}'.format(col),
                        height=600,
                        margin=go.Margin(l=0, r=200, b=100, t=100, pad=4)   # Margins -Left, Right, Top Bottom, Padding
                        )
                    data= [trace]
                    fig= go.Figure(data=data,layout= layout)
                    st.plotly_chart(fig)
        with col2:
                if st.checkbox("Count_plot"):
                # all_columns_names= df.columns.tolist()
                # s=df[all_columns_names[0]].str.strip().value_counts()
                    if plot_btn:
                        s=df[col].str.strip().value_counts()
                        trace= go.Bar(
                                x=s.index,
                                y=s.values,
                                showlegend= True
                                )
                        layout= go.Layout(
                            title= 'Count of {}'.format(col),
                        )
                        data= [trace]
                        fig= go.Figure(data=data,layout= layout)
                        st.plotly_chart(fig)