from api.database import db, ma


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=True)
    tel = db.Column(db.String(20), nullable=True)
    mail = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return "<User %r>" % self.name

    def getUserList():

        # select * from users
        user_list = db.session.query(User).all()

        if user_list == None:
            return []
        else:
            return user_list

    def registUser(user):
        record = User(
            name=user["name"],
            address=user["address"],
            tel=user["tel"],
            mail=user["mail"],
        )

        # insert into users(name, address, tel, mail) values(...)
        db.session.add(record)
        db.session.commit()

        return user


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = ("id", "name", "address", "tel", "mail")
