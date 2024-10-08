from altair import value
import streamlit as st
import os
import pandas as pd
from streamlit_modal import Modal
from streamlit_option_menu import option_menu


if 'edit' not in st.session_state:
    st.session_state.edit = False
if 'button_label' not in st.session_state:
    st.session_state.button_label = "Edit"
def show_data(emp):
    # MARK: Show Data
    for i in range(len(emp)):
        with st.container(border=1):
            r1c1,r1c3 = st.columns([7,3])
            with r1c1:
                st.html(f"""
                        <style>
                            button[kind="primary"]{{
                                all: unset;
                                background-color: #22384F;
                                color: white;
                                border-radius: 50px;
                                text-align: center;
                                cursor: pointer;
                                font-size: 20px;
                                width: 65%;
                                padding: 10px ;
                            }}
                            .cnt{{
                                width: 100%;
                                margin-left:20px;
                                display: flex;
                                align-items: center;
                            
                            }}
                            .cnt img{{
                                width: 50px;
                                height: 50px;
                                border-radius: 50px;
                                
                            }}
                            .cnt div{{
                                margin-top: 14px;
                                margin-left: 20px;
                                display: flex;
                                justify-content: center;
                                align-items: center;                                
                                color: #333;
                            }}
                        </style>
                        <div class="cnt">
                            <img src="https://www.w3schools.com/howto/img_avatar.png" alt="Avatar" style="width:50px; border-radius:50px">
                            <b style="margin: 20px;" >{emp[i]["emp_no"]}</b>
                            <b style="margin: 20px;" >{emp[i]["name"]}</b>
                        </div>
                    """)
            with r1c3:
                st.html("""
                    <div style="width:50px;height:3px display:flex; alignItems: center"></div>
                        """)
                if st.button("View",key=i,type="primary"):
                    st.session_state.open_modal = True
                    st.session_state.usr_prof = emp[i]
                    st.rerun()

def set_data(emp):
    st.session_state.data = emp.to_dict('records')

def Search(cursor):
    modal = Modal(
        "Employee Profile",
        key="modal",
    )
    if "usr_prof" not in st.session_state:
        st.session_state.usr_prof = {}
    if "search" not in st.session_state:
        st.session_state.search = False
    if "searchinp" not in st.session_state:
        st.session_state.searchinp = ""

    if "data" not in st.session_state:
        st.session_state.data = {}
    if "open_modal" not in st.session_state:
        st.session_state.open_modal = False

    if st.session_state.open_modal == False:
        st.title("Search")
        search1, search2,search3 = st.columns([7,1,3])
        with search1:
            st.session_state.searchinp = st.text_input("search",placeholder="Search by Patient ID")
        with search2:
            st.write("<div><br></div>", unsafe_allow_html=True)
            st.session_state.search = st.button("Search", type="primary")

        if st.session_state.search:
            cursor.execute(f"SELECT * FROM Employee_det WHERE emp_no like '%{st.session_state.searchinp}%' ")

            emp = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
            if emp.empty:
                st.error("No records found")
            else:
                set_data(emp)

        r0c1,r0c2 = st.columns([7,3])
        with r0c1:
            show_data(st.session_state.data)


    else:
        # MARK: Modal
        st.title("Employee Profile")
        r0c1, r0c2 = st.columns([8,2], vertical_alignment='center')
        with r0c1:
            with st.container(border=1):
                r1c1, r1c2, r1c3 = st.columns([2,3,4])
                cursor.execute(f"SELECT * FROM vitals WHERE emp_no = '{st.session_state.usr_prof['emp_no']}'")
                vitals = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
                cursor.execute(f"SELECT * FROM consultation WHERE emp_no = '{st.session_state.usr_prof['emp_no']}'")
                consultation = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
                
                cursor.execute(f"SELECT * FROM x_ray WHERE emp_no = '{st.session_state.usr_prof['emp_no']}'")
                xray = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
                cursor.execute(f"SELECT * FROM womens_pack WHERE emp_no = '{st.session_state.usr_prof['emp_no']}'")
                womens = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
                
            with r1c1:
                st.image('./src/assets/Male User.png', width=160)
            with r1c2:
                st.write(f"Name: {st.session_state.usr_prof['name']}")
                st.write(f"Employee ID: {st.session_state.usr_prof['emp_no']}")
                st.write(f"Aadhar No: {st.session_state.usr_prof['aadhar_no']}")
            with r1c3:
                st.write(f"Blood Grp: {st.session_state.usr_prof['blood_group']}")
                st.write(f"Department: {st.session_state.usr_prof['department']}")
                st.write(f"Phone No: {st.session_state.usr_prof['office_phone_no'][1:]}")
        with r0c2:
            st.html(f"""
                        <style>
                            button[kind="primary"]{{
                                all: unset;
                                background-color: #22384F;
                                color: white;
                                border-radius: 10px;
                                text-align: center;
                                cursor: pointer;
                                font-size: 20px;
                                width: 65%;
                                padding: 10px ;
                            }}
                        </style>
                        
                    """)
            if st.button(st.session_state.button_label, key=0, type="primary"):
                # Toggle the edit state
                st.session_state.edit = not st.session_state.edit

                # Switch button label based on the edit state
                if st.session_state.edit:
                    st.session_state.button_label = "Save"
                    st.rerun()
                else:
                    st.session_state.button_label = "Edit"
                    st.rerun()
            st.button("Active",key=1,type="primary")
        with st.container(border=1,height=500):
            menu = option_menu(
                    None,
                    ["Personal Details", "Employment Details","Vitals", "Medical/Surgical History", "Visit Reason", "Vaccinations"],
                    key="menu",
                    orientation="horizontal",
                    icons=['a','b','c', 'a','b','c','a','b','c']
                )
            if menu == "Personal Details":
                r0c1,r0c2 = st.columns([5,6])
                with r0c1:
                # MARK: Personal Details
                    # st.markdown(f"""
                    #     **Age**: {st.text_input( label = "Age", label_visibility='collapsed', value = st.session_state.usr_prof.get('age', 'N/A'))}<br>
                    #     **DOB**: {st.session_state.usr_prof.get('dob', 'N/A')}<br>
                    #     **Sex**: {st.session_state.usr_prof.get('gender', 'N/A')}<br>
                    #     **Aadhar No**: {st.session_state.usr_prof.get('aadhar_no', 'N/A')}
                    # """, unsafe_allow_html=True)
                    rr0c1, rr0c2 = st.columns(2)
                    with rr0c1:
                        st.write('Age :')
                        st.write('\n')
                        st.write('DOB :')
                        st.write('\n')
                        st.write("Sex :")
                        st.write('\n')
                        st.write("Aadhar No:")
                    with rr0c2:
                        st.text_input(label = "age", label_visibility='collapsed', disabled=not st.session_state.edit ,value=st.session_state.usr_prof.get('age', 'N/A'))
                        st.text_input(label = "dob", label_visibility='collapsed', value=st.session_state.usr_prof.get('dob', 'N/A'))
                        st.text_input(label = "sex", label_visibility='collapsed', value=st.session_state.usr_prof.get('gender', 'N/A'))
                        st.text_input(label = "adno", label_visibility='collapsed', value=st.session_state.usr_prof.get('aadhar_no', 'N/A'))
                with r0c2:
                    # st.write(f"**Mail ID (Personal)**: {st.session_state.usr_prof['personal_mail']}")
                    # st.write("**Identification Mark**:")
                    # st.markdown(f" * {st.session_state.usr_prof['identification_mark']}")
                    rr0c1, rr0c2 = st.columns(2)
                    with rr0c1:
                        st.write('Mail ID :')
                        st.write('\n')
                        st.write('Identification Mark :')
                        st.write('\n')
                    with rr0c2:
                        st.text_input(label = "age", label_visibility='collapsed', value=st.session_state.usr_prof.get('personal_mail', 'N/A'))
                        st.text_input(label = "dob", label_visibility='collapsed', value=st.session_state.usr_prof.get('identification_mark', 'N/A'))
                        
            if menu == "Employment Details":
                r0c1,r0c2 = st.columns([5,6])
                with r0c1:
                # MARK: Personal Details
                    # st.markdown(f"""
                    #     **Employee No**: {st.session_state.usr_prof.get('emp_no', 'N/A')}<br>
                    #     **Designation**: {st.session_state.usr_prof.get('designation', 'N/A')}<br>
                    #     **Department H/O**: {st.session_state.usr_prof.get('department', 'N/A')}
                    # """, unsafe_allow_html=True)
                    rr0c1, rr0c2 = st.columns(2)
                    with rr0c1:
                        st.write('Employee No :')
                        st.write('\n')
                        st.write('Designation :')
                        st.write('\n')
                        st.write("Department H/O :")
                    with rr0c2:
                        st.text_input(label = "eno", label_visibility='collapsed', value=st.session_state.usr_prof.get('emp_no', 'N/A'))
                        st.text_input(label = "des", label_visibility='collapsed', value=st.session_state.usr_prof.get('designation', 'N/A'))
                        st.text_input(label = "dept", label_visibility='collapsed', value=st.session_state.usr_prof.get('department', 'N/A'))
                with r0c2:
                    # st.write(f"**Mail ID (Office)**: {st.session_state.usr_prof['office_mail']}")
                    # st.write(f"**Nature of Job H/O**:{st.session_state.usr_prof['nature_of_job']}")
                    # st.write(f"**Employer**:{st.session_state.usr_prof['personal_mail']}")
                    # st.write(f"**Contractor**:{st.session_state.usr_prof['personal_mail']}")
                    rr0c1, rr0c2 = st.columns(2)
                    with rr0c1:
                        st.write('Mail ID (Office) :')
                        st.write('\n')
                        st.write('Nature of Job H/O :')
                        st.write('\n')
                        st.write("Employer :")
                        st.write('\n')
                        st.write("Contractor :")
                    with rr0c2:
                        st.text_input(label = "mail", label_visibility='collapsed' ,value=st.session_state.usr_prof.get('office_mail', 'N/A'))
                        st.text_input(label = "job", label_visibility='collapsed', value=st.session_state.usr_prof.get('nature_of_job', 'N/A'))
                        st.text_input(label = "mep", label_visibility='collapsed', value=st.session_state.usr_prof.get('employer', 'N/A'))
                        st.text_input(label = "cot", label_visibility='collapsed', value=st.session_state.usr_prof.get('contractor', 'N/A'))
            # if menu == "Contact Details":
            #     r0c1,r0c2 = st.columns([5,6])
            #     with r0c1:
            #     # MARK: Personal Details
            #         st.markdown(f"""
            #             **Employee No**: {st.session_state.usr_prof.get('emp_no', 'N/A')}<br>
            #             **Designation**: {st.session_state.usr_prof.get('designation', 'N/A')}<br>
            #             **Department H/O**: {st.session_state.usr_prof.get('department', 'N/A')}
            #         """, unsafe_allow_html=True)
            #     with r0c2:
            #         st.write(f"**Mail ID (Office)**: {st.session_state.usr_prof['office_mail']}")
            #         st.write(f"**Nature of Job H/O**:{st.session_state.usr_prof['nature_of_job']}")
            #         st.write(f"**Employer**:{st.session_state.usr_prof['personal_mail']}")
            #         st.write(f"**Contractor**:{st.session_state.usr_prof['personal_mail']}")
            if menu == "Vitals":
                r0c1,r0c2 = st.columns([5,6])
                with r0c1:
                # # MARK: Personal Details
                #     st.markdown(f"""
                #         <b>Blood Pressure</b><br/>
                #         **Systolic**: {vitals['Systolic'][0]}<br>
                #         **Diastolic**: {vitals['Diastolic'][0]}<br>
                #         **Pulse Rate**: {vitals['PulseRate'][0]}<br>
                #         **SPO2**: {vitals['SpO2'][0]}
                #         **Respiratory Rate**: {vitals['RespiratoryRate'][0]}
                #     """, unsafe_allow_html=True)
                    rr0c1, rr0c2 = st.columns(2)
                    with rr0c1:
                        st.write('Blood Pressure :')
                        st.write('\n')
                        st.write('Systolic :')
                        st.write('\n')
                        st.write("Diastolic :")
                        st.write('\n')
                        st.write("Pulse Rate :")
                        st.write('\n')
                        st.write("Respiratory Rate :")
                    with rr0c2:
                        st.text_input(label = "BMI1", label_visibility='collapsed' ,value=vitals['Systolic'][0])
                        st.text_input(label = "Height1", label_visibility='collapsed', value=vitals['Diastolic'][0])
                        st.text_input(label = "Temperature1", label_visibility='collapsed', value=vitals['PulseRate'][0])
                        st.text_input(label = "Weight1", label_visibility='collapsed', value=vitals['SpO2'][0])
                        st.text_input(label = "Weight1", label_visibility='collapsed', value=vitals['RespiratoryRate'][0])
                    
                with r0c2:
                # # MARK: Personal Details
                #     st.markdown(f"""
                #         <b>Blood Pressure</b><br/>
                #         **Systolic**: {vitals['Systolic'][0]}<br>
                #         **Diastolic**: {vitals['Diastolic'][0]}<br>
                #         **Pulse Rate**: {vitals['PulseRate'][0]}<br>
                #         **SPO2**: {vitals['SpO2'][0]}
                #         **Respiratory Rate**: {vitals['RespiratoryRate'][0]}
                #     """, unsafe_allow_html=True)
                    rr0c1, rr0c2 = st.columns(2)
                    with rr0c1:
                        st.write('BMI :')
                        st.write('\n')
                        st.write('Height :')
                        st.write('\n')
                        st.write("Temperature :")
                        st.write('\n')
                        st.write("Weight :")
                    with rr0c2:
                        st.text_input(label = "BMI", label_visibility='collapsed' ,value=vitals['BMI'][0])
                        st.text_input(label = "Height", label_visibility='collapsed', value=vitals['Height'][0])
                        st.text_input(label = "Temperature", label_visibility='collapsed', value=vitals['Temperature'][0])
                        st.text_input(label = "Weight", label_visibility='collapsed', value=vitals['Weight'][0])
                # with r0c2:
                #     st.write(f"**BMI (in Value)**: {vitals['BMI'][0]}")
                #     st.write(f"**Height**: {vitals['Height'][0]}")
                #     st.write(f"**Temperature**: {vitals['Temperature'][0]}")
                #     st.write(f"**Weight**: {vitals['Weight'][0]}")
            if menu == "Visit Reason":
                r0c1,r0c2 = st.columns([3,6])
                with r0c1:
                # MARK: Personal Details
                    st.write("**Select the Year**")
                    st.date_input('Date', label_visibility='collapsed')
                    st.write("**Select the Reason**")
                    menu1 = option_menu(
                    None,
                    menu_icon='./src/assets/Folder.png',
                    options=["Pre Employment", "Pre Placement","Annual/Periodical","Camps", "Fitness After Medical Leave", "Illness", "Injury", "Followup Visit", "Special Work Fitness"],
                    key="menu1",
                    icons=['a','b','c', 'a','b','c','a','b','c']
                    )
                with r0c2:
                    if menu1 == "Camps":
                        menu2 = option_menu(
                        None,
                        menu_icon='./src/assets/Folder.png',
                        options=["Mandatory Camps", "Optional Camps"],
                        key="menu2",
                        orientation='horizontal',
                        icons=['a','b']
                        )
                        r3c1, r3c2, r3c3, r3c4, r3c5 = st.columns([2,2,2,2,2])
                        with r3c1:
                            st.markdown("<b style = 'color: #22384F'>Hospital Name</b>", unsafe_allow_html=True)
                        with r3c2:
                            st.markdown("<b style = 'color: #22384F'>Purpose</b>", unsafe_allow_html=True)
                        with r3c3:
                            st.markdown("<b style = 'color: #22384F'>Doctor</b>", unsafe_allow_html=True)
                        with r3c4:
                            st.markdown("<b style = 'color: #22384F'>Visited Date</b>", unsafe_allow_html=True)
                        with r3c5:
                            st.markdown("<b style = 'color: #22384F'>Details</b>", unsafe_allow_html=True)
                    else:
                        r3c1, r3c2, r3c3, r3c4, r3c5 = st.columns([2,2,2,2,2])
                        with r3c1:
                            st.markdown("<b style = 'color: #22384F'>Hospital Name</b>", unsafe_allow_html=True)
                        with r3c2:
                            st.markdown("<b style = 'color: #22384F'>Purpose</b>", unsafe_allow_html=True)
                        with r3c3:
                            st.markdown("<b style = 'color: #22384F'>Doctor</b>", unsafe_allow_html=True)
                        with r3c4:
                            st.markdown("<b style = 'color: #22384F'>Visited Date</b>", unsafe_allow_html=True)
                        with r3c5:
                            st.markdown("<b style = 'color: #22384F'>Details</b>", unsafe_allow_html=True)
            if( menu == "Vaccinations"):
                r0c1, r0c2 = st.columns([3,7])
                with r0c1:
                    st.subheader("Disease Name")
                    menu1 = option_menu(
                    None,
                    menu_icon='./src/assets/Folder.png',
                    options=["Typhoid", "Covid"],
                    key="menu2",
                    icons=['a','b']
                    )
                with r0c2:
                    r3c1, r3c2, r3c3, r3c4, r3c5 = st.columns([2,1,3,2,2])
                    with r3c1:
                        st.markdown("<b style = 'color: #22384F'>S no.</b>", unsafe_allow_html=True)
                    with r3c2:
                        st.markdown("<b style = 'color: #22384F'>Status</b>", unsafe_allow_html=True)
                    with r3c3:
                        st.markdown("<b style = 'color: #22384F'>Name of Vaccine</b>", unsafe_allow_html=True)
                    with r3c4:
                        st.markdown("<b style = 'color: #22384F'>Dose</b>", unsafe_allow_html=True)
                    with r3c5:
                        st.markdown("<b style = 'color: #22384F'>Booster</b>", unsafe_allow_html=True)
    if st.button("close"):
        st.session_state.open_modal = False
        st.rerun()
