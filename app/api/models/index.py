import re
from api.database import db, ma
from sqlalchemy import *
from .answer import Answer, AnswerInformative
from .user import User
from .categorytag import IndexCategoryTag
from .favorite_index import FavoriteIndex
from .community_tag import UserCommunityTag
import datetime
from flask import abort
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql


class Index(db.Model):
    __tablename__ = "indices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    index = db.Column(db.String(50), nullable=False)
    questioner = db.Column(db.Integer, nullable=False)
    language_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.TIMESTAMP, nullable=True)

    def __repr__(self):
        return "<Index %r>" % self.id

    def getIndexList(request_dict):
        # リクエストから取得
        sort = int(request_dict["sort"]) if request_dict["sort"] is not None else 1
        language_id = request_dict["language_id"]
        include_no_answer = (
            int(request_dict["include_no_answer"])
            if request_dict["include_no_answer"] is not ""
            else 1
        )
        keyword = request_dict["keyword"]

        category_tag_id_list = (
            re.findall(r"\d+", request_dict["category_tag_id"])
            if request_dict["category_tag_id"] != ""
            else ""
        )

        if category_tag_id_list != "":
            category_tag_filter = Index.get_category_tag_filter(category_tag_id_list)

        index_limit = (
            int(request_dict["index_limit"])
            if request_dict["index_limit"] is not ""
            else 300
            if int(request_dict["index_limit"]) > 300
            else 100
        )

        answer_count = Index.get_answer_count()
        best_answer = Index.get_best_answer()
        frequently_used_count = IndexUserCommunityTag.countCommunityTag()

        index_list = db.session.query(
            Index.id,
            Index.index,
            User.username,
            func.ifnull(frequently_used_count.c.frequently_used_count, 0).label(
                "frequently_used_count"
            ),
            Index.language_id,
            Index.date,
            answer_count.c.answer_count,
            best_answer.c.best_answer,
        ).outerjoin(
            frequently_used_count,
            Index.id == frequently_used_count.c.index_id,
        )

        if include_no_answer == 2:
            index_list = index_list.join(
                best_answer, Index.id == best_answer.c.index_id
            )
        else:
            index_list = index_list.outerjoin(
                best_answer, Index.id == best_answer.c.index_id
            )

        index_list = index_list.filter(
            Index.index.contains(f"{keyword}"),
            Index.language_id == language_id,
            User.id == Index.questioner,
            Index.id == answer_count.c.index_id,
        )

        if category_tag_id_list != "":
            index_list = index_list.filter(Index.id == category_tag_filter.c.index_id)

        if include_no_answer == 3:
            index_list = index_list.filter(answer_count.c.answer_count == 0)

        if sort == 2:
            index_list = index_list.order_by(desc(text("frequently_used_count")))
        elif sort == 3:
            index_list = index_list.order_by(desc(text("answer_count")))

        index_list = (
            index_list.order_by(desc(Index.date)).distinct(Index.id).limit(index_limit)
        )

        if index_list == null:
            return []
        else:
            return index_list

    def getIndex(index_id):

        answer_count = Index.get_answer_count()
        best_answer = Index.get_best_answer()
        frequently_used_count = IndexUserCommunityTag.countCommunityTag()

        index = (
            db.session.query(
                Index.id,
                Index.index,
                User.username,
                func.ifnull(frequently_used_count.c.frequently_used_count, 0).label(
                    "frequently_used_count"
                ),
                Index.language_id,
                Index.date,
                answer_count.c.answer_count,
                best_answer.c.best_answer,
            )
            .outerjoin(best_answer, Index.id == best_answer.c.index_id)
            .outerjoin(
                frequently_used_count,
                Index.id == frequently_used_count.c.index_id,
            )
            .filter(
                User.id == Index.questioner,
                Index.id == answer_count.c.index_id,
                Index.id == Index.id == index_id,
            )
            .one()
        )

        return index

    def getUserIndexList(request_dict):
        # リクエストから取得
        sort = int(request_dict["sort"]) if request_dict["sort"] is not None else 1
        language_id = request_dict["language_id"]
        include_no_answer = (
            int(request_dict["include_no_answer"])
            if request_dict["include_no_answer"] is not ""
            else 1
        )
        user_id = request_dict["user_id"]

        index_limit = (
            int(request_dict["index_limit"])
            if request_dict["index_limit"] is not ""
            else 300
            if int(request_dict["index_limit"]) > 300
            else 100
        )

        answer_count = Index.get_answer_count()
        best_answer = Index.get_best_answer()
        frequently_used_count = IndexUserCommunityTag.countCommunityTag()

        index_list = db.session.query(
            Index.id,
            Index.index,
            User.username,
            func.ifnull(frequently_used_count.c.frequently_used_count, 0).label(
                "frequently_used_count"
            ),
            Index.language_id,
            Index.date,
            answer_count.c.answer_count.label("answer_count"),
            best_answer.c.best_answer,
        ).outerjoin(
            frequently_used_count,
            Index.id == frequently_used_count.c.index_id,
        )

        if include_no_answer == 2:
            index_list = index_list.join(
                best_answer, Index.id == best_answer.c.index_id
            )
        else:
            index_list = index_list.outerjoin(
                best_answer, Index.id == best_answer.c.index_id
            )

        index_list = index_list.filter(
            Index.index.contains(f"{keyword}"),
            Index.language_id == language_id,
            User.id == Index.questioner,
            User.id == user_id,
            Index.id == answer_count.c.index_id,
        )

        if include_no_answer == 3:
            index_list = index_list.filter(answer_count.c.answer_count == 0)

        if sort == 2:
            index_list = index_list.order_by(desc(text("frequently_used_count")))
        elif sort == 3:
            index_list = index_list.order_by(desc(text("answer_count")))

        index_list = (
            index_list.order_by(desc(Index.date)).distinct(Index.id).limit(index_limit)
        )

        if index_list == null:
            return []
        else:
            return index_list

    # 回答者数が少ない見出しを取得
    def get_unpopular_question(request_dict):

        language_id_filters = []
        for language_id in request_dict["language_ids"]:
            language_id_filters.append(Index.language_id == language_id)

        is_random = request_dict["is_random"] if request_dict["is_random"] != "" else 1

        index_limit = (
            int(request_dict["index_limit"])
            if request_dict["index_limit"] is not ""
            else 30
            if int(request_dict["index_limit"]) > 30
            else 3
        )

        answer_count = Index.get_answer_count()
        best_answer = Index.get_best_answer()
        frequently_used_count = IndexUserCommunityTag.countCommunityTag()

        index_list = db.session.query(
            Index.id,
            Index.index,
            User.username,
            func.ifnull(frequently_used_count.c.frequently_used_count, 0).label(
                "frequently_used_count"
            ),
            Index.language_id,
            Index.date,
            answer_count.c.answer_count,
            best_answer.c.best_answer,
        ).outerjoin(
            frequently_used_count,
            Index.id == frequently_used_count.c.index_id,
        )

        index_list = index_list.outerjoin(
            best_answer, Index.id == best_answer.c.index_id
        )

        index_list = index_list.filter(
            or_(*language_id_filters),
            User.id == Index.questioner,
            Index.id == answer_count.c.index_id,
            answer_count.c.answer_count == 0,
        )

        index_list = index_list.distinct(Index.id)

        if is_random == "2":
            index_list = index_list.order_by(func.rand())

        index_list = index_list.limit(index_limit).all()

        return index_list

    def getFavotiteIndexList(request_dict):
        # リクエストから取得
        sort = int(request_dict["sort"]) if request_dict["sort"] is not None else 1
        language_id = request_dict["language_id"]
        index_limit = (
            int(request_dict["index_limit"])
            if request_dict["index_limit"] is not ""
            else 300
            if int(request_dict["index_limit"]) > 300
            else 100
        )
        user_id = request_dict["user_id"]

        answer_count = Index.get_answer_count()
        best_answer = Index.get_best_answer()
        frequently_used_count = IndexUserCommunityTag.countCommunityTag()

        index_list = db.session.query(
            Index.id,
            Index.index,
            User.username,
            func.ifnull(frequently_used_count.c.frequently_used_count, 0).label(
                "frequently_used_count"
            ),
            Index.language_id,
            Index.date,
            answer_count.c.answer_count,
            best_answer.c.best_answer,
        ).outerjoin(
            frequently_used_count,
            Index.id == frequently_used_count.c.index_id,
        )

        index_list = index_list.outerjoin(
            best_answer,
            Index.id == best_answer.c.index_id,
        )

        index_list = index_list.filter(
            Index.language_id == language_id,
            User.id == Index.questioner,
            Index.id == answer_count.c.index_id,
            Index.id == FavoriteIndex.index_id,
            FavoriteIndex.user_id == user_id,
        )

        if sort == 2:
            index_list = index_list.order_by(desc(text("frequently_used_count")))
        elif sort == 3:
            index_list = index_list.order_by(desc(text("answer_count")))

        index_list = (
            index_list.order_by(desc(Index.date)).distinct(Index.id).limit(index_limit)
        )

        if index_list == null:
            return []
        else:
            return index_list

    # お勧めの見出しを取得
    def getReccomendQuestion(request_dict):

        language_id_filters = []
        for language_id in request_dict["language_ids"]:
            language_id_filters.append(Index.language_id == language_id)

        community_tag_id = request_dict["community_tag"]

        index_limit = (
            int(request_dict["index_limit"])
            if request_dict["index_limit"] is not ""
            else 30
            if int(request_dict["index_limit"]) > 300
            else 300
        )

        answer_count = Index.get_answer_count()
        best_answer = Index.get_best_answer()
        community_tag = IndexUserCommunityTag.getIndexUserCommunityTag()
        frequently_used_count = IndexUserCommunityTag.countCommunityTag()

        index_list = db.session.query(
            Index.id,
            Index.index,
            User.username,
            func.ifnull(frequently_used_count.c.frequently_used_count, 0).label(
                "frequently_used_count"
            ),
            Index.language_id,
            Index.date,
            answer_count.c.answer_count,
            best_answer.c.best_answer,
            community_tag.c.community_tag_id,
        ).outerjoin(
            frequently_used_count,
            Index.id == frequently_used_count.c.index_id,
        )

        index_list = index_list.outerjoin(
            best_answer, Index.id == best_answer.c.index_id
        )

        index_list = index_list.outerjoin(
            community_tag, Index.id == community_tag.c.index_id
        )

        index_list = index_list.filter(
            or_(*language_id_filters),
            User.id == Index.questioner,
            Index.id == answer_count.c.index_id,
            community_tag.c.community_tag_id == community_tag_id,
        )

        index_list = index_list.distinct(Index.id)

        index_list = index_list.order_by(func.rand())

        index_list = index_list.limit(index_limit).all()

        return index_list

    def registIndex(indices):
        record = Index(
            index=indices["index"],
            questioner=indices["questioner"],
            language_id=indices["language_id"],
            date=datetime.datetime.now(),
        )

        db.session.add(record)
        db.session.flush()
        db.session.commit()

        return record

    def get_answer_count():
        # 回答者数を取得するためのクエリ
        answer_count = (
            db.session.query(
                Index.id.label("index_id"),
                func.count(Answer.index_id).label("answer_count"),
            )
            .outerjoin(Answer, Index.id == Answer.index_id)
            .group_by(Index.id)
            .subquery("answer_count")
        )

        return answer_count

    def get_best_answer():
        # ベストアンサーを一覧取得するためのクエリ
        informative_count = AnswerInformative.countInformative()

        max_informative = (
            db.session.query(
                informative_count.c.answer_id,
                func.max(func.ifnull(informative_count.c.informative_count, 0)).label(
                    "max_count"
                ),
            )
            .group_by(informative_count.c.answer_id)
            .subquery("best_answer")
        )

        best_answer = (
            db.session.query(
                Answer.id,
                Answer.index_id,
                func.any_value(Answer.definition).label("best_answer"),
            )
            .join(
                max_informative,
                Answer.id == max_informative.c.answer_id,
            )
            .group_by(Answer.id)
            .having(func.max(Answer.date))
            .subquery("best_answer")
        )

        return best_answer

    def get_category_tag_filter(category_tag_id_list):

        count = False
        for category_tag_id in category_tag_id_list:
            if count is False:
                filter_index_id = (
                    db.session.query(IndexCategoryTag.index_id.label("index_id"))
                    .filter(
                        IndexCategoryTag.category_tag_id == category_tag_id,
                    )
                    .subquery("filter_index_id")
                )
                count = True
            else:
                filter_index_id = (
                    db.session.query(IndexCategoryTag.index_id.label("index_id"))
                    .filter(
                        IndexCategoryTag.index_id == filter_index_id.c.index_id,
                        IndexCategoryTag.category_tag_id == category_tag_id,
                    )
                    .subquery("filter_index_id")
                )

        return filter_index_id


class IndexUserCommunityTag(db.Model):
    __tablename__ = "indices_users_communitytags"

    index_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __repr__(self):
        return "<indices_users_communitytags %r>" % self.index_id, self.user_id

    def getIndexUserCommunityTag():

        community_tag_list = (
            db.session.query(
                IndexUserCommunityTag.index_id,
                IndexUserCommunityTag.user_id,
                UserCommunityTag.community_tag_id,
            )
            .outerjoin(
                IndexUserCommunityTag,
                IndexUserCommunityTag.user_id == UserCommunityTag.user_id,
            )
            .subquery("community_tag")
        )

        return community_tag_list

    def countupCommunityTag(request):
        index_id = request["index_id"]
        user_id = request["user_id"]

        # 存在確認
        communitytag_exist = (
            db.session.query(IndexUserCommunityTag)
            .filter(
                IndexUserCommunityTag.user_id == user_id,
                IndexUserCommunityTag.index_id == index_id,
            )
            .first()
        )

        if communitytag_exist is not None:
            return False

        try:
            record = IndexUserCommunityTag(user_id=user_id, index_id=index_id)
            db.session.add(record)
            db.session.flush()
            db.session.commit()
        except ValueError:
            return False

        index = Index.getIndex(index_id)

        return index

    def countdownCommunityTag(request):
        index_id = request["index_id"]
        user_id = request["user_id"]

        # 存在確認
        communitytag_exist = (
            db.session.query(IndexUserCommunityTag)
            .filter(
                IndexUserCommunityTag.user_id == user_id,
                IndexUserCommunityTag.index_id == index_id,
            )
            .first()
        )

        if communitytag_exist is None:
            return False

        try:
            db.session.query(IndexUserCommunityTag).filter(
                IndexUserCommunityTag.index_id == index_id,
                IndexUserCommunityTag.user_id == user_id,
            ).delete(synchronize_session="fetch")
            db.session.flush()
            db.session.commit()
        except ValueError:
            return

        index = Index.getIndex(index_id)

        return index

    def countCommunityTag():

        communitytag_count = (
            db.session.query(
                IndexUserCommunityTag.index_id,
                func.count(IndexUserCommunityTag.index_id).label(
                    "frequently_used_count"
                ),
            )
            .group_by(IndexUserCommunityTag.index_id)
            .subquery("frequently_used_count")
        )

        return communitytag_count


class IndexSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Index
        load_instance = True
        fields = (
            "id",
            "index",
            "questioner",
            "language_id",
            "frequently_used_count",
            "date",
            "username",
            "index_id",
            "definition",
            "origin",
            "note",
            "informative_count",
            "best_answer",
            "answer_count",
            "categorytags",
            "community_tag_id",
        )
