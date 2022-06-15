import peewee

db = peewee.PostgresqlDatabase('verify_app', user='shadrin', password='SeriouS11', host='45.89.67.84', port=5432)


# class BaseModel(peewee.Model):
#     class Meta:
#         database = db


# class Users(BaseModel):
#     UID = peewee.IntegerField( unique = True, primary_key=True )
#     SUB = peewee.IntegerField(default = 0)


#     @classmethod
#     def get_row(cls, UID):
#         return cls.get(UID == UID)

#     @classmethod
#     def row_exists(cls, UID):
#         query = cls().select().where(cls.UID == UID)
#         return query.exists()

#     @classmethod
#     def creat_row(cls, UID):
#         user, created = cls.get_or_create(UID=UID)



# class ProxyList(BaseModel):
#     Proxy = peewee.TextField()
#     Role = peewee.TextField( default = 'Default' )


# class TaskList(BaseModel):
#     Task_id = peewee.TextField(unique = True)
#     UID = peewee.IntegerField()
#     Task_link = peewee.TextField()
    

# class UniquePhone(BaseModel):
#     UID = peewee.TextField(primary_key=True)
#     Task_phone = peewee.IntegerField()



# db.create_tables([TaskList])
# db.create_tables([UniquePhone])
# db.create_tables([ProxyList])
# db.create_tables([Users])
db.connect()
