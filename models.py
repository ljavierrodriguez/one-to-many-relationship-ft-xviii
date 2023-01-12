from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="")
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    #todos = db.relationship("Todo", backref="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }

    def serialize_with_todos(self):
        return {
            "id": self.id,
            "username": self.username,
            "todos": list(map(lambda todo: todo.serialize(), self.todos))
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    priority = db.Column(db.String(20), default="low") # high medium low
    done = db.Column(db.Boolean(), default=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", backref="todos")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "done": self.done,
            "user": self.user.name if self.user.name else self.user.username
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Invoice(db.Model):
    __tablename__ = 'invoices'
    id = db.Column(db.Integer, primary_key=True)
    clients_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sellers_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", foreign_keys="[Invoice.clients_id]", primaryjoin="User.id==Invoice.clients_id")
    seller = db.relationship("User", foreign_keys="[Invoice.sellers_id]", primaryjoin="User.id==Invoice.sellers_id")
    details = db.relationship("InvoiceDetail", backref="invoice")



class InvoiceDetail(db.Model):
    __tablename__ = 'invoices_details'
    id = db.Column(db.Integer, primary_key=True)
    invoices_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship("Product")

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    categories_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    category = db.relationship("Category")