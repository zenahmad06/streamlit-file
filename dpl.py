#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import xgboost as xgb
if 'approve' not in st.session_state:
    st.session_state['approve']=""
#make wide columns
st.set_page_config(layout='wide')
st.title('Loan Approval prediction')
# make three column with ration with 2
col1,col2,col3=st.columns([2,2,2])
# make input  box
with col1:
    age=st.text_input('Enter age :')
    income=st.text_input('Income :')
    home_ownership=st.selectbox("Home ownership", options=['Rent','Mortgage','Own','Other'])
with col2:
    loan_intent=st.selectbox("Loan Intention", options=['Education','Medical','Personal','Venture',
                                                        'Debt Consolidation','Home Improvement'])
    ps_emp_length=st.text_input('Enter Person Employee Length :')
    loan_amount=st.text_input('Loan Amount :')
    loan_grade=st.selectbox("Loan Grade", options=[i for i in 'ABCDEFG'])
    
with col3:
    has_cdity=st.selectbox("has person credit bearue file ", options=['Yes','No'])
    credit_length=st.text_input('Credit history length :')
    if st.button('submit'):
        #the inpu box is none
        if (not age.strip() or not income.strip() or not home_ownership.strip()
           or not loan_intent.strip() or not ps_emp_length.strip() or not loan_grade.strip()
            or not has_cdity.strip() or not credit_length.strip() or not loan_amount.strip()):
            st.error('Fill the input box')
        else:
            try :
                age_var=float(age)
                income_var=float(income)
                ps_emp_length_var=float(ps_emp_length)
                credit_length_var=float(credit_length)
                loan_amount_var=float(loan_amount)
                if (age_var > 0 and income_var > 0 and ps_emp_length_var > 0 and credit_length_var > 0 and loan_amount_var > 0)  :
                    dat_num={
                        'person_age':age_var,
                        'person_income':income_var,
                        'person_emp_length':ps_emp_length_var,
                        'loan_amnt':loan_amount_var,
                        'cb_person_cred_hist_length':credit_length_var,
                        
                    }
                    

                    import pandas as pd
                    dat_input=pd.DataFrame([dat_num])
                    #eksport
                    vardummy={
                        'person_home_ownership':[home_ownership.strip().lower()],
                        'loan_intent':[loan_intent.replace(" ","").lower()]
                        
                    }
                    dat_dummi=pd.DataFrame({
                        'person_home_ownership':[home_ownership.strip().lower()],
                        'loan_intent':[loan_intent.replace(" ","").lower()]
                    })
                    dat_dummi_df=pd.get_dummies(dat_dummi,columns=['person_home_ownership','loan_intent'],
                                                prefix="",prefix_sep="").astype(int)
                    #eksport the column dummy
                    import json
                    with open('columns_dummy.json','r') as f:
                        dummi_kol=json.load(f)
                    for i in dummi_kol:
                        if i not in dat_dummi_df.columns:
                            dat_dummi_df[i]=0
                            
                    dat_dummi_df=dat_dummi_df[dummi_kol]

                    #handle categorical data
                    grade='ABCDEFG'
                    map_grade={}
                    for i,j in zip(grade,range(len(grade))):
                        map_grade[i]=j
                    dat_dummi_df['loan_grade']=map_grade[loan_grade]
                    if has_cdity=='Yes':
                        dat_dummi_df['cb_person_default_on_file']=1
                    else:
                        dat_dummi_df['cb_person_default_on_file']=0
                    #merge
                    final_input=pd.concat([dat_input,dat_dummi_df],axis=1)
                    st.dataframe(final_input)
                    
                    #eksport model machine learning
                    import pickle
                    model=pickle.load(open("model_approval.pkl","rb"))
                    dmatrix_final=xgb.DMatrix(final_input)
                    predic=model.predict(dmatrix_final)
                    
                    if predic==1:
                        st.session_state['approve']='Loan Approved'
                    else:
                        st.session_state['approve']='Loan Denied'



                else:
                    st.error('invalid number')
            except Exception as e:
                st.error(f'the error : {e}')
st.title('Is Approve ?')

st.markdown(
    f"""
    <div style=
        "border: 1px solid #ccc; 
        padding: 10px;
        border-radius: 5px;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80%;
        width: 50%;
        margin-left:20%;
        margin-right:20%;
        fontsize:18pt;
        fontweight:bold;
        "><h2>{st.session_state['approve']}</h2>
        
    </div>
    """,
    unsafe_allow_html=True
)


# In[19]:


import pandas as pd

df = pd.DataFrame({
    "person_home_ownership": ["mortgage"],
    "loan_intent": ["homeimprovement"]
})

dummy_df = pd.get_dummies(df, columns=["person_home_ownership", "loan_intent"]).astype(int)
print(dummy_df)
print(df)

