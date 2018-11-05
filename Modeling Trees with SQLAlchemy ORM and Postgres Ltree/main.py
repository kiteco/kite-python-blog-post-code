from sqlalchemy import Column, Integer, String, Sequence, Index, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, remote, foreign, sessionmaker
from sqlalchemy.sql import expression
from sqlalchemy_utils import LtreeType, Ltree
from sqlalchemy_utils.types.ltree import LQUERY

Base = declarative_base()

engine = create_engine("postgresql://postgres:mysecret@postgres/postgres")

id_seq = Sequence("nodes_id_seq")


class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, id_seq, primary_key=True)
    name = Column(String, nullable=False)
    path = Column(LtreeType, nullable=False)

    parent = relationship(
        "Node",
        primaryjoin=(remote(path) == foreign(func.subpath(path, 0, -1))),
        backref="children",
        viewonly=True,
    )

    def __init__(self, name, parent=None):
        _id = engine.execute(id_seq)
        self.id = _id
        self.name = name
        ltree_id = Ltree(str(_id))
        self.path = ltree_id if parent is None else parent.path + ltree_id

    __table_args__ = (Index("ix_nodes_path", path, postgresql_using="gist"),)

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Node({})'.format(self.name)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# To create a tree like the example shown
# at the top of this post:
cats = Node("cats")
big = Node("big", parent=cats)
small = Node("small", parent=cats)
wild = Node("wild", parent=small)
domestic = Node("domestic", parent=small)
session.add_all((cats, big, small, wild, domestic))
for big_cat in ("lion", "tiger", "jaguar"):
    session.add(Node(big_cat, parent=big))
for small_wildcat in ("ocelot", "bobcat"):
    session.add(Node(small_wildcat, parent=wild))
for domestic_cat in ("persian", "bengal", "shorthair"):
    session.add(Node(domestic_cat, parent=domestic))

session.flush()

# To retrieve a whole subtree:
whole_subtree = session.query(Node).filter(Node.path.descendant_of(domestic.path)).all()
print('Whole subtree:', whole_subtree)
# [domestic, persian, bengal, shorthair]

# Get only the third layer of nodes:
third_layer = session.query(Node).filter(func.nlevel(Node.path) == 3).all()
print('Third layer:', third_layer)
# [wild, domestic, lion, tiger, jaguar]

# Get all the siblings of a node:
shorthair = session.query(Node).filter_by(name="shorthair").one()
siblings = session.query(Node).filter(
    # We can use Python's slice notation on ltree paths:
    Node.path.descendant_of(shorthair.path[:-1]),
    func.nlevel(Node.path) == len(shorthair.path),
    Node.id != shorthair.id,
).all()
print('Siblings of shorthair:', siblings)
# [persian, bengal]

# Using an LQuery to get immediate children of two parent nodes at different depths:
query = "*.%s|%s.*{1}" % (big.id, wild.id)
lquery = expression.cast(query, LQUERY)
immediate_children = session.query(Node).filter(Node.path.lquery(lquery)).all()
print('Immediate children of big and wild:', immediate_children)
# [lion, tiger, ocelot, jaguar, bobcat]
