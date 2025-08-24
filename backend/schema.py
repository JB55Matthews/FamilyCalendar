import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .models import FamilyModel, MemberModel


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

schema = graphene.Schema(query=Query)