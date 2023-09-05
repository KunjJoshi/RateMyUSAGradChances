from .models import *
import hashlib
import random
import hashlib
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def getOptionalData(grewaive, toeflgiven, ieltsgiven, hasworkex, request):
    if not bool(grewaive):
        gregiven=request.data['gre_given']
        if gregiven:
         gre_qv=request.data['gre_qv']
         gre_awa=request.data['gre_awa']
        else:
            gre_qv='0'
            gre_awa='0'
    else:
        gregiven=False
        gre_qv='0'
        gre_awa='0'
    
    if bool(toeflgiven):
        toefl_score=request.data['toefl_score']
    else:
        toefl_score='0'
    
    if bool(ieltsgiven):
        ielts_bands=request.data['ielts_bands']
    else:
        ielts_bands='0'
    
    if bool(hasworkex):
        total_work_ex=request.data['workex_no']
    else:
        total_work_ex='0'
    
    return gregiven,gre_qv, gre_awa, toefl_score, ielts_bands, total_work_ex

def createStudentProfile(stud_id, email, name, username, password, phone, city, college, state, gre_given, toefl_given, ielts_given, gre_qv, gre_awa, toefl_score, ielts_bands, noofproj, has_work_ex, work_ex, research, conf, patent, grade, max_grade, backlogs_two, backlogs_rest, relevant_courses, gre_waive):
    try:
        student=User.objects.get(id=stud_id)
        hash_object=hashlib.sha256()
        hash_object.update(password.encode('utf-8'))
        pwd=str(hash_object.hexdigest())
        student.email=email
        student.phone=phone
        student.name=name
        student.username=username
        student.password=pwd
        student.city=city
        student.college=college
        student.state=state
        student.gre_given=gre_given
        student.gre_score_quant_verbal=gre_qv
        student.gre_score_awa=gre_awa
        student.toefl_given=toefl_given
        student.toefl_score=toefl_score
        student.ielts_given=ielts_given
        student.ielts_bands=ielts_bands
        student.has_relevant_work_ex=has_work_ex
        student.work_ex_years=work_ex
        student.noof_research_papers=research
        student.noof_conference_papers=conf
        student.noof_patents=patent
        student.noofprojects=noofproj
        student.backlogs_in_first_two_sems=backlogs_two
        student.backlogs_in_rest=backlogs_rest
        student.grade=grade
        student.max_possible_grade=max_grade
        student.noof_relevant_courses=relevant_courses
        student.gre_waiveoff=gre_waive
        student.save()
        return True
    except Exception as e:
        print(e)
        return False
    

def sendEmail(email):
    try:
        student=User.objects.get(email=email)
        otp=str(random.randint(000000,999999))
        hash_object=hashlib.sha256()
        hash_object.update(otp.encode('utf-8'))
        hashedotp=str(hash_object.hexdigest())
        studentLoggedInBefore=Otp.objects.filter(user=student).exists()
        if studentLoggedInBefore:
            otpobject=Otp.objects.get(user=student)
            otpobject.otp=hashedotp
            otpobject.otp_date=datetime.datetime.today()
            otpobject.save()
            s=smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()
            s.login('kjoshi@verifasttech.com','Garsa@3112')
            msg=MIMEMultipart()
            msg['Subject']='Your OTP to login to College Help'
            text=f"Your One Time Password to log into College Help is {otp}"
            msg.attach(MIMEText(text))
            s.sendmail(from_addr='kjoshi@verifasttech.com', to_addrs=email, msg=msg.as_string())
            s.quit()
            response={'error':False, 'msg':'Student Already Exists, OTP Sent'}
            return True, response
        else:
            otpobject=Otp.objects.create(user=student)
            otpobject.otp=hashedotp
            otpobject.otp_date=datetime.datetime.today()
            otpobject.save()
            s=smtplib.SMTP('smtp.gmail.com',587)
            s.starttls()
            s.login('kjoshi@verifasttech.com','Garsa@3112')
            msg=MIMEMultipart()
            msg['Subject']='Your OTP to login to College Help'
            text=f"Your One Time Password to log into College Help is {otp}"
            msg.attach(MIMEText(text))
            s.sendmail(from_addr='kjoshi@verifasttech.com', to_addrs=email, msg=msg.as_string())
            s.quit()
            response={'error':False, 'msg':'New Student, OTP Sent'}
            return True, response
    except Exception as e:
        resp={'error':True, 'msg':str(e)}
        return False, resp
    
def verifyOtp(email, otp):
    try:
        student=User.objects.get(email=email)
        print(student.email)
        otpexists=Otp.objects.filter(user=student).exists()
        if otpexists:
            otpobj=Otp.objects.get(user=student)
            otp=str(otp)
            hash_object=hashlib.sha256()
            hash_object.update(otp.encode('utf-8'))
            hashedotp=str(hash_object.hexdigest())
            if hashedotp==otpobj.otp:
                msg='true'
                return True,msg
            else:
                msg='fmsg1'
                return False,msg
        
        else:
            msg='fmsg2'
            return False, msg
    except Exception as e:
        print(e)
        msg='emsg'
        return False, msg

def hashPassword(pwd):
    hash_object=hashlib.sha256()
    hash_object.update(str(pwd).encode('utf-8'))
    hashedpwd=str(hash_object.hexdigest())
    return hashedpwd


def calculateProfileScore(userid):
    try:
        student=User.objects.get(id=userid)
        waiveoff=student.gre_waiveoff
        tgiven=student.toefl_given
        igiven=student.ielts_given
        greg=student.gre_given
        if not waiveoff:
            if greg:
             qvscore=float(student.gre_score_quant_verbal)
             qvperc=float(qvscore/340)*100
             awascore=float(student.gre_score_awa)
             awaperc=float(awascore/6)*100
            else:
                qvperc=float(0)
                awaperc=float(0)
            if tgiven and not igiven:
                tscore=float(student.toefl_score)
                engperc=float(tscore/120)*100
            elif igiven and not tgiven:
                iscore=float(student.ielts_bands)
                engperc=float(iscore/9)*100
            elif not igiven and not tgiven:
                engperc=float(0)*100
            elif igiven and tgiven:
                iscore=float(student.ielts_bands)
                tscore=float(student.toefl_score)
                iperc=float(iscore/9)
                tperc=float(tscore/120)
                engperc=max(iperc,tperc)*100
            workyears=float(student.work_ex_years)
            projs=float(student.noofprojects)
            courses=float(student.noof_relevant_courses)
            research=float(student.noof_research_papers)
            conf=float(student.noof_conference_papers)
            patent=float(student.noof_patents)
            grade=float(student.grade)
            maxgrade=float(student.max_possible_grade)
            gradeperc=float(grade/maxgrade)*100
            blogtwo=float(student.backlogs_in_first_two_sems)
            blogrest=float(student.backlogs_in_rest)
            profilescore=float((0.15*qvperc)+(0.03*awaperc)+(0.1*engperc)+(0.05*workyears)+(0.1*projs)+(0.1*conf)+(0.1*courses)+(0.1*research)+(0.1*patent)+(0.17*gradeperc)-(0.05*blogtwo)-(0.25*blogrest))
            return profilescore
        else:
            if tgiven and not igiven:
                tscore=float(student.toefl_score)
                engperc=float(tscore/120)
            elif igiven and not tgiven:
                iscore=float(student.ielts_bands)
                engperc=float(iscore/9)
            elif not igiven and not tgiven:
                engperc=float(0)
            elif igiven and tgiven:
                iscore=float(student.ielts_bands)
                tscore=float(student.toefl_score)
                iperc=float(iscore/9)
                tperc=float(tscore/120)
                engperc=max(iperc,tperc)
            workyears=float(student.work_ex_years)
            projs=float(student.noofprojects)
            courses=float(student.noof_relevant_courses)
            research=float(student.noof_research_papers)
            conf=float(student.noof_conference_papers)
            patent=float(student.noof_patents)
            grade=float(student.grade)
            maxgrade=float(student.max_possible_grade)
            gradeperc=float(grade/maxgrade)
            blogtwo=float(student.backlogs_in_first_two_sems)
            blogrest=float(student.backlogs_in_rest)
            profilescore=float((0.15*engperc)+(0.05*workyears)+(0.13*projs)+(0.13*conf)+(0.1*courses)+(0.13*research)+(0.13*patent)+(0.21*gradeperc)-(0.05*blogtwo)-(0.25*blogrest))
            return profilescore
    except Exception as e:
        print(e)
        return float(0)

def calcChances(score, maxscore):
    chance=float(score/maxscore)*100
    if chance>=100:
        chance=99.0
    return chance
            

            










