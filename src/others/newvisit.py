from altair import Column
import streamlit as st
import os
import pandas as pd
from  streamlit_option_menu import option_menu
import numpy as np
import json
import datetime
import mysql.connector
from datetime import datetime



if "form_data" not in st.session_state:
        st.session_state.form_data = {} 

def systolic_diastolic_chart(systolic, diastolic):
    systolic = int(systolic)
    diastolic = int(diastolic)
    if systolic ==0 or diastolic ==0:
        return ["0", "black"]
    elif systolic < 90 or diastolic < 60:
        return ["Hypotension", "00ff00"]
    elif 90 <= systolic <= 120 and 60 <= diastolic <= 80:
        return ["Normal", "green"]
    elif 120 < systolic <= 129 and 60 <= diastolic <= 80:
        return ["Elevated", "yellow"]
    elif 130 <= systolic <= 139 or 80 <= diastolic <= 89:
        return ["HT Stage 1", "orange"]
    elif 140 <= systolic <= 180 or 90 <= diastolic <= 120:
        return ["HT Stage 2", "red"]
    elif systolic > 180 or diastolic > 120:
        return ["HT Crisis", "#990000"]
    else:
        return "Invalid input"


def Form(visitreason,select, select1, connection, cursor):

    st.write("""
        <style>
            div.stButton > button[kind="primary"] {
                all: unset;
                background-color: #22384F;
                color: white;
                border-radius: 5px;
                text-align: center;
                cursor: pointer;
                font-size: 10px;
                width: 25%;
                padding: 5px;
                margin-left: auto;  /* Align the button to the right */
                display: block;
            }
            div.stButton {
                display: flex;
                justify-content: flex-end;  /* Moves button container to the right */
            }
        </style>
    """, unsafe_allow_html=True)
    

    if select1=="Healthy":
        if visitreason=="Camps (Optional)":
            form_name = option_menu(
            None,
            ["Basic Details", "Vitals","Medical History", "Investigations",  "Consultation"],
            orientation="horizontal",
            icons=['a','a','a','a','a']
        )
        elif visitreason=="Special Work Fitness":
            form_name = option_menu(
            None,
            ["Basic Details", "Vitals", "Fitness", "Consultation"],
            orientation="horizontal",
            icons=['a','a','a','a']
        )
        elif visitreason=="Special Work Fitness (Renewal)" or select=="Visitor":
            form_name = option_menu(
            None,
            ["Basic Details", "Vitals","Medical History", "Fitness", "Consultation"],
            orientation="horizontal",
            icons=['a','a','a','a','a']
        )
        elif visitreason=="Fitness After Medical Leave":
            form_name = option_menu(
            None,
            ["Basic Details","Vitals","Medical History", "Fitness", "Consultation","Medical Leave/Sickness Absence Ratio"],  #not defined
            orientation="horizontal",
            icons=['a','a','a','a','a','a','a']
            )
        elif visitreason=="Mock Drill" or visitreason=="BP Sugar Check":
            form_name= option_menu(
                None,
                ["Basic Details", "Vitals"],
                orientation="horizontal",
                icons=['a','a']
            )
        else:
            form_name = option_menu(
                None,
                ["Basic Details", "Vitals","Medical History", "Investigations", "Fitness", "Consultation"],
                orientation="horizontal",
                icons=['a','a','a','a','a','a']
            )
    if select1=="Unhealthy":
        if select=="Contractor" and visitreason=="Over counter Injury Outside the premises":
            form_name = option_menu(
            None,
            ["Basic Details","Consultation","Prescription","Referral" ],
            orientation="horizontal",
            icons=['a','a','a','a','a']
            )
        elif visitreason=="Illness" or visitreason=="BP Sugar (Abnormal)" or visitreason=="Injury Outside the premises" or visitreason=="Over counter Injury Outside the premises":
            form_name = option_menu(
            None,
            ["Basic Details", "Vitals","Medical History","Consultation","Prescription","Referral" ],
            orientation="horizontal",
            icons=['a','a','a','a','a','a','a','a']
            )
        elif visitreason=="Injury":
            form_name = option_menu(
            None,
            ["Basic Details","Prescription","Referral"],
            orientation="horizontal",
            icons=['a','a','a']
            )
        elif visitreason=="Over counter Injury":
            form_name = option_menu(
            None,
            ["Basic Details","Consultation","Prescription","Referral"],
            orientation="horizontal",
            icons=['a','a','a','a','a']
            )
        elif select!="Contractor"and visitreason=="Follow up Visits":
            form_name = option_menu(
            None,
            ["Basic Details","Vitals","Investigations","Consultation","Prescription","Referral"],
            orientation="horizontal",
            icons=['a','a','a','a','a','a',]
            )
        else:
            form_name = option_menu(
            None,
            ["Basic Details", "Vitals","Consultation","Prescription","Referral" ],
            orientation="horizontal",
            icons=['a','a','a','a','a',]
            )

    rc1, rc2, rc3 = st.columns([1,3,2])
    with rc1:
        st.header("Get User")
    with rc2:
        st.session_state.form_data["Employee ID"] = st.text_input("Employee ID", value=st.session_state.form_data.get("Employee ID", ""))
    with rc3: 
        if st.button("Get Info", type="primary"):  
            cursor.execute(f"SELECT * FROM Employee_det WHERE emp_no = '{st.session_state.form_data['Employee ID']}'")
            data = cursor.fetchone()
            if data is not None:
                
                st.session_state.form_data["Visit Reason"] = "Pre Employment"  # Hardcoded value
                st.session_state.form_data["Employee Name"] = data[1]
                st.session_state.form_data["Employee Age"] = data[3]
                st.session_state.form_data['Gender'] = data[4]
                st.session_state.form_data['Mobile No.'] = data[14][1:] if data[14] else ""
                st.session_state.form_data['Address'] = data[22] if data[22] is not None else ""
                st.session_state.form_data['Department'] = data[12]
                st.session_state.form_data['Work'] = data[11]
                st.session_state.form_data['Blood Group'] = data[7]
                st.session_state.form_data['Vaccination Status'] = data[9]
            else:
                st.warning("No basic Data Found")
            cursor.execute(f"SELECT * FROM vitals WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if  len(df)!=0:
                st.session_state.form_data["Systolic"] = df[-1][3]
                st.session_state.form_data["Diastolic"] = df[-1][4]
                st.session_state.form_data["Pulse"] = df[-1][5]
                st.session_state.form_data["Temperature"] = df[-1][7]
                st.session_state.form_data["Respiratory Rate"] = df[-1][8]
                st.session_state.form_data["spo2"] = df[-1][6]
                st.session_state.form_data["BMI"] = df[-1][11]
                st.session_state.form_data["Weight"] = df[-1][10]
                st.session_state.form_data["Height"] = df[-1][9]
            else:
                st.warning("No Vitals found")
            cursor.execute(f"SELECT * FROM medicalpersonalhist WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Personal History"] = df[0][3]
                st.session_state.form_data["Medical History"] = df[0][4]
                st.session_state.form_data["Surgical History"] = df[0][5]
                st.session_state.form_data["Father"] = df[-1][6]
                st.session_state.form_data["Mother"] = df[-1][7]
            else:
                st.warning("No Medical History found")
            cursor.execute(f"SELECT * FROM hematology_result WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Hemoglobin"] = df[-1][3]
                st.session_state.form_data["Total RBC"] = df[-1][6]
                st.session_state.form_data["Total WBC"] = df[-1][9]
                st.session_state.form_data["Neutrophil"] = df[-1][30]
                st.session_state.form_data["Monocyte"] = df[-1][39]
                # st.session_state.form_data["PCV"] = df[-1][]
                st.session_state.form_data["MCV"] = df[-1][15]
                st.session_state.form_data["MCH"] = df[-1][18]
                st.session_state.form_data["Lymphocyte"] = df[-1][33]
                st.session_state.form_data["ESR"] = df[-1][45]            
                st.session_state.form_data["MCHC"] = df[-1][21]
                st.session_state.form_data["Platelet Count"] = df[-1][24]
                st.session_state.form_data["RDW"] = df[-1][27]
                st.session_state.form_data["Eosinophil"] = df[-1][36]
                st.session_state.form_data["Basophil"] = df[-1][42]
                st.session_state.form_data["Preipheral Blood Smear - RBC Morphology"] = df[-1][48]
                st.session_state.form_data["Preipheral Blood Smear - Parasites"] = df[-1][49]
                st.session_state.form_data["Preipheral Blood Smear - Others"] = df[-1][50]
            else:
                st.warning("No Hematology Result found")
            cursor.execute(f"SELECT * FROM routine_sugartest WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Glucose (F)"] = df[-1][3]
                st.session_state.form_data["Glucose (PP)"] = df[-1][6]
                st.session_state.form_data["Random Blood sugar"] = df[-1][9]
                st.session_state.form_data["Estimated Average Glucose"] = df[-1][12]
                st.session_state.form_data["HbA1c"] = df[-1][15]
                st.session_state.form_data["Employee ID"] = df[-1][2]
            else:
                st.warning("No Routine Sugar Test Result found")
            cursor.execute(f"SELECT * FROM rft_result WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Urea"] = df[-1][3]
                st.session_state.form_data['BUN'] = df[-1][6]
                st.session_state.form_data["Serum Creatinine"] = df[-1][9]
                st.session_state.form_data["Uric Acid"] = df[-1][12] 
                st.session_state.form_data["Sodium"] = df[-1][15]
                st.session_state.form_data["Potassium"] = df[-1][18]
                st.session_state.form_data["Calcium"] = df[-1][21]
                st.session_state.form_data["Phosphorus"] = df[-1][24]
                st.session_state.form_data["Chloride"] = df[-1][27]
            else:
                st.warning("No Renal Function Test Result found")
            cursor.execute(f"SELECT * FROM lipid_profile WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Total Cholesterol"] = df[-1][3]
                st.session_state.form_data["Triglycerides"] = df[-1][6]
                st.session_state.form_data["HDL - Cholesterol"] = df[-1][9]
                st.session_state.form_data["LDL- Cholesterol"] = df[-1][15]
                st.session_state.form_data["CHOL HDL ratio"] = df[-1][18]
                st.session_state.form_data["VLDL -Choleserol"] = df[-1][12]
                st.session_state.form_data["LDL.CHOL/HDL.CHOL Ratio"] = df[-1][21]
            else:
                st.warning("No Lipid Profile Test Result found")
            cursor.execute(f"SELECT * FROM liver_function WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Bilirubin - Total"] = df[-1][3] 
                st.session_state.form_data["Bilirubin - Direct"] = df[-1][6] 
                st.session_state.form_data["Bilirubin - Indirect"] = df[-1][9]
                st.session_state.form_data["SGOT /AST"] = df[-1][12] 
                st.session_state.form_data["SGPT /ALT"] = df[-1][15] 
                st.session_state.form_data["Alkaline phosphatase"] = df[-1][18] 
                st.session_state.form_data["Total Protein"] = df[-1][21] 
                st.session_state.form_data["Albumin (Serum )"] = df[-1][24] 
                st.session_state.form_data["Globulin(Serum)"] = df[-1][27] 
                st.session_state.form_data["Alb/Glob Ratio"] = df[-1][30] 
                st.session_state.form_data["Gamma Glutamyl transferase"] = df[-1][33] 
            else:
                st.warning("No Liver Function Test Result found")
            cursor.execute(f"SELECT * FROM thyroid_function_test WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["T3- Triiodothyroine"] = df[-1][3]
                st.session_state.form_data["T4 - Thyroxine"] = df[-1][6] 
                st.session_state.form_data["TSH- Thyroid Stimulating Hormone"] = df[-1][7]  
            else:
                st.warning("No Thyroid Function Test Result found")
            cursor.execute(f"SELECT * FROM autoimmune_test WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["ANA (Antinuclear Antibody)"] = df[-1][3]
                st.session_state.form_data["Anti ds DNA"] = df[-1][6] 
                st.session_state.form_data["Rheumatoid factor"] = df[-1][12] 
                st.session_state.form_data["Anticardiolipin Antibodies (IgG & IgM)"] = df[-1][9] 
            else:
                st.warning("No Auto Inumme Test Result found")
            cursor.execute(f"SELECT * FROM coagulation_test WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Prothrombin Time (PT)"] = df[-1][3] 
                st.session_state.form_data["PT INR"] = df[-1][6] 
                st.session_state.form_data["Bleeding Time (BT)"] = df[-1][9] 
                st.session_state.form_data["Clotting Time (CT)"] = df[-1][12] 
            else:
                st.warning("No Coagulation Test Result found")
            cursor.execute(f"SELECT * FROM enzymes_cardio WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                
                st.session_state.form_data["Acid Phosphatase"] = df[-1][3] 
                st.session_state.form_data["Adenosine Deaminase"] = df[-1][6] 
                st.session_state.form_data["Amylase"] = df[-1][9] 
                st.session_state.form_data["ECG"] = df[-1][27] 
                st.session_state.form_data["ECG-Comments"] = df[-1][28] 
                st.session_state.form_data["Troponin- T"] = df[-1][15] 
                st.session_state.form_data["Troponin- I"] = df[-1][18] 
                st.session_state.form_data["CPK - TOTAL"] = df[-1][21] 
                st.session_state.form_data["ECHO"] = df[-1][29] 
                st.session_state.form_data["ECHO-Comments"] = df[-1][30] 
                st.session_state.form_data["Lipase"] = df[-1][12] 
                st.session_state.form_data["CPK - MB"] = df[-1][24]
                st.session_state.form_data["TMT"] = df[-1][31] 
                st.session_state.form_data["TMT-Comments"] = df[-1][32] 
                st.warning("No Enzymes Cardio Test Result found")
            cursor.execute(f"SELECT * FROM urine_routine WHERE emp_no =  {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Colour"] = df[-1][3] 
                st.session_state.form_data["Appearance"] = df[-1][6] 
                st.session_state.form_data["Reaction (pH)"] = df[-1][9] 
                st.session_state.form_data["Specific gravity"] = df[-1][12] 
                st.session_state.form_data["Crystals"] = df[-1][45] 
                st.session_state.form_data["Bacteria"] = df[-1][48]
                st.session_state.form_data["Protein/Albumin"] = df[-1][15] 
                st.session_state.form_data["Glucose (Urine)"] = df[-1][18] 
                st.session_state.form_data["Ketone Bodies"] = df[-1][21] 
                st.session_state.form_data["Urobilinogen"] = df[-1][24] 
                st.session_state.form_data["Casts"] = df[-1][42] 
                st.session_state.form_data["Bile Salts"] = df[-1][27] 
                st.session_state.form_data["Bile Pigments"] = df[-1][30] 
                st.session_state.form_data["WBC / Pus cells"] = df[-1][33] 
                st.session_state.form_data["Red Blood Cells"] = df[-1][36] 
                st.session_state.form_data["Epithelial cells"] = df[-1][39]  
            else:
                st.warning("No Urine Routine Test Result found")
            cursor.execute(f"SELECT * FROM serology_result WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Screening For HIV I & II"] = df[-1][3] 
                st.session_state.form_data["HBsAg"] = df[-1][6] 
                st.session_state.form_data["HCV"] = df[-1][9] 
                st.session_state.form_data["VDRL"] = df[-1][15]
                st.session_state.form_data["Dengue NS1Ag"] = df[-1][18] 
                st.session_state.form_data["Dengue IgG"] = df[-1][21] 
                st.session_state.form_data["Dengue IgM"] = df[-1][24] 
                st.session_state.form_data["WIDAL"] = df[-1][12]  
  
            else:
                st.warning("No Serology Result found")
            cursor.execute(f"SELECT * FROM motion WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Colour (Motion)"] = df[-1][3] 
                st.session_state.form_data["Appearance (Motion)"] = df[-1][6] 
                st.session_state.form_data["Occult Blood"] = df[-1][9] 
                st.session_state.form_data["Cyst"] = df[-1][15] 
                st.session_state.form_data["Mucus"] = df[-1][18] 
                st.session_state.form_data["Pus Cells"] = df[-1][21]
                st.session_state.form_data["Ova"] = df[-1][12] 
                st.session_state.form_data["RBCs"] = df[-1][24] 
                st.session_state.form_data["Others"] = df[-1][27] 
            else:
                st.warning("No Motion Result found")
            cursor.execute(f"SELECT * FROM routine_culture WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Urine"] = df[-1][3]
                st.session_state.form_data["Motion"] = df[-1][6] 
                st.session_state.form_data["Sputum"] = df[-1][9]
                st.session_state.form_data["Blood"] = df[-1][12] 
            else:
                st.warning("No Routine Cultre Sensitivity Result found")
            cursor.execute(f"SELECT * FROM mens_pack WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["PSA (Prostate specific Antigen)"] = df[-1][3]
            else:
                st.warning("No Men's Pack Result found")
            cursor.execute(f"SELECT * FROM womens_pack WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Mammogram"] = df[-1][3] 
                st.session_state.form_data["Mammogram-Comments"] = df[-1][4] 
                st.session_state.form_data["PAP Smear"] = df[-1][5] 
                st.session_state.form_data["PAP Smear-Comments"] = df[-1][6] 
            else:
                st.warning("No Women's Pack Result found")
            cursor.execute(f"SELECT * FROM occupational_profile WHERE emp_no =  {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0:
                st.session_state.form_data["Audiometry"] = df[-1][3] 
                st.session_state.form_data["Audiometry-Comments"] = df[-1][4] 
                st.session_state.form_data["PFT"] = df[-1][5] 
                st.session_state.form_data["PFT-Comments"] = df[-1][6]  
            else:
                st.warning("No Occupational Profile found")
            cursor.execute(f"SELECT * FROM other_tests WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Pathology"] = df[-1][3] 
                st.session_state.form_data["Pathology-Comments"] = df[-1][4]
            else:
                st.warning("No Other Test Result found")
            cursor.execute(f"SELECT * FROM ophthalmic_report WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["Vision"] = df[-1][3] 
                st.session_state.form_data["Vision-Comments"] = df[-1][4] 
                st.session_state.form_data["Color Vision"] = df[-1][5] 
                st.session_state.form_data["Color Vision-Comments"] = df[-1][6] 
            else:
                st.warning("No Ophthalmic Test Result found")
            cursor.execute(f"SELECT * FROM x_ray WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                
                st.session_state.form_data["X-RAY Chest"] =df[-1][3] 
                st.session_state.form_data["X-RAY Chest-Comments"] =df[-1][4] 
                st.session_state.form_data["X-RAY KUB"] =df[-1][9] 
                st.session_state.form_data["X-RAY KUB-Comments"] =df[-1][10] 
                st.session_state.form_data["X-RAY Spine"] =df[-1][5] 
                st.session_state.form_data["X-RAY Spine-Comments"] =df[-1][6] 
                st.session_state.form_data["X-RAY Pelvis"] =df[-1][11] 
                st.session_state.form_data["X-RAY Pelvis-Comments"] =df[-1][12] 
                st.session_state.form_data["X-RAY Abdomen"] =df[-1][7] 
                st.session_state.form_data["X-RAY Abdomen-Comments"] =df[-1][8] 
            else:
                st.warning("No X-Ray Test Result found")
            cursor.execute(f"SELECT * FROM usg WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                
                st.session_state.form_data["USG ABDOMEN"] = df[-1][3] 
                st.session_state.form_data["USG ABDOMEN-Comments"] = df[-1][4] 
                st.session_state.form_data["USG KUB"] = df[-1][9] 
                st.session_state.form_data["USG KUB-Comments"] = df[-1][10] 
                st.session_state.form_data["USG Pelvis"] = df[-1][5] 
                st.session_state.form_data["USG Pelvis-Comments"] = df[-1][6]  
                st.session_state.form_data["USG Neck"] = df[-1][7] 
                st.session_state.form_data["USG Neck-Comments"] = df[-1][8] 
                    
            else:
                st.warning("No USG Test Result found")
            cursor.execute(f"SELECT * FROM ct_report WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                st.session_state.form_data["CT Brain"] = df[-1][3] 
                st.session_state.form_data["CT Brain-Comments"] = df[-1][4] 
                st.session_state.form_data["CT Lungs"] = df[-1][9] 
                st.session_state.form_data["CT Lungs-Comments"] = df[-1][10] 
                st.session_state.form_data["CT Abdomen"] = df[-1][5]   
                st.session_state.form_data["CT Abdomen-Comments"] = df[-1][6] 
                st.session_state.form_data["CT Spine"] = df[-1][11] 
                st.session_state.form_data["CT Spine-Comments"] = df[-1][12] 
                st.session_state.form_data["CT Pelvis"] = df[-1][7] 
                st.session_state.form_data["CT Pelvis-Comments"] = df[-1][8]  
            else:
                st.warning("No CT Test Result found")
            cursor.execute(f"SELECT * FROM mri WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            df = cursor.fetchall()
            if len(df)!=0: 
                
                st.session_state.form_data["MRI Brain"] = df[-1][3] 
                st.session_state.form_data["MRI Brain-Comments"] = df[-1][4]  
                st.session_state.form_data["MRI Lungs"] = df[-1][9]
                st.session_state.form_data["MRI Lungs-Comments"] = df[-1][10]
                st.session_state.form_data["MRI Abdomen"] = df[-1][5] 
                st.session_state.form_data["MRI Abdomen-Comments"] = df[-1][6] 
                st.session_state.form_data["MRI Spine"] = df[-1][11] 
                st.session_state.form_data["MRI Spine-Comments"] = df[-1][12] 
                st.session_state.form_data["MRI Pelvis"] = df[-1][7]
                st.session_state.form_data["MRI Pelvis-Comments"] = df[-1][8]
            else:
                st.warning("No MRI Test Result found")
            # cursor.execute(f"SELECT * FROM fitness WHERE emp_no = {st.session_state.form_data["Employee ID"]};")
            # df = cursor.fetchall()
            # if len(df)!=0: 
            #     st.session_state.form_data["Fitness"] = df[-1][3]
            #     st.session_state.form_data["Fitness-Comments"] = df[-1][3] 
            # else:
            #     st.warning("No MRI Test Result found")
            
    if form_name == "Basic Details":
        st.subheader("Basic Details")
        
        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            st.session_state.form_data["Visit Date"] = st.date_input("Visit Date")
            st.session_state.form_data["Gender"] = st.text_input("Gender", value=st.session_state.form_data.get("Gender", ""))
            st.session_state.form_data["Mobile No."] = st.text_input("Mobile No.", value=st.session_state.form_data.get("Mobile No.", ""))
            st.session_state.form_data["Vaccination Status"] = st.selectbox("Vaccination Status", options=['Yes', 'No'])
        
        with r1c2:
            st.session_state.form_data["Reference Type"] = st.selectbox('Select the hospital for the reference range', ["manipal", "Dharan", "Poornima"], index=0)
            st.session_state.form_data["Employee Name"] = st.text_input("Employee Name", value=st.session_state.form_data.get("Employee Name", ""))
            st.session_state.form_data["Department"] = st.text_input("Department", value=st.session_state.form_data.get("Department", ""))
            st.session_state.form_data["Blood Group"] = st.text_input("Blood Group", value=st.session_state.form_data.get("Blood Group", ""))

        with r1c3:
            st.session_state.form_data["Visit Reason"] = st.text_input('Visit Reason', value = st.session_state.form_data.get("Visit Reason"))
            st.session_state.form_data["Employee Age"] = st.text_input("Employee Age", value=st.session_state.form_data.get("Employee Age", ""))
            st.session_state.form_data["Work"] = st.text_input("Work", value=st.session_state.form_data.get("Work", ""))
            
        st.session_state.form_data["Address"] = st.text_area("Address", value=st.session_state.form_data.get("Address", ""))

        r2c1, r2c2, r2c3 = st.columns([5, 2, 3])
        

        
                
        with r2c3:
            if st.button("Add Data", type="primary"):
                emp_id = st.session_state.form_data["Employee ID"]
                sql = """
                INSERT INTO basicdetails (
                    emp_no, PatientName, PatientAge, Gender,
                    MobileNo, Address, Department, Work, BloodGroup, Vaccinated, vistreason, hospital, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    emp_id,
                    st.session_state.form_data["Employee Name"],
                    st.session_state.form_data["Employee Age"],
                    st.session_state.form_data["Gender"],
                    st.session_state.form_data["Mobile No."],
                    st.session_state.form_data["Address"],
                    st.session_state.form_data["Department"],
                    st.session_state.form_data["Work"],
                    st.session_state.form_data["Blood Group"],
                    st.session_state.form_data["Vaccination Status"],
                    st.session_state.form_data["Visit Reason"],
                    st.session_state.form_data["Reference Type"],
                    st.session_state.form_data["Health status"]
                )
                try:
                    # Execute the SQL INSERT command
                    cursor.execute(sql, values)
                    connection.commit()  # Commit the changes to the database
                    st.success("Data Added Successfully")  # Show success message
                except mysql.connector.Error as e:
                    st.error(f"Error inserting data: {e}")  
    elif form_name == "Vitals":
        st.header("Vitals")
        r1c1,r1c2,r1c3 = st.columns([5,3,9])
        with r1c1:
            systolic = st.session_state.form_data.get("Systolic", "0")
            diastolic = st.session_state.form_data.get("Diastolic", "0")

            st.session_state.form_data["Systolic"] = st.text_input("Systolic", value=systolic,)
            st.session_state.form_data["Diastolic"] = st.text_input("Diastolic", value=diastolic)

        with r1c2:
            # show the charts for the systolic and diastolic based on the data input
            st.write("""
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 300px; height: 50px; border-radius: 10px; margin-left: 50px;"></div>
            """, unsafe_allow_html=True)
            st.write("""
            <style>
                button[kind="secondary"]{
                    all: unset;
                    background-color: #22384F;
                    color: white;
                    border-radius: 5px;
                    text-align: center;
                    cursor: pointer;
                    font-size: 20px;
                    padding: 10px;
                    
                }
            </style>
            """,unsafe_allow_html=True)
            val = st.button("🧮", type="secondary")
        with r1c3:
            if val:
                val,color = systolic_diastolic_chart(systolic, diastolic)
                st.write(f"""
                    <style>
                        .chart_container {{
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: center;
                            width: 300px;
                            height: 80px;
                            border-radius: 10px;
                            margin-left: 50px;
                        }}
                        .chart-value h1{{
                            margin-top: 50px;
                            margin-left: 50px;
                            color: {color}
                        }}
                        .bar-values {{
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                            width: 300px;
                            height: 200px;
                        }}
                        .Normal {{
                            width: 19.5%;
                            height: 10px;
                            background-color: #00ff00af;
                            border-top-left-radius: 10px;
                            border-bottom-left-radius: 10px;
                        }}
                        .Elevated {{
                            width: 19.5%;
                            height: 10px;
                            background-color: #ffff00af;
                        }}
                        .HT-Stage-1 {{
                            width: 19.5%;
                            height: 10px;
                            background-color: #ff9900af;
                        }}
                        .HT-Stage-2 {{
                            width: 19.5%;
                            height: 10px;
                            background-color: #ff0000af;
                        }}
                        .HT-crisis {{
                            width: 19.5%;
                            height: 10px;
                            background-color: #990000af;
                            border-top-right-radius: 10px;
                            border-bottom-right-radius: 10px;
                        }}
                    </style>
                    <div class="chart_container">
                        <div class="chart-value"><h1>{val}</h1></div>
                        <div class="bar-values">
                            <div class="Normal"></div>
                            <div class="Elevated"></div>
                            <div class="HT-Stage-1"></div>
                            <div class="HT-Stage-2"></div>
                            <div class="HT-crisis"></div>
                        </div>
                    </div>
                """,unsafe_allow_html=True)
        
        r2c1,r2c2,r2c3 = st.columns(3)
        with r2c1:
            st.session_state.form_data["Pulse"] = st.text_input("Pulse", value=st.session_state.form_data.get("Pulse", ""))
            st.session_state.form_data["spo2"] = st.text_input("SpO2", value=st.session_state.form_data.get("spo2", ""))
            st.session_state.form_data["BMI"] = st.text_input("BMI", value=st.session_state.form_data.get("BMI", ""))

        with r2c2:
            st.session_state.form_data["Respiratory Rate"] = st.text_input("Respiratory Rate", value=st.session_state.form_data.get("Respiratory Rate", ""))
            st.session_state.form_data["Weight"] = st.text_input("Weight", value=st.session_state.form_data.get("Weight", ""))

        with r2c3:
            st.session_state.form_data["Temperature"] = st.text_input("Temperature", value=st.session_state.form_data.get("Temperature", ""))
            st.session_state.form_data["Height"] = st.text_input("Height", value=st.session_state.form_data.get("Height", ""))

        # Define layout for the button
        r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
        

        
        with r3c3:
            if st.button("Add Data", type="primary"):
                try:
                    emp_id = st.session_state.form_data["Employee ID"]
                    if not emp_id:
                        st.error("Employee ID is missing!")
                        return
                    
                    cursor.execute("""
                        INSERT INTO vitals (emp_no, Systolic, Diastolic, PulseRate, entry_date,Spo2, BMI, RespiratoryRate, Weight, Temperature, Height)
                        VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        emp_id,
                        st.session_state.form_data["Systolic"],
                        st.session_state.form_data["Diastolic"],
                        st.session_state.form_data["Pulse"],
                        datetime.now().date(),
                        st.session_state.form_data["spo2"],
                        st.session_state.form_data["BMI"],
                        st.session_state.form_data["Respiratory Rate"],
                        st.session_state.form_data["Weight"],
                        st.session_state.form_data["Temperature"],
                        st.session_state.form_data["Height"]
                    ))
                    connection.commit()
                    st.success("Data successfully added/updated!")
                except Exception as e:
                    st.error(f"Error saving data: {e}")
                    

    elif form_name == "Investigations":
        
        inv_form = ["HAEMATALOGY","ROUTINE SUGAR TESTS","RENAL FUNCTION TEST & ELECTROLYTES","LIPID PROFILE","LIVER FUNCTION TEST","THYROID FUNCTION TEST","AUTOIMMUNE TEST","COAGULATION TEST","ENZYMES & CARDIAC Profile","URINE ROUTINE","SEROLOGY","MOTION","ROUTINE CULTURE & SENSITIVITY TEST","Men's Pack","Women's Pack","Occupational Profile","Others TEST","OPHTHALMIC REPORT","X-RAY","USG","CT","MRI"]


        select_inv = st.selectbox("Select Investigation Form", inv_form)

        if select_inv == "HAEMATALOGY":
        
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                st.session_state.form_data["Hemoglobin"] = st.text_input("Hemoglobin", value=st.session_state.form_data.get("Hemoglobin", ""))
                st.session_state.form_data["Total RBC"] = st.text_input("Total RBC", value=st.session_state.form_data.get("Total RBC", ""))
                st.session_state.form_data["Total WBC"] = st.text_input("Total WBC", value=st.session_state.form_data.get("Total WBC", ""))
                st.session_state.form_data["Neutrophil"] = st.text_input("Neutrophil", value=st.session_state.form_data.get("Neutrophil", ""))
                st.session_state.form_data["Monocyte"] = st.text_input("Monocyte", value=st.session_state.form_data.get("Monocyte", ""))

            with r1c2:
                st.session_state.form_data["PCV"] = st.text_input("PCV", value=st.session_state.form_data.get("PCV", ""))
                st.session_state.form_data["MCV"] = st.text_input("MCV", value=st.session_state.form_data.get("MCV", ""))
                st.session_state.form_data["MCH"] = st.text_input("MCH", value=st.session_state.form_data.get("MCH", ""))
                st.session_state.form_data["Lymphocyte"] = st.text_input("Lymphocyte", value=st.session_state.form_data.get("Lymphocyte", ""))
                st.session_state.form_data["ESR"] = st.text_input("ESR", value=st.session_state.form_data.get("ESR", ""))

            with r1c3:
                st.session_state.form_data["MCHC"] = st.text_input("MCHC", value=st.session_state.form_data.get("MCHC", ""))
                st.session_state.form_data["Platelet Count"] = st.text_input("Platelet Count", value=st.session_state.form_data.get("Platelet Count", ""))
                st.session_state.form_data["RDW"] = st.text_input("RDW", value=st.session_state.form_data.get("RDW", ""))
                st.session_state.form_data["Eosinophil"] = st.text_input("Eosinophil", value=st.session_state.form_data.get("Eosinophil", ""))
                st.session_state.form_data["Basophil"] = st.text_input("Basophil", value=st.session_state.form_data.get("Basophil", ""))

            st.session_state.form_data["Preipheral Blood Smear - RBC Morphology"] = st.text_area("Preipheral Blood Smear - RBC Morphology", value=st.session_state.form_data.get("Preipheral Blood Smear - RBC Morphology", ""))
            st.session_state.form_data["Preipheral Blood Smear - Parasites"] = st.text_area("Preipheral Blood Smear - Parasites", value=st.session_state.form_data.get("Preipheral Blood Smear - Parasites", ""))
            st.session_state.form_data["Preipheral Blood Smear - Others"] = st.text_area("Preipheral Blood Smear - Others", value=st.session_state.form_data.get("Preipheral Blood Smear - Others", ""))

            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])

            with r3c3:
                if st.button("Add Data", type="primary"):

                                    # Prepare data for insertion
                    sql = """
                        INSERT INTO hematology_result (
                            emp_no, entry_date, 
                            heamoglobin, 
                            rbc_count,  
                            wbc_count, 
                            haemotocrit,
                            mcv, 
                            mch, 
                            mchc, 
                            platelet, 
                            rdw, 
                            neutrophil, 
                            lymphocyte, 
                            eosinophil, 
                            monocyte,  
                            basophils, 
                            esr, 
                            pbs_rbc, pbc_parasites, pbc_others, year, hospital
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    data = (
                        st.session_state.form_data["Employee ID"],  # emp_no
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Hemoglobin"],  # heamoglobin, unit
                        st.session_state.form_data["Total RBC"],  # rbc_count, unit
                        st.session_state.form_data["Total WBC"],  # wbc_count, unit
                        st.session_state.form_data["PCV"],  # haemotocrit, unit
                        st.session_state.form_data["MCV"],  # mcv, unit
                        st.session_state.form_data["MCH"],  # mch, unit
                        st.session_state.form_data["MCHC"],  # mchc, unit
                        st.session_state.form_data["Platelet Count"],  # platelet, unit
                        st.session_state.form_data["RDW"],  # rdw, unit
                        st.session_state.form_data["Neutrophil"],  # neutrophil, unit
                        st.session_state.form_data["Lymphocyte"],  # lymphocyte, unit
                        st.session_state.form_data["Eosinophil"],  # eosinophil, unit
                        st.session_state.form_data["Monocyte"],  # monocyte, unit
                        st.session_state.form_data["Basophil"],  # basophils, unit
                        st.session_state.form_data["ESR"],  # esr, unit
                        st.session_state.form_data["Preipheral Blood Smear - RBC Morphology"],  # pbs_rbc
                        st.session_state.form_data["Preipheral Blood Smear - Parasites"],  # pbc_parasites
                        st.session_state.form_data["Preipheral Blood Smear - Others"],  # pbc_others
                        datetime.now().year,  
                        st.session_state.form_data["Reference Type"], 
                    )

                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.success("Data Inserted Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error inserting data: {e}")
        

        if select_inv == "ROUTINE SUGAR TESTS":
            r1c1, r1c2, r1c3 = st.columns(3)
            
            
            
            with r1c1:
                st.session_state.form_data["Glucose (F)"] = st.text_input("Glucose (F)", value=st.session_state.form_data.get("Glucose (F)", ""))
                st.session_state.form_data["Glucose (PP)"] = st.text_input("Glucose (PP)", value=st.session_state.form_data.get("Glucose (PP)", ""))
            
            with r1c2:
                st.session_state.form_data["Random Blood sugar"] = st.text_input("Random Blood sugar", value=st.session_state.form_data.get("Random Blood sugar", ""))
                st.session_state.form_data["Estimated Average Glucose"] = st.text_input("Estimated Average Glucose", value=st.session_state.form_data.get("Estimated Average Glucose", ""))
            
            with r1c3:
                st.session_state.form_data["HbA1c"] = st.text_input("HbA1c", value=st.session_state.form_data.get("HbA1c", ""))
            
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):

                    # Prepare data for insertion
                    sql = """
                        INSERT INTO routine_sugartest (
                            entry_date, emp_no, glucosef, glucosepp, rbs,
                            eag, hba1c, year, hospital, batch
                        ) VALUES (
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s
                        )
                    """
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data['Employee ID'],  # Use the fetched emp_no
                        st.session_state.form_data["Glucose (F)"],  # glucosef
                        st.session_state.form_data["Glucose (PP)"],  # glucosepp
                        st.session_state.form_data["Random Blood sugar"],  # rbs
                        st.session_state.form_data["Estimated Average Glucose"],  # eag
                        st.session_state.form_data["HbA1c"],  # hba1c
                        datetime.now().year,  # year
                        st.session_state.form_data["Reference Type"],  # hospital (replace with actual hospital name)
                        'your_batch'  # batch (replace with actual batch number)
                    )

                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.success("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")

                

        if select_inv == "RENAL FUNCTION TEST & ELECTROLYTES":
            if 'BUN Range' not in st.session_state.form_data:
                st.session_state.form_data['BUN Range'] = ""
            if 'emp_no' not in st.session_state:
                st.session_state.emp_no = st.text_input("Employee No", value="")  # Replace with actual logic to fetch emp_no

            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                st.session_state.form_data["Urea"] = st.text_input("Urea", value=st.session_state.form_data.get("Urea", ""))
                st.session_state.form_data["BUN"] = st.text_input("BUN", value=st.session_state.form_data.get("BUN", ""))
                st.session_state.form_data["Calcium"] = st.text_input("Calcium", value=st.session_state.form_data.get("Calcium", ""))
                
            with r1c2:
                st.session_state.form_data["Serum Creatinine"] = st.text_input("Serum Creatinine", value=st.session_state.form_data.get("Serum Creatinine", ""))
                
                st.session_state.form_data["Uric Acid"] = st.text_input("Uric Acid", value=st.session_state.form_data.get("Uric Acid", ""))
                st.session_state.form_data["Chloride"] = st.text_input("Chloride", value=st.session_state.form_data.get("Chloride", ""))
            with r1c3:
                st.session_state.form_data["Sodium"] = st.text_input("Sodium", value=st.session_state.form_data.get("Sodium", ""))
                
                st.session_state.form_data["Potassium"] = st.text_input("Potassium", value=st.session_state.form_data.get("Potassium", ""))
                st.session_state.form_data["Phosphorus"] = st.text_input("Phosphorus", value=st.session_state.form_data.get("Phosphorus", ""))
            r2c1, r2c2, r2c3 = st.columns(3)
                        

            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare data for insertion
                    sql = """
                        INSERT INTO rft_result (
                            entry_date, emp_no, urea, 
                            bun, 
                            sr_creatinine, 
                            uric_acid, 
                            sodium, 
                            potassium, 
                            calcium, 
                            phosphorus, 
                            chloride, 
                            year, hospital, batch
                        ) VALUES (
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s, %s,
                            %s, %s
                        )
                    """
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Urea"],
                        st.session_state.form_data["BUN"], 
                        st.session_state.form_data["Serum Creatinine"], 
                        st.session_state.form_data["Uric Acid"], 
                        st.session_state.form_data["Sodium"], 
                        st.session_state.form_data["Potassium"], 
                        st.session_state.form_data["Calcium"], 
                        st.session_state.form_data["Phosphorus"], 
                        st.session_state.form_data["Chloride"], 
                        datetime.now().year,  # year
                        st.session_state.form_data["Reference Type"],  # hospital (replace with actual hospital name)
                        'your_batch'  # batch (replace with actual batch number)
                    )

                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")

        
        elif select_inv == "LIPID PROFILE":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Initialize keys if they don't exist
            lipid_keys = [
                "Total Cholesterol",
                "Triglycerides",
                "HDL - Cholesterol",
                "LDL- Cholesterol",
                "CHOL HDL ratio",
                "VLDL -Choleserol",
                "LDL.CHOL/HDL.CHOL Ratio"
            ]
            
            for key in lipid_keys:
                if key not in st.session_state.form_data:
                    st.session_state.form_data[key] = ""

            # Creating input fields
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                st.session_state.form_data["Total Cholesterol"] = st.text_input("Total Cholesterol", value=st.session_state.form_data.get("Total Cholesterol", ""))
                st.session_state.form_data["Triglycerides"] = st.text_input("Triglycerides", value=st.session_state.form_data.get("Triglycerides", ""))
                st.session_state.form_data["HDL - Cholesterol"] = st.text_input("HDL - Cholesterol", value=st.session_state.form_data.get("HDL - Cholesterol", ""))
            with r1c2:
                st.session_state.form_data["LDL- Cholesterol"] = st.text_input("LDL- Cholesterol", value=st.session_state.form_data.get("LDL- Cholesterol", ""))
                st.session_state.form_data["CHOL HDL ratio"] = st.text_input("CHOL HDL ratio", value=st.session_state.form_data.get("CHOL HDL ratio", ""))
            with r1c3:
                st.session_state.form_data["VLDL -Choleserol"] = st.text_input("VLDL -Choleserol", value=st.session_state.form_data.get("VLDL -Choleserol", ""))
                st.session_state.form_data["LDL.CHOL/HDL.CHOL Ratio"] = st.text_input("LDL.CHOL/HDL.CHOL Ratio", value=st.session_state.form_data.get("LDL.CHOL/HDL.CHOL Ratio", ""))

            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO lipid_profile (
                            entry_date, emp_no,
                            tcholesterol, triglycerides,
                            hdl_cholesterol, ldl_cholesterol,
                            chol_hdlratio, vldl_cholesterol,
                            ldlhdlratio
                        ) VALUES (
                            %s, %s,
                            %s, %s,
                            %s, %s,
                            %s, %s,
                            %s
                        )
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Total Cholesterol"],
                        st.session_state.form_data["Triglycerides"],
                        st.session_state.form_data["HDL - Cholesterol"],
                        st.session_state.form_data["LDL- Cholesterol"],
                        st.session_state.form_data["CHOL HDL ratio"],
                        st.session_state.form_data["VLDL -Choleserol"],
                        st.session_state.form_data["LDL.CHOL/HDL.CHOL Ratio"]
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                    
            


        
        elif select_inv == "LIVER FUNCTION TEST":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for liver function test
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                st.session_state.form_data["Bilirubin - Total"] = st.text_input("Bilirubin - Total", value=st.session_state.form_data.get("Bilirubin - Total", ""))
                st.session_state.form_data["Bilirubin - Direct"] = st.text_input("Bilirubin - Direct", value=st.session_state.form_data.get("Bilirubin - Direct", ""))
                st.session_state.form_data["Bilirubin - Indirect"] = st.text_input("Bilirubin - Indirect", value=st.session_state.form_data.get("Bilirubin - Indirect", ""))
                st.session_state.form_data["SGOT /AST"] = st.text_input("SGOT /AST", value=st.session_state.form_data.get("SGOT /AST", ""))
            with r1c2:
                st.session_state.form_data["SGPT /ALT"] = st.text_input("SGPT /ALT", value=st.session_state.form_data.get("SGPT /ALT", ""))
                st.session_state.form_data["Alkaline phosphatase"] = st.text_input("Alkaline phosphatase", value=st.session_state.form_data.get("Alkaline phosphatase", ""))
                st.session_state.form_data["Total Protein"] = st.text_input("Total Protein", value=st.session_state.form_data.get("Total Protein", ""))
                st.session_state.form_data["Albumin (Serum )"] = st.text_input("Albumin (Serum )", value=st.session_state.form_data.get("Albumin (Serum )", ""))
            with r1c3:
                st.session_state.form_data["Globulin(Serum)"] = st.text_input("Globulin(Serum)", value=st.session_state.form_data.get("Globulin(Serum)", ""))
                st.session_state.form_data["Alb/Glob Ratio"] = st.text_input("Alb/Glob Ratio", value=st.session_state.form_data.get("Alb/Glob Ratio", ""))
                st.session_state.form_data["Gamma Glutamyl transferase"] = st.text_input("Gamma Glutamyl transferase", value=st.session_state.form_data.get("Gamma Glutamyl transferase", ""))

            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO liver_function (
                            entry_date, emp_no,
                            bilirubin_total, bilirubin_direct, bilirubin_indirect,
                            sgot_alt, sgpt_alt, alkaline_phosphatase,
                            total_protein, albumin, globulin,
                            alb_globratio, gammagt
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Bilirubin - Total"],
                        st.session_state.form_data["Bilirubin - Direct"],
                        st.session_state.form_data["Bilirubin - Indirect"],
                        st.session_state.form_data["SGOT /AST"],
                        st.session_state.form_data["SGPT /ALT"],
                        st.session_state.form_data["Alkaline phosphatase"],
                        st.session_state.form_data["Total Protein"],
                        st.session_state.form_data["Albumin (Serum )"],
                        st.session_state.form_data["Globulin(Serum)"],
                        st.session_state.form_data["Alb/Glob Ratio"],
                        st.session_state.form_data["Gamma Glutamyl transferase"]
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                    


        
        elif select_inv == "THYROID FUNCTION TEST":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for thyroid function test
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                st.session_state.form_data["T3- Triiodothyroine"] = st.text_input("T3- Triiodothyroine", value=st.session_state.form_data.get("T3- Triiodothyroine", ""))
                st.session_state.form_data["T4 - Thyroxine"] = st.text_input("T4 - Thyroxine", value=st.session_state.form_data.get("T4 - Thyroxine", ""))
            with r1c2:
                st.session_state.form_data["TSH- Thyroid Stimulating Hormone"] = st.text_input("TSH- Thyroid Stimulating Hormone", value=st.session_state.form_data.get("TSH- Thyroid Stimulating Hormone", ""))

            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])

            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO thyroid_function_test (
                            entry_date, emp_no,
                            t3, t4, tsh
                        ) VALUES (%s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["T3- Triiodothyroine"],
                        st.session_state.form_data["T4 - Thyroxine"],
                        st.session_state.form_data["TSH- Thyroid Stimulating Hormone"]
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.success("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                    

            # Displaying the form data
            



        elif select_inv == "AUTOIMMUNE TEST":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for Autoimmune Test
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                st.session_state.form_data["ANA (Antinuclear Antibody)"] = st.text_input("ANA (Antinuclear Antibody)", value=st.session_state.form_data.get("ANA (Antinuclear Antibody)", ""))
                st.session_state.form_data["Anti ds DNA"] = st.text_input("Anti ds DNA", value=st.session_state.form_data.get("Anti ds DNA", ""))
            with r1c2:
                st.session_state.form_data["Rheumatoid factor"] = st.text_input("Rheumatoid factor", value=st.session_state.form_data.get("Rheumatoid factor", ""))
            with r1c3:
                st.session_state.form_data["Anticardiolipin Antibodies (IgG & IgM)"] = st.text_input("Anticardiolipin Antibodies (IgG & IgM)", value=st.session_state.form_data.get("Anticardiolipin Antibodies (IgG & IgM)", ""))

            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])

            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO autoimmune_test (
                            entry_date, emp_no,
                            ana, adna, rheumatoid, anticardiolipin
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["ANA (Antinuclear Antibody)"],
                        st.session_state.form_data["Anti ds DNA"],
                        st.session_state.form_data["Rheumatoid factor"],
                        st.session_state.form_data["Anticardiolipin Antibodies (IgG & IgM)"]
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.success("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                    

            # Displaying the form data
            


        elif select_inv == "COAGULATION TEST":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for Coagulation Test
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                st.session_state.form_data["Prothrombin Time (PT)"] = st.text_input("Prothrombin Time (PT)", value=st.session_state.form_data.get("Prothrombin Time (PT)", ""))
                st.session_state.form_data["PT INR"] = st.text_input("PT INR", value=st.session_state.form_data.get("PT INR", ""))
            with r1c2:
                st.session_state.form_data["Bleeding Time (BT)"] = st.text_input("Bleeding Time (BT)", value=st.session_state.form_data.get("Bleeding Time (BT)", ""))
            with r1c3:
                st.session_state.form_data["Clotting Time (CT)"] = st.text_input("Clotting Time (CT)", value=st.session_state.form_data.get("Clotting Time (CT)", ""))

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO coagulation_test (
                            entry_date, emp_no,
                            pt, ptinr, bt, ct
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Prothrombin Time (PT)"],
                        st.session_state.form_data["PT INR"],
                        st.session_state.form_data["Bleeding Time (BT)"],
                        st.session_state.form_data["Clotting Time (CT)"]
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.success("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                    

            
            


        elif select_inv == "ENZYMES & CARDIAC Profile":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for Enzymes & Cardiac Profile
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                st.session_state.form_data["Acid Phosphatase"] = st.text_input("Acid Phosphatase", value=st.session_state.form_data.get("Acid Phosphatase", ""))
                st.session_state.form_data["Adenosine Deaminase"] = st.text_input("Adenosine Deaminase", value=st.session_state.form_data.get("Adenosine Deaminase", ""))
                st.session_state.form_data["Amylase"] = st.text_input("Amylase", value=st.session_state.form_data.get("Amylase", ""))
                st.session_state.form_data["ECG"] = st.selectbox("ECG", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["ECG"] == "Abnormal":
                    st.session_state.form_data["ECG-Comments"] = st.text_area("ECG-Comments", value=st.session_state.form_data.get("ECG-Comments", ""))
            
            with r1c2:
                st.session_state.form_data["Troponin- T"] = st.text_input("Troponin- T", value=st.session_state.form_data.get("Troponin- T", ""))
                st.session_state.form_data["Troponin- I"] = st.text_input("Troponin- I", value=st.session_state.form_data.get("Troponin- I", ""))
                st.session_state.form_data["CPK - TOTAL"] = st.text_input("CPK - TOTAL", value=st.session_state.form_data.get("CPK - TOTAL", ""))
                st.session_state.form_data["ECHO"] = st.selectbox("ECHO", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["ECHO"] == "Abnormal":
                    st.session_state.form_data["ECHO-Comments"] = st.text_area("ECHO-Comments", value=st.session_state.form_data.get("ECHO-Comments", ""))
            
            with r1c3:
                st.session_state.form_data["Lipase"] = st.text_input("Lipase", value=st.session_state.form_data.get("Lipase", ""))
                st.session_state.form_data["CPK - MB"] = st.text_input("CPK - MB", value=st.session_state.form_data.get("CPK - MB", ""))
                st.session_state.form_data["TMT"] = st.selectbox("TMT", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["TMT"] == "Abnormal":
                    st.session_state.form_data["TMT-Comments"] = st.text_area("TMT-Comments", value=st.session_state.form_data.get("TMT-Comments", ""))

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO enzymes_cardio (
                            entry_date, emp_no,
                            acid_phosphatase, adenosine, amylase,
                            ecg, ecg_comments, troponin_t, troponin_i,
                            cpk_total, echo, echo_comments, lipase,
                            cpk_mb, tmt, tmt_comments
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Acid Phosphatase"],
                        st.session_state.form_data["Adenosine Deaminase"],
                        st.session_state.form_data["Amylase"],
                        st.session_state.form_data["ECG"],
                        st.session_state.form_data.get("ECG-Comments", ""),
                        st.session_state.form_data["Troponin- T"],
                        st.session_state.form_data["Troponin- I"],
                        st.session_state.form_data["CPK - TOTAL"],
                        st.session_state.form_data["ECHO"],
                        st.session_state.form_data.get("ECHO-Comments", ""),
                        st.session_state.form_data["Lipase"],
                        st.session_state.form_data["CPK - MB"],
                        st.session_state.form_data["TMT"],
                        st.session_state.form_data.get("TMT-Comments", "")
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
            



        elif select_inv == "URINE ROUTINE":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for Urine Routine
            r1c1, r1c2, r1c3 = st.columns(3)
            
            with r1c1:
                st.session_state.form_data["Colour"] = st.text_input("Colour", value=st.session_state.form_data.get("Colour", ""))
                st.session_state.form_data["Appearance"] = st.text_input("Appearance", value=st.session_state.form_data.get("Appearance", ""))
                st.session_state.form_data["Reaction (pH)"] = st.text_input("Reaction (pH)", value=st.session_state.form_data.get("Reaction (pH)", ""))
                st.session_state.form_data["Specific gravity"] = st.text_input("Specific gravity", value=st.session_state.form_data.get("Specific gravity", ""))
                st.session_state.form_data["Crystals"] = st.text_input("Crystals", value=st.session_state.form_data.get("Crystals", ""))
                st.session_state.form_data["Bacteria"] = st.text_input("Bacteria", value=st.session_state.form_data.get("Bacteria", ""))

            with r1c2:
                st.session_state.form_data["Protein/Albumin"] = st.text_input("Protein/Albumin", value=st.session_state.form_data.get("Protein/Albumin", ""))
                st.session_state.form_data["Glucose (Urine)"] = st.text_input("Glucose (Urine)", value=st.session_state.form_data.get("Glucose (Urine)", ""))
                st.session_state.form_data["Ketone Bodies"] = st.text_input("Ketone Bodies", value=st.session_state.form_data.get("Ketone Bodies", ""))
                st.session_state.form_data["Urobilinogen"] = st.text_input("Urobilinogen", value=st.session_state.form_data.get("Urobilinogen", ""))
                st.session_state.form_data["Casts"] = st.text_input("Casts", value=st.session_state.form_data.get("Casts", ""))

            with r1c3:
                st.session_state.form_data["Bile Salts"] = st.text_input("Bile Salts", value=st.session_state.form_data.get("Bile Salts", ""))
                st.session_state.form_data["Bile Pigments"] = st.text_input("Bile Pigments", value=st.session_state.form_data.get("Bile Pigments", ""))
                st.session_state.form_data["WBC / Pus cells"] = st.text_input("WBC / Pus cells", value=st.session_state.form_data.get("WBC / Pus cells", ""))
                st.session_state.form_data["Red Blood Cells"] = st.text_input("Red Blood Cells", value=st.session_state.form_data.get("Red Blood Cells", ""))
                st.session_state.form_data["Epithelial cells"] = st.text_input("Epithelial cells", value=st.session_state.form_data.get("Epithelial cells", ""))

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion (add your SQL connection logic)
                    sql = """
                        INSERT INTO urine_routine (
                            entry_date, emp_no,
                            colour, appearance, reaction_ph, specific_gravity,
                            protein_albumin, glucose_urine, ketone_bodies,
                            urobilinogen, casts, bile_salts,
                            bile_pigments, wbc_pus_cells, red_blood_cells,
                            epithelial_cells, crystals, bacteria
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Colour"],
                        st.session_state.form_data["Appearance"],
                        st.session_state.form_data["Reaction (pH)"],
                        st.session_state.form_data["Specific gravity"],
                        st.session_state.form_data["Protein/Albumin"],
                        st.session_state.form_data["Glucose (Urine)"],
                        st.session_state.form_data["Ketone Bodies"],
                        st.session_state.form_data["Urobilinogen"],
                        st.session_state.form_data["Casts"],
                        st.session_state.form_data["Bile Salts"],
                        st.session_state.form_data["Bile Pigments"],
                        st.session_state.form_data["WBC / Pus cells"],
                        st.session_state.form_data["Red Blood Cells"],
                        st.session_state.form_data["Epithelial cells"],
                        st.session_state.form_data["Crystals"],
                        st.session_state.form_data["Bacteria"]
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.success("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                    



        elif select_inv == "SEROLOGY":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for Serology tests
            r1c1, r1c2, r1c3 = st.columns(3)

            with r1c1:
                st.session_state.form_data["Screening For HIV I & II"] = st.text_input("Screening For HIV I & II", value=st.session_state.form_data.get("Screening For HIV I & II", ""))
                st.session_state.form_data["HBsAg"] = st.text_input("HBsAg", value=st.session_state.form_data.get("HBsAg", ""))
                st.session_state.form_data["HCV"] = st.text_input("HCV", value=st.session_state.form_data.get("HCV", ""))

            with r1c2:
                st.session_state.form_data["VDRL"] = st.text_input("VDRL", value=st.session_state.form_data.get("VDRL", ""))
                st.session_state.form_data["Dengue NS1Ag"] = st.text_input("Dengue NS1Ag", value=st.session_state.form_data.get("Dengue NS1Ag", ""))
                st.session_state.form_data["Dengue IgG"] = st.text_input("Dengue IgG", value=st.session_state.form_data.get("Dengue IgG", ""))

            with r1c3:
                st.session_state.form_data["Dengue IgM"] = st.text_input("Dengue IgM", value=st.session_state.form_data.get("Dengue IgM", ""))
                st.session_state.form_data["WIDAL"] = st.text_input("WIDAL", value=st.session_state.form_data.get("WIDAL", ""))

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion (add your SQL connection logic)
                    sql = """
                        INSERT INTO serology_result (
                            entry_date, emp_no,
                            hiv_screening, hbsag, hcv, 
                            vdrl, denguens, dengueigg, 
                            dengueigm, widal
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Screening For HIV I & II"],
                        st.session_state.form_data["HBsAg"],
                        st.session_state.form_data["HCV"],
                        st.session_state.form_data["VDRL"],
                        st.session_state.form_data["Dengue NS1Ag"],
                        st.session_state.form_data["Dengue IgG"],
                        st.session_state.form_data["Dengue IgM"],
                        st.session_state.form_data["WIDAL"]
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                

            # Displaying the form data
            


        elif select_inv == "MOTION":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for Motion tests
            r1c1, r1c2, r1c3 = st.columns(3)

            with r1c1:
                st.session_state.form_data["Colour (Motion)"] = st.text_input("Colour (Motion)", value=st.session_state.form_data.get("Colour (Motion)", ""))
                st.session_state.form_data["Appearance (Motion)"] = st.text_input("Appearance (Motion)", value=st.session_state.form_data.get("Appearance (Motion)", ""))
                st.session_state.form_data["Occult Blood"] = st.text_input("Occult Blood", value=st.session_state.form_data.get("Occult Blood", ""))

            with r1c2:
                st.session_state.form_data["Cyst"] = st.text_input("Cyst", value=st.session_state.form_data.get("Cyst", ""))
                st.session_state.form_data["Mucus"] = st.text_input("Mucus", value=st.session_state.form_data.get("Mucus", ""))
                st.session_state.form_data["Pus Cells"] = st.text_input("Pus Cells", value=st.session_state.form_data.get("Pus Cells", ""))

            with r1c3:
                st.session_state.form_data["Ova"] = st.text_input("Ova", value=st.session_state.form_data.get("Ova", ""))
                st.session_state.form_data["RBCs"] = st.text_input("RBCs", value=st.session_state.form_data.get("RBCs", ""))
                st.session_state.form_data["Others"] = st.text_input("Others", value=st.session_state.form_data.get("Others", ""))

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion (add your SQL connection logic)
                    sql = """
                        INSERT INTO motion (
                            entry_date, emp_no,
                            colour, appearance, occult_blood, 
                            cyst, mucus, pus_cells, 
                            ova, rbcs, others_t
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data['Employee ID'],  # emp_no
                        st.session_state.form_data["Colour (Motion)"],
                        st.session_state.form_data["Appearance (Motion)"],
                        st.session_state.form_data["Occult Blood"],
                        st.session_state.form_data["Cyst"],
                        st.session_state.form_data["Mucus"],
                        st.session_state.form_data["Pus Cells"],
                        st.session_state.form_data["Ova"],
                        st.session_state.form_data["RBCs"],
                        st.session_state.form_data["Others"]
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                  
            


        elif select_inv == "ROUTINE CULTURE & SENSITIVITY TEST":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for Routine Culture & Sensitivity tests
            r1c1, r1c2, r1c3 = st.columns(3)

            with r1c1:
                st.session_state.form_data["Urine"] = st.text_input("Urine", value=st.session_state.form_data.get("Urine", ""))
                st.session_state.form_data["Motion"] = st.text_input("Motion", value=st.session_state.form_data.get("Motion", ""))

            with r1c2:
                st.session_state.form_data["Sputum"] = st.text_input("Sputum", value=st.session_state.form_data.get("Sputum", ""))

            with r1c3:
                st.session_state.form_data["Blood"] = st.text_input("Blood", value=st.session_state.form_data.get("Blood", ""))

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion (add your SQL connection logic)
                    sql = """
                        INSERT INTO routine_culture (
                            entry_date, emp_no,
                            urine, motion, sputum, blood
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Urine"],
                        st.session_state.form_data["Motion"],
                        st.session_state.form_data["Sputum"],
                        st.session_state.form_data["Blood"]
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                    
            


        elif select_inv == "Men's Pack":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input field for PSA (Prostate Specific Antigen)
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                st.session_state.form_data["PSA (Prostate specific Antigen)"] = st.text_input("PSA (Prostate specific Antigen)", 
                    value=st.session_state.form_data.get("PSA (Prostate specific Antigen)", "")
                )

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion (add your SQL connection logic)
                    sql = """
                        INSERT INTO mens_pack (
                            entry_date, emp_no,
                            psa
                        ) VALUES (%s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["PSA (Prostate specific Antigen)"]
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
            

        
        elif select_inv == "Women's Pack":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for Mammogram and PAP Smear
            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                st.session_state.form_data["Mammogram"] = st.selectbox("Mammogram", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["Mammogram"] == "Abnormal":
                    st.session_state.form_data["Mammogram-Comments"] = st.text_area("Mammogram-Comments", 
                        value=st.session_state.form_data.get("Mammogram-Comments", "")
                    )

            with r1c2:
                st.session_state.form_data["PAP Smear"] = st.selectbox("PAP Smear", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["PAP Smear"] == "Abnormal":
                    st.session_state.form_data["PAP Smear-Comments"] = st.text_area("PAP Smear-Comments", 
                        value=st.session_state.form_data.get("PAP Smear-Comments", "")
                    )

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion (add your SQL connection logic)
                    sql = """
                        INSERT INTO womens_pack (
                            entry_date, emp_no,
                            mammogram_nm_ab, mammogram_comment,
                            pap_nm_ab, pap_comment
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Mammogram"],
                        st.session_state.form_data.get("Mammogram-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["PAP Smear"],
                        st.session_state.form_data.get("PAP Smear-Comments", "")  # Comment if Abnormal
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
            


        elif select_inv == "Occupational Profile":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for Audiometry and PFT
            r1c1, r1c2, r1c3 = st.columns(3)

            with r1c1:
                st.session_state.form_data["Audiometry"] = st.selectbox("Audiometry", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["Audiometry"] == "Abnormal":
                    st.session_state.form_data["Audiometry-Comments"] = st.text_area("Audiometry-Comments", 
                        value=st.session_state.form_data.get("Audiometry-Comments", "")
                    )

            with r1c2:
                st.session_state.form_data["PFT"] = st.selectbox("PFT", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["PFT"] == "Abnormal":
                    st.session_state.form_data["PFT-Comments"] = st.text_area("PFT-Comments", 
                        value=st.session_state.form_data.get("PFT-Comments", "")
                    )

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])

            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion (add your SQL connection logic)
                    sql = """
                        INSERT INTO occupational_profile (
                            entry_date, emp_no,
                            audiometry_nm_ab, audiometry_comment,
                            pft_nm_ab, pft_comment
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Audiometry"],
                        st.session_state.form_data.get("Audiometry-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["PFT"],
                        st.session_state.form_data.get("PFT-Comments", "")  # Comment if Abnormal
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")

        
        elif select_inv == "Others TEST":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for Pathology
            r1c1, r1c2, r1c3 = st.columns(3)

            with r1c1:
                st.session_state.form_data["Pathology"] = st.selectbox("Pathology", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["Pathology"] == "Abnormal":
                    st.session_state.form_data["Pathology-Comments"] = st.text_area("Pathology-Comments", 
                        value=st.session_state.form_data.get("Pathology-Comments", "")
                    )

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])

            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO other_tests (
                            entry_date, emp_no,
                            pathology, pathology_comments
                        ) VALUES (%s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Pathology"],
                        st.session_state.form_data.get("Pathology-Comments", "")  # Comment if Abnormal
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")


        elif select_inv == "OPHTHALMIC REPORT":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for Vision and Color Vision
            r1c1, r1c2, r1c3 = st.columns(3)

            with r1c1:
                st.session_state.form_data["Vision"] = st.selectbox("Vision", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["Vision"] == "Abnormal":
                    st.session_state.form_data["Vision-Comments"] = st.text_area("Vision-Comments", 
                        value=st.session_state.form_data.get("Vision-Comments", "")
                    )

            with r1c2:
                st.session_state.form_data["Color Vision"] = st.selectbox("Color Vision", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["Color Vision"] == "Abnormal":
                    st.session_state.form_data["Color Vision-Comments"] = st.text_area("Color Vision-Comments", 
                        value=st.session_state.form_data.get("Color Vision-Comments", "")
                    )

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])

            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO ophthalmic_report (
                            entry_date, emp_no,
                            vision, vision_comments,
                            colourvision, colourvision_comment
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["Vision"],
                        st.session_state.form_data.get("Vision-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["Color Vision"],
                        st.session_state.form_data.get("Color Vision-Comments", "")  # Comment if Abnormal
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                    
            

        
        elif select_inv == "X-RAY":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for X-RAY results
            r1c1, r1c2, r1c3 = st.columns(3)

            with r1c1:
                st.session_state.form_data["X-RAY Chest"] = st.selectbox("X-RAY Chest", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["X-RAY Chest"] == "Abnormal":
                    st.session_state.form_data["X-RAY Chest-Comments"] = st.text_area("X-RAY Chest-Comments", 
                        value=st.session_state.form_data.get("X-RAY Chest-Comments", "")
                    )
                st.session_state.form_data["X-RAY KUB"] = st.selectbox("X-RAY KUB", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["X-RAY KUB"] == "Abnormal":
                    st.session_state.form_data["X-RAY KUB-Comments"] = st.text_area("X-RAY KUB-Comments", 
                        value=st.session_state.form_data.get("X-RAY KUB-Comments", "")
                    )

            with r1c2:
                st.session_state.form_data["X-RAY Spine"] = st.selectbox("X-RAY Spine", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["X-RAY Spine"] == "Abnormal":
                    st.session_state.form_data["X-RAY Spine-Comments"] = st.text_area("X-RAY Spine-Comments", 
                        value=st.session_state.form_data.get("X-RAY Spine-Comments", "")
                    )
                st.session_state.form_data["X-RAY Pelvis"] = st.selectbox("X-RAY Pelvis", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["X-RAY Pelvis"] == "Abnormal":
                    st.session_state.form_data["X-RAY Pelvis-Comments"] = st.text_area("X-RAY Pelvis-Comments", 
                        value=st.session_state.form_data.get("X-RAY Pelvis-Comments", "")
                    )

            with r1c3:
                st.session_state.form_data["X-RAY Abdomen"] = st.selectbox("X-RAY Abdomen", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["X-RAY Abdomen"] == "Abnormal":
                    st.session_state.form_data["X-RAY Abdomen-Comments"] = st.text_area("X-RAY Abdomen-Comments", 
                        value=st.session_state.form_data.get("X-RAY Abdomen-Comments", "")
                    )

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])

            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO x_ray (
                            entry_date, emp_no,
                            chest_nm_ab, chest_comment,
                            kub_nm_ab, kub_comment,
                            spine_nm_ab, spine_comment,
                            pelvis_nm_ab, pelvis_comment,
                            abdomen_nm_ab, abdomen_comment
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["X-RAY Chest"],
                        st.session_state.form_data.get("X-RAY Chest-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["X-RAY KUB"],
                        st.session_state.form_data.get("X-RAY KUB-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["X-RAY Spine"],
                        st.session_state.form_data.get("X-RAY Spine-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["X-RAY Pelvis"],
                        st.session_state.form_data.get("X-RAY Pelvis-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["X-RAY Abdomen"],
                        st.session_state.form_data.get("X-RAY Abdomen-Comments", "")  # Comment if Abnormal
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                    
            

                
        elif select_inv == "USG":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for USG results
            r1c1, r1c2, r1c3 = st.columns(3)

            with r1c1:
                st.session_state.form_data["USG ABDOMEN"] = st.selectbox("USG ABDOMEN", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["USG ABDOMEN"] == "Abnormal":
                    st.session_state.form_data["USG ABDOMEN-Comments"] = st.text_area("USG ABDOMEN-Comments", 
                        value=st.session_state.form_data.get("USG ABDOMEN-Comments", "")
                    )
                st.session_state.form_data["USG KUB"] = st.selectbox("USG KUB", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["USG KUB"] == "Abnormal":
                    st.session_state.form_data["USG KUB-Comments"] = st.text_area("USG KUB-Comments", 
                        value=st.session_state.form_data.get("USG KUB-Comments", "")
                    )

            with r1c2:
                st.session_state.form_data["USG Pelvis"] = st.selectbox("USG Pelvis", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["USG Pelvis"] == "Abnormal":
                    st.session_state.form_data["USG Pelvis-Comments"] = st.text_area("USG Pelvis-Comments", 
                        value=st.session_state.form_data.get("USG Pelvis-Comments", "")
                    )

            with r1c3:
                st.session_state.form_data["USG Neck"] = st.selectbox("USG Neck", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["USG Neck"] == "Abnormal":
                    st.session_state.form_data["USG Neck-Comments"] = st.text_area("USG Neck-Comments", 
                        value=st.session_state.form_data.get("USG Neck-Comments", "")
                    )

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])

            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO usg (
                            entry_date, emp_no,
                            abdomen, abdomen_comments,
                            kub, kub_comments,
                            pelvis, pelvis_comments,
                            neck, neck_comments
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["USG ABDOMEN"],
                        st.session_state.form_data.get("USG ABDOMEN-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["USG KUB"],
                        st.session_state.form_data.get("USG KUB-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["USG Pelvis"],
                        st.session_state.form_data.get("USG Pelvis-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["USG Neck"],
                        st.session_state.form_data.get("USG Neck-Comments", "")  # Comment if Abnormal
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
            

        
        elif select_inv == "CT":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for CT results
            r1c1, r1c2, r1c3 = st.columns(3)

            with r1c1:
                st.session_state.form_data["CT Brain"] = st.selectbox("CT Brain", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["CT Brain"] == "Abnormal":
                    st.session_state.form_data["CT Brain-Comments"] = st.text_area("CT Brain-Comments", 
                        value=st.session_state.form_data.get("CT Brain-Comments", "")
                    )
                st.session_state.form_data["CT Lungs"] = st.selectbox("CT Lungs", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["CT Lungs"] == "Abnormal":
                    st.session_state.form_data["CT Lungs-Comments"] = st.text_area("CT Lungs-Comments", 
                        value=st.session_state.form_data.get("CT Lungs-Comments", "")
                    )

            with r1c2:
                st.session_state.form_data["CT Abdomen"] = st.selectbox("CT Abdomen", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["CT Abdomen"] == "Abnormal":  
                    st.session_state.form_data["CT Abdomen-Comments"] = st.text_area("CT Abdomen-Comments", 
                        value=st.session_state.form_data.get("CT Abdomen-Comments", "")
                    )
                st.session_state.form_data["CT Spine"] = st.selectbox("CT Spine", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["CT Spine"] == "Abnormal":
                    st.session_state.form_data["CT Spine-Comments"] = st.text_area("CT Spine-Comments", 
                        value=st.session_state.form_data.get("CT Spine-Comments", "")
                    )

            with r1c3:
                st.session_state.form_data["CT Pelvis"] = st.selectbox("CT Pelvis", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["CT Pelvis"] == "Abnormal":
                    st.session_state.form_data["CT Pelvis-Comments"] = st.text_area("CT Pelvis-Comments", 
                        value=st.session_state.form_data.get("CT Pelvis-Comments", "")
                    )

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])
            
            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO ct_report (
                            entry_date, emp_no,
                            brain, brain_comment,
                            ct_lungs, ct_lungs_comment,
                            abdomen, abdomen_comment,
                            spine, spine_comment,
                            pelvis, pelvis_comment
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["CT Brain"],
                        st.session_state.form_data.get("CT Brain-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["CT Lungs"],
                        st.session_state.form_data.get("CT Lungs-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["CT Abdomen"],
                        st.session_state.form_data.get("CT Abdomen-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["CT Spine"],
                        st.session_state.form_data.get("CT Spine-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["CT Pelvis"],
                        st.session_state.form_data.get("CT Pelvis-Comments", "")  # Comment if Abnormal
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                    
            

        
        elif select_inv == "MRI":
            # Ensure the form_data is initialized
            if 'form_data' not in st.session_state:
                st.session_state.form_data = {}

            # Creating input fields for MRI results
            r1c1, r1c2, r1c3 = st.columns(3)

            with r1c1:
                st.session_state.form_data["MRI Brain"] = st.selectbox("MRI Brain", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["MRI Brain"] == "Abnormal":
                    st.session_state.form_data["MRI Brain-Comments"] = st.text_area("MRI Brain-Comments", 
                        value=st.session_state.form_data.get("MRI Brain-Comments", "")
                    )
                st.session_state.form_data["MRI Lungs"] = st.selectbox("MRI Lungs", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["MRI Lungs"] == "Abnormal":
                    st.session_state.form_data["MRI Lungs-Comments"] = st.text_area("MRI Lungs-Comments", 
                        value=st.session_state.form_data.get("MRI Lungs-Comments", "")
                    )

            with r1c2:
                st.session_state.form_data["MRI Abdomen"] = st.selectbox("MRI Abdomen", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["MRI Abdomen"] == "Abnormal":
                    st.session_state.form_data["MRI Abdomen-Comments"] = st.text_area("MRI Abdomen-Comments", 
                        value=st.session_state.form_data.get("MRI Abdomen-Comments", "")
                    )
                st.session_state.form_data["MRI Spine"] = st.selectbox("MRI Spine", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["MRI Spine"] == "Abnormal":
                    st.session_state.form_data["MRI Spine-Comments"] = st.text_area("MRI Spine-Comments", 
                        value=st.session_state.form_data.get("MRI Spine-Comments", "")
                    )

            with r1c3:
                st.session_state.form_data["MRI Pelvis"] = st.selectbox("MRI Pelvis", ["Normal", "Abnormal"], index=0)
                if st.session_state.form_data["MRI Pelvis"] == "Abnormal":
                    st.session_state.form_data["MRI Pelvis-Comments"] = st.text_area("MRI Pelvis-Comments", 
                        value=st.session_state.form_data.get("MRI Pelvis-Comments", "")
                    )

            # Save button layout
            r3c1, r3c2, r3c3 = st.columns([6, 4, 4])

            with r3c3:
                if st.button("Add Data", type="primary"):
                    # Prepare SQL insertion
                    sql = """
                        INSERT INTO mri (
                            entry_date, emp_no,
                            brain, brain_comments,
                            mri_lungs, mri_lungs_comments,
                            abdomen, abdomen_comments,
                            spine, spine_comments,
                            pelvis, pelvis_comments
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    data = (
                        datetime.now().date(),  # entry_date
                        st.session_state.form_data["Employee ID"],  # emp_no
                        st.session_state.form_data["MRI Brain"],
                        st.session_state.form_data.get("MRI Brain-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["MRI Lungs"],
                        st.session_state.form_data.get("MRI Lungs-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["MRI Abdomen"],
                        st.session_state.form_data.get("MRI Abdomen-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["MRI Spine"],
                        st.session_state.form_data.get("MRI Spine-Comments", ""),  # Comment if Abnormal
                        st.session_state.form_data["MRI Pelvis"],
                        st.session_state.form_data.get("MRI Pelvis-Comments", "")  # Comment if Abnormal
                    )

                    # Assuming you have already established a connection
                    try:
                        cursor.execute(sql, data)
                        connection.commit()
                        st.write("Data Saved Successfully")
                    except mysql.connector.Error as e:
                        st.write(f"Error saving data: {e}")
                    
            

        
    elif form_name == "Fitness":
        st.header("Fitness")

        # Multiselect for fitness options
        st.session_state.form_data["Fitness"] = st.multiselect(
            "Fitness", 
            ["Fit to Join", "Unfit", "Conditional Fit", "Fitness Res. Duty", "Fitness with conditional", 
            "Height Work", "Confined Space", "Gasline", "SCBA", "Fire Rescue"]
        )

        # Fitness comments
        st.session_state.form_data["Fitness-Comments"] = st.text_area(
            "Fitness-Comments", 
            value=st.session_state.form_data.get("Fitness-Comments", "")
        )

        # Layout for Add Data button
        r3c1, r3c2, r3c3 = st.columns([6, 4, 4])

        with r3c3:
            if st.button("Add Data", type="primary"):
                # Collect form data
                patient_id = st.session_state.form_data.get("Employee ID")  # Assuming you have Employee ID from the earlier form
                fitness_status = ", ".join(st.session_state.form_data["Fitness"])  # Join selected fitness options
                fitness_comments = st.session_state.form_data["Fitness-Comments"]

                # Insert the data into the MySQL fitness table
                insert_query = f"""
                INSERT INTO fitness (PatientID, Status, comments, emp_no)
                VALUES ('{patient_id}', '{fitness_status}', '{fitness_comments}', '{emp_no}')
                """

                try:
                    # Execute the insert query
                    cursor.execute(insert_query)
                    connection.commit()  # Ensure to commit the transaction
                    st.success("Data Saved Successfully")
                except Exception as e:
                    st.error(f"Error saving data: {str(e)}")
        

        
    elif form_name == "Consultation":
        st.header("Consultation")

        # Reason for visit
        if(visitreason == "Annual / Periodic" or visitreason == "Periodic (FH)"):
            st.session_state.form_data["Remarks"] = st.text_area("Remarks", value=st.session_state.form_data.get("Remarks", ""))
            st.file_uploader("Upload Self Declaration", type=['xlsx'], key="Self-declaration")
            st.file_uploader("Upload Reports", type=['xlsx'], key="Reports")
        elif(visitreason in ["Camps (Mandatory)", "Camps (Optional)", "Illness", "Follow up Visits", "BP Sugar (Abnormal)", "Injury Outside the premises"]):
            st.session_state.form_data["Remarks"] = st.text_area("Remarks", value=st.session_state.form_data.get("Remarks", ""))
            st.file_uploader("Upload Reports", type=['xlsx'], key="Reports")
            if(select1 == "Unhealthy" and visitreason in ["Illness", "Follow up Visits", "BP Sugar (Abnormal)", "Injury Outside the premises"]):
                st.session_state.form_data["Diagnosis"] = st.text_area("Diagnosis", value=st.session_state.form_data.get("Diagnosis", ""))
                st.session_state.form_data["Complaints"] = st.text_area("Complaints", value=st.session_state.form_data.get("Complaints", ""))
        elif(select1 == "Unhealthy" and visitreason in ["Over counter Illness", "Over counter Injury"]):
            st.session_state.form_data["Diagnosis"] = st.text_area("Diagnosis", value=st.session_state.form_data.get("Diagnosis", ""))
            st.session_state.form_data["Complaints"] = st.text_area("Complaints", value=st.session_state.form_data.get("Complaints", ""))        
        elif(visitreason in ["Special Work Fitness", "Special Work Fitness (Renewal)"]):
            st.file_uploader("Upload Self Declaration", type=['xlsx'], key="Self-declaration")
        elif(visitreason == "Fitness After Medical Leave"):
            st.file_uploader("Upload Self Declaration", type=['xlsx'], key="Self-declaration")
            st.file_uploader("Upload FC External", type=['xlsx'], key="FC-external")
            st.file_uploader("Upload Reports", type=['xlsx'], key="Reports")
        elif(visitreason == "Over counter Injury Outside the premises" or (visitreason == None and select1 == "Unhealthy")):
            st.session_state.form_data["Remarks"] = st.text_area("Remarks", value=st.session_state.form_data.get("Remarks", ""))
            st.session_state.form_data["Diagnosis"] = st.text_area("Diagnosis", value=st.session_state.form_data.get("Diagnosis", ""))
            st.session_state.form_data["Complaints"] = st.text_area("Complaints", value=st.session_state.form_data.get("Complaints", ""))

        else:
            st.session_state.form_data["Remarks"] = st.text_area("Remarks", value=st.session_state.form_data.get("Remarks", ""))
            st.file_uploader("Upload Self Declaration", type=['xlsx'], key="Self-declaration")
            st.file_uploader("Upload FC External", type=['xlsx'], key="FC-external")
            st.file_uploader("Upload Reports", type=['xlsx'], key="Reports")

        # Dropdown for Submitted By and Assign Doctor
        st.write("""
            <div style='float:right;marin-right:100px;margin-top:25px'>
            <label for="doctor">Submitted By:</label>
            <select style='height:35px;width:100px;text-align:center;background-color:rgb(240,242,246);border:none;border-radius:5px;' name="doctor" id="doctor">
                <option value="SK">SK</option>
                <option value="Nurse">Nurse</option>
            </select>
            <label for="doctor">Assign Doctor:</label>
            <select style='height:35px;width:100px;text-align:center;background-color:rgb(240,242,246);border:none;border-radius:5px;' name="doctor" id="doctor">
                <option value="SK">SK</option>
                <option value="Nurse">Nurse</option>
            </select>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Submit", type="primary"):
            # Collect form data
            emp_no = st.session_state.form_data.get("Employee ID")  # Assuming Employee ID was collected earlier
            complaints = st.session_state.form_data.get("Complaints", "")
            diagnosis = st.session_state.form_data.get("Diagnosis", "")
            remarks = st.session_state.form_data.get("Remarks", "")
            
            # Construct the SQL query to insert data into the consultation table
            insert_query = f"""
            INSERT INTO consultation (emp_no, entry_date, complaints, diagnosis, remarks)
            VALUES ('{emp_no}', CURDATE(), '{complaints}', '{diagnosis}', '{remarks}')
            """

            try:
                # Execute the query
                cursor.execute(insert_query)
                connection.commit()  # Commit transaction
                st.success("Consultation Data Saved Successfully")
            except Exception as e:
                st.error(f"Error saving consultation data: {str(e)}")
            finally:
                st.rerun()  # Rerun the app to reset the state

        


    elif form_name == "Medical History":
        st.header("Medical History")
        
        # Personal History -> multi select box
        #     Smoker
        #     Alcoholic
        #     Veg
        #     Mixed Diet
        # Medical History - multi select box
        #     BP
        #     DM
        #     Others
        # Surgical History -> header
        #     Family History -> sub header
        #         Father    -> text_area
        #         Mother    -> text_area

        st.session_state.form_data["Personal History"] = st.multiselect("Personal History", ["Smoker", "Alcoholic", "Veg", "Mixed Diet"])
        st.session_state.form_data["Medical History"] = st.multiselect("Medical History", ["BP", "DM", "Others"])
        
        st.header("Surgical History")

        st.text_area("comments", value = st.session_state.form_data["Surgical History"])
        
        st.markdown("<h3 style='margin-left:30px;'> Family History </h3>", unsafe_allow_html=True)


        r1c1, r1c2, r1c3 = st.columns([1,6,2])

        with r1c2:
            st.session_state.form_data["Father"] = st.text_area("Father",value=st.session_state.form_data.get("Father", ""))
            st.session_state.form_data["Mother"] = st.text_area("Mother",value=st.session_state.form_data.get("Mother", ""))

        r3c1,r3c2,r3c3 = st.columns([6,4,4])
        
        
        with r3c3:
            if st.button("Add Data", type="primary"):
                st.write("Data Saved")
                st.session_state.form_data["visitreason"] = visitreason
                st.rerun()
            if st.button("Submit", type = "primary"):
                i = st.session_state.form_data # MARK: Data Insert
                try:
                    insert_basicdetails = ("INSERT INTO basic_details (emp_no, entry_date, PatientAge, PatientName, Gender, Department, Work, MobileNo, BloodGroup, Vaccinated, Address) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                    basicdetails_data = (i.get("Employee ID"), i.get("Visit Date"), i.get("Employee Age"), i.get("Employee Name"), i.get("Gender"), i.get("Department"), i.get("Work"),i.get("Mobile No."), i.get("Blood Group"), i.get("Vaccination Status"), i.get("Address"))
                    cursor.execute(insert_basicdetails, basicdetails_data)
                    connection.commit()
                except Exception as e:
                    st.write(e)
                    st.write("Error in basic details")


                try:
                    insert_vitals = ("INSERT INTO vitals(emp_no, entry_date, Systolic, Diastolic, PulseRate, SpO2, Temperature, RespiratoryRate, Height, Weight, BMI) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)") 
                    vitals_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Systolic"), i.get("Diastolic"), i.get("Pulse"), i.get("spo2"), i.get("Temperature"), i.get("Respiratory Rate"), i.get("Height"), i.get("Weight"), i.get("BMI"))
                    cursor.execute(insert_vitals, vitals_values)
                    connection.commit()
                    st.write("Vitals Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in vitals")

                
                try:
                    insert_hematology = ("INSERT INTO hematology_result(emp_no, entry_date, heamoglobin,  rbc_count, wbc_count, haemotocrit, mcv, mch, mchc, platelet, rdw, neutrophil, lymphocyte, eosinophil, monocyte, basophils, esr, pbs_rbc, pbc_parasites, pbc_others) VALUES(%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)")
                    hematology_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Hemoglobin"), i.get("Total RBC"), i.get("Total WBC"), i.get("PCV"), i.get("MCV"), i.get("MCH"), i.get("MCHC"), i.get("Platelet Count"), i.get("RDW"), i.get("Neutrophil"), i.get("Lymphocyte"), i.get("Eosinophil"), i.get("Monocyte"), i.get("Basophil"), i.get("ESR"), i.get("Preipheral Blood Smear - RBC Morphology"), i.get("Preipheral Blood Smear - Parasites"), i.get("Preipheral Blood Smear - Others"))
                    cursor.execute(insert_hematology, hematology_values)
                    connection.commit()
                    st.write("Hematology Inserted")

                except Exception as e:
                    st.write(e)
                    st.write("Error in hematology")

                try:
                    insert_rst = ("INSERT INTO routine_sugartest(emp_no, entry_date, glucosef, glucosepp, rbs, eag, hba1c) VALUES(%s, %s, %s, %s, %s, %s, %s)")
                    rst_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Glucose (F)"), i.get("Glucose (PP)"), i.get("Random Blood sugar"), i.get("Estimated Average Glucose"), i.get("HbA1c"))
                    cursor.execute(insert_rst, rst_values)
                    connection.commit()
                    st.write("Data Submitted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in rst")

                try:
                    insert_rft = ("INSERT INTO rft_result(entry_date, emp_no, urea, bun, sr_creatinine, uric_acid, sodium, potassium, calcium, phosphorus, chloride, bicarbonate ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                    rft_values = (i.get("Visit Date"), i.get("Employee ID"), i.get("Urea"), i.get("Blood urea nitrogen (BUN)"), i.get("Sr.Creatinine"), i.get("Uric acid"), i.get("Sodium"), i.get("Potassium"), i.get("Calcium"), i.get("Phosphorus"), i.get("Chloride"), i.get("Bicarbonate"))                    
                    cursor.execute(insert_rft, rft_values)
                    connection.commit()
                    st.write("RFT Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in rft")

                    
                try:
                    insert_lipid_prof = ("INSERT INTO lipid_profile(emp_no, entry_date, tcholesterol,triglycerides, hdl_cholesterol, vldl_cholesterol, ldl_cholesterol, chol_hdlratio, ldlhdlratio) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)")
                    lipid_prof_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Total Cholesterol"), i.get("Triglycerides"), i.get("HDL - Cholesterol"), i.get("VLDL -Choleserol"), i.get("LDL- Cholesterol"), i.get("CHOL HDL ratio"), i.get("LDL.CHOL/HDL.CHOL Ratio"))                    
                    cursor.execute(insert_lipid_prof, lipid_prof_values)
                    connection.commit()
                    st.write("Lipid Profile Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in lipid profile")

                try:
                    insert_lft = ("INSERT INTO liver_function(emp_no, entry_date, bilirubin_total, bilirubin_direct, bilirubin_indirect, sgot_alt, sgpt_alt, alkaline_phosphatase, total_protein, albumin, globulin, alb_globratio, gammagt) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ")
                    lft_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Bilirubin - Total"), i.get("Bilirubin - Direct"), i.get("Bilirubin - Indirect"), i.get("SGOT /AST"), i.get("SGPT /ALT"), i.get("Alkaline phosphatase"), i.get("Total Protein"), i.get("Albumin (Serum )"), i.get("Globulin(Serum)"), i.get("Alb/Glob Ratio"), i.get("Gamma Glutamyl transferase"))                    
                    cursor.execute(insert_lft, lft_values)
                    connection.commit()
                    st.write("LFT Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in lft")
                
                try:
                    insert_tft = ("INSERT INTO thyroid_function_test(emp_no, entry_date, t3, t4, tsh) VALUES(%s, %s, %s, %s, %s)")
                    tft_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("T3- Triiodothyroine"), i.get("T4 - Thyroxine"), i.get("TSH- Thyroid Stimulating Hormone"))                    
                    cursor.execute(insert_tft, tft_values)
                    connection.commit()
                    st.write("TFT Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in tft")

                try:
                    insert_ait = ("INSERT INTO autoimmune_test(emp_no, entry_date, ana, adna, anticardiolipin, rheumatoid) VALUES(%s, %s, %s, %s, %s, %s)")
                    ait_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("ANA (Antinuclear Antibody)"), i.get("Anti ds DNA"), i.get("Anticardiolipin Antibodies (IgG & IgM)"), i.get("Rheumatoid factor"))
                    cursor.execute(insert_ait, ait_values)
                    connection.commit()
                    st.write("AIT Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in ait")

                try:
                    insert_coagulation = ("INSERT INTO coagulation_test(emp_no, entry_date, pt, ptinr, bt, ct) VALUES(%s, %s, %s, %s, %s, %s)")
                    coagulation_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Prothrombin Time (PT)"), i.get("PT INR"), i.get("Bleeding Time (BT)"), i.get("Clotting Time (CT)"))
                    cursor.execute(insert_coagulation, coagulation_values)
                    connection.commit()
                    st.write("Coagulation Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in coagulation")

                try:
                    insert_enzymes_cardio = ("INSERT INTO enzymes_cardio(emp_no, entry_date,acid_phosphatase,adenosine,amylase,lipase,troponin_t, troponin_i, cpk_total, cpk_mb, ecg, ecg_comments, echo,echo_comments, tmt, tmt_comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                    enzymes_cardio_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Acid Phosphatase"), i.get("Adenosine Deaminase"), i.get("Amylase"), i.get("Lipase"), i.get("Troponin- T"), i.get("Troponin- I"), i.get("CPK - Total"), i.get("CPK - MB"), i.get("ECG"), i.get("ECG-Comments"), i.get("ECHO"), i.get("ECHO-Comments"), i.get("TMT"), i.get("TMT-Comments"))
                    cursor.execute(insert_enzymes_cardio, enzymes_cardio_values)
                    connection.commit()
                    st.write("Enzymes Cardio Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in enzymes cardio")
                
                try:
                    insert_urine_routine = ("INSERT INTO urine_routine(emp_no, entry_date, colour, apperance, reaction, specific_gravity, protein_albumin, glucose, ketone, urobilinogen, bile_salts, bile_pigments, wbc_pluscells, rbc, epithelial_cell, casts, crystals, bacteria) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                    urine_routine_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Colour"), i.get("Appearance"), i.get("Reaction (pH)"), i.get("Specific Gravity"), i.get("Protein/Albumin"), i.get("Glucose (Urine)"), i.get("Ketone Bodies"), i.get("Urobilinogen"), i.get("Bile Salts"), i.get("Bile Pigments"), i.get("WBC / Pus cells"), i.get("Red Blood Cells"), i.get("Epithelial celss"), i.get("Casts"), i.get("Crystals"), i.get("Bacteria"))
                    cursor.execute(insert_urine_routine, urine_routine_values)
                    connection.commit()
                    st.write("Urine Routine Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in urine routine")

                try:
                    insert_serology = ("INSERT INTO serology_result(emp_no, entry_date, hiv_screening , hbsag, hcv, widal, vdrl, denguens, dengueigg, dengueigm) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                    serology_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Screening For HIV I & II"), i.get("HBsAg"), i.get("HCV"), i.get("WIDAL"), i.get("VDRL"), i.get("Dengue NS1Ag"), i.get("Dengue IgG"), i.get("Dengue IgM"))
                    cursor.execute(insert_serology, serology_values)
                    connection.commit()
                    st.write("Serology Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in serology")

                try:
                    insert_motion = ("INSERT INTO motion(emp_no, entry_date, colour, appearance, occult_blood, ova, cyst, mucus, pus_cells, rbcs, others_t) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                    motion_values = (i.get("Employee ID"), i.get("Visi Date"), i.get("Colour (Motion)"), i.get("Appearance (Motion)"), i.get("Occult Blood"), i.get("Ova"), i.get("Cyst"), i.get("Mucus"), i.get("Pus Cells"), i.get("RBCs"), i.get("Others"))
                    cursor.execute(insert_motion, motion_values)
                    connection.commit()
                    st.write("Motion Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in motion")

                try:
                    insert_routie_culture = ("INSERT INTO routine_culture(emp_no, entry_date, urine, motion, sputum, blood) VALUES( %s, %s, %s, %s, %s, %s)")
                    routine_culture_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Urine"), i.get("Motion"), i.get("Sputum"), i.get("Blood"))
                    cursor.execute(insert_routie_culture, routine_culture_values)
                    connection.commit()
                    st.write("Routine Culture Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in routine culture")

                try:
                    insert_mens_pack = ("INSERT INTO mens_pack(emp_no, entry_date, psa) VALUES(%s, %s, %s)")
                    mens_pack_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("PSA (Prostate specific Antigen)"))
                    cursor.execute(insert_mens_pack, mens_pack_values)
                    connection.commit()
                    st.write("Mens Pack Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in mens pack")
                
                try:
                    insert_womens_pack = ("INSERT INTO womens_pack(emp_no, entry_date, mammogram_nm_ab, mammogram_comment, pap_nm_ab, pap_comment) VALUES(%s, %s, %s, %s, %s, %s)")
                    womens_pack_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Mammogram"), i.get("Mammogram-Comments"), i.get("PAP Smear"), i.get("PAP Smear-Comments"))
                    cursor.execute(insert_womens_pack, womens_pack_values)
                    connection.commit()
                    st.write("Womens Pack Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in womens pack")

                try:
                    insert_occupational_profile = ("INSERT INTO occupational_profile(emp_no, entry_date, audiometry_nm_ab, audiometry_comment, pft_nm_ab, pft_comment) VALUES(%s, %s, %s, %s, %s, %s)")
                    occupational_profile_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Audiometry"), i.get("Audiometry-Comments"), i.get("PFT"), i.get("PFT-Comments"))
                    cursor.execute(insert_occupational_profile, occupational_profile_values)
                    connection.commit()
                    st.write("Occupational Profile Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in occupational profile")
                

                try:
                    insert_other_test = ("INSERT INTO other_tests(emp_no, entry_date, pathology, pathology_comments) VALUES(%s, %s, %s, %s)")
                    other_test_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Pathology"), i.get("Pathology-Comments"))
                    cursor.execute(insert_other_test, other_test_values)
                    connection.commit()
                    st.write("Other Test Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in other test")

                try:
                    insert_ophthalmic_report = ("INSERT INTO ophthalmic_report(emp_no, entry_date, vision, vision_comments, colourvision, colourvision_comment) VALUES(%s, %s, %s, %s, %s, %s)")
                    ophthalmic_report_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Vision"), i.get("Vision-Comments"), i.get("Colour Vision"), i.get("Colour Vision-Comments"))
                    cursor.execute(insert_ophthalmic_report, ophthalmic_report_values)
                    connection.commit()
                    st.write("Ophthalmic Report Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in ophthalmic report")

                try:
                    insert_x_ray = ("INSERT INTO x_ray(emp_no, entry_date, chest_nm_ab, chest_comment, spine_nm_ab, spine_comment, abdomen_nm_ab, abdomen_comment, kub_nm_ab, kub_comment, pelvis_nm_ab, pelvis_comment) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                    x_ray_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("X-RAY Chest"), i.get("X-RAY Chest-Comments"), i.get("X-RAY Spine"), i.get("X-RAY Spine-Comments"), i.get("X-RAY Abdomen"), i.get("X-RAY Abdomen-Comments"), i.get("X-RAY KUB"), i.get("X-RAY KUB-Comments"), i.get("X-RAY Pelvis"), i.get("X-RAY Pelvis-Comments"))
                    cursor.execute(insert_x_ray, x_ray_values)
                    connection.commit()
                    st.write("X-Ray Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in x-ray")
                
                try:
                    insert_usg = ("INSERT INTO usg(emp_no, entry_date, abdomen, abdomen_comments, pelvis, pelvis_comments,neck, neck_comments, kub, kub_comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                    usg_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("USG ABDOMEN"), i.get("USG ABDOMEN-Comments"), i.get("USG Pelvis"), i.get("USG Pelvis-Comments"), i.get("USG Neck"), i.get("USG Neck-Comments"), i.get("USG KUB"), i.get("USG KUB-Comments"))
                    cursor.execute(insert_usg, usg_values)
                    connection.commit()
                    st.write("USG Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in usg")
                
                try:
                    insert_ct_report = ("INSERT INTO ct_report(emp_no, entry_date, brain, brain_comment, abdomen, abdomen_comment, pelvis, pelvis_comment, ct_lungs, ct_lungs_comment, spine, spine_comment) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                    ct_report_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("CT Brain"), i.get("CT Brain-Comments"), i.get("CT Abdomen"), i.get("CT Abdomen-Comments"), i.get("CT Pelvis"), i.get("CT Pelvis-Comments"), i.get("CT Lungs"), i.get("CT Lungs-Comments"), i.get("CT Spine"), i.get("CT Spine-Comments"))
                    cursor.execute(insert_ct_report, ct_report_values)
                    connection.commit()
                    st.write("CT Report Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in ct report")

                try:
                    insert_mri_report = ("INSERT INTO mri(emp_no, entry_date, brain, brain_comments, abdomen, abdomen_comments, pelvis, pelvis_comments, mri_lungs, mri_lungs_comments, spine, spine_comments) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                    mri_report_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("MRI Brain"), i.get("MRI Brain-Comments"), i.get("MRI Abdomen"), i.get("MRI Abdomen-Comments"), i.get("MRI Pelvis"), i.get("MRI Pelvis-Comments"), i.get("MRI Lungs"), i.get("MRI Lungs-Comments"), i.get("MRI Spine"), i.get("MRI Spine-Comments"))
                    cursor.execute(insert_mri_report, mri_report_values)
                    connection.commit()
                    st.write("MRI Report Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in mri report")
                
                try:
                    insert_consultation = ("INSERT INTO consultation(emp_no, entry_date, complaints, diagnosis, remarks) VALUES(%s, %s, %s, %s, %s)")
                    consultation_values = (i.get("Employee ID"), i.get("Visit Date"), i.get("Complaints"), i.get("Diagnosis"), i.get("Remarks"))
                    cursor.execute(insert_consultation, consultation_values)
                    connection.commit()
                    st.write("Consultation Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in consultation")

                try:
                    insert_medical_history = ("INSERT INTO medicalpersonalhist(emp_no, entry_date, personal_history, medical_history, father, mother) VALUES(%s, %s, %s, %s, %s, %s)")
                    medical_history_values = (i.get("Employee ID"), i.get("Visit Date"), json.dumps(i.get("Personal History")), json.dumps(i.get("Medical History")), i.get("Father"), i.get("Mother"))
                    cursor.execute(insert_medical_history, medical_history_values)
                    connection.commit()
                    st.write("Medical History Inserted")
                except Exception as e:
                    st.write(e)
                    st.write("Error in medical history")

                    
        

    if form_name == "Prescription":
        def get_medicines_by_category(connection, category):
            cursor = connection.cursor()
            query = "SELECT medicine_name FROM pharmacy_inventory WHERE category = %s"
            cursor.execute(query, (category,))
            result = cursor.fetchall()
            cursor.close()
            # Flatten the result and return a list of medicine names
            return [row[0] for row in result]
        def reduce_medicine_quantity(connection, medicine_name, quantity):
            cursor = connection.cursor()
            # Debug information
            print(f"Trying to reduce quantity for {medicine_name} by {quantity}")
            
            # Update quantity
            query = "UPDATE pharmacy_inventory SET quantity = quantity - %s WHERE medicine_name = %s AND quantity >= %s"
            cursor.execute(query, (quantity, medicine_name, quantity))
            connection.commit()
        # Check if rows were affected (if the quantity is reduced)
        if cursor.rowcount == 0:
            print(f"Medicine {medicine_name} does not have enough stock or does not exist")
        cursor.close()
    # In the elif block (as described earlier)
        if form_name == "Prescription":
            
            tablets = get_medicines_by_category(connection, "Tablets")
            injections = get_medicines_by_category(connection, "Injection")
            creams = get_medicines_by_category(connection, "Creams")
            others = get_medicines_by_category(connection, "Other")

            tablets = get_medicines_by_category(connection, "Tablets")
            injections = get_medicines_by_category(connection, "Injection")
            creams = get_medicines_by_category(connection, "Creams")
            others = get_medicines_by_category(connection, "Other")

        st.header("Prescription")

        st.write("""
            <style>
                button[kind="primary"] {
                    all: unset;
                    background-color: #22384F;
                    color: white;
                    border-radius: 5px;
                    text-align: center;
                    cursor: pointer;
                    font-size: 20px;
                    width: 10%;
                    padding: 10px;
                    margin-left:1000px;
                }
            </style>
        """, unsafe_allow_html=True)

        # Tablets Section
        st.subheader("Tablets")
        c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 2])
        with c1:
            tablet1 = st.selectbox("Name of the Drug", tablets, index=None, key="tablet1")
            tablet2 = st.selectbox("Name of the Drug", tablets, index=None, key="tablet2")
        with c2:
            qty1 = st.text_input("Qty", key="qty1")
            qty2 = st.text_input("Qtys", key="qty2")

        if st.button("Add Tablets", type='primary'):
            try:
                qty1 = int(qty1)
                qty2 = int(qty2)
                reduce_medicine_quantity(connection, tablet1, qty1)
                reduce_medicine_quantity(connection, tablet2, qty2)
                st.success(f"{tablet1} and {tablet2} quantities updated successfully!")
            except ValueError:
                st.error("Please enter valid quantities.")

        # Injections Section
        st.subheader("Injections")
        c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 2])
        with c1:
            injection1 = st.selectbox("Name of the Drug", injections, index=None, key="injection1")
            injection2 = st.selectbox("Name of the Drug", injections, index=None, key="injection2")
        with c2:
            qty3 = st.text_input("Qty", key="qty3")
            qty4 = st.text_input("Qtys", key="qty4")

        if st.button("Add Injections", type="primary"):
            try:
                qty3 = int(qty3)
                qty4 = int(qty4)
                reduce_medicine_quantity(connection, injection1, qty3)
                reduce_medicine_quantity(connection, injection2, qty4)
                st.success(f"{injection1} and {injection2} quantities updated successfully!")
            except ValueError:
                st.error("Please enter valid quantities.")

        # Creams Section
        st.subheader("Creams")
        c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 2])
        with c1:
            cream1 = st.selectbox("Name of the Drug", creams, index=None, key="cream1")
            cream2 = st.selectbox("Name of the Drug", creams, index=None, key="cream2")
        with c2:
            qty5 = st.text_input("Qty", key="qty5")
            qty6 = st.text_input("Qtys", key="qty6")

        if st.button("Add Creams", type="primary"):
            try:
                qty5 = int(qty5)
                qty6 = int(qty6)
                reduce_medicine_quantity(connection, cream1, qty5)
                reduce_medicine_quantity(connection, cream2, qty6)
                st.success(f"{cream1} and {cream2} quantities updated successfully!")
            except ValueError:
                st.error("Please enter valid quantities.")

        # Others Section
        st.subheader("Others")
        c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 2])
        with c1:
            other1 = st.selectbox("Name of the Drug", others, index=None, key="other1")
            other2 = st.selectbox("Name of the Drug", others, index=None, key="other2")
        with c2:
            qty7 = st.text_input("Qty", key="qty7")
            qty8 = st.text_input("Qtys", key="qty8")

        if st.button("Add Others", type="primary"):
            try:
                qty7 = int(qty7)
                qty8 = int(qty8)
                reduce_medicine_quantity(connection, other1, qty7)
                reduce_medicine_quantity(connection, other2, qty8)
                st.success(f"{other1} and {other2} quantities updated successfully!")
            except ValueError:
                st.error("Please enter valid quantities.")

        # Close the database connection
        connection.close()
            

    elif form_name=="Referral":
        st.header("Referral")
        referral = st.radio("Referral", ("Yes", "No"))
        hospital_name = st.text_input("Name of the Hospital", placeholder="Comments...")
        doctor_name = st.text_input("Doctor name", placeholder="Comments...")
        condition_type = st.radio("Condition Type", ("Occupational", "Non-occupational", "Domestic"))
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear"):
                referral = None
                hospital_name = ""
                doctor_name = ""
                condition_type = None
        with col2:
            if st.button("Submit"):
                st.success("Form submitted successfully!")
                st.write("Referral:", referral)
                st.write("Hospital Name:", hospital_name)
                st.write("Doctor Name:", doctor_name)
                st.write("Condition Type:", condition_type)


def New_Visit(connection,cursor):
    st.header("NewVisit")

    global selected, select

    with st.container(border=1):
        r0c1, r0c2 = st.columns([5, 5])

        with r0c1:
            # First selectbox for Employee, Contractor, Visitor
            select = st.selectbox(
                "Select Type", 
                options=["Employee", "Contractor", "Visitor"]
            )

        with r0c2:
            # Second selectbox for Healthy, Unhealthy
            select1 = st.selectbox(
                "Select Health Status",
                options=["Healthy", "Unhealthy"]
            )
            st.session_state.form_data["Health status"] = select1
        # If select is not Visitor and health status is Healthy
        if select != "Visitor" and select1 == "Healthy":
            with r0c1:
                # Third selectbox for various healthy options
                select2 = st.selectbox(
                    "Healthy Options", 
                    options=["Medical Examination", "Periodic Work Fitness", "Fitness After Medical Leave", "Mock Drill", "BP Sugar Check"]
                )

            if select == "Contractor" and select2 == "Medical Examination":
                with r0c2:
                    # Selectbox for Medical Examination for Contractor
                    selected = st.selectbox(
                        "Medical Examination (Contractor)",
                        options=["Pre Employment", "Pre Employment(FH)", "Pre Employment(CC)", "Pre Placement", "Annual / Periodic", "Camps (Mandatory)", "Camps (Optional)"]
                    )

            elif select2 == "Medical Examination":
                with r0c2:
                    # Selectbox for Medical Examination for Employee
                    selected = st.selectbox(
                        "Medical Examination (Employee)",
                        options=["Pre Employment", "Pre Employment(FH)", "Pre Placement", "Annual / Periodic", "Periodic (FH)", "Camps (Mandatory)", "Camps (Optional)"]
                    )

            elif select2 == "Periodic Work Fitness":
                with r0c2:
                    # Selectbox for Periodic Work Fitness
                    selected = st.selectbox(
                        "Periodic Work Fitness",
                        options=["Special Work Fitness", "Special Work Fitness (Renewal)"]
                    )

            elif select2 == "Fitness After Medical Leave":
                with r0c2:
                    # Selectbox for Fitness After Medical Leave
                    selected = st.selectbox(
                        "Fitness After Medical Leave",
                        options=["Fitness After Medical Leave"]
                    )

            elif select2 == "Mock Drill" or select2 == "BP Sugar Check":
                with r0c2:
                    # Selectbox for Mock Drill or BP Sugar Check
                    selected = st.selectbox(
                        select2,
                        options=[select2]
                    )

        # If select is not Visitor and health status is Unhealthy
        if select != "Visitor" and select1 == "Unhealthy":
            with r0c1:
                # Selectbox for Unhealthy options
                select2 = st.selectbox(
                    "Unhealthy Options", 
                    options=["Out Patient"]
                )

            if select2 == "Out Patient":
                with r0c2:
                    # Selectbox for Out Patient options
                    selected = st.selectbox(
                        "Out Patient",
                        options=["Illness", "Over counter Illness", "Injury", "Over counter Injury", "Follow up Visits", "BP Sugar (Abnormal)", "Injury Outside the premises", "Over counter Injury Outside the premises"]
                    )

    with st.container(border=1): #initially height was 700
        if select=="Visitor" and select1=="Healthy":
            Form(None,select,select1,connection,cursor)
        elif select=="Visitor" and select1=="Unhealthy":
            Form(None,select,select1,connection,cursor)
        elif selected == "Pre Employment":
            Form("Pre Employment",select,select1,connection,cursor)
        
        elif selected == "Pre Employment(FH)":
            Form("Pre Employment(FH)",select,select1,connection,cursor)
        
        elif selected == "Pre Employment(CC)":
            Form("Pre Employment(CC)",select,select1,connection,cursor)
        
        elif selected == "Pre Placement":
            Form("Pre Placement",select,select1,connection,cursor)
        
        elif selected == "Annual / Periodic":
            Form("Annual / Periodic",select,select1,connection,cursor)
        
        elif selected == "Periodic (FH)":
            Form("Periodic (FH)",select,select1,connection,cursor)
        
        elif selected == "Camps (Mandatory)":
            Form("Camps (Mandatory)",select,select1,connection,cursor)
        
        elif selected == "Camps (Optional)":
            Form("Camps (Optional)",select,select1,connection,cursor)



        elif selected=="Special Work Fitness":
            Form("Special Work Fitness",select,select1,connection,cursor)

        elif selected=="Special Work Fitness (Renewal)":
            Form("Special Work Fitness (Renewal)",select,select1,connection,cursor)

        elif selected=="Fitness After Medical Leave":
            Form("Fitness After Medical Leave",select,select1,connection,cursor)
        elif selected=="Mock Drill" or selected=="BP Sugar Check":
            Form(selected,select,select1,connection,cursor)


            
        
        elif selected == "Illness":
            Form("Illness",select,select1,connection,cursor)
        
        elif selected == "Over counter Illness":
            Form("Over counter Illness",select,select1,connection,cursor)                    
        
        elif selected == "Injury":
            Form("Injury",select,select1,connection,cursor)
        
        elif selected == "Over counter Injury":
            Form("Over counter Injury",select,select1,connection,cursor)
        
        elif selected == "Follow up Visits":
            Form("Follow up Visits",select,select1,connection,cursor)
        
        elif selected == "BP Sugar (Abnormal)":
            Form("BP Sugar (Abnormal)",select,select1,connection,cursor)
        
        elif selected == "Injury Outside the premises":
            Form("Injury Outside the premises",select,select1,connection,cursor)

        elif selected == "Over counter Injury Outside the premises":
            Form("Over counter Injury Outside the premises",select,select1,connection,cursor)
        else:
            st.write("Select a visit reason", selected)