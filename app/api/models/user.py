from api.database import db, ma


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    icon = db.Column(db.String(300), nullable=True)

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
            id=user["id"],
            username=user["username"],
            email=user["email"],
            password=user["password"],
            icon=user["icon"],
        )

        # insert into users(name, address, tel, mail) values(...)
        db.session.add(record)
        db.session.commit()

        return user


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = ("id", "username", "email", "password", "icon")
