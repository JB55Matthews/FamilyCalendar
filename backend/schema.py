import graphene
from graphql import GraphQLError
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import FamilyModel, MemberModel
from .extensions import db_session


class Family(SQLAlchemyObjectType):
    class Meta:
        model = FamilyModel
        interfaces = (relay.Node, )


class Member(SQLAlchemyObjectType):
    class Meta:
        model = MemberModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    
    allFamilys = SQLAlchemyConnectionField(Family.connection)
    allMembers = SQLAlchemyConnectionField(Member.connection)

    memberById = graphene.Field(Member, id=graphene.Int(required=True))
    familyMembers = graphene.List(Member, familyId=graphene.Int(required=True))
    idByFamilyLogin = graphene.Field(Family, email=graphene.String(required=True), password=graphene.String(required=True))

    def resolve_memberById(self, info, **args):
        id = args.get("id")
        memebers_query = Member.get_query(info)
        member = memebers_query.filter(MemberModel.id==id).first()
        return member
    
    def resolve_familyMembers(self, info, **args):
        family_id = args.get("familyId")
        memebers_query = Member.get_query(info)
        members = memebers_query.filter(MemberModel.family_id==family_id)
        return members
    
    def resolve_idByFamilyLogin(self, info, **args):
        email = args.get("email")
        password = args.get("password")
        familys_query = Family.get_query(info)
        family = familys_query.filter(FamilyModel.email==email).first()
        if family != None:
            if (family.check_password(password)):
                return family
        return GraphQLError("Invalid Login")



class createFamily(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    
    ok = graphene.Boolean()
    family = graphene.Field(lambda: Family)

    def mutate(self, info, email, password):
        familys_query = Family.get_query(info)
        family = familys_query.filter(FamilyModel.email==email).first()
        if family != None:
            return GraphQLError("email already exists")
        
        family = FamilyModel(email=email)
        family.set_password(password)
        db_session.add(family)
        db_session.commit()
        return createFamily(family=family, ok=True)
    
class Mutation(graphene.ObjectType):
    createFamily  = createFamily.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)