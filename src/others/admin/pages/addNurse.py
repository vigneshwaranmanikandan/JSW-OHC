import streamlit as st
from  streamlit_option_menu import option_menu
import mysql.connector

def addNurse():
    st.title("Add Nurse")
    r0c1,r0c2,r0c3= st.columns([3,2,4])
    with r0c1:
        
        form_name = option_menu(
            None,
            ["Basic details","Register Mail Id"],
            orientation="horizontal",
            icons=['a','a','a','a','a']
        )
        
    if form_name == "Basic details":
            r1c1,r1c2,r1c3 = st.columns([3,2,4])

            with r1c1:
                name = st.text_input("Name")
                dob = st.date_input("Date of Birth")
                sex = st.selectbox("Sex", options=["Male", "Female", "Other"])
                aadhar_no = st.text_input("Aadhar No.")
                identification_marks = st.text_input("Identification Marks")
                blood_group = st.text_input("Blood Group")
                height = st.number_input("Height in cm", format="%f")
                weight = st.number_input("Weight in Kg", format="%f")
                
            with r1c2:
                employee_no = st.text_input("Employee No.")
                date_of_joining = st.date_input("Date of Joining")
                designation = st.text_input("Designation")
                department = st.text_input("Department")
                nature_of_job = st.text_input("Nature of Job")
                phone_personal = st.text_input("Phone (Personal)")
                phone_office = st.text_input("Phone (Office)")
                mail_id_personal = st.text_input("Mail Id (Personal)")
                
                
            with r1c3:
                mail_id_office = st.text_input("Mail Id (Office)")
                emergency_contact_person = st.text_input("Emergency Contact Person")
                emergency_contact_relation = st.text_input("Emergency Contact Relation")
                emergency_contact_phone = st.text_input("Emergency Contact Phone")
                mail_id_emergency_contact_person = st.text_input("Mail Id (Emergency Contact Person)")
                address = st.text_area("Address")

            # Age is calculated from DOB
            from datetime import date
            age = date.today().year - dob.year - ((date.today().month, date.today().day) < (dob.month, dob.day))
            st.text(f"Age: {age}")

            # Save button 
            st.write("""
            <style>
                button[kind="primary"]{
                    background-color: #22384F;
                    color: white;
                    border-radius: 5px;
                    text-align: center;
                    cursor: pointer;
                    font-size: 20px;
                    width: 10%;
                    padding: 8px ;
                    margin-left:1440px
                }
            </style>
            """,unsafe_allow_html=True)  
            if st.button(label="Save",type="primary"):
            # Call save to database function
                save_nurse_to_db(employee_no, name, dob, age, sex, aadhar_no, identification_marks,
                                blood_group, height, weight, date_of_joining, designation, department,
                                nature_of_job, phone_personal, phone_office, mail_id_personal, mail_id_office,
                                emergency_contact_person, emergency_contact_relation, emergency_contact_phone,
                                mail_id_emergency_contact_person, address)
                #st.write("Data Saved")
    
    else:
        st.write("""
            <style>
                button[kind="primary"]{
                    background-color: #22384F;
                    color: white;
                    border-radius: 5px;
                    text-align: center;
                    cursor: pointer;
                    font-size: 20px;
                    width: 25%;
                    padding: 8px ;
                    margin-left:510px
                }
            </style>
            """,unsafe_allow_html=True)
        r1c1,r1c2,r1c3 = st.columns([2,3,2])
        with r1c2:
            email=st.text_input("Email",value="@jsw.in")
            st.button(label="Check")
            password=st.text_input("Password",type="password")
            st.button(label="Register",type="primary")

def save_nurse_to_db(emp_no, name, dob, age, gender, aadhar_no, identification_mark, blood_group,
                     height, weight, date_of_join, designation, department, nature_of_job,
                     personal_phone_no, office_phone_no, personal_mail, office_mail,
                     emg_con_person, emg_con_relation, emg_con_number, emg_con_mail, address):
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host="mysql-5893c62-jsw-test.a.aivencloud.com",  # e.g., localhost
            user="avnadmin",  # MySQL username
            password="AVNS_uVkEh0awpxi9I4bEOCq",  # MySQL password
            database="defaultdb",# Name of the database where the 'doctor' table exists
            port=19129  
        )

        # Create a cursor object
        cursor = connection.cursor()

        # SQL query to insert nurse data into the 'nurse' table
        insert_query = """
        INSERT INTO nurse (emp_no, name, dob, age, gender, aadhar_no, identification_mark, blood_group, height, 
        weight, date_of_join, designation, department, nature_of_job, personal_phone_no, office_phone_no, 
        personal_mail, office_mail, emg_con_person, emg_con_relation, emg_con_number, emg_con_mail, address) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Execute the query with the form data
        cursor.execute(insert_query, (emp_no, name, dob, age, gender, aadhar_no, identification_mark, blood_group,
                                      height, weight, date_of_join, designation, department, nature_of_job,
                                      personal_phone_no, office_phone_no, personal_mail, office_mail, emg_con_person,
                                      emg_con_relation, emg_con_number, emg_con_mail, address))

        # Commit the transaction
        connection.commit()

        # Display success message
        st.success("Nurse's data has been saved successfully!")

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()