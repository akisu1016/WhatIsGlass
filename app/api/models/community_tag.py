import re
from api.database import db, ma
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import relationship
from sqlalchemy import *
from flask import abort


class CommunityTag(db.Model):
    __tablename__ = "communitytags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "<communitytags %r>" % self.name

    def getCommunityTagList():

        community_tag_list = (
            db.session.query(
                CommunityTag.id, CommunityTag.name.label("community_tag_name")
            )
            .order_by(asc(CommunityTag.id))
            .all()
        )

        if community_tag_list is None:
            return []
        else:
            return community_tag_list


class UserCommunityTag(db.Model):
    __tablename__ = "users_communitytags"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    community_tag_id = db.Column(
        db.Integer, db.ForeignKey("communitytags.id"), primary_key=True
    )

    def __repr__(self):
        return "<users_communitytags %r>" % self.user_id, self.community_tag_id

    def getCommunityTagList(user):

        user_id = user["id"]

        user_community_tag_list = (
            db.session.query(
                UserCommunityTag.user_id,
                UserCommunityTag.community_tag_id,
                CommunityTag.name.label("community_tag_name"),
            )
            .join(
                CommunityTag,
                UserCommunityTag.community_tag_id == CommunityTag.id,
            )
            .filter(
                UserCommunityTag.user_id == user_id,
            )
            .all()
        )

        if user_community_tag_list is None:
            return []
        else:
            return user_community_tag_list

    def editCommunityTag(request_dict):

        user_id = request_dict["user_id"]
        community_tag_id_list = request_dict["community_tags"]

        for community_tag in community_tag_id_list:
            community_tag_list = (
                db.session.query(CommunityTag)
                .filter(CommunityTag.id == community_tag)
                .all()
            )
            if len(community_tag_list) == 0:
                return abort(400, {"message": "category_tag does not exists"})

        # ユーザーコミュニティタグのアップデート
        db.session.query(UserCommunityTag).filter(
            UserCommunityTag.user_id == user_id
        ).delete(synchronize_session="fetch")

        for community_tag in community_tag_id_list:
            record = UserCommunityTag(user_id=user_id, community_tag_id=community_tag)
            db.session.add(record)

        db.session.flush()
        db.session.commit()

        update_users_community_tag_list = (
            db.session.query(
                CommunityTag.id,
                CommunityTag.name.label("community_tag_name"),
            )
            .join(
                UserCommunityTag, UserCommunityTag.community_tag_id == CommunityTag.id
            )
            .filter(UserCommunityTag.user_id == user_id)
            .all()
        )

        return update_users_community_tag_list


class CommunityTagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CommunityTag
        load_instance = True
        fields = ("id", "community_tag_name")


class UserCommunityTagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserCommunityTag
        load_instance = True
        fields = ("user_id", "community_tag_id", "community_tag_name")
