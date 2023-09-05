from .models import *
from rest_framework_jwt.settings import api_settings
import datetime
from .helpers import *
import random
import string
from datetime import timedelta
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import smtplib


jwt_payload_handler=api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler=api_settings.JWT_ENCODE_HANDLER


class UniversityStudent(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request):
     try:
        print(request.user)
        userid=request.user.id
        student=User.objects.get(id=userid)
        gpa=(float(student.grade)/float(student.max_possible_grade))*4
        studentData={
            'name':student.name,
            'username':student.username,
            'college':student.college,
            'state':student.state,
            'city':student.city,
            'gre_given':student.gre_given,
            'gre_waiveoff':student.gre_waiveoff,
            'gre_qv':student.gre_score_quant_verbal,
            'gre_awa':student.gre_score_awa,
            'toefl_given':student.toefl_given,
            'toefl_score':student.toefl_score,
            'ielts_given':student.ielts_given,
            'ielts_bands':student.ielts_bands,
            'projects':student.noofprojects,
            'has_work_ex':student.has_relevant_work_ex,
            'work_ex_years':student.work_ex_years,
            'research':student.noof_research_papers,
            'conference':student.noof_conference_papers,
            'patent':student.noof_patents,
            'grade':student.grade,
            'max_grade':student.max_possible_grade,
            'us_gpa':gpa,
            'gre_waive':student.gre_waiveoff,
            'courses':student.noof_relevant_courses,
            'profile_score':student.profile_score
        }

        resp={'error':False, 'data':studentData}
        return Response(resp, status=status.HTTP_200_OK)
     except Exception as e:
        resp={'error':True, 'msg':'Something Went Wrong', 'exception':str(e)}
        return Response(resp, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
       try:
          email=request.data['email']
          name=request.data['name']
          username=request.data['username']
          phone=request.data['phone']
          city=request.data['city']
          state=request.data['state']
          college=request.data['college']
          password=request.data['password']
          gre_waive=request.data['gre_waiveoff']
          toefl_given=request.data['toefl_given']
          ielts_given=request.data['ielts_given']
          has_work_ex=request.data['has_work_ex']
          noofproj=request.data['no_of_projects']
          research=request.data['research_papers']
          conf=request.data['conference_papers']
          patent=request.data['patents']
          grade=request.data['grade']
          max_grade=request.data['max_grade']
          backlogs_two=request.data['backlogs_in_first_two']
          backlogs_rest=request.data['backlogs_in_rest']
          relevant_courses=request.data['courses']
          userexists=User.objects.filter(email=email).exists()
          if userexists:
             student=User.objects.get(email=email)
             stud_id=student.id
             gre_given, gre_qv, gre_awa, toefl_score, ielts_bands, work_ex= getOptionalData(gre_waive, toefl_given, ielts_given, has_work_ex, request)
             boolSuccess=createStudentProfile(stud_id, email, name, username, password, phone, city, college, state, gre_given, toefl_given, ielts_given, gre_qv, gre_awa, toefl_score, ielts_bands, noofproj, has_work_ex, work_ex, research, conf, patent, grade, max_grade, backlogs_two, backlogs_rest, relevant_courses, gre_waive)
             if boolSuccess:
                resp={'error':False, 'msg':'Student Profile Created'}
                return Response(resp, status=status.HTTP_201_CREATED)
             else:
                resp={'error':True, 'msg':'Problem in Creating Student Profile'}
                return Response(resp, status=status.HTTP_400_BAD_REQUEST)
          else:
             student=User.objects.create(
                email=email
             )
             stud_id=student.id
             gre_given, gre_qv, gre_awa, toefl_score, ielts_bands, work_ex= getOptionalData(gre_waive, toefl_given, ielts_given, has_work_ex, request)
             boolSuccess=createStudentProfile(stud_id, email, name, username, password, phone, city, college, state, gre_given, toefl_given, ielts_given, gre_qv, gre_awa, toefl_score, ielts_bands, noofproj, has_work_ex, work_ex, research, conf, patent, grade, max_grade, backlogs_two, backlogs_rest, relevant_courses,gre_waive)
             if boolSuccess:
                resp={'error':False, 'msg':'Student Profile Created'}
                return Response(resp, status=status.HTTP_201_CREATED)
             else:
                resp={'error':True, 'msg':'Problem in Creating Student Profile'}
                return Response(resp, status=status.HTTP_400_BAD_REQUEST)
       except Exception as e:
          resp={'error':True, 'msg':'Something Went Wrong', 'exception':str(e)}
          return Response(resp,status=status.HTTP_200_OK )
    
    def put(self,request):
       try:
          userid=request.user.id
          student=User.objects.get(id=userid)
          reqdict=dict(request.data)
          reqkeys=list(reqdict.keys())
          print(reqkeys)

          if 'city' in reqkeys:
            student.city=reqdict['city']
            student.save()
          if 'college' in reqkeys:
            student.college=reqdict['college']
            student.save()
          if 'state' in reqkeys:
            student.state=reqdict['state']
            student.save()
          if 'gre_given' in reqkeys:
            student.gre_given=bool(reqdict['gre_given'])
            student.save()
          if 'gre_qv' in reqkeys:
            student.gre_score_quant_verbal=reqdict['gre_qv']
            student.save()
          if 'gre_awa' in reqkeys:
            student.gre_score_awa=reqdict['gre_awa']
            student.save()
          if 'gre_waive' in reqkeys:
            student.gre_waiveoff=reqdict['gre_waive']
            student.save()
          if 'toefl_given' in reqkeys:
             student.toefl_given=bool(reqdict['toefl_given'])
             student.save()
          if 'toefl_score' in reqkeys:
            student.toefl_score=reqdict['toefl_score']
            student.save()
          if 'ielts_given' in reqkeys:
            student.ielts_given=bool(reqdict['ielts_given'])
            student.save()
          if 'ielts_bands' in reqkeys:
             student.ielts_bands=reqdict['ielts_bands']
             student.save()
          if 'has_work_ex' in reqkeys:
             student.has_relevant_work_ex=bool(reqdict['has_work_ex'])
             student.save()
          if 'noof_work_ex' in reqkeys:
             student.work_ex_years=reqdict['noof_work_ex']
             student.save()
          if 'noofprojects' in reqkeys:
             student.noofprojects=reqdict['noofprojects']
             student.save()
          if 'research' in reqkeys:
             student.noof_research_papers=reqdict['research']
             student.save()
          if 'conference' in reqkeys:
             student.noof_conference_papers=reqdict['conference']
             student.save()
          if 'patent' in reqkeys:
             student.noof_patents=reqdict['patent']
             student.save()
          if 'course' in reqkeys:
             student.noof_relevant_courses=reqdict['course']
             student.save()
          if 'grade' in reqkeys:
             student.grade=reqdict['grade']
             student.save()
          if 'backlogs_two' in reqkeys:
             student.backlogs_in_first_two_sems=reqdict['backlogs_two']
             student.save()
          if 'backlogs_rest' in reqkeys:
             student.backlogs_in_rest=reqdict['backlogs_rest']
             student.save()
          resp={'error':False, 'msg':'Profile Updated'}
          return Response(resp,status=status.HTTP_200_OK)
       except Exception as e:
          resp={'error':True, 'msg':'Something Went Wrong','exception':str(e)}
          return Response(resp, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
       userid=request.user.id
       student=User.objects.get(id=userid)
       student.delete()

       response={'error':False, 'msg':'Student User Deleted'}
       return Response(response, status=status.HTTP_200_OK)


class sendOTP(APIView):
   permission_classes=(AllowAny,) 
   def post(self, request):
      try:
         email=request.data['email']
      except:
         email=None
      try:
         otp=request.data['otp']
      except:
         otp=None
      try:
         if email is not None and otp is None:
            print('In Case 1')
            userexists=User.objects.filter(email=email)
            if userexists:
               emailSent,response=sendEmail(email)
               if emailSent:
                  return Response(response, status=status.HTTP_200_OK)
               else:
                  return Response(response, status=status.HTTP_400_BAD_REQUEST)
            
            else:
               student=User.objects.create(email=email)
               emailSent, response=sendEmail(email)
               if emailSent:
                  return Response(response, status=status.HTTP_200_OK)
               else:
                  return Response(response, status=status.HTTP_400_BAD_REQUEST)
         elif email is not None and otp is not None:
            correctOtp,msg=verifyOtp(email, otp)
            if correctOtp:
               student=User.objects.get(email=email)
               studData={
                  'name':student.name,
                  'username':student.username,
                  'profile_score':student.profile_score
               }
               resp={'error':False,'student':studData, 'token':self.getToken(student)}
               return Response(resp, status=status.HTTP_200_OK)
            else:
               if msg=='fmsg1':
                  resp={'error':True, 'msg':'Otp Verification Failed'}
                  return Response(resp, status=status.HTTP_200_OK)
               else:
                  resp={'error':True, 'msg':'User doesnt exist'}
                  return Response(resp,status=status.HTTP_200_OK )
      except Exception as e:
         resp={'error':True, 'msg':str(e)}
         return Response(resp, status=status.HTTP_400_BAD_REQUEST)
   def getToken(self, user):
      payload=jwt_payload_handler(user)
      token=jwt_encode_handler(payload)
      return token

class StudentLogin(APIView):
   permission_classes=(AllowAny, )
   def post(self, request):
      try:
         username=request.data['username']
      except:
         username=None
      try:
         password=request.data['password']
      except:
         password=None
      try:
         if username is not None and password is not None:
            studentexists=User.objects.filter(username=username).exists()
            if studentexists:
               student=User.objects.get(username=username)
               hashedpwd=hashPassword(password)
               if student.password==hashedpwd:
                  studData={
                     'name':student.name,
                     'college':student.college,
                     'profile_score':student.profile_score,
                     'id':student.id
                  }
                  response={'error':False, 'student':studData, 'msg':'student logged in successfully', 'token':self.getToken(student)}
                  return Response(response, status=status.HTTP_200_OK)
               else:
                  response={'error':True, 'msg':'Student Password Entered Incorrect'}
                  return Response(response, status=status.HTTP_200_OK)
            else:
               return Response({'error':True, 'msg':'Create Account'}, status=status.HTTP_200_OK)
         else:
            response={'error':True, 'msg':'Username or Password incorrect'}
            return Response(response, status=status.HTTP_200_OK)
      except Exception as e:
         response={'error':True, 'msg':'Something Wnet Wrong', 'exception':str(e)}
         return Response(response,status=status.HTTP_400_BAD_REQUEST)
   def getToken(self, user):
      payload=jwt_payload_handler(user)
      token=jwt_encode_handler(payload)
      return token
         
               

               
               
               
             
          
         
          
             


