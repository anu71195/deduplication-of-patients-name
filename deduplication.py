import csv
import math
import data

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




def read_file(file_name):
	fp=open(file_name,"r");
	text=(csv.DictReader(fp));
	dataset=[];
	for row in text:
		dataset.append(row);
	fp.close();
	return dataset;

def write_file(unique_names,file_name):
	fw=open(file_name,"w")
	writer=csv.DictWriter(fw,fieldnames=['fn','ln','gn','dob']);
	writer.writeheader();
	for entry in unique_names:
		writer.writerow(entry)


dataset=read_file(data.training_file)
count_unique_training=data.count_unique_training;
cost_distance=math.inf;
m=len(dataset);#m=number of training examples
threshold=-1;
flag=1;
print("TRAINING DATA TAKEN FROM",data.training_file,"FILE")
print("TRAINING...\n")
while flag :
	threshold+=1;
	counter=0;
	dob_weight=threshold;
	gender_weight=threshold*2;
	unique_names=[];
	labels={};
	for i in range(m):
		labels[i]=-1;
	for i in range(len(dataset)):
		for j in range(len(dataset)):
			costfn=levenstein(dataset[i]['fn'],dataset[j]['fn'])
			costln=levenstein(dataset[i]['ln'],dataset[j]['ln'])
			dobcost=(dataset[i]['dob']!=dataset[j]['dob'])*dob_weight
			gendercost=(dataset[i]['gn']!=dataset[j]['gn'])*gender_weight
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
	
	if cost_distance> abs(len(unique_names)-count_unique_training):
		cost_distance=abs(len(unique_names)-count_unique_training);
		optimum_threshold=threshold;
		flag=1;
	else: 
		flag=0;
	print(len(unique_names),"----",threshold);

print("\nOPTIMUM THRESHOLD FOUND...")
print("SYSTEM TRAINED")
print("OPTIMUM THRESHOLD = ",optimum_threshold)


print("\nTESTING...",end="")
dataset=read_file(data.testing_file)
threshold=optimum_threshold;
counter=0;
dob_weight=threshold;
gender_weight=threshold*2;
unique_names=[];
labels={};
for i in range(m):
	labels[i]=-1;
for i in range(len(dataset)):
	for j in range(len(dataset)):
		costfn=levenstein(dataset[i]['fn'],dataset[j]['fn'])
		costln=levenstein(dataset[i]['ln'],dataset[j]['ln'])
		dobcost=(dataset[i]['dob']!=dataset[j]['dob'])*dob_weight
		gendercost=(dataset[i]['gn']!=dataset[j]['gn'])*gender_weight
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
print("DONE")
print("GENERATING OUTPUT IN ",data.output_file,"FILE...",end="")
write_file(unique_names,data.output_file);
print("DONE")
# print(len(unique_names),"----",threshold);
# print(unique_names)