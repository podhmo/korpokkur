mako_scaffold
========================================

* utility for portable model definition with sqlalchemy
* black magic? of cource.

what is portable model definition?
----------------------------------------

sqlalchemy, it is ok that just definition declarative model class depends on another model.
(e.g. We have two model, Group and User. User depends on Group Model.)

But,when providing model classes like these as a library, we are thinking about portability.

* Library User: creating Operator model depends on User. but User class is provided by Library.
* Library Author: We have convinient User Model, so, share it.
* (Both of Two): but's what tablename is this Model?(e.g. User,user,users,mylib_users?)

This package's motibation is solving such a problem like above.

How to use this?
----------------------------------------

Library Author code::

    #foo/auth.py
    import sqlalchemy as sa
    from sqlalchemy.orm import relationship
    from mako_scaffold import (
        ModelCreation, 
        ModuleProvider, 
        ModelSeed, 
        with_tablename, 
        with_modelname, 
    )

    creation = ModelCreation()
    _provider = ModuleProvider(creation)
    create_models = _provider

    @creation.register("Group")
    class Group(ModelSeed):
        id=sa.Column(sa.Integer, primary_key=True, nullable=False)
        name=sa.Column(sa.String(255), nullable=False)

    @creation.register("User", depends=["Group"])
    class User(ModelSeed):
        id=sa.Column(sa.Integer, primary_key=True, nullable=False)
        name=sa.Column(sa.String(255), nullable=False)

        @with_tablename("Group")
        def group_id(cls, group_table_name):
            return sa.Column(sa.Integer, sa.ForeignKey("{}.id".format(group_table_name)), nullable=True)

        @with_modelname("Group")
        def group(cls, name):
            return relationship(name)

        def verify_password(self, password):
            return self.password_digest == password

Library User can decide table name provided by library. 

Library User code::

        from foo.auth import create_models
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()        
        contract = {"User": {"table_name": "users"}, 
                    "Group": {"table_name": "groups", "model_name": "_Group"}}
        models = create_models(Base, contract)

        models._Group # Group model defined in foo.auth.py
        models.User # User model defined in foo.auth.py

more over, also enable to inject dependents model.

Library User code::

        from foo.auth import create_models
        from sqlalchemy.ext.declarative import declarative_base

        Base = declarative_base()
        class MyGroup(Base):
            id = sa.Column(sa.Integer, primary_key=True, nullable=False)
            special = sa.Column(sa.String("32"), doc="this is special")
            __tablename__ = "my_groups"

        contract = {"User": {"table_name": "users"}, 
                    "Group": {"model": MyGroup}}

        models = create_models(Base, contract)

        models.Group # Group model define by library user
        models.User # User model defined in foo.auth.py


