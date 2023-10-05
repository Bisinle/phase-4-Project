from api import  make_response,jsonify,Product,Vendor,Customer,User,Order,Category,app,db,request
from api.serialization import api,vendor_schema,vendors_schema, customer_schema,users_schema,order_model_input
from api.serialization import order_schema,orders_schema, customers_schema, product_schema,category_schema
from api.serialization import user_schema,ns,Resource,user_model_input,login_input_model,vendor_model_update
from api.serialization import vendor_model_input
import uuid
import jwt
import datetime
from functools import wraps




def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token =None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # print(token)

        if not token:
            return jsonify({"message" : "Token is missing"})

        try:
            print('------------------------------------------------')
            data= jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
            # print(data)

            current_user = User.query.filter_by(public_id= data['public_id']).first()
            print(current_user)

            if not current_user:
                return jsonify({"message" : "something went wrong"})


        except:
                return jsonify({"message" : "Token is invalid"},401)
        return f(current_user,*args, **kwargs)
    return decorated


@ns.route('/vendors')
class Vendors(Resource):
    @token_required
    def get(current_user,self):
        if  current_user.roles !='Admin':
            return jsonify({"message":"only Admins are allowed to access  this "})
        all_vendors = Vendor.query.all()

        if not all_vendors:
            return make_response(jsonify({"message":"no vendors found"}))
        
        return make_response(vendors_schema.dump(all_vendors),200)
    
    @ns.expect(vendor_model_input)
    @token_required
    def post(current_user,self):
        data = request.get_json()
        print(data)
        # if current_user.roles !='Admin':
        #     return jsonify({"message":"only admins can perform this task "})
        email=data['first_name']+'@' + data['company'][:4]+'.com'
        vendor =Vendor(
            first_name=data['first_name'],
            last_name=data['last_name'],
            company=data['company'],
            email=email,
            phone_number=data['phone_number'],
            user_id=current_user.id
             
         )
        db.session.add(vendor)
        db.session.commit()
        return jsonify({"message":" vendor created successfully "},vendor_schema.dump(vendor))

''' ___________________T O K E N _____________D E C O R A T O R         '''

@ns.route('/vendors/<id>')
class Vendoer_by_id(Resource):
    @ns.expect(vendor_model_update)
    def put(self,id):
        # get the vendor
        vendor = Vendor.query.filter_by(id=id).first()
        if not vendor:
            return jsonify({"message":"vendor not found"})

        data = request.get_json()
        data['email'] = vendor.first_name+'@'+data['company'][:5]+'.com'
        for  attr in data:
            setattr(vendor, attr, data[attr])
        db.session.commit()

        # return jsonify(vendor_schema.dump(vendor),200)
        return jsonify({"message":" vendor updated successfully "},200)


    def delete(selft,id):
        vendor = Vendor.query.filter_by(id=id).first()

        if not vendor:
            return jsonify({"message":"vendor not found"})
        
        db.session.delete(vendor)
        db.session.commit()
        return jsonify({"Deleted":True,
                        "message":"vendor deleted successfully"})



''' ___________________C U S T O M E R S __________________________ R O U T E S        '''

@ns.route('/customers')
class CustomerS(Resource):
    def get(self):
        all_customers = Customer.query.all()
        return make_response(customers_schema.dump(all_customers),200)

@ns.route('/customer/<id>')
class customer_by_id(Resource):
    def put(self,id):
        # get the vendor
        customer = Customer.query.filter_by(id=id).first()
        if not customer:
            return jsonify({"message":"customer not found"})

        data = request.get_json()
        # data['email'] = customer.first_name+'@gmail.com'
        for  attr in data:
            setattr(customer, attr, data[attr])
        db.session.commit()

        return jsonify(customer_schema.dump(customer),200)
        # return jsonify({"message":" customer updated successfully "},200)


    def delete(selft,id):
        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            return jsonify({"message":"customer not found"})
        
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"Deleted":True,
                        "message":"customer deleted successfully"})




''' ___________________O R D E R S__________________________ R O U T E S        '''

@ns.route('/orders')
class Orders(Resource):
    def get(self):
        orders = Order.query.all()

        if not orders:
            return jsonify({"message":"NO in the database"})
        
        return make_response(orders_schema.dump(orders))

    @ns.expect(order_model_input)
    def post(self):
        data = request.get_json()
        # if not data:
        #     return jsonify({"message":"you have not submitted an order"})

        order_list =[]
        if type(data) is list:
            for order in data:
                order = Order(
                item_price=order['item_price'],
                item_quantity=order['item_quantity'],
                address=order['address'],
                amount = int(order['item_price']) * int(order['item_quantity'])
            )
                order_list.append(order)
        db.session.add_all(order_list)
        db.session.commit()
        if type(data) is dict:
                 order = Order(
                item_price=data['item_price'],
                item_quantity=data['item_quantity'],
                address=data['address'],
                amount = int(data['item_price']) * int(data['item_quantity'])
            )
        db.session.add(order)
        db.session.commit()

        return jsonify({"message":"Order has been placed successfully "})
        


 




''' ___________________P R O D U C T S___________________________ R O U T E S        '''

@ns.route('/products')
class Products(Resource):
    def get(self):
        all_products = Product.query.all()
        return make_response(product_schema.dump(all_products),200)

@ns.route('/product/<id>')
class product_by_id(Resource):
    def put(self,id):
        # get the vendor
        product = Product.query.filter_by(id=id).first()
        if not product:
            return jsonify({"message":"product not found"})

        data = request.get_json()
        # data['email'] = product.first_name+'@gmail.com'
        for  attr in data:
            setattr(product, attr, data[attr])
        db.session.commit()

        return jsonify(product_schema.dump(product),200)
        # return jsonify({"message":" product updated successfully "},200)


    def delete(selft,id):
        product = Product.query.filter_by(id=id).first()

        if not product:
            return jsonify({"message":"product not found"})
        
        db.session.delete(product)
        db.session.commit()
        return jsonify({"Deleted":True,
                        "message":"product deleted successfully"})




'''-----------------------------C A T E G O R I E S ---------------------'''
@ns.route('/categories')
class Categories(Resource):
    def get(self):
        categories = Category.query.all()

        if not categories:
            return jsonify({"message":"NO in the database"})
        
        return make_response((category_schema.dump(categories)))





@ns.route('/users')
class Users(Resource):
    def get(self):
        all_users = User.query.all()
        return make_response(users_schema.dump(all_users),200)





'''-------- S I G N -------- U P ----------------------------'''

@ns.route('/signup')
class Signup (Resource):

    @ns.expect(user_model_input)
    def post(self):
        
        data =request.get_json()
        
        new_user = User(
            user_name=data['user_name'],
            profile_picture=data['profile_picture'],    
            password_hash = data['password'],
            public_id = str(uuid.uuid4()),
            roles=data['roles']

        )

       

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"mesage":"successfully added user"})

        
'''-----------------L O G I N -----------------------------'''
@ns.route('/login')
class Login(Resource):
    
    @ns.expect(login_input_model)
    def post(self):
        if request.authorization:
            auth = request.authorization
            username=auth.username
            password=auth.password
        elif ns.payload:
            data = ns.payload  # Access JSON data from the request body

            username = data.get('username')
            password = data.get('password')

        if not username or not password:
            return jsonify({"message": "Please provide both username and password"}), 400

        user = User.query.filter_by(user_name=username).first()
        if not user:
             return jsonify({"message": "User not found"}), 404
        
        if user.authenticate(password):
            # Import these modules at the top of your script:
            # import jwt
            # import datetime
            
            # Generate a JWT token
            token = jwt.encode(
                {'public_id': user.public_id, 
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=59)},
                 app.config['SECRET_KEY'],
                  algorithm="HS256")
            
            return make_response(jsonify({"token": token}), 200)
        
        return jsonify({"message": "Authentication failed"}), 401


