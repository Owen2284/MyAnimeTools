"""Modified version of code found at: https://sukhbinder.wordpress.com/2016/05/10/quick-gantt-chart-with-matplotlib/"""

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import WEEKLY,MONTHLY, DateFormatter, rrulewrapper, RRuleLocator 
import numpy as np
  
 
def createDate(datetxt):
	"""Creates the date"""
	year,month,day=datetxt.split('-')
	date = dt.datetime(int(year), int(month), int(day))
	#if (dt.datetime.now() - date) > dt.timedelta(days=1):
	#	date += dt.timedelta(days=1)
	mdate = matplotlib.dates.date2num(date)	
	return mdate
 
def createGanttChart(indatalist):
	"""Create gantt charts with matplotlib. Give list of tuples: (id, name, colour number, start date, end date).""" 

	# Initialise storage.
	ylabels = []
	customDates = []
	customColours = []
	colourTranslator = ["k", "g", "b", "y", "r", "c", "w"]

	# Store the incomping data in the correct lists, and format dates.
	for initem in indatalist:
		ylabel = initem[1]
		colourNum = initem[2]
		startdate = initem[3]
		enddate = initem[4]
		ylabels.append(ylabel)
		customDates.append([createDate(startdate),createDate(enddate)])
		customColours.append(colourTranslator[colourNum])

	# Convert data into dict with key ylabel and values [startDate, endDate]
	ilen=len(ylabels)
	pos = np.arange(0.5,ilen*0.5+0.5,0.5)
	task_dates = {}
	for i,task in enumerate(ylabels):
		task_dates[task] = customDates[i]

	# Plot and axis configuration.
	fig = plt.figure(figsize=(20,8))
	ax = fig.add_subplot(111)

	# Plotting the gantt bars.
	for i in range(len(ylabels)):
		 start_date,end_date = task_dates[ylabels[i]]
		 ax.barh((i*0.5)+0.5, end_date - start_date, left=start_date, height=0.36, align='center', edgecolor='black', color=customColours[i], alpha = 0.8, label=ylabels[i])

	# Other visualisation code.
	locsy, labelsy = plt.yticks(pos,ylabels)
	plt.setp(labelsy, fontsize = 14)
	#ax.axis('tight')
	ax.set_ylim(ymin = -0.1, ymax = ilen*0.5+0.5)
	ax.grid(color = 'g', linestyle = ':')
	ax.xaxis_date()
	rule = rrulewrapper(WEEKLY, interval=1)
	loc = RRuleLocator(rule)
	#formatter = DateFormatter("%d-%b '%y")
	formatter = DateFormatter("%d-%b")
	ax.xaxis.set_major_locator(loc)
	ax.xaxis.set_major_formatter(formatter)
	labelsx = ax.get_xticklabels()
	plt.setp(labelsx, rotation=30, fontsize=10)
	font = font_manager.FontProperties(size='small')
	#ax.legend(loc=1,prop=font)
	ax.invert_yaxis()
	fig.autofmt_xdate()

	# Returning the Gantt chart.
	return plt