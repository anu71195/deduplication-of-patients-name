import csv
import math
import data
#data library has been created to add the data from outside like name of the input files, training file, output files and the number of unique entries in training file
#Levenstein function gives the difference between two strings(here names) the output given is the minmum edit delete or additions done
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



#reading data from the file mentioned in data.py library and return it in the form of dataset
def read_file(file_name):
	fp=open(file_name,"r");
	text=(csv.DictReader(fp));
	dataset=[];
	for row in text:
		dataset.append(row);
	fp.close();
	return dataset;

#writing a csv file with the unique names and the file given in the data.py library
def write_file(unique_names,file_name):
	fw=open(file_name,"w")
	writer=csv.DictWriter(fw,fieldnames=['fn','ln','gn','dob']);
	writer.writeheader();
	for entry in unique_names:
		writer.writerow(entry)


dataset=read_file(data.training_file)
count_unique_training=data.count_unique_training;#unique names given in the training set
cost_distance=math.inf;
m=len(dataset);#m=number of training examples
threshold=-1;#while training start the threshold with 0 (in loop +1 is added to do so) and then increment it each time by one till we are getting better solution 
flag=1;
print("TRAINING DATA TAKEN FROM",data.training_file,"FILE")
print("TRAINING...\n")
while flag :
	threshold+=1;
	counter=0;
	dob_weight=threshold;#this tells that if dob are not equal then also the person are different
	gender_weight=threshold*2;#this tells that if gender is different then the person are surely different
	unique_names=[];
	labels={};
	for i in range(m):
		labels[i]=-1;
	for i in range(len(dataset)):
		for j in range(len(dataset)):
			costfn=levenstein(dataset[i]['fn'],dataset[j]['fn'])#cost of first name  of every pair
			costln=levenstein(dataset[i]['ln'],dataset[j]['ln'])#cost of second name of every pair
			dobcost=(dataset[i]['dob']!=dataset[j]['dob'])*dob_weight#dob cost of every pair
			gendercost=(dataset[i]['gn']!=dataset[j]['gn'])*gender_weight#gender cost of every pair
			if(costfn+costln+dobcost+gendercost<threshold): #sorting the names in unique and same names
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
	labels=sorted(labels.items(),key=lambda k:k[1])#sorting in by the label number
	counter=0;
	for rows in labels:#finding all the unique names
		if counter<=rows[1]:
			unique_names.append(dataset[rows[0]]);
			counter=rows[1]+1;
	
	if cost_distance> abs(len(unique_names)-count_unique_training):#deciding how long the loop should run if no development in the optimum threshold break
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
label_counter=0;
temp_labels={};
temp=-1;
for rows in labels:
	if temp==rows[1]:
		temp_labels[rows[0]]=label_counter;
	else :
		label_counter+=1;
		temp_labels[rows[0]]=label_counter;
	temp=rows[1];		
	if counter<=rows[1]:
		unique_names.append(dataset[rows[0]]);
		counter=rows[1]+1;
		# print(unique_names)
y_labels=[0 for _ in range(m)]
for rows in temp_labels:
	y_labels[rows]=temp_labels[rows]
	# print(rows)

# print(labels)
# print(y_labels)
print("DONE")
print("GENERATING OUTPUT IN ",data.output_file,"FILE...",end="")
write_file(unique_names,data.output_file);
print("DONE")
print("NUMBER OF UNIQUE NAMES GENERATED ARE",len(unique_names))
