import csv
import math

def levenstein(str1,str2):
	m=len(str1)
	n=len(str2)
	dp=[[0 for _ in range(n+1)] for _ in range(m+1)]#dp is a (m+1)*(n+1) matrix
	for i in range(n+1):
		dp[0][i]=i;
	for j in range(m+1):
		dp[j][0]=j;
	for i in range(n+1):
		for j in range(m+1):
			if str1[j-1]==str2[i-1]:
				dp[j][i]=dp[j-1][i-1]
			else :
				dp[j][i]=1+min(dp[j-1][i-1],dp[j-1][i],dp[j][i-1]);
	return dp[m][n];


fp=open("training_data.csv","r");
text=(csv.DictReader(fp));
count_unique_training=42;
dataset=[];
for row in text:
	dataset.append(row);
m=len(dataset);#m=number of training examples
for threshold in range(10):
	counter=0;
	dob_weight=threshold;
	gender_weight=threshold*2;
	unique_names=[];
	labels={};
	for i in range(m):
		labels[i]=-1;
	train_data=dataset[0:math.floor(7*m/10)];
	validation_data=dataset[math.ceil(7*m/10):];

	for i in range(len(dataset)):
		for j in range(len(dataset)):
			costfn=levenstein(dataset[i]['fn'],dataset[j]['fn'])
			costln=levenstein(dataset[i]['ln'],dataset[j]['ln'])
			dobcost=dataset[i]['dob']!=dataset[j]['dob']
			gendercost=dataset[i]['gn']!=dataset[j]['gn']
			dobcost*=dob_weight;
			gendercost*=gender_weight;
			if(costfn+costln+dobcost+gendercost<threshold):
				if labels[j]==-1 and labels[i]==-1:
					labels[j]=counter;
					counter+=1;
					labels[i]=labels[j]
				else :
					if labels[j]==-1:
						labels[j]=labels[i];
					elif labels[i]==-1:
						labels[i]=labels[j]
					else :
						labels[i]=min(labels[i],labels[j]);
						labels[j]=labels[i]


			else:
				if labels[i]==-1:
					labels[i]=counter;
					counter+=1;
				if labels[j]==-1:
					labels[j]=counter;
					counter+=1;
	labels=sorted(labels.items(),key=lambda k:k[1])
	counter=0;
	for rows in labels:
		if counter<=rows[1]:
			unique_names.append(dataset[rows[0]]);
			counter=rows[1]+1;
	if threshold==5:
		print(unique_names)

