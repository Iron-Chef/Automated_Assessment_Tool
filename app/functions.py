from app.models import Formativetest, Multiplechoice, User
from app.forms import QChoiceForm, DIFFICULTY_RATING
from flask_login import current_user
from app import app,db

def add_question_1():
        QCform = QChoiceForm()
        test = Formativetest.query.order_by(Formativetest.id.desc()).first()
        if QCform.question_1.data.question != '-':
            question_1 = QCform.question_1.data
            test.linkedquestions.append(question_1)            
        if QCform.WriteMCquestion_1.question.data !='':
            Q1multi= Multiplechoice(
            user_id=current_user.id,
            question=QCform.WriteMCquestion_1.question.data, 
            answer_1=QCform.WriteMCquestion_1.answer1.data,ans_choice_1=QCform.WriteMCquestion_1.ans_multi_select_1.data, 
            answer_2=QCform.WriteMCquestion_1.answer2.data,ans_choice_2=QCform.WriteMCquestion_1.ans_multi_select_2.data, 
            answer_3=QCform.WriteMCquestion_1.answer3.data, ans_choice_3=QCform.WriteMCquestion_1.ans_multi_select_3.data,
            answer_4=QCform.WriteMCquestion_1.answer4.data, ans_choice_4=QCform.WriteMCquestion_1.ans_multi_select_4.data,
            marks=QCform.WriteMCquestion_1.marks.data,
            rating = dict(DIFFICULTY_RATING).get(QCform.WriteMCquestion_1.rating.data),
            rating_num = QCform.WriteMCquestion_1.rating.data,
            topic_tag =QCform.WriteMCquestion_1.topic.data,
            feedback=QCform.WriteMCquestion_1.feedback.data,
            question_type = 'Multiplechoice'
            )
            db.session.add(Q1multi)
            db.session.commit()
            question_1 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_1)           
        if QCform.WriteFTGquestion_1.question.data !='':
            Q1FTG = Multiplechoice(
            user_id = current_user.id,
            question = QCform.WriteFTGquestion_1.question.data, 
            answer_1 = QCform.WriteFTGquestion_1.answer.data,
            answer_2 = '',
            answer_3 = '',
            answer_4 = '',
            topic_tag = QCform.WriteFTGquestion_1.topic.data,
            marks = QCform.WriteFTGquestion_1.marks.data, 
            rating = dict(DIFFICULTY_RATING).get(QCform.WriteFTGquestion_1.rating.data),
            rating_num = QCform.WriteFTGquestion_1.rating.data,
            feedback = QCform.WriteFTGquestion_1.feedback.data,
            question_type = "fill_in_the_blank"
            )
            db.session.add(Q1FTG)
            db.session.commit()
            question_1 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_1)

def add_question_2():
        QCform = QChoiceForm()
        test = Formativetest.query.order_by(Formativetest.id.desc()).first()
        if QCform.question_2.data.question != '-':
            question_2 = QCform.question_2.data
            test.linkedquestions.append(question_2)
        if QCform.WriteMCquestion_2.question.data !='':
            Q2multi= Multiplechoice(
            user_id=current_user.id,
            question=QCform.WriteMCquestion_2.question.data, 
            answer_1=QCform.WriteMCquestion_2.answer1.data,ans_choice_1=QCform.WriteMCquestion_2.ans_multi_select_1.data, 
            answer_2=QCform.WriteMCquestion_2.answer2.data,ans_choice_2=QCform.WriteMCquestion_2.ans_multi_select_2.data, 
            answer_3=QCform.WriteMCquestion_2.answer3.data, ans_choice_3=QCform.WriteMCquestion_2.ans_multi_select_3.data,
            answer_4=QCform.WriteMCquestion_2.answer4.data, ans_choice_4=QCform.WriteMCquestion_2.ans_multi_select_4.data,
            marks=QCform.WriteMCquestion_2.marks.data,
            rating = dict(DIFFICULTY_RATING).get(QCform.WriteMCquestion_2.rating.data),
            rating_num = QCform.WriteMCquestion_2.rating.data,
            topic_tag =QCform.WriteMCquestion_2.topic.data,
            feedback=QCform.WriteMCquestion_2.feedback.data,
            question_type = 'Multiplechoice'
            )
            db.session.add(Q2multi)
            db.session.commit()
            question_2 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_2)
        if QCform.WriteFTGquestion_2.question.data !='':
            Q2FTG = Multiplechoice(
            user_id = current_user.id,
            question = QCform.WriteFTGquestion_2.question.data, 
            answer_1 = QCform.WriteFTGquestion_2.answer.data,
            answer_2 = '',
            answer_3 = '',
            answer_4 = '',
            topic_tag = QCform.WriteFTGquestion_2.topic.data,
            marks = QCform.WriteFTGquestion_2.marks.data, 
            rating = dict(DIFFICULTY_RATING).get(QCform.WriteFTGquestion_2.rating.data),
            rating_num = QCform.WriteFTGquestion_2.rating.data,
            feedback = QCform.WriteFTGquestion_2.feedback.data,
            question_type = "fill_in_the_blank"
            )
            db.session.add(Q2FTG)
            db.session.commit()
            question_2 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_2)

def add_question_3():
        QCform = QChoiceForm()
        test = Formativetest.query.order_by(Formativetest.id.desc()).first()
        if QCform.question_3.data.question != '-':
            question_3 = QCform.question_3.data
            test.linkedquestions.append(question_3)
        if QCform.WriteMCquestion_3.question.data !='':
            Q3multi= Multiplechoice(
            user_id=current_user.id,
            question=QCform.WriteMCquestion_3.question.data, 
            answer_1=QCform.WriteMCquestion_3.answer1.data,ans_choice_1=QCform.WriteMCquestion_3.ans_multi_select_1.data, 
            answer_2=QCform.WriteMCquestion_3.answer2.data,ans_choice_2=QCform.WriteMCquestion_3.ans_multi_select_2.data, 
            answer_3=QCform.WriteMCquestion_3.answer3.data, ans_choice_3=QCform.WriteMCquestion_3.ans_multi_select_3.data,
            answer_4=QCform.WriteMCquestion_3.answer4.data, ans_choice_4=QCform.WriteMCquestion_3.ans_multi_select_4.data,
            marks=QCform.WriteMCquestion_3.marks.data,
            rating = dict(DIFFICULTY_RATING).get(QCform.WriteMCquestion_3.rating.data),
            rating_num = QCform.WriteMCquestion_3.rating.data,
            topic_tag =QCform.WriteMCquestion_3.topic.data,
            feedback=QCform.WriteMCquestion_3.feedback.data,
            question_type = 'Multiplechoice'
            )
            db.session.add(Q3multi)
            db.session.commit()
            question_3 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_3)
        if QCform.WriteFTGquestion_3.question.data !='':
            Q3FTG = Multiplechoice(
            user_id = current_user.id,
            question = QCform.WriteFTGquestion_3.question.data, 
            answer_1 = QCform.WriteFTGquestion_3.answer.data,
            answer_2 = '',
            answer_3 = '',
            answer_4 = '',
            topic_tag = QCform.WriteFTGquestion_1.topic.data,
            marks = QCform.WriteFTGquestion_3.marks.data,
            rating = dict(DIFFICULTY_RATING).get(QCform.WriteFTGquestion_3.rating.data),
            rating_num = QCform.WriteFTGquestion_3.rating.data, 
            feedback = QCform.WriteFTGquestion_3.feedback.data,
            question_type = "fill_in_the_blank"
            )
            db.session.add(Q3FTG)
            db.session.commit()
            question_3 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_3)

def add_question_4():
        QCform = QChoiceForm()
        test = Formativetest.query.order_by(Formativetest.id.desc()).first()
        if QCform.question_4.data.question != '-':
            question_4 = QCform.question_4.data
            test.linkedquestions.append(question_4)
        if QCform.WriteMCquestion_4.question.data !='':
            Q4multi= Multiplechoice(
            user_id=current_user.id,
            question=QCform.WriteMCquestion_4.question.data, 
            answer_1=QCform.WriteMCquestion_4.answer1.data,ans_choice_1=QCform.WriteMCquestion_4.ans_multi_select_1.data, 
            answer_2=QCform.WriteMCquestion_4.answer2.data,ans_choice_2=QCform.WriteMCquestion_4.ans_multi_select_2.data, 
            answer_3=QCform.WriteMCquestion_4.answer3.data, ans_choice_3=QCform.WriteMCquestion_4.ans_multi_select_3.data,
            answer_4=QCform.WriteMCquestion_4.answer4.data, ans_choice_4=QCform.WriteMCquestion_4.ans_multi_select_4.data,
            marks=QCform.WriteMCquestion_4.marks.data,
            rating = dict(DIFFICULTY_RATING).get(QCform.WriteMCquestion_4.rating.data),
            rating_num = QCform.WriteMCquestion_4.rating.data,
            topic_tag = QCform.WriteMCquestion_4.topic.data,
            feedback=QCform.WriteMCquestion_4.feedback.data,
            question_type = 'Multiplechoice'
            )
            db.session.add(Q4multi)
            db.session.commit()
            question_4 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_4)
        if QCform.WriteFTGquestion_4.question.data !='':
            Q4FTG = Multiplechoice(
            user_id = current_user.id,
            question = QCform.WriteFTGquestion_4.question.data, 
            answer_1 = QCform.WriteFTGquestion_4.answer.data,
            answer_2 = '',
            answer_3 = '',
            answer_4 = '',
            topic_tag = QCform.WriteFTGquestion_1.topic.data,
            marks = QCform.WriteFTGquestion_4.marks.data,
            rating = dict(DIFFICULTY_RATING).get(QCform.WriteFTGquestion_4.rating.data),
            rating_num = QCform.WriteFTGquestion_4.rating.data,
            feedback = QCform.WriteFTGquestion_4.feedback.data,
            question_type = "fill_in_the_blank"
            )
            db.session.add(Q4FTG)
            db.session.commit()
            question_4 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_4)

def add_question_5():
        QCform = QChoiceForm()
        test = Formativetest.query.order_by(Formativetest.id.desc()).first()    
        if QCform.question_5.data.question != '-':
            question_5 = QCform.question_5.data
            test.linkedquestions.append(question_5)
        if QCform.WriteMCquestion_5.question.data !='':
            Q5multi= Multiplechoice(
            user_id=current_user.id,
            question=QCform.WriteMCquestion_5.question.data, 
            answer_1=QCform.WriteMCquestion_5.answer1.data,ans_choice_1=QCform.WriteMCquestion_5.ans_multi_select_1.data, 
            answer_2=QCform.WriteMCquestion_5.answer2.data,ans_choice_2=QCform.WriteMCquestion_5.ans_multi_select_2.data, 
            answer_3=QCform.WriteMCquestion_5.answer3.data, ans_choice_3=QCform.WriteMCquestion_5.ans_multi_select_3.data,
            answer_4=QCform.WriteMCquestion_5.answer4.data, ans_choice_4=QCform.WriteMCquestion_5.ans_multi_select_4.data,
            marks=QCform.WriteMCquestion_5.marks.data,
            rating = dict(DIFFICULTY_RATING).get(QCform.WriteMCquestion_5.rating.data),
            rating_num = QCform.WriteMCquestion_5.rating.data,
            topic_tag = QCform.WriteMCquestion_5.topic.data,
            feedback=QCform.WriteMCquestion_5.feedback.data,
            question_type = 'Multiplechoice'
            )
            db.session.add(Q5multi)
            db.session.commit()
            question_5 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_5)
        if QCform.WriteFTGquestion_5.question.data !='':
            Q5FTG = Multiplechoice(
            user_id = current_user.id,
            question = QCform.WriteFTGquestion_5.question.data, 
            answer_1 = QCform.WriteFTGquestion_5.answer.data,
            answer_2 = '',
            answer_3 = '',
            answer_4 = '',
            topic_tag = QCform.WriteFTGquestion_1.topic.data,
            marks = QCform.WriteFTGquestion_5.marks.data,
            rating = dict(DIFFICULTY_RATING).get(QCform.WriteFTGquestion_5.rating.data),
            rating_num = QCform.WriteFTGquestion_5.rating.data, 
            feedback = QCform.WriteFTGquestion_5.feedback.data,
            question_type = "fill_in_the_blank"
            )
            db.session.add(Q5FTG)
            db.session.commit()
            question_5 = Multiplechoice.query.order_by(Multiplechoice.id.desc()).first()
            test.linkedquestions.append(question_5)