import pymysql

from menu import menu


class SMDBHandler:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def getSize2(self):
        mydb = None
        mydbCursor = None
        login = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select size,price from customized_pizza"
            mydbCursor.execute(sql)
            row = mydbCursor.fetchall()
            if len(row) > 0:
                login = row
            else:
                login = None
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return login

    def priceMenu(self):
        mydb = None
        mydbCursor = None
        login = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select size,price from price"
            mydbCursor.execute(sql)
            row = mydbCursor.fetchall()
            if len(row) > 0:
                login = row
            else:
                login = None
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return login

    def getMenu2(self):
        mydb = None
        mydbCursor = None
        login = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select pizza_name from menu"
            mydbCursor.execute(sql)
            row = mydbCursor.fetchall()
            if len(row) > 0:
                login = row
            else:
                login = None
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return login

    def pizzaMenu(self):
        mydb = None
        mydbCursor = None
        login = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()

            sql = "select pizza_name,ingredients,discount,path from menu"
            mydbCursor.execute(sql)
            row = mydbCursor.fetchall()
            if len(row) > 0:
                login = row
            else:
                login = None
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return login

    def add_order(self, name, phno, add):
        mydb = None
        mydbCursor = None
        login = None
        row = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()

            sql = "insert into customer (name,phone,address,status) values(%s,%s,%s,%s)"
            args = (name, phno, add, "unprocessing")
            mydbCursor.execute(sql, args)
            mydb.commit()
            SQL = "SELECT cust_id FROM customer where name=%s ORDER BY ABS(TIMESTAMPDIFF(SECOND, date_column, NOW())) LIMIT 1"
            mydbCursor.execute(SQL, name)
            login = mydbCursor.fetchone()

            if login is None or login == "()":
                login = None
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return login

    def sign_in(self, username, password):
        mydb = None
        mydbCursor = None
        flag = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select username,password from registration where username=%s"
            args = (username)
            mydbCursor.execute(sql, args)
            row = mydbCursor.fetchone()
            if row is not None or row != "()":
                if row[0] == username and row[1] == password:
                    flag = True
            else:
                flag = False
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def sign_up(self, fullname, username, email, password):
        mydb = None
        mydbCursor = None
        flag = False
        try:

            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select username from registration where username=%s"
            args = (username)
            mydbCursor.execute(sql, args)
            row = mydbCursor.fetchone()
            if row != "()" or row is not None:
                sql = "insert into  registration (email,password,loyality_points,fullName,username) values(%s,%s,%s,%s,%s)"
                args = (email, password, 0, fullname, username)
                mydbCursor.execute(sql, args)
                mydb.commit()
                flag = True
            else:
                flag = False
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def add_pizza(self, id, name, size, price):
        mydb = None
        mydbCursor = None
        flag = False
        try:

            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "insert into cust_pizza (cust_id,pizza_name,size,price) values(%s,%s,%s,%s)"
            args = (id, name, size, price)
            mydbCursor.execute(sql, args)
            mydb.commit()
            flag = True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def updateCart(self, id, count, sum):
        mydb = None
        mydbCursor = None
        flag = False
        try:

            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "update customer set price=%s, quantity=%s where cust_id=%s "
            args = (sum, count, id)
            mydbCursor.execute(sql, args)
            mydb.commit()
            flag = True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def updateCartt(self, id, count, sum, uname):
        mydb = None
        mydbCursor = None
        flag = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select reg_id,loyality_points from registration where username=%s"
            mydbCursor.execute(sql,uname)
            r1 = mydbCursor.fetchone()
            lPoints = r1[1]
            if lPoints >= 1000 and count == 1:
                sum=0
                lPoints = "You got a free Pizza :)"
                sql = "update registration set loyality_points=%s where username=%s"
                mydbCursor.execute(sql,(0,uname))
                mydb.commit()
            else:
                lPoints = lPoints + 100
                sql = "update registration set loyality_points=%s where username=%s"
                mydbCursor.execute(sql,(lPoints,uname))
                mydb.commit()
                lPoints = uname+"you have " + str(lPoints) + " loyality points"
            sql = "update customer set reg_id=%s,price=%s, quantity=%s where cust_id=%s "
            args = (r1[0],sum, count, id[0])
            mydbCursor.execute(sql, args)
            mydb.commit()
            flag = lPoints
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag
    def getLoyalityPoints(self,uname):
        mydb = None
        mydbCursor = None
        flag = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select loyality_points from registration where username=%s"
            mydbCursor.execute(sql,uname)
            r1 = mydbCursor.fetchone()
            lPoints = r1[0]
            flag = lPoints
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag
    
    # Admin INterface

    def addpizza(self, obj, path, s, m, l):
        mydb = None
        mydbCursor = None
        flag = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "insert into menu(pizza_name,ingredients,discount,path) values(%s,%s,%s,%s)"
            arg = (obj.pizza_name, obj.ingredients, obj.discount, path)
            mydbCursor.execute(sql, arg)
            mydb.commit()
            sql = "select pizza_id from menu where pizza_name=%s"
            mydbCursor.execute(sql, obj.pizza_name)
            id = mydbCursor.fetchone()
            # print(id)
            if id is not None or id != "()":
                sql = "insert into price (pizza_id,size,price) values(%s,%s,%s) "
                mydbCursor.execute(sql, (id, 'S', s))
                mydb.commit()
                sql = "insert into price (pizza_id,size,price) values(%s,%s,%s)"
                mydbCursor.execute(sql, (id, 'M', m))
                mydb.commit()
                sql = "insert into price (pizza_id,size,price) values(%s,%s,%s)"
                mydbCursor.execute(sql, (id, 'L', l))
                mydb.commit()

                flag = True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def show_pizza(self):

        mydb = None
        mydbCursor = None
        flag = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select * from menu"
            mydbCursor.execute(sql)
            row = mydbCursor.fetchall()
            # if len(row) > 0:
            #     flag = row
            flag = row
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def deletepizza(self, name):
        mydb = None
        mydbCursor = None
        flag = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "delete from menu where pizza_name=%s"
            args = (name)
            mydbCursor.execute(sql, args)
            mydb.commit()
            flag = True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def updatepizza(self, pizza_name, Cd, path, s, m, l):
        mydb = None
        mydbCursor = None
        login = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select pizza_id from menu where pizza_name=%s"
            mydbCursor.execute(sql, pizza_name)
            id = mydbCursor.fetchone()
            # print(id[0])
            # -----
            sql = "update menu set "
            flag = True
            flag2 = True
            arg = []
            if Cd.pizza_name != "":
                if flag:
                    sql += "pizza_name = %s"
                    arg.append(Cd.pizza_name)
                    flag = False
                else:
                    sql += " and pizza_name = %s"
                    arg.append(Cd.pizza_name)
            if Cd.ingredients != "":
                if flag:
                    sql += "ingredients = %s"
                    arg.append(Cd.ingredients)
                    flag = False
                else:
                    sql += " and ingredients = %s"
                    arg.append(Cd.ingredients)
            if Cd.discount != "":
                if flag:
                    sql += "discount = %s"
                    arg.append(int(Cd.discount))
                    flag = False
                else:
                    sql += " and  discount = %s"
                    arg.append(int(Cd.discount))
            if path != "":
                if flag:
                    sql += "path = %s"
                    arg.append(path)
                    flag = False
                else:
                    sql += " and  path = %s"
                    arg.append(path)
            id = id[0]
            if s != "":
                flag2 = False
                sql = "update price set price=%s where pizza_id=%s and size=%s "
                mydbCursor.execute(sql, (s, id, 'S'))
                mydb.commit()
            if m != "":
                flag2 = False
                sql = "update price set price=%s where pizza_id=%s and size=%s "
                mydbCursor.execute(sql, (m, id, 'M'))
                mydb.commit()
            if l != "":
                flag2 = False
                sql = "update price set price=%s where pizza_id=%s and size=%s"
                mydbCursor.execute(sql, (l, id, 'L'))
                mydb.commit()
            if flag != True:
                sql += " where pizza_name = %s"
                arg.append(pizza_name)
                arg = tuple(arg)
                # print(sql)
                # print(arg)
                mydbCursor.execute(sql, arg)
                row = mydb.affected_rows()
                mydb.commit()
                # print(row)
                if row > 0:
                    login = True
            if flag2 != True:
                login = True

        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return login

    def check_update_pizza(self, pizza_name):
        mydb = None
        mydbCursor = None
        flag = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select * from menu  where pizza_Name=%s "
            arg = (pizza_name)
            row = mydbCursor.execute(sql, arg)
            if row > 0:
                flag = True
            else:
                flag = False
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def show_unprocessed(self):

        mydb = None
        mydbCursor = None
        flag = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select * from customer where status=%s"
            mydbCursor.execute(sql, "unprocessing")
            row = mydbCursor.fetchall()
            # if len(row) > 0:
            #     flag = row
            flag = row
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def show_processing(self):

        mydb = None
        mydbCursor = None
        flag = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select * from customer where status=%s"
            mydbCursor.execute(sql, "processing")
            row = mydbCursor.fetchall()
            # if len(row) > 0:
            #     flag = row
            flag = row
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def show_processed(self):

        mydb = None
        mydbCursor = None
        flag = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select * from customer where status=%s"
            mydbCursor.execute(sql, "Delivered")
            row = mydbCursor.fetchall()
            # if len(row) > 0:
            #     flag = row
            flag = row
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def show_all(self):

        mydb = None
        mydbCursor = None
        flag = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select * from customer"
            mydbCursor.execute(sql)
            row = mydbCursor.fetchall()
            # if len(row) > 0:
            #     flag = row
            flag = row
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def pizzaMenu2(self, id):
        mydb = None
        mydbCursor = None
        login = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()

            sql = "select pizza_name,ingredients,discount,path,size,price from menu join price on menu.pizza_id=price.pizza_id where menu.pizza_id=%s "
            mydbCursor.execute(sql, id)
            row = mydbCursor.fetchall()
            if len(row) > 0:
                login = row
            else:
                login = None
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return login

    def size(self):
        mydb = None
        mydbCursor = None
        login = None
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select count(*) from menu"
            mydbCursor.execute(sql)
            row = mydbCursor.fetchall()
            if len(row) > 0:
                login = row
            else:
                login = None
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return login

    def change_status(self, id):
        mydb = None
        mydbCursor = None
        flag = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select cust_id from customer where cust_id=%s"
            mydbCursor.execute(sql, id)
            id = mydbCursor.fetchone()
            if id[0] is not None or id != "()":
                sql = "select status from customer where cust_id=%s"
                mydbCursor.execute(sql, id)
                row = mydbCursor.fetchone()
                # print(row[0])
                if row[0] == "unprocessing":
                    sql = "update customer set status=%s where cust_id=%s"
                    mydbCursor.execute(sql, ("processing", id))
                    mydb.commit()
                    flag = True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag

    def changestatus(self, id):
        mydb = None
        mydbCursor = None
        flag = False
        try:
            mydb = pymysql.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            mydbCursor = mydb.cursor()
            sql = "select cust_id from customer where cust_id=%s"
            mydbCursor.execute(sql, id)
            id = mydbCursor.fetchone()
            if id[0] is not None or id != "()":
                sql = "select status from customer where cust_id=%s"
                mydbCursor.execute(sql, id)
                row = mydbCursor.fetchone()
                if row[0] == "processing":
                    sql = "update customer set status=%s where cust_id=%s"
                    mydbCursor.execute(sql, ("Delivered", id))
                    mydb.commit()
                    flag = True
        except Exception as e:
            print(str(e))
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            return flag
# dhlr = SMDBHandler("localhost", "root", "1234", "web_project")

# dhlr.updateCartt(14,2,2600,"nomi")