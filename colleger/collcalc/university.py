from .models import *
from .helpers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

class University(APIView):
    permission_classes=(IsAuthenticated, )
    def get(self, request):
        try:
            uni_id=request.query_params.get('uni_id')
        except:
            uni_id=None
        try:
            if uni_id is None:
                #list all unis
                unilist=list(Universities.objects.all().values('id','uni_name','picture','course','world_ranking').order_by('world_ranking'))
                response={'error':False, 'universities':unilist}
                return Response(response, status=status.HTTP_200_OK)
            else:
                #list single university
                uni=Universities.objects.get(id=uni_id)
                uniData={
                    'name':uni.uni_name,
                    'code':uni.uni_code,
                    'location':uni.location,
                    'rank':uni.world_ranking,
                    'preferred_ps':uni.preferred_profile_score,
                    'course':uni.course,
                    'photo':uni.picture
                    }
                resp={'error':False, 'university':uniData}
                return Response(resp, status=status.HTTP_200_OK)
        except Exception as e:
            resp={'error':True, 'exception':str(e)}
            return Response(resp, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        try:
            name=request.data['name']
            code=request.data['unicode']
            pref_ps=request.data['preferred_profile_score']
            rank=request.data['rank']
            location=request.data['location']
            img=request.data['picture']
            course=request.data['course']
            uniexists=Universities.objects.filter(uni_name=name, uni_code=code, course=course ).exists()
            if uniexists:
                response={'error':False, 'msg':'University Exists'}
                return Response(response, status=status.HTTP_200_OK)
            else:
                uni=Universities.objects.create(
                    uni_name=name,
                    course=course,
                    preferred_profile_score=pref_ps,
                    uni_code=code,
                    world_ranking=int(rank),
                    picture=img,
                    location=location
                )
                response={'error':False, 'msg':'University Added'}
                return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            res={'error':True, 'msg':str(e)}
            return Response(res, status=status.HTTP_200_OK)
    
    def delete(self, request):
        try:
            uni_id=request.query_params.get('uni_id')
        except:
            uni_id=None
        try:
            university=Universities.objects.get(id=uni_id)
            university.delete()
            response={'error':False, 'msg':'Uni Deleted'}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response={'error':True, 'msg':str(e)}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
