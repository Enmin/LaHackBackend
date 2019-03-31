import pymongo
from bson.objectid import ObjectId
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["sizer_db"]
mycol_login = mydb["user_login_info"]
mycol_logininfo = mydb["user_info"]
def get_user(username):
	li=[]
	for x in mycol_login.find({"username":username}):
		li.append(x)
	return li
def create_new_user(username,password,gender):
	usr=get_user(username)
	if len(usr)!=0:
		print("User exists already.Please login")
	else:
		new_usr={"username":username,"password":password,"self-identified gender":gender,"num_data":0,"data":[]}
		z = mycol_login.insert_one(new_usr)

	# def update_info():

def login(username,password):
	usr=get_user(username)
	if len(usr)==0:
		print("This user does not exist. Please signup first")
	else:
		user=usr[0]
		if (password==user["password"]):
			print("You've successfully logged in!")
		else:
			print("Wrong password")
def construct_new_user_info(username,date,m1,m2,m3):
	info= {"username":username,"date":date,"m1":m1,"m2":m2,"m3":m3}
	return info
info = construct_new_user_info("aurora","03_29_2019",10,20,30)
def add_new_user_info(info):
	#add an order to order
	user_info=info

	#increase the order number of user
	r=get_user(info["username"])
	num_data=r[0]["num_data"]
	info["userid"]=r[0]['_id']
	num_data+=1

	orderID = mycol_logininfo.insert(user_info)
	print(orderID)
	print(type(orderID))
	#key="order"+str(num_order)
	#add orderID to user
	data_pre=view_prev_data(info["username"])
	fg=1
	for dt in data_pre:
		if dt["date"]== info["date"]:
			mydb.user_info.remove( {"_id": dt["objectid"]});
			dt["objectid"]=orderID
			num_data-=1
			fg = 0
	if fg == 1:
		data_pre.append({"date":info["date"],"objectid":orderID})
	new_data_user={"$set":{"data":data_pre}}
	query={'_id':r[0]['_id']}
	new_num={"$set":{"num_data":num_data}}
	mycol_login.update_one(query,new_data_user)
	mycol_login.update_one(query,new_num)


def view_prev_data(username):
	r=get_user(username)
	data=r[0]["data"]
	return data
	# orders=[]
	# for x in order_id.values():
	# 	for y in mycol_order.find({"_id":x}):
	# 		orders.append(y)
	# return orders

#


u1=create_new_user("aurora","12345","female")
u2=create_new_user("jenny","123","female")
info = construct_new_user_info("aurora","03_29_2019",10,20,30)
info2 = construct_new_user_info("aurora","03_29_2019",10,20,40)
add_new_user_info(info2)
# #print(view_upcoming_order("aurora"))
# # cancel_order("aurora",ObjectId('5c3a4afc2c0147cd96b8e34d'))
# set_deliver_time("jenny","01_30_12_00","01_30_13_00")
# print(deliver_recommendation("jenny"))
# # print(get_deliver_time("aurora"))
# # accept_deliver_task("aurora",ObjectId('5c3a60292c0147cf1ed099e7'))




















