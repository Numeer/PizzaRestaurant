from flask import Flask, request, jsonify, render_template, session, make_response, Response, redirect,flash,jsonify
from menu import menu
from db import SMDBHandler
import stripe
list1 = []
app = Flask(__name__)
app.secret_key = 'lololololooololololoolololololololololololololololololol'

stripe_keys = {
    'secret_key': "sk_test_51KL7RNA9AoZgJPE6pwuEMldpxAjHi6gmJfb8kTTtL37PrTB2oh37tdZRPSJvcVAjGo5F4tfwrFhfAK92z81SBNvV00fz3XCwOX",
    'publishable_key': "pk_test_51KL7RNA9AoZgJPE6zSNaQX2BCiD62j3XBhjdtpMb3U1B05Bv5RipIokn6E8qP2nApLNfN4DEISe9Qf9KXZqC4vQw003IHAAs7q"
}
stripe.api_key = stripe_keys['secret_key']


@app.route('/', methods=['POST', 'GET'])
def signin():
    if session.get("username") is None:
        return render_template("signin.html")
    else:
        flash("Already Logged In ")
        return redirect("/menu")

@app.route("/sign_in", methods=["POST"])
def sign_in():
    try:
        username = request.form["username"]
        password = request.form["pwd"]
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        flag = dhlr.sign_in(username, password)
        if flag:
            session["username"] = username
            flash("Login Successfully")
            return redirect("/menu")
        else:
            error = "Invalid Username or Password"
            return render_template("Signin.html", error=error)
    except Exception as e:
        return render_template("Signin.html", error=str(e))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template("signup.html")


@app.route('/sign_up', methods=["POST"])
def sign_Up():
    try:
        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["pwd"]
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        flag = dhlr.sign_up(fullname, username, email, password)
        if flag == True:
            session["username"] = username
            flash("Sign Up SuccessFully ")
            return redirect("/menu")
        else:
            error = "Error! Username already exist"
            return render_template("signup.html", error=error)
    except Exception as e:
        return render_template("signup.html", error=str(e))


@app.route('/profile',methods=['POST','GET'])
def profile():
    if session.get("username") is not None:
        uname=session["username"]
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        lpoints = dhlr.getLoyalityPoints(uname)
        return render_template("profile.html",lpoints=lpoints,name=uname)


@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect("/")
@app.route('/menu', methods=['POST', 'GET'])
def main():
    try:
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        size = dhlr.size()
        size = size[0][0]
        # print(size)
        list1 = []
        for s in range(size+1):
            p1 = dhlr.pizzaMenu2(s)
            if p1 is not None:
                p1 = list(p1)
                list1.append(p1)
        # print(list1)
        row1 = dhlr.getMenu2()
        row2 = dhlr.getSize2()
        if session.get("username") is not None:
            uname=session["username"]
            return render_template("home.html", list=list1, row1=row1, row2=row2,profile=uname)
        else:
            return render_template("home.html", list=list1, row1=row1, row2=row2)
    except Exception as e:
        return render_template("home.html", list=list1, row1=row1, row2=row2,error=str(e))


@app.route('/confirm')
def confirmOrder():
    try:
        if list1 != [] :
            dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
            if session.get("username")!=None:
                username=session["username"]
                lPoints = dhlr.getLoyalityPoints(username)
                if lPoints >= 1000:
                    points="Hoooo Congratulations You can get one free pizza your loyality points are "+str(lPoints)
                    return render_template("order.html",point2=points)
                points = username+" you have "+str(lPoints)
                return render_template("order.html",points=points)
            else:
                return render_template("order.html")
        else:
            flash("Please select an item before proceeding to checkout order")
            return redirect("/menu")
    except Exception as e:
        return render_template("home.html",error=str(e))


@app.route('/Confirm', methods=['POST'])
def ConfirmOrder():
    try:
        count = 0
        sum = 0
        error = None
        name = request.form["name"]
        phone = request.form["phNo"]
        if phone[:2] == "03":
            if len(phone) != 11:
                error = "Length of phone must be 11 if 03 is used"
                raise Exception(error)
        elif phone[:4] == "+923":
            if len(phone) != 13:
                error = "Length of phone must be 13 if +923 is used"
                raise Exception(error)
        else:
            error = "Invalid phone number"
            raise Exception(error)
        add = request.form["address"]
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")

        inserted = dhlr.add_order(name, phone, add)
        if inserted is not None:
            session["id"] = inserted
            id = session.get("id")
            for list in list1:
                dhlr.add_pizza(id, list[0], list[1], int(list[2]))
                count += 1
                sum += int(list[2])
            if session.get("username") is not None:
                uname=session["username"]
                lPoints = dhlr.updateCartt(id, count, sum,uname)
                if lPoints is not None:
                    return render_template("order.html", msg="Order added successfully",points = lPoints)
                else:
                    error = "Order not added"
                    raise Exception(error)
            else:
                if dhlr.updateCart(id, count, sum):
                    return render_template("order.html", msg="Order added successfully")
                else:
                    error = "Order not added"
                    raise Exception(error)
        else:
            error = "Order not added"
            raise Exception(error)
    except Exception as e:
        if error is None:
            error = str(e)
        return render_template("order.html", error=error)



@app.route("/checkout", methods=["POST"])
def process_checkout():
    line_items = request.json.get("lineItems")
    list2 = []
    for item in line_items:
        list2.append(item['name'])
        list2.append(item['size'])
        list2.append(item['price'])
        list1.append(list2)
        list2 = []
    return list2

@app.route('/charge', methods=['GET', 'POST'])
def charge():
    for list in list1:
        sum += int(list[2])
    amount = sum
    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template("payment.html")


@app.route('/admin')
def dashboard():  # put application's code here
    return render_template("dashboard.html")


@app.route("/addpizza")
def addpizza():
    return render_template("adddpizza.html")


@app.route("/add_Pizza", methods=["POST", "GET"])
def add_Pizza():
    try:
        pizza_name = request.form["pizza_name"]
        ingredients = request.form["ingredients"]
        discount = request.form["discount"]
        small = request.form["small-price"]
        medium = request.form["medium-price"]
        large = request.form["large-price"]
        path = request.form["path"]
        c = menu(pizza_name, ingredients, discount)
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")

        flag = dhlr.addpizza(c, path, small, medium, large)
        # print(flag)
        if flag == True:
            session["pizza_name"] = pizza_name
            message = "Pizza Added SuccessFully "
            return render_template("dashboard.html", message=message)
        else:
            error = "Error! Kindly add again"
            return render_template("adddpizza.html", error=error)
    except Exception as e:
        return render_template("adddpizza.html", error=str(e))


@app.route("/show_all_pizza")
def show_all_pizza():

    try:
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        size = dhlr.size()
        size = size[0][0]
        # print(size)
        list1 = []
        for s in range(size+1):
            p1 = dhlr.pizzaMenu2(s)
            if p1 is not None:
                p1 = list(p1)
                list1.append(p1)
            pizza = dhlr.show_pizza()
        if pizza != None:
            return render_template("showpizza.html", list=list1, pizzas=pizza)
        else:
            er = "Hello you didn't add any pizza "
            return render_template("showpizza.html", error=er)
    except Exception as e:
        return render_template("dashboard.html", error=str(e))


@app.route("/delete_pizza_form")
def delete_pizza_form():
    try:
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        flag = dhlr.show_pizza()
        if flag is not None:
            return render_template("deletepizza.html", pizzas=flag)
        else:
            er = "Awwww you didn't add any pizzas "
            return render_template("dashboard.html", flag=None, message=er)
    except Exception as e:
        return render_template("deletepizza.html", error=str(e))


@app.route("/delete_pizza", methods=["POST"])
def delete_pizza():
    try:
        pizza_name = request.form["Pizza_Name"]
        # print(pizza_name)
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        # print('hello')
        flag = dhlr.deletepizza(pizza_name)
        # print(menu)
        if flag is not False:
            message = "Pizza deleted successfully!"
            return render_template("dashboard.html", message=message)
        else:
            er = "Awwww you do not have  any  this pizza_name"
            return render_template("deletepizza.html", error=er)
    except Exception as e:
        return render_template("deletepizza.html", error=str(e))


@app.route("/update_pizza_form")
def updateform():
    try:
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        flag = dhlr.show_pizza()
        size = dhlr.size()
        size = size[0][0]
        # print(size)
        list1 = []
        for s in range(size+1):
            p1 = dhlr.pizzaMenu2(s)
            if p1 is not None:
                p1 = list(p1)
                list1.append(p1)
        if flag is not None:
            return render_template("updatepizza.html", pizzas=flag, list=list1)
        else:
            er = "Awwww you didn't add any pizzas "
            return render_template("dashboard.html", flag=None, message=er)
    except Exception as e:
        return render_template('/update_pizza_form', error=str(e))


@app.route("/update_pizza", methods=["POST"])
def update_pizza():
    try:
        pizza_name = request.form["Pizza_Name"]
        session["pizza_name"] = pizza_name
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        flag = dhlr.check_update_pizza(pizza_name)
        flag2 = dhlr.show_pizza()
        size = dhlr.size()
        size = size[0][0]
        # print(size)
        list1 = []
        for s in range(size+1):
            p1 = dhlr.pizzaMenu2(s)
            if p1 is not None:
                p1 = list(p1)
                list1.append(p1)
        if flag == True:
            return render_template("update.html")
        else:
            error = "This pizza name does not exist!"
            return render_template('updatepizza.html', pizzas=flag2, list=list1, error=error)
    except Exception as e:
        return render_template("updatepizza.html", error=str(e))


@app.route("/updateprocess", methods=["POST"])
def updateproces():
    try:
        if session.get("pizza_name") != None:
            name = session["pizza_name"]
            pizza_name = request.form["Pizza_Name"]
            ingredients = request.form["Ingredients"]
            path = request.form["Path"]
            discount = request.form["Discount"]
            small_price = request.form["small_price"]
            medium_price = request.form["medium_price"]
            large_price = request.form["large_price"]
            dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
            size = dhlr.size()
            size = size[0][0]
            # print(size)
            list1 = []
            for s in range(size+1):
                p1 = dhlr.pizzaMenu2(s)
                if p1 is not None:
                    p1 = list(p1)
                    list1.append(p1)
            c = menu(pizza_name, ingredients, discount)

            flag = dhlr.updatepizza(
                name, c, path, small_price, medium_price, large_price)
            if flag == True:
                # print(flag)
                msg = "Waooo Pizza Updated SuccessFully!"
                return render_template("dashboard.html", message=msg)
            else:
                flag2 = dhlr.show_pizza()
                return render_template("updatepizza.html", pizzas=flag2, list=list1, error="Something went wrong try again:(")
        else:
            return render_template("updatepizza.html", error="Fill this form first :_(")

    except Exception as e:
        return render_template("updatepizza.html", error=str(e))


@app.route("/show_status")
def show_status():
    return render_template("showstatus.html")


@app.route("/show_unprocessed_status")
def show_unprocessed_status():

    try:
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        pizza = dhlr.show_unprocessed()
        if pizza != None:
            return render_template("showunprocessed.html", pizzas=pizza)
        else:
            er = "Something went wrong Try Again "
            return render_template("showunprocessed.html", pizzas=pizza, error=er)
    except Exception as e:
        return render_template("dashboard.html", error=str(e))


@app.route("/change_status", methods=['POST'])
def change_status():
    try:
        id = request.form["customer-id"]
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        pizz = dhlr.show_unprocessed()
        pizza = dhlr.change_status(id)
        if pizza:
            flash("Status Changed to processing Successfully")
            return redirect('/show_unprocessed_status')
        else:
            er = "Something went wrong try Again "
            return render_template("showunprocessed.html", error=er, pizzas=pizz)
    except Exception as e:
        return render_template("showunprocessed.html", error=str(e))


@app.route("/change_status_delivered", methods=['POST'])
def change_status_delivered():
    try:
        id = request.form["customer-id"]
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        pizz = dhlr.show_processing()
        pizza = dhlr.changestatus(id)
        if pizza:
            flash("Status Changed to Delivered Successfully")
            return redirect('/showprocessing')
        else:
            er = "Something Went wrong Try Again"
            return render_template("showprocessing.html", error=er, pizzas=pizz)
    except Exception as e:
        return render_template("showprocessing.html", error=str(e))


@app.route("/showprocessing")
def showprocessing():

    try:
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")

        pizza = dhlr.show_processing()
        if pizza != None:
            return render_template("showprocessing.html", pizzas=pizza)
        else:
            er = "Something went wrong "
            return render_template("showprocessing.html", error=er)
    except Exception as e:
        return render_template("dashboard.html", error=str(e))


@app.route("/showprocessed")
def showprocessed():
    try:
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")

        pizza = dhlr.show_processed()
        if pizza != None:
            return render_template("showprocessed.html", pizzas=pizza)
        else:
            er = "Something went wrong "
            return render_template("showprocessed.html", error=er)
    except Exception as e:
        return render_template("dashboard.html", error=str(e))


@app.route("/showalll")
def showalll():

    try:
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")
        list=[]
        pizza = dhlr.show_all()
        for id in pizza:
            list.append({"id":id[0],"name":id[1],"phone":id[2],"address":id[3],"quantity":id[4],"price":id[5],"status":id[6],"date_column":id[7]})

        return list
    except Exception as e:
        return render_template("dashboard.html", error=str(e))

@app.route("/showall")
def showall():

    try:
        dhlr = SMDBHandler("localhost", "root", "1234", "web_project")

        pizza = dhlr.show_all()
        if pizza != None:
            # print("hey")
            return render_template("ajex.html", pizzas=pizza)
        else:
            er = "Hello you didn't add any pizza "
            return render_template("ajex.html", error=er)
    except Exception as e:
        return render_template("dashboard.html", error=str(e))

@app.route("/contact")
def contact():
     return render_template("contact.html")
if __name__ == '__main__':
    app.run(debug=True)
