import streamlit as st
import os
from  streamlit_option_menu import option_menu
import json

def Review_People(connection, accessLevel):
    st.header("Review People")
    form_name = option_menu(
            None,
            ["Today Review", "Tomorrow Review","Not Attempted"],
            orientation="horizontal",
            icons=['a','a','a']
        )
    with st.container(border=1,height=800):
        st.markdown(
            """
            <style>
            .vertical-line {
                border-left: 1px solid #D3D3D3;
                height: 750px;
                margin-left: 10px;
                margin-right: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        n1c1,n1c2, n1c3 = st.columns([2,0.5,7])
        with n1c1:
            select = option_menu(
                None, 
                ["Pre Employment", "Pre Placement", "Annual / Periodical", "Camps", "Fitness After Medical Leave","Illness","Injury","Followup Visit","Special Work Fitness"],
                menu_icon='building-fill-add',
                icons=['a','a','a','a','a','a','a','a','a','a','a',],
                default_index=0
            )
        with n1c2:
            st.markdown('<div class="vertical-line"></div>', unsafe_allow_html=True)
        