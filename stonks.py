import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import os

def getData():
	dataDict = {}
	historicalStockData = {}

	for root, dirs, files in os.walk("./data"):		
		for filename in files:
			if(filename.endswith('csv')):
				data_df = pd.read_csv("./data/"+filename)['Close Price']	
				historicalStockData[filename[:-4]] =  data_df.to_numpy()
	return historicalStockData


def run(days = 200):
	dataDict = getData()
	tradeMarkers = []
	netProfit = 0 
	for key in dataDict:
		movingAvgs = []
		vals = dataDict[key]
		movingAvg = np.sum(vals[:days]) / days
		movingAvgs.append(movingAvg)
		holding = False
		spent = 0
		earned = 0
		lastBuy = None
		for i in range(days, len(vals) - 1):
			movingAvgs.append(movingAvg)
			if holding and vals[i] > movingAvg:     #sell signal
				holding = False
				#print("moving avg is " + str(movingAvg) + " and selling at " + str(vals[i]) + " for notional pnl of " + str(vals[i] - lastBuy))
				earned += vals[i]
				tradeMarkers.append('Sell')
			elif not holding and vals[i] < movingAvg:     #buy signal
				holding = True
				#print("moving avg is " + str(movingAvg) + " and buying at " + str(vals[i]))
				spent += vals[i]
				lastBuy = vals[i]
				tradeMarkers.append('Buy')
			else:
				tradeMarkers.append(None)

			#print(movingAvg)
			movingAvg += (vals[i] - vals[i - days]) / days
			#print(movingAvg)
		if holding:
			earned += vals[-1]		#clear position at the end
			#print("selling at " + str(vals[-1]))
		# plt.plot(movingAvgs)
		# plt.plot(vals[days:len(vals)-1])
		# plt.title(key)
		# plt.show()
		netProfit = netProfit + earned - spent
		print(key + "           " + str((earned - spent)))	
	print("")
	print("Net Profit " + "  " + str(netProfit))
#print(getData())
run()