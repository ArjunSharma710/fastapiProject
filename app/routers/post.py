from fastapi import APIRouter,Depends, Response
from .. import schemas,models
from typing import List,Optional
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2
from fastapi import HTTPException,status
from sqlalchemy import func

router = APIRouter(prefix="/posts",tags=["Posts"])

@router.get("/",response_model= List[schemas.PostOut])
def get_posts(db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user),limit:int=10,skip:int=0, search:Optional[str]=""):

    posts = db.query(models.Posts).all()

    results = db.query(models.Posts, func.count(models.Vote.post_id.label("votes"))).join(models.Vote, models.Vote.post_id==models.Posts.id, isouter=True).group_by(models.Posts.id).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()

    return [{"post":post,"votes":votes}for post,votes in results]



@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    #post = db.query(models.Posts).filter(models.Posts.owner_id==id).first()

    post = db.query(models.Posts,func.count(models.Vote.post_id.label("votes"))).join(models.Vote,models.Posts.id==models.Vote.post_id,isouter=True).group_by(models.Posts.id).filter(models.Posts.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the post with {id}was not found')

    return {"post": post[0],"votes":post[1]}



@router.post("/",response_model=schemas.Post,status_code=status.HTTP_201_CREATED)
def create_post(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    new_post = models.Posts(owner_id = current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id==id)

    if post.first()== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id}not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)



@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,incoming_post:schemas.PostCreate,db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
    updated= db.query(models.Posts).filter(models.Posts.id==id)
    postt= updated.first()

    if postt==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id}not found")

    updated.update(incoming_post.dict(),synchronize_session=False)
    db.commit()

    return updated.first()
