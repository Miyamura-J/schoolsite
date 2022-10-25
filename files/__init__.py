from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, listdir
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aergeufgeiufh eifhiuefh a'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth/")

    from .models import User, Note
    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_db(app):
    if not path.exists("files/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database Created!")

        from .models import Major, Year, Module, Document
        major_names = ["CYCLE PRÉPARATOIRE","G INFORMATIQUE","G INDUSTRIEL","G DES PROCÉDÉS ENERGIE ET ENVIRONNEMENT","G ELECTRIQUE","G CIVIL","G MÉCANIQUE","G FINANCE ET INGENIERIE DECISIONNELLE"]
        with app.app_context():
            for major_name in major_names:
                if not Major.query.filter_by(name=major_name).first():
                    new_major = Major(name=major_name)
                    db.session.add(new_major)

            majors_abb = [name.split("_")[1] for name in sorted(listdir("modules/"))]
            for i in range(len(majors_abb)):
                for j in range(1,4):
                    year_name = majors_abb[i]+" "+str(j)
                    if not Year.query.filter_by(name=year_name).first() and year_name!="CP 3":
                        new_year = Year(name=year_name,major_id=i+1)
                        db.session.add(new_year)
                
            module_files = sorted(listdir("modules/"))
            year_id = 0
            for file in module_files:
                file = open("modules/"+file,'r')
                year_id += 1
                for line in file.readlines():
                    line = line.replace("\n", "")
                    if line[0] == "#":
                        year_id += 1
                    else:
                        if not Module.query.filter_by(name=line).first():
                            module_name = line
                            db.session.add(Module(name=module_name))
                        module = Module.query.filter_by(name=line).first()
                        module.years.append(Year.query.get(year_id))
                        

            db.session.commit()