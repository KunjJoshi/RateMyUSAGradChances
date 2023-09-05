from .models import *
from .helpers import *
from rest_framework_jwt.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class calcProfileScore(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request):
        try:
            userid=request.user.id
            prof_score=calculateProfileScore(userid)
            response={'error':False, 'profile_score':prof_score}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response={'error':True, 'msg':str(e)}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class CalcChancesOfAdmit(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self,request):
        try:
            uni_id=request.query_params.get('uni_id')
        except:
            uni_id=None
        try:
            if uni_id is not None:
                userid=request.user.id
                student=User.objects.get(id=userid)
                university=Universities.objects.get(id=uni_id)
                prof_score=student.profile_score
                pref_ps=university.preferred_profile_score
                chances=calcChances(prof_score, pref_ps)
                response={'error':False, 'chances':chances}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response={'error':True, 'msg':'No Uni Selected'}
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response={'error':True, 'msg':str(e)}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class shortlistUnis(APIView):
    def get(self,request):
        try:
            format=request.query_params.get('format')
        except:
            format='352'
        try:
            coursetaken=request.query_params.get('course')
        except:
            coursetaken='MSCS'
        try:
            userid=request.user.id
            student=User.objects.get(id=userid)
            myscore=student.profile_score
            ambno=int(format[0])
            tarno=int(format[1])
            safeno=int(format[2])
            amblist=Universities.objects.filter(world_ranking__lt=100, course=coursetaken)
            ambitious=[]
            for uni in amblist:
                ambdict={}
                pref_ps=uni.preferred_profile_score
                chance=calcChances(myscore, pref_ps)
                ambdict['name']=uni.uni_name
                ambdict['course']=uni.course
                ambdict['chance']=chance
                ambitious.append(ambdict)
            ambitious=sorted(ambitious, key= lambda x: x['chance'], reverse=True)
            ambitious=ambitious[:ambno]


            tarlist=Universities.objects.filter(world_ranking__gt=100, world_ranking__lt=500, course=coursetaken)
            target=[]
            for uni in tarlist:
                tardict={}
                pref_ps=uni.preferred_profile_score
                chance=calcChances(myscore, pref_ps)
                tardict['name']=uni.uni_name
                tardict['course']=uni.course
                tardict['chance']=chance
                target.append(tardict)
            target=sorted(target, key= lambda x: x['chance'], reverse=True)
            target=ambitious[:tarno]

            safelist=Universities.objects.filter(world_ranking__gt=500, course=coursetaken)
            safe=[]
            for uni in safelist:
                safedict={}
                pref_ps=uni.preferred_profile_score
                chance=calcChances(myscore, pref_ps)
                safedict['name']=uni.uni_name
                safedict['course']=uni.course
                safedict['chance']=chance
                safe.append(ambdict)
            safe=sorted(safe, key= lambda x: x['chance'], reverse=True)
            safe=ambitious[:safeno]
            return Response({'error':False, 'safe':safe, 'target':target, 'ambitious':ambitious}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':True, 'msg':str(e)}, status=status.HTTP_400_BAD_REQUEST)




            
