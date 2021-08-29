import io
import base64
from flask.helpers import url_for
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from flask import Flask, render_template,request,redirect
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier as RFC
from seaborn import heatmap, histplot, despine, relplot, catplot, countplot


#from seaborn.distributions import distplot
matplotlib.use('Agg')

app = Flask(__name__)

#df = pd.read_csv('Retention_Dataset.csv')
global data_df
data_df = {}
# Retention_Dataset
# Clinton_Voting_Percent

def file_is_csv(filename):
    if filename[-3:] == 'csv':
        return True
    return False

count = 1   # flag for animation
@app.route('/',methods=['GET','POST'])
def upload_file():

    if request.method == 'POST':

        print('-------------->')
        print(request.files)
        print(request.files['file'])

        if 'file' not in request.files :        # No file selected
            error_msg = "Choose a File"
            return render_template('index.html', error_msg=error_msg,flag = False)

        file = request.files['file']

        if file.filename == '':                 # simply submitting 
            error_msg = "Choose a File"
            return render_template('index.html', error_msg=error_msg,flag = False)

        if not file_is_csv(file.filename):      # check uploaded csv or not
            error_msg = "Upload only *CSV files"
            return render_template('index.html', error_msg=error_msg,flag = False)
        
        up_df = pd.read_csv(file)
        #print(up_df.head())
        data_df['data'] = up_df
        
        return render_template('index.html', error_msg='',flag = True)
    return render_template('index.html', error_msg='',flag = False)


@app.route('/Analysis')
def Analysis():

    try:
        df = data_df['data']
    except KeyError:
        return redirect(url_for('upload_file'))

    df_cols, df_dim, cat_col, num_col, mis_val, mis_detail, u_col, cols_data = get_data(df)
    
    '''df_cols = df.columns.tolist()
    df_dim = df.shape   # shape

    cols_data = {i: {'type': '', 'sub_type': '', 'null_val': '', 'mini': '', 'maxi': '',
                     'mean': '', 'median': '', 'mode': '', 'st_dev': '', 'vari': '', 'Quant': '', 'iqr': ''} for i in df_cols}

    cat_col, num_col, u_col = [], [], []   # column types
    for i in df.columns:

        u_sum = len(pd.unique(df[i]))       # unique vales
        if u_sum == df_dim[0]:
            u_col.append(i)

        if df[i].dtype == 'object':
            cat_col.append(i)
            cols_data[i]['type'] = 'Categorical'
        else:
            num_col.append(i)
            cols_data[i]['type'] = 'Numerical'
            cols_data[i]['mini'] = df[i].min()
            cols_data[i]['maxi'] = df[i].max()
            cols_data[i]['mean'] = round(df[i].mean(), 2)
            cols_data[i]['median'] = df[i].median()
            cols_data[i]['st_dev'] = round(df[i].std(), 2)

            if i not in u_col:
                cols_data[i]['vari'] = round(df[i].var(), 2)
                cols_data[i]['Quant'] = [round(df[i].quantile(0.1), 3), round(df[i].quantile(0.7), 3)]
                cols_data[i]['iqr'] = round((cols_data[i]['Quant'][1] - cols_data[i]['Quant'][0]),3)

        cols_data[i]['sub_type'] = df[i].dtype.name

        cols_data[i]['null_val'] = df[i].isna().sum()

        if i not in u_col:                  # mode
            # convert series to list and to st and replaceing "'".
            cols_data[i]['mode'] = str(df[i].mode().tolist())[
                1:-1].replace("'", '')

    mis_val = df.isna().sum()  # missing values

    mis_detail = [(df_cols[i], mis_val[i]) for i in range(
        len(mis_val)) if mis_val[i] != 0]    # missing_val details

    data_df['df_cols'] = df_cols
    data_df['u_col'] = u_col
    data_df['num_col'] = num_col
    data_df['cat_col'] = cat_col
    data_df['mis_detail'] = mis_detail'''

    '''top_rows = []
    for i in range(10):
        top_rows.append(df.iloc[i:i+1].values.flatten().tolist())'''
    top_rows = df.iloc[:10].to_html(index=False)

    dist_data = plot_dist(df,num_col,u_col)
    corr_data = plot_corr(df,num_col)

    return render_template('Analysis.html', df=df.to_json(), df_cols=df_cols, top_rows=top_rows,rec_n=df_dim[0], col_n=df_dim[1], cat_col=cat_col, num_col=num_col, mis_val=mis_val, mis_detail=mis_detail, u_col=u_col, cols_data=cols_data, dist_data=dist_data, corr_data=corr_data)

def get_data(df):
    df_cols = df.columns.tolist()
    df_dim = df.shape   # shape

    cols_data = {i: {'type': '', 'sub_type': '', 'null_val': '', 'mini': '', 'maxi': '',
                     'mean': '', 'median': '', 'mode': '', 'st_dev': '', 'vari': '', 'Quant': '', 'iqr': ''} for i in df_cols}

    cat_col, num_col, u_col = [], [], []   # column types
    for i in df.columns:

        u_sum = len(pd.unique(df[i]))       # unique vales
        if u_sum == df_dim[0]:
            u_col.append(i)

        if df[i].dtype == 'object':
            cat_col.append(i)
            cols_data[i]['type'] = 'Categorical'
        else:
            num_col.append(i)
            cols_data[i]['type'] = 'Numerical'
            cols_data[i]['mini'] = df[i].min()
            cols_data[i]['maxi'] = df[i].max()
            cols_data[i]['mean'] = round(df[i].mean(), 2)
            cols_data[i]['median'] = df[i].median()
            cols_data[i]['st_dev'] = round(df[i].std(), 2)

            if i not in u_col:
                cols_data[i]['vari'] = round(df[i].var(), 2)
                cols_data[i]['Quant'] = [round(df[i].quantile(0.1), 3), round(df[i].quantile(0.7), 3)]
                cols_data[i]['iqr'] = round((cols_data[i]['Quant'][1] - cols_data[i]['Quant'][0]),3)

        cols_data[i]['sub_type'] = df[i].dtype.name

        cols_data[i]['null_val'] = df[i].isna().sum()

        if i not in u_col:                  # mode
            # convert series to list and to st and replaceing "'".
            cols_data[i]['mode'] = str(df[i].mode().tolist())[
                1:-1].replace("'", '')

    mis_val = df.isna().sum()  # missing values

    mis_detail = [(df_cols[i], mis_val[i]) for i in range(
        len(mis_val)) if mis_val[i] != 0]    # missing_val details

    data_df['df_cols'] = df_cols
    data_df['u_col'] = u_col
    data_df['num_col'] = num_col
    data_df['cat_col'] = cat_col
    data_df['mis_detail'] = mis_detail

    return df_cols, df_dim, cat_col, num_col, mis_val, mis_detail, u_col, cols_data


def plot_dist(df, num_col, u_col):

    fig_dist_data = {i:[] for i in num_col}
    num_col = [i for i in num_col if i not in u_col]
    for i in num_col:
        plt.close()

        histplot(df[i], kde=True, color="#051e50", alpha=0.85, shrink=0.65)
        plt.yticks([])
        plt.ylabel('')
        plt.xlabel('')
        despine(top=True, right=True, left=True, bottom=False)

        fig_buf = io.BytesIO()
        plt.savefig(fig_buf, format='png', bbox_inches='tight',pad_inches=0)
        fig_dist_data[i]=base64.b64encode(fig_buf.getbuffer()).decode("ascii")

    return fig_dist_data


def plot_corr(df,num_col):

    plt.close()

    fig_corr_data = []
    corr_method=['pearson','spearman','kendall']
    n_cols = len(num_col)

    if n_cols > 11:
        annot = False
    else:
        annot = True

    for i in range(3):
        plt.close()

        corr = df.corr(method=corr_method[i])

        if corr.shape[0] != 0:
            # Generate a mask for the upper triangle

            mask = np.triu(np.ones_like(corr, dtype=bool))
            
            heatmap(corr, cmap='coolwarm',mask=mask,vmin=-1, vmax=1, center=0,linewidths=.5, annot=annot, xticklabels=True, yticklabels=True,fmt='.2f')

            # Saving image to a temporary buffer.
            pear_buf = io.BytesIO()
            plt.savefig(pear_buf, format='png', bbox_inches='tight',pad_inches=0)
            fig_corr_data.append(base64.b64encode(pear_buf.getbuffer()).decode("ascii"))

    return fig_corr_data

@app.route('/Analysis/custom_plot',methods=['GET', 'POST'])
def plot_custom():

    try:
        df = data_df['data']
    except:
        return redirect(url_for('Analysis'))


    plt.close()

    cols_wo_unq = [i for i in data_df['df_cols'] if i not in data_df['u_col']]
    rel_plot_types = ['box','strip','scatter']
    dist_plot_types = ['box','violin','boxen','count','hist']

    if request.method == "POST":
        details = request.form.to_dict(flat=False)
        #print('---------------->')
        #print(details)
        
        if request.form['plot_type'] == "rel_plot":
            x_col = request.form['x_col']
            y_col = request.form['y_col']
            plot_type = request.form['rel_plot_type']

            if plot_type == 'strip' or plot_type == "box":
                catplot(x=x_col,y=y_col,data=df,kind=plot_type)
            else:
                relplot(x=x_col,y=y_col,data=df,kind="scatter")
        
            if len(df[x_col].unique()) >8:
                plt.xticks(rotation=90)
                

        else:
            col_name = request.form['dist_col']
            plot_type = request.form['dist_plot_type']
        
            if plot_type in ["box","violin",'boxen']:
                catplot(y=col_name,data=df,kind=plot_type)

            elif plot_type == "hist":
                histplot(x=col_name,data=df)
            
            else:
                countplot(x=col_name,data=df)
            
            if len(df[col_name].unique()) >8:
                plt.xticks(rotation=90)

        pear_buf = io.BytesIO()
        plt.savefig(pear_buf, format='png', bbox_inches='tight')
        fig_data = base64.b64encode(pear_buf.getbuffer()).decode("ascii")

        return render_template('custom-plot.html',cols=cols_wo_unq,data_df=data_df, rel_plot_types=rel_plot_types,dist_plot_types=dist_plot_types, fig_data = fig_data)


    return render_template('custom-plot.html',cols=cols_wo_unq,data_df=data_df, rel_plot_types=rel_plot_types, dist_plot_types=dist_plot_types)


'''@app.route('/feature_imp',methods = ['GET','POST'])
def feature_importance():
    df = data_df['data']

    # convert categorical to Numerical
    for i in df.columns:
        if df[i].dtype == 'object':
            df[i] = LabelEncoder().fit_transform(df[i])

    if request.method == 'POST':
        target_var = request.form['output_var']
    
    return render_template('feature_imp.html')'''

if __name__ == '__main__':
    app.run(debug=True)
