import pandas as pd
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import argparse
sns.set()

def parseInput():
	parser = argparse.ArgumentParser()
	parser.add_argument("--venderid", help="Enter the venderid", default='*')
	parser.add_argument("--month", help="Enter the month to run analysis for. Format (YYYY-MM)", default='*')
	args = parser.parse_args()
	return args.venderid,args.month

def main():
	print('Cash Vs. Credit Distribution For Trips Under $150')
	#Read the VenderId and Month
	venderid, month = parseInput()
	extracted_files = glob.glob('..\\..\\Data\\{0}\\{1}\\processed\\*.csv'.format(venderid, month))
	df = pd.DataFrame()
	list_ = []
	for fileName in extracted_files:
		short_df = pd.read_csv(fileName)
		list_.append(short_df)
	df = pd.concat(list_)
	
	df = df[df['pickup_area'] != 'Not Specified']
	df = df[df['dropoff_area'] != 'Not Specified']
	
	print('Filtering Cash and Credit Card Payments')
	df = df[df['payment_type'].isin([1,2])]
	
	df['payment_type'] = df.payment_type.apply(lambda x: 'Credit' if x == 1 else 'Cash')
	df = df.rename(columns = {'dropoff_area':'Dropoff Area', 'payment_type':'Payment Type', 'total_amount':'Amount'})
	
	grouped_series_df = df['Amount'].groupby([df['Dropoff Area'], df['Payment Type']]).mean()
	grouped_df = grouped_series_df.to_frame()
	grouped_df = grouped_df.reset_index()
	grouped_df = grouped_df.round(2)
	grouped_df
	
	#store the output in csv
	report_name = 'reports\\csv\\'
	
	#Create reports folder if not exists
	if not os.path.exists(report_name):
		os.makedirs(report_name)
	
	save_file_name = None
	if not venderid == '*':
		save_file_name = venderid+'_'
	else:
		save_file_name = 'All_'
		
	if not month == '*':
		save_file_name = save_file_name+month+'_'
	else:
		save_file_name = save_file_name+'All_'
	
	save_file_name = save_file_name+dt.datetime.strftime(dt.datetime.now(),'%Y_%m_%d_%H_%M_%S')
	
	grouped_df.to_csv(report_name+save_file_name+'.csv', sep=',', encoding='utf-8', index=False)
	print('CSV output saved to: {0}'.format(report_name+save_file_name+'.csv'))
	create_violin_plot(df, save_file_name)
	print('End')
	
def create_violin_plot(df, save_file_name):
	plt.subplots(figsize=(20,10))
	rc={'font.size': 24, 'axes.labelsize': 24, 'legend.fontsize': 24.0, 
		'axes.titlesize': 32, 'xtick.labelsize': 18, 'ytick.labelsize': 18}
	sns.set(rc=rc, style='whitegrid')
	violin_plot = sns.violinplot(x="Dropoff Area", y="Amount", hue="Payment Type", data=df, split=True,
								 inner="quart", palette={"Cash": "#DC143C", "Credit": "#FF8C00"})
	violin_plot.set_ylim(-25, 200)

	#title
	violin_plot.set_title('Cash Vs. Credit Distribution For Trips Under $150')
	violin_plot.title.set_fontsize(36)
	violin_plot.title.set_position([.5, 1.02])
	violin_plot.title.set_fontweight(weight='bold')
	violin_plot.title.set_color('#4D4D4D')

	#XyLabels
	violin_plot.xaxis.get_label().set_fontsize(30)
	violin_plot.xaxis.get_label().set_fontweight(weight='bold')
	violin_plot.xaxis.get_label().set_color('#4D4D4D')

	violin_plot.yaxis.get_label().set_fontsize(30)
	violin_plot.yaxis.get_label().set_fontweight(weight='bold')
	violin_plot.yaxis.get_label().set_color('#4D4D4D')

	#Ticks
	plt.setp(violin_plot.get_xticklabels(), rotation=45, fontsize=24, color='#B2912F', fontweight='bold')
	plt.setp(violin_plot.get_yticklabels(), fontsize=24, color='#B2912F', fontweight='bold')

	violin_plot.set(xlabel='Dropoff Area', ylabel='Trip Amount')

	sns.despine(left=True)
	sns.despine(left=True)
	
	#store the output in csv
	report_name = 'reports\\png\\'
	
	#Create reports folder if not exists
	if not os.path.exists(report_name):
		os.makedirs(report_name)
	
	plt.gcf().subplots_adjust(bottom=0.25)
	plt.savefig(report_name+save_file_name+'.png', dpi=200, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=1.0,
        frameon=None)
	print('Graph output stored to: {0}'.format(report_name+save_file_name+'.png'))
	
main()