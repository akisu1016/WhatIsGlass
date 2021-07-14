import re
from api.database import db, ma
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import relationship
from sqlalchemy import *
from .index import Index


class CategoryTag(db.Model):
    __tablename__ = "categorytags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "<categorytags %r>" % self.name

    def getCategoryTagList():

        category_tag_list = (
            db.session.query(
                CategoryTag.id, CategoryTag.name.label("category_tag_name")
            )
            .order_by(asc(CategoryTag.id))
            .all()
        )

        if category_tag_list is None:
            return []
        else:
            return category_tag_list


class IndexCategoryTag(db.Model):
    __tablename__ = "indices_categorytags"

    index_id = db.Column(db.Integer, db.ForeignKey("indices.id"), primary_key=True)
    category_tag_id = db.Column(
        db.Integer, db.ForeignKey("categorytags.id"), primary_key=True
    )

    def __repr__(self):
        return "<indices_categorytags %r>" % self.index_id

    def getCategoryTagList(index):

        index_id = index["id"]

        index_category_tag_list = (
            db.session.query(
                IndexCategoryTag.index_id,
                IndexCategoryTag.category_tag_id,
                CategoryTag.name.label("category_name"),
            )
            .join(
                CategoryTag,
                IndexCategoryTag.category_tag_id == CategoryTag.id,
            )
            .filter(
                IndexCategoryTag.index_id == index_id,
            )
            .all()
        )

        if index_category_tag_list is None:
            return []
        else:
            return index_category_tag_list


class CategorytagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CategoryTag
        load_instance = True
        fields = ("id", "category_tag_name")


class IndexCategorytagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IndexCategoryTag
        load_instance = True
        fields = ("index_id", "category_tag_id", "category_name")
