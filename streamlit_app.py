import cmath
import streamlit as st
import os
import numpy as np
import pandas as pd
from PIL import Image
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from gtspython import tonGrad
st.set_page_config(layout="wide")
default_directory_path = r"C:\Users\AAlmgren\Documents\Projects\Drilling Compliance\csv"
directory_path = st.text_input("Type folder:", default_directory_path)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Resumed","Conversion", "Detailed Conversion","Conversion by vein","DDH detail","New structures", "Waterfall", "Res Table"])
my_list=['ZN','AG','PB','CU']

def list_files_in_directory(directory_path):
    files = os.listdir(directory_path)
    return files


# Using "with" notation
with st.sidebar:
    mines = ["San Cristobal", "Andaychagua", "Animon"]
    years = ["21_22", "22_23"]
    selected_mine = st.sidebar.selectbox("Mine:", mines, index=0)
    selected_year = st.sidebar.selectbox("Year:", years, index=1)
    material = st.radio("Evaluate by: ", ['Tonnes', 'Metal'])
    
    string = default_directory_path+"\\"+selected_mine+"_ton_"+selected_year+".csv"
    stringcomp = default_directory_path+"\\"+selected_mine+"_comp_"+selected_year+".csv"
    csv_file_path = string
    comp_file_path = stringcomp
    df0 = pd.read_csv(csv_file_path)
    df = df0[(df0['TYPE'] == 'DRE')]
    df_rescat = df0[(df0['TYPE'] == 'DRE')]
       
    def add_cat(df=''):
        df.loc[(df['index']==1),    "Category"] = 'Measured to Measured'
        df.loc[(df['index']==2) ,   "Category"] = 'Indicated to Measured'
        df.loc[(df['index']==3) ,   "Category"] = 'Inferred to Measured'
        df.loc[(df['index']==4) ,   "Category"] = 'Mineral Potential to Measured'
        df.loc[(df['index']==5) ,   "Category"] = 'New Measured' 
        df.loc[(df['index']==6) ,   "Category"] = 'Lost Measured'                     
        df.loc[(df['index']==7) ,   "Category"] = 'Measured to Indicated'
        df.loc[(df['index']==8) ,   "Category"] = 'Indicated to Indicated'
        df.loc[(df['index']==9) ,   "Category"] = 'Inferred to Indicated'
        df.loc[(df['index']==10) ,  "Category"] = 'Mineral Potential to Indicated'  
        df.loc[(df['index']==11) ,  "Category"] = 'New Indicated'  
        df.loc[(df['index']==12) ,  "Category"] = 'Lost Indicated'                     
        df.loc[(df['index']==13) ,  "Category"] = 'Measured to Inferred'
        df.loc[(df['index']==14) ,  "Category"] = 'Indicated to Inferred'
        df.loc[(df['index']==15) ,  "Category"] = 'Inferred to Inferred' 
        df.loc[(df['index']==16) ,  "Category"] = 'Mineral Potential to Inferred'  
        df.loc[(df['index']==17) ,  "Category"] = 'New Inferred'  
        df.loc[(df['index']==18) ,  "Category"] = 'Lost Inferred'                     
        df.loc[(df['index']==19) ,  "Category"] = 'Measured to Mineral Potential' 
        df.loc[(df['index']==20) ,  "Category"] = 'Indicated to Mineral Potential' 
        df.loc[(df['index']==21) ,  "Category"] = 'Inferred to Mineral Potential' 
        df.loc[(df['index']==22) ,  "Category"] = 'Mineral Potential unchanged'
        df.loc[(df['index']==23) ,  "Category"] = 'New MinPot' 
        df.loc[(df['index']==24) ,  "Category"] = 'Lost MinPot'
        # Column used to metrics in PowerBi. only upgrade in caterory, and new/deleted tonnes. Downgrade and categories unchanges don't enter in the DDRE category.
        # 1 - Gain and losses in New Measured, excluding downgrades.
        # 2 - Gain and losses in New Indicated, excluding downgrades.
        # 3 - Gain and losses in New Inferred, excluding downgrades.
        # 4 - Gain and losses in New MinPot, excluding downgrades.
        # 5 - Previous Measured keeps Measured, with slight changes
        # 6 - Previous indicated keeps indicated, with slight changes
        # 7 - Previous Inferred keeps Inferred, with slight changes
        # 8 - Previous MinPot keeps MinPot, with slight changes
        df.loc[(df['index']==1)  , "DDDRE"] = 5
        df.loc[(df['index']==2)  , "DDDRE"] = 1
        df.loc[(df['index']==3)  , "DDDRE"] = 1
        df.loc[(df['index']==4)  , "DDDRE"] = 1
        df.loc[(df['index']==5)  , "DDDRE"] = 1
        df.loc[(df['index']==6)  , "DDDRE"] = 1
        df.loc[(df['index']==7)  , "DDDRE"] = 9
        df.loc[(df['index']==8)  , "DDDRE"] = 6
        df.loc[(df['index']==9)  , "DDDRE"] = 2
        df.loc[(df['index']==10) , "DDDRE"] = 2
        df.loc[(df['index']==11) , "DDDRE"] = 2
        df.loc[(df['index']==12) , "DDDRE"] = 2
        df.loc[(df['index']==13) , "DDDRE"] = 9
        df.loc[(df['index']==14) , "DDDRE"] = 9 
        df.loc[(df['index']==15) , "DDDRE"] = 7 
        df.loc[(df['index']==16) , "DDDRE"] = 3 
        df.loc[(df['index']==17) , "DDDRE"] = 3 
        df.loc[(df['index']==18) , "DDDRE"] = 3
        df.loc[(df['index']==19) , "DDDRE"] = 9 
        df.loc[(df['index']==20) , "DDDRE"] = 9 
        df.loc[(df['index']==21) , "DDDRE"] = 9    
        df.loc[(df['index']==22) , "DDDRE"] = 8
        df.loc[(df['index']==23) , "DDDRE"] = 4
        df.loc[(df['index']==24) , "DDDRE"] = 4         
        
        df.loc[(df['index']==1)  , "DDDRE2"] = 1
        df.loc[(df['index']==2)  , "DDDRE2"] = 1
        df.loc[(df['index']==3)  , "DDDRE2"] = 1
        df.loc[(df['index']==4)  , "DDDRE2"] = 1
        df.loc[(df['index']==5)  , "DDDRE2"] = 1
        df.loc[(df['index']==6)  , "DDDRE2"] = 1
        df.loc[(df['index']==7)  , "DDDRE2"] = 9
        df.loc[(df['index']==8)  , "DDDRE2"] = 2
        df.loc[(df['index']==9)  , "DDDRE2"] = 2
        df.loc[(df['index']==10) , "DDDRE2"] = 2
        df.loc[(df['index']==11) , "DDDRE2"] = 2
        df.loc[(df['index']==12) , "DDDRE2"] = 2
        df.loc[(df['index']==13) , "DDDRE2"] = 9
        df.loc[(df['index']==14) , "DDDRE2"] = 9 
        df.loc[(df['index']==15) , "DDDRE2"] = 3 
        df.loc[(df['index']==16) , "DDDRE2"] = 3 
        df.loc[(df['index']==17) , "DDDRE2"] = 3 
        df.loc[(df['index']==18) , "DDDRE2"] = 3
        df.loc[(df['index']==19) , "DDDRE2"] = 9 
        df.loc[(df['index']==20) , "DDDRE2"] = 9 
        df.loc[(df['index']==21) , "DDDRE2"] = 9    
        df.loc[(df['index']==22) , "DDDRE2"] = 4
        df.loc[(df['index']==23) , "DDDRE2"] = 4
        df.loc[(df['index']==24) , "DDDRE2"] = 4
        return df
    
    def add_cat_2(df=''):
        df['Category']=''
        if df.shape[0]>0:
            df.loc[(df['DDDRE']==1),    "Category"] = 'Converted to Measured'
            df.loc[(df['DDDRE']==2) ,   "Category"] = 'Converted to Indicated'
            df.loc[(df['DDDRE']==3) ,   "Category"] = 'Converted to Inferred'
            df.loc[(df['DDDRE']==4) ,   "Category"] = 'Add Mineral Potential'
            df.loc[(df['DDDRE']==5) ,   "Category"] = 'Changes inside Measured'
            df.loc[(df['DDDRE']==6) ,   "Category"] = 'Changes inside Indicated'
            df.loc[(df['DDDRE']==7) ,   "Category"] = 'Changes inside Inferred'
            df.loc[(df['DDDRE']==8) ,   "Category"] = 'Changes inside Min Pot'
            df.loc[(df['DDDRE']==9) ,   "Category"] = 'Downgrades'
            df['DDDRE'] = df['DDDRE'].round()
            #.astype(int)
        return df
    def add_cat_rescat(df=''):
        df['Category']=''
        if df.shape[0]>0:
            df.loc[(df['RE']==1),    "Category"] = 'Measured'
            df.loc[(df['RE']==2) ,   "Category"] = 'Indicated'
            df.loc[(df['RE']==3) ,   "Category"] = 'Inferred'
            df.loc[(df['RE']==4) ,   "Category"] = 'Mineral Potential'
            df.loc[(df['RE']==-99) , "Category"] = 'Non Classified'
            df.loc[(df['RE']==0) ,   "Category"] = 'Non Classified'
            df['DDDRE'] = df['DDDRE'].round()
            #.astype(int)
        return df    
    df_comp = pd.read_csv(comp_file_path)
    df_comp['DRE'] = df_comp['DRE'].astype(float)
#    df_comp['DRE'] = df_comp['DRE'].round().astype(int)
    
    selected_domain = st.multiselect("Filter by VEIN:", df["VEIN"].unique())
    selected_mined_a = st.selectbox("Filter by MINED_A:", df["MINED_A"].unique(),index=1)
    selected_cutoff_a = st.selectbox("Filter by CUTOFF:", df["CUTOFF"].unique(),index=1)
    selected_buffer = st.selectbox("Filter by BUFFER:", df["BUFFER"].unique(),index=0)

with tab2:

    if selected_mined_a:
        df = df[df["MINED_A"].isin([selected_mined_a])]
    if selected_cutoff_a:
        df = df[df["CUTOFF"].isin([selected_cutoff_a])]
    if selected_buffer:
        df = df[df["BUFFER"].isin([selected_buffer])]
    if selected_domain:
        df = df[df["VEIN"].isin(selected_domain)]

    def build_table(df=df,df_comp=df_comp,var1=''):
        #Create two columns: afer drilling and before drilling
        x1 = df[df['PHASE'] == 'Before Drilling'].groupby(var1).sum().reset_index()
        x2 = df[df['PHASE'] == 'After Drilling'].groupby(var1).sum().reset_index()
        # if not x1.shape[0]>0:
        #     x1 = x2
        #     x1.rename(columns = {'After Drilling':'Before Drilling'}, inplace = True)
        x3 = x1.merge(x2, on=var1, how='outer')
    
        x3['Forecasted '+material+' (t)'] = x3[material.upper()+'_x'].round(0)
        x3['Converted '+material+' (t)'] = x3[material.upper()+'_y'].round(0)
        return x3
        
    x3=build_table(df=df,var1='index')
    x3=add_cat(df=x3)
    x3.loc[(x3['index'] == 1) | (x3['index'] == 8) | (x3['index'] == 15) | (x3['index'] == 22), "Forecasted "+material+" (t)"] = 0
    x3.loc[(x3['index'] == 1) | (x3['index'] == 8) | (x3['index'] == 15) | (x3['index'] == 22), "Converted "+material+" (t)"] = x3[material.upper()+'_y'].round(0) - x3[material.upper()+'_x'].round(0)
 
    if selected_domain:
        df_comp = df_comp[df_comp["VEIN"].isin(selected_domain)]

    df_comp2=df_comp.drop_duplicates(subset=['BHID'], keep='last')
    x4 = df_comp2.groupby('DRE')['DEPTH'].sum().reset_index()
    x5 = x3.merge(x4, right_on='DRE', left_on='index', how='outer')
    x7 = x5.groupby('DDDRE').sum().reset_index()
    x6=add_cat_2(df=x7)
    
    x6['Meters drilled (m)']=x6['DEPTH'].round(0)
    x6['Conversion']=x6['Converted '+material+' (t)']/x6['Forecasted '+material+' (t)']
    x6['t/m']=(x6['Converted '+material+' (t)']/x6['Meters drilled (m)'])
    x6['index']=x6['index'].round(0)
    x6['t/m']=x6['t/m'].round(0)
    x6['Conversion'] = x6['Conversion'].astype(float).map("{:.0%}".format)
    x6 = x6[['index','Category','Forecasted '+material+' (t)','Converted '+material+' (t)','Meters drilled (m)','t/m','Conversion','DDDRE']]
    def resumed_cat(df=df):
        df.loc[(df['DDDRE']==5),    "DDDRE"] = 1
        df.loc[(df['DDDRE']==6) ,   "DDDRE"] = 2
        df.loc[(df['DDDRE']==7) ,   "DDDRE"] = 3
        df.loc[(df['DDDRE']==8) ,   "DDDRE"] = 4
        df.sort_values(by=['DDDRE'], inplace=True)
        return df
    x7=resumed_cat(df=x6)
    x8 = x7[['Category','Forecasted '+material+' (t)','Converted '+material+' (t)','Meters drilled (m)','t/m','Conversion']]

    x9 = x7.groupby('DDDRE').sum().reset_index()
    x9=add_cat_2(df=x9)
    x9['t/m']=(x9['Converted '+material+' (t)']/x9['Meters drilled (m)'])
    x9['t/m']=x9['t/m'].round(0)
    x9['Conversion']=x9['Converted '+material+' (t)']/x9['Forecasted '+material+' (t)']
    x9['Conversion'] = x9['Conversion'].astype(float).map("{:.0%}".format)
    x9 = x9[['DDDRE','Category','Forecasted '+material+' (t)','Converted '+material+' (t)','Meters drilled (m)','t/m','Conversion']]
    x9.sort_values(by=['DDDRE'], inplace=True)
    x10 = x9[['Category','Forecasted '+material+' (t)','Converted '+material+' (t)','Meters drilled (m)','t/m','Conversion']]
    st.dataframe(x10, hide_index=True)

 #   x9 = x7.groupby('DDDRE').sum().reset_index()  

#     def on_more_click(show_more, idx):
#         show_more[idx] = True


#     def on_less_click(show_more, idx):
#         show_more[idx] = False
    
#     if "show_more" not in st.session_state:
#         st.session_state["show_more"] = dict.fromkeys([0,1,2,3,4], False)
#     show_more = st.session_state["show_more"]

#     cols = st.columns(7)
#     fields = ['Category','Forecasted '+material+' (t)','Converted '+material+' (t)','Meters drilled (m)','t/m','Conversion','More']

#     # header
#     for col, field in zip(cols, fields):
#         col.write("**" + field + "**")

#  # rows
#     for idx, row in x10.iterrows():

#         col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
#         col1.write(str(row['Category']))
#         col2.write(str(row['Forecasted '+material+' (t)']))
#         col3.write(str(row['Converted '+material+' (t)']))
#         col4.write(str(row['Meters drilled (m)']))
#         col5.write(str(row['t/m']))
#         col6.write(str(row['Conversion']))
#         placeholder = col7.empty()
#         if show_more[idx]:
#             placeholder.button(
#                  "less", key=str(idx), on_click=on_less_click, args=[show_more, idx]
#              )

# #             # do stuff
#             st.write("This is some more stuff with a checkbox")
# #             # temp = st.selectbox("Select one", ["A", "B", "C"], key=idx)
# #             # st.write("You picked ", temp)
# #             # st.write("---")
#         else:
#             placeholder.button(
#                 "more",
#                 key=idx,
#                 on_click=on_more_click,
#                 args=[show_more, idx],
#                 type="primary",
#             )

with tab1:
    df_tab2_1 = x9[x9['DDDRE']<5]
    df_tab2_1 = df_tab2_1[['Category','t/m','Conversion']]
    st.dataframe(df_tab2_1, hide_index=True)

with tab3:
    st.dataframe(x8, hide_index=True)


with tab4:
    selected_cat = st.selectbox("Detailing by:", x6["Category"].unique())
    x11=df
    x11=add_cat(x11)
    x11=add_cat_2(x11)
    # x11=resumed_cat(df=x11)
    def retrieve_dddre(categ=''):
        val=0
        if categ=='Converted to Measured':  val=1
        if categ=='Converted to Indicated': val=2
        if categ=='Converted to Inferred':  val=3
        if categ=='Add Mineral Potential':  val=4
        if categ=='Changes inside Measured':  val=5
        if categ=='Changes inside Indicated':  val=6
        if categ=='Changes inside Inferred':  val=7
        if categ=='Changes inside Min Pot':  val=8
        return val
    val=retrieve_dddre(categ=selected_cat)
    x11=add_cat(x11)
    x11=x11[x11['DDDRE']==val]
    x11=build_table(x11,var1='VEIN')
    df_comp3=add_cat_2(df_comp)
    df_comp3=df_comp3[df_comp3['DDDRE']==val]
    x12 = df_comp3.groupby(['VEIN','DDDRE'])['DEPTH'].sum().reset_index()
    x13 = x11.merge(x12, right_on='VEIN', left_on='VEIN',how='left')
    x13['Meters drilled (m)']=x13['DEPTH'].round(0)
    x13['Conversion']=x13['Converted '+material+' (t)']/x13['Forecasted '+material+' (t)']
    x13['t/m']=(x13['Converted '+material+' (t)']/x13['Meters drilled (m)'])
    # x7['index']=x7['index'].round(0)
    x13['t/m']=x13['t/m'].round(0)
    x13['Conversion'] = x13['Conversion'].astype(float).map("{:.0%}".format)
    x14 = x13[['VEIN','Forecasted '+material+' (t)','Converted '+material+' (t)','Meters drilled (m)','t/m','Conversion']]



    st.dataframe(x14, hide_index=True)

    
with tab5:
    selected_categ = st.selectbox("Category:", x6["Category"].unique())
    selected_vein = st.selectbox("Vein:", x13["VEIN"].unique())
    df_comp5=resumed_cat(df_comp)
    df_comp5=add_cat_2(df_comp5)
    if selected_categ:
        df_comp5=df_comp5[df_comp5['Category']==selected_cat]
    df_comp5=df_comp5[df_comp5['VEIN']==selected_vein]
    x15=df_comp5
    x15['Meters drilled (m)']=x15['DEPTH'].round(0)
    x15['Previous Rescat']=x15['RE_OLD'].round(0)
    x15['Current Rescat']=x15['RE'].round(0)
    # # x13['Conversion']=x13['Converted '+material+' (t)']/x13['Forecasted '+material+' (t)']
    # # x13['t/m']=(x13['Converted '+material+' (t)']/x13['Meters drilled (m)'])
    # # # x7['index']=x7['index'].round(0)
    # # x13['t/m']=x13['t/m'].round(0)
    # # x13['Conversion'] = x13['Conversion'].astype(float).map("{:.0%}".format)
    x15 = x15[['BHID','Meters drilled (m)','Previous Rescat','Current Rescat','EQ','EQ_OLD','PL','PL_OLD']]   
    
    st.dataframe(x15, hide_index=True)
    
    folder_path = r"C:\Users\AAlmgren\Documents\Projects\Volcan"+"\\"+selected_mine+"\\2023\work\images"
    #folder_path = path_1+"\\"+selected_mine+"_ton_"+selected_year+".csv"
   # Adicionando uma opção para selecionar uma pasta de imagens PNG
    #folder_path = st.text_input("Digite o caminho da pasta com imagens PNG:")
    
    # Adicionando filtros por nome parcial de imagem
    filter_text1 = selected_vein+'_'
    filter_text2 = selected_year[:2]
    filter_text3 = selected_year[-2:]
    filter_text4 = 'RE_'
    # Verificando se a pasta existe
    if os.path.exists(folder_path):
        # Listando todos os arquivos PNG na pasta que correspondem aos filtros
        image_files = [f for f in os.listdir(folder_path) if (f.lower().endswith(filter_text2+'.png') or f.lower().endswith(filter_text3+'.png'))
                       and filter_text1.lower() in f.lower() and filter_text4.lower() in f.lower()]
        
        # Exibindo imagens da pasta usando a navegação por setas do teclado
        if len(image_files) > 0:
            current_image_index = st.session_state.get('current_image_index', 0)
            if current_image_index >= len(image_files):
                current_image_index = 0
            elif current_image_index < 0:
                current_image_index = len(image_files) - 1
            
            st.image(Image.open(os.path.join(folder_path, image_files[current_image_index])), caption=image_files[current_image_index], use_column_width=True)
            
            # Adicionando controles para navegação de imagens
            st.text(f"Imagem {current_image_index + 1} de {len(image_files)}")
            if st.button("Anterior"):
                current_image_index = current_image_index-1
            if st.button("Proxima"):
                current_image_index = current_image_index+1
            
            st.session_state['current_image_index'] = current_image_index
        else:
            st.text(f"Nenhuma imagem PNG encontrada na pasta com os filtros: '{filter_text1}' e '{filter_text2}'")
    else:
        st.text("Digite um caminho de pasta válido.")


    
with tab6:
    new_mat = st.radio("Evaluate by: ", ['Only New Structures', 'All Structures increased its size', 'Structures trimmed', 'Balance of gains and losses'])
    
    x60=df
    x61=add_cat(x60)
    x61=add_cat_2(x61)
    # x11=resumed_cat(df=x11)
    x61=add_cat(x61)
    if (new_mat=='All Structures increased its size'):
        x61=x61[((x61['RE']>0) & (x61['RE']<4))]
    if (new_mat=='Only New Structures'):
        x61=x61[(x61['RE']>0) & (x61['RE']<4)]
    if new_mat=='Structures trimmed':
        x61=x61[((x61['RE']==-99) | (x61['RE']==4)) & ((x61['RE_OLD']==1) | (x61['RE_OLD']==2) | (x61['RE_OLD']==3))]
    x61=build_table(x61,var1='VEIN')
#    x61=x61[x61[['TONNES_x']].isna()]
    if new_mat=='Only New Structures':
        x61=x61[x61['TONNES_x'].isnull()]
    df_comp=add_cat_2(df_comp)
    df_comp2 = df_comp[df_comp["VEIN"].isin(x61["VEIN"].unique())]
    df_comp2=df_comp2.drop_duplicates(subset=['BHID'], keep='last')
# # df_comp=df_comp[df_comp['DDDRE']==val]
    x63 = df_comp.groupby(['VEIN'])['DEPTH'].sum().reset_index()
    df_comp3 = df_comp2.groupby(['VEIN'])['DEPTH'].sum().reset_index()
    df_comp3['DEPTH_DISTINCT']= df_comp3['DEPTH']
    df_comp3= df_comp3[['VEIN','DEPTH_DISTINCT']]
    x63['Meters drilled (m)']=x63['DEPTH'].round(0)
   # st.dataframe(x63, hide_index=True)
    x64 = x61.merge(x63, on='VEIN',how='left')
    x64 = x64.merge(df_comp3, on='VEIN',how='left')

    x64['Conversion']=x64['Converted '+material+' (t)']/x64['Forecasted '+material+' (t)']
    x64['t/m'] = (x64['Converted '+material+' (t)']/x64['Meters drilled (m)']).round(0)
    x64.rename(columns = {'Forecasted '+material+' (t)':'Previous '+material+' (t)'}, inplace = True)
    x64.rename(columns = {'Converted '+material+' (t)':'New '+material+' (t)'}, inplace = True)
    x64 = x64.fillna(0)
    x64['Delta '+material+' (t)'] = (x64['New '+material+' (t)']-x64['Previous '+material+' (t)']).round(0)
    x65 = x64[['VEIN','Previous '+material+' (t)','New '+material+' (t)','Delta '+material+' (t)','Meters drilled (m)','t/m']]
    #x65=x64.append(x64.sum(numeric_only=True).rename('Total'), ignore_ind,ex=True)



    #st.dataframe(x65, hide_index=True)
 #   x66 = x65[['Converted '+material+' (t)','Meters drilled (m)']].sum()
    
    summary1 = pd.DataFrame({
    'Vein': ['Total'],
    'Previous '+material+' (t)': [x64['Previous '+material+' (t)'].sum()],
    'New '+material+' (t)': [x64['New '+material+' (t)'].sum()],
    'Delta '+material+' (t)': [x64['Delta '+material+' (t)'].sum()],
    'Meters drilled (m)': [x64['DEPTH_DISTINCT'].sum().round(0)],
    't/m': [(x64['New '+material+' (t)'].sum()/x64['Meters drilled (m)'].sum()).round(0)]
})
    
    st.dataframe(x65, hide_index=True)
    st.dataframe(summary1, hide_index=True)

    gt_option = st.checkbox("Gt curve")
    
    if gt_option:
        gt_path=r"C:\Users\AAlmgren\Documents\Projects\Volcan\\"+selected_mine+"\\2023\work\GradeTon_Figures"

        from pathlib import Path
        workpath=r"C:\Users\AAlmgren\Documents\Projects\Volcan\\"+selected_mine+"\\2023\work\\"
        fils = 'bm_'+x65["VEIN"].unique()+'_23.csv'
        imagenns = [x for x in Path(workpath).iterdir() if x in fils]

        for filebm in fils:
        #     tonGrad(fname=filebm,grades = ['ZN','AG','PB','CU'],
        #     dens='DENSITY',cogvar='ZNEQ',ton='TON',
        #     unit=1,blksizcol=['XINC','YINC','ZINC'],minedfi='MINED',minedva=1,
        #     initcog=0,maxcog=10,ncogs=20,calcton=True,root=workpath)
        
            image_files_gt = [f for f in os.listdir(gt_path)]
                # Exibindo imagens da pasta usando a navegação por setas do teclado
            if len(image_files_gt) > 0:
                current_image_index_gt = st.session_state.get('current_image_index_gt', 0)
                if current_image_index_gt >= len(image_files_gt):
                    current_image_index_gt = 0
                elif current_image_index_gt < 0:
                    current_image_index_gt = len(image_files_gt) - 1
                    
            st.image(Image.open(os.path.join(gt_path, image_files_gt[current_image_index_gt])), caption=image_files_gt[current_image_index_gt], use_column_width=True)
    


            
with tab7:

    # Sample data
    data = {
        'Category': ['Start', 'Category A', 'Category B', 'Category C', 'End'],
        'Value': [100, -20, -30, 40, -10]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Create a Streamlit app
    st.title("Waterfall Chart in Streamlit")

    # Display the original data table
    st.write("Original Data:")
    st.dataframe(df)

    # Create a waterfall chart
    fig = go.Figure(go.Waterfall(
        name="",
        orientation="v",
        textposition="outside",
        text=df['Value'],
        x=df['Category'],
        y=df['Value']
    ))

    # Customize the chart
    fig.update_layout(title="Waterfall Chart", showlegend=False)

    # Display the waterfall chart
    st.write("Waterfall Chart:")
    st.plotly_chart(fig)

with tab8:

    if selected_mined_a:
        df_rescat = df_rescat[df_rescat["MINED_A"].isin([selected_mined_a])]
    if selected_cutoff_a:
        df_rescat = df_rescat[df_rescat["CUTOFF"].isin([selected_cutoff_a])]
    if selected_buffer:
        df_rescat = df_rescat[df_rescat["BUFFER"].isin([selected_buffer])]
    if selected_domain:
        df_rescat = df_rescat[df_rescat["VEIN"].isin(selected_domain)]

    def build_table_rescat(df=df,phase='Before Drilling'):
        #Create two columns: afer drilling and before drilling
        x1 = df[df['PHASE'] == phase]
        df_grade=(x1.groupby('RE')[my_list+[material.upper()]]
                         .apply(lambda x: x[my_list].mul(x[material.upper()], axis=0).sum() / x[material.upper()].sum()))
        df5 = pd.DataFrame()
        df4=x1.groupby(['RE']).sum()
        df5[material+' (Mt)']=df4[material.upper()]
        df5.index.rename('index', inplace=True)
        df_grade.index.rename('index', inplace=True)
        #if df5.shape[0]>0:
        df6=pd.merge(df5,df_grade,on='index',how='left')
        df6.loc[(df6[material+' (Mt)'] >0) , material+' (Mt)'] = df6[material+' (Mt)'] / 1000000
        df6 = df6.round(1)  # Round all columns to 1 decimal place
        return df6


    x81=build_table_rescat(df=df_rescat,phase='Before Drilling')
    st.write('YE 2022 Resources Table')
    st.dataframe(x81, hide_index=True)
    x82=build_table_rescat(df=df_rescat,phase='After Drilling')
    st.write('YE 2023 Resources Table')
    st.dataframe(x82, hide_index=True)
