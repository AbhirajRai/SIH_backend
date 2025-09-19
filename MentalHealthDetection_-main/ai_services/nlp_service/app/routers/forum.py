from ai_services.nlp_service.app.models.forum import ForumPost, ForumReport
from ai_services.nlp_service.app.schemas import ForumPostRequest, ForumPostResponse
from ai_services.nlp_service.app.services import analyze_toxicity, analyze_emotion
from ai_services.nlp_service.app.db import get_session

import uuid

router = APIRouter()

@router.post("/forum/post", response_model=ForumPostResponse)
def create_post(post_req: ForumPostRequest, session: Session = Depends(get_session)):
    toxicity = analyze_toxicity(post_req.content).get("toxic", 0)
    flagged = toxicity > 0.5  # Example threshold

    post = ForumPost(
        id=str(uuid.uuid4()),
        user_id=post_req.user_id,
        topic=post_req.topic,
        content=post_req.content,
        timestamp=datetime.utcnow(),
        flagged=flagged,
        reports=0
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.get("/forum/posts/{topic}", response_model=List[ForumPostResponse])
def get_posts(topic: str, limit: int = Query(20, le=100), session: Session = Depends(get_session)):
    posts = session.query(ForumPost).filter(ForumPost.topic == topic).order_by(ForumPost.timestamp.desc()).limit(limit).all()
    return posts

@router.post("/forum/report/{post_id}")
def report_post(post_id: str, reporter_id: Optional[str] = None, reason: Optional[str] = None, session: Session = Depends(get_session)):
    try:
        post = session.query(ForumPost).filter(ForumPost.id == post_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Post not found")

    report = ForumReport(
        id=str(uuid.uuid4()),
        post_id=post_id,
        reporter_id=reporter_id,
        reason=reason,
        timestamp=datetime.utcnow()
    )
    session.add(report)

    post.reports += 1
    if post.reports >= 3:  # Example threshold for auto-flagging
        post.flagged = True

    session.commit()
    return {"message": "Report submitted successfully"}
