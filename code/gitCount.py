#!/usr/bin/env python3
#-*- coding:utf-8 -*-

__author__='xuehao'


import time
import re
import json
import os
import sys
import requests
import gitTime

							
##########################
##########################
#	class Info
#	to save the informations of the commit in the repo.
###########################
########################### 
class Info():
	def __init__(self):
	#commit info:
		self.commit_dic={}	#show_commit_dic(False) { 0:[commit,time,diff,email,info] }
		self.commit_list=[]
		self.time_list=[]	#show_commit_time()
		self.commit_lenth=0
	#other info:
		self.user_email=[]
		self.time_diff=[]

	#####
	#	Functions
	#	
	########################################################################################
	#	1.1  get_time_diff(time_list):compute the differece of the time between two commits
	########################################################################################
	def get_time_diff(self):
		p_time = re.compile("(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\:(\S+)\:(\S+)\s+(\S+)")
		i=0
	#for each member in time_list , turn it in to Time(class),and set the 'time_diff' as the new member of the time_list 	
		while(i<len(self.time_list)):
			cp_time=p_time.search(self.time_list[i])
			time=gitTime.Time()		
			time.set(cp_time.group(7),cp_time.group(2),cp_time.group(3),cp_time.group(4),cp_time.group(5),cp_time.group(6))
			self.time_list[i]=time		
			i=i+1
		i=0	
		while(i<len(self.time_list)-1):			
			self.time_diff.append(self.time_list[i].diff(self.time_list[i+1]))
			i=i+1
		self.time_diff.append(-1)	#for the first commit we set de diff_time as -1.	

	#######################################################################################################################################
	#	1. INIT FUNCTION. 
	# 	get_commit_dic(self,st_time,ed_time):for each commit get the commit_id and commit_time and return two list. 
	#######################################################################################################################################
	def get_commit_dic(self,st_time=gitTime.Time(),ed_time=gitTime.Time()):#get commit and commit_time
		cmd = "git log -1"		#"git log" for listing out commit data
		output = os.popen(cmd)
		info = output.read()
	#get commit in commit_list and time in time_list
		#last commit:	
		p_commit = re.compile("commit (\w+)")
		p_date = re.compile("Date\:\s+(\S+ \S+ \S+ \S+ \S+)")
		p_email = re.compile("<\S+@\S+>")
		last_commit = p_commit.search(info).group(1)
		last_email = p_email.search(info).group(0)
		last_time = p_date.search(info).group(1)		
		self.commit_list.append(last_commit)		
		self.time_list.append(last_time)
		self.user_email.append(last_email)
		print("last commit: " , last_commit,"\nlast time:",last_time , "\nlast email:",last_email)
	
		#other commit:
		sha=last_commit
		while(sha!=None):
			print(sha,len(self.commit_list))
			cmd = "git log -1 " + sha +'^'
			output = os.popen(cmd)
			info = output.read()
		#get time in time_list			
			try:	
				sha=p_commit.search(info).group(1)
				all_time=p_date.search(info).group(1)
				email=p_email.search(info).group(0)
				self.commit_list.append(sha)
				self.time_list.append(all_time)
				self.user_email.append(email)			
			except:
				print("first of the commit")
				break	
	#compare the lenth of the commit_list and time_list to confirm the lists have the same lenth.	
		if(len(self.commit_list)!=len(self.time_list)!=len(user_email)):
			print("miss data in Info FUN get_commit_dic!")
			print("error data!")
			exit()
		else:
			self.commit_lenth=len(self.commit_list)
	#get difference between time
		self.get_time_diff()		
	#init commit_dic for all data 	
		for i in range(0,len(self.commit_list)):
			self.commit_dic[i]=[self.commit_list[i],self.time_list[i],self.time_diff[i],self.user_email[i]]
			

	#get datas from st_time to ed_time
		#time_now=Time()
		#time_now.set_str(str(time.strftime('%Y %m %d %H %M %S',time.gmtime())))
		i=0		
		temp={}
		for key in self.commit_dic:
			if(st_time.cmp_with(self.commit_dic[key][1])==False):
				if(self.commit_dic[key][1].cmp_with(ed_time)==False):
					temp[i]=self.commit_dic[key]
					i+=1	
				else:
					continue		
		try:		
			self.commit_dic=temp
			self.commit_lenth=len(self.commit_dic)
		except:
			print('ed_time error in Info FUN get_commit_dic!')

	


	#####################################################################################################################
	#		2.show_commit_list()
	####################################################################################################################
	def show_commit_list(self):
		print(self.commit_list)	


	######################################################################################################################
	#		3.show_commit_time()
	########################################################################################################################
	def show_time_list(self):
		for i in self.time_list:
			i.show()

	#################################################################################################################
	#		4.show_commit_dic(diff)  
	#	diff = true : show more information											
	#################################################################################################################
	def show_commit_dic(self,diff=False):
		for key in self.commit_dic:
			print(self.commit_dic[key][0])
			self.commit_dic[key][1].show()
			if(diff):			
				print(self.commit_dic[key][2])
			print(self.commit_dic[key][3])
			try:
				print(self.commit_dic[key][4])
			except:
				continue
	
	
################################
################################
#	class coder
################################
################################
class Coder:
	def __init__(self):
		#user info:
		self.user_stats={}
		self.user_sort=[]	#show_user_sort()
		self.user_num=0
	
	
	####################################################################
	#	1.1  is_merge(commit_sha):to confirm the commit is not been merged.
	####################################################################
	def is_merge(self,commit_sha):
		cmd = "git log -1 " + commit_sha
		output = os.popen(cmd)
		title = output.read()
		p_merge = re.compile("Merge")
		if(p_merge.search(title) is not None):
			print('merge')
			return True
		else:
			return False


	###################################################################
	#	INIT FUNC
	#	1.collect_stats:for each commit get commit informations.
	# 	information include lines of code in each commit 
	###################################################################
	def collect_stats(self,commit_dic):
		for key in commit_dic:
			print(key)
			m=commit_dic[key][0]
			t=commit_dic[key][2]
			#ignore merge commit
			if(self.is_merge(m)):
				#print('Pass!:',m,' is a Merge commit')
				git_show_command = "git show -s --format=%an " + m		
				output = os.popen(git_show_command)
				user = output.read().strip(' \t\n\r')
				if(user in self.user_stats):
					stats = self.user_stats[user]
					stats['commit_times'] += 1
					p_email=re.compile(commit_dic[key][3])
					if(p_email.search(stats['email']) == None):
						stats['email'] = stats['email'] +commit_dic[key][3]
					self.user_stats[user] = stats
				else:
					new_stat = {'additions':0, 'deletions':0, 'total':0, 'contribute':0,'email':commit_dic[key][3], 'commit_times':1}
					self.user_num+=1
					self.user_stats[user] = new_stat
				info='Pass! Merge commit'		
				commit_dic[key].append(info)
				continue
		
			#get user and commit data
			git_show_command = "git show -s --format=%an " + m		
			output = os.popen(git_show_command)
			user = output.read().strip(' \t\n\r')
			#print(git_show_command)
			#print(user)
		
			if(m==commit_dic[len(commit_dic)-1][0]):#if m is the first commit
				git_diff_command="git diff --shortstat "+m
			else:
				git_diff_command = "git diff --shortstat "+m + " " + m + "^"
			output = os.popen(git_diff_command)
			data = output.read()
			#print(git_diff_command)
			#print(m,data)
		
			p_ins = re.compile("(\d+) insertion")
			r_ins = p_ins.search(data)

			ins_data = 0
			del_data = 0

			if(r_ins is not None):
				ins_str = r_ins.group(1)
				ins_data = int(ins_str)
	

			p_del = re.compile("(\d+) deletion")
			r_del = p_del.search(data)

			if(r_del is not None):
				del_str = r_del.group(1)
				del_data = int(del_str)
		 
			#ignore those commit which ins(line)/time(s) is more than 1/60.(assume that a man can code one line in a minute)
			if(t=="-1" or t=='-1'):
				#print("ok!: "+m[0:7])
				info='ok!'			
			elif(ins_data/float(t)<float(1/60)):
				#print("ok!: "+m[0:7])
				info='ok!'			
			else:
				#print("Pass!: "+m[0:7]+' commiter:'+user+' commit too ofen ',ins_data/t,' lines/s')		
				info='Pass! too fast to be true!' + str(ins_data/t) +'lines/s'				
				ins_data = 0
				del_data = 0
			
			#save the data
			#########----------------------------how to count contribute----------------------------###########	
			if(user in self.user_stats):
				stats = self.user_stats[user]
				stats['additions'] += ins_data
				stats['deletions'] += del_data
				stats['total'] += (ins_data + del_data)
				stats['contribute'] += (ins_data*0.7+del_data*0.3)
				stats['commit_times'] += 1
				p_email=re.compile(commit_dic[key][3])
				if(p_email.search(stats['email']) == None):
					stats['email'] = stats['email'] +commit_dic[key][3]
				self.user_stats[user] = stats
			else:
				new_stat = {'additions':ins_data, 'deletions':del_data, 'total':ins_data+del_data, 'contribute':ins_data*0.7+del_data*0.3, 'email':commit_dic[key][3], 'commit_times':1}
				self.user_num+=1
				self.user_stats[user] = new_stat
				
			#save information				
			commit_dic[key].append(info)


	#################################################################################################################
	#		2.sort_coder()
	#################################################################################################################
	def sort_coder(self):
		temp=[]
		for i in self.user_stats:
			temp.append(  [i,"add:"+str(self.user_stats[i]['additions']),"del:"+str(self.user_stats[i]['deletions']),"tot:"+str(self.user_stats[i]['total']),self.user_stats[i]['contribute'],"commit_times:"+str(self.user_stats[i]['commit_times']),"email:"+str(self.user_stats[i]['email'])]  )
		temp.sort(key=lambda x:x[4],reverse=True)		
		assert self.user_num==len(temp),'error in FUNC:sort_coder!'
		self.user_sort=temp
		

	#################################################################################################################
	#		3.show_user_sort()
	#################################################################################################################
	def show_user_sort(self):
		for i in self.user_sort:
			print(i)

###################################################################
#	main program
###################################################################
if __name__=='__main__':
	#init time
	st_time=gitTime.Time()
	ed_time=gitTime.Time()
	st_time.set(2010,12,1,0,0,100)
	ed_time.set(2016,1,1,0,0,0)
	 
	#init commit 
	commit=Info()
	commit.get_commit_dic(st_time,ed_time)

	#init user info
	user=Coder()
	user.collect_stats(commit.commit_dic)
	user.sort_coder()
	user.show_user_sort()	

	##########################################
	#	result
	##########################################
	#commit.show_commit_dic(False)
	#commit.show_commit_list()
	#commit.show_time_list()




