from django.shortcuts import render
from app1.models import *
from app1.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from pusher import pusher_client
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.db.models import Q



class PremiumUpgrade(APIView):

    def get(self, request):
        try:
            premium_packages = MembershipPackage.objects.all().order_by('id')

            for package in premium_packages:
                print(package.id)
                
            serializer = MembershipPackageSerializer(premium_packages, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class Billing(APIView):

    def get(self,request,premium_id):

        premium  = get_object_or_404(MembershipPackage,id = premium_id)

        print(premium,"............")


        billing_details = {


            'plan_name'      :   premium.plan_name,
            'description'    :   premium.description,
            'plan_price'     :   premium.plan_price,
            'time_period'    :   premium.time_period

        }


        return JsonResponse(billing_details)



class UpdatePremiumProfile(APIView):

    def post(self, request, **kwargs):

        data = request.data

        print(data,"..........")       
        member_id = data.get('member_id')
        plan_name = data.get('plan_name')


        member    = get_object_or_404(Basic_Details,member_id = member_id)

        if plan_name == 'Diamond':
            member.is_diamond = True

        elif plan_name == 'Gold':
            member.is_gold = True

        elif plan_name == 'Platinum':
            member.is_platinum = True

        
        member.save()

        return JsonResponse({'message': 'Membership status updated successfully'})
    

class PremiumMember(APIView):
    def get(self, request):
        try:

            premium_users = Basic_Details.objects.filter(
                Q(is_diamond=True) | Q(is_gold=True) | Q(is_platinum=True),
                is_verified=True,
                is_active=True,
                is_superuser=False
            ).order_by('-id')

            member_details = []

            for user in premium_users:
                member_details.append({
                    'id': user.id,
                    'email': user.email_id,
                    'date_of_birth': user.date_of_birth,
                    'is_diamond': user.is_diamond,
                    'is_gold': user.is_gold,
                    'is_platinum': user.is_platinum
                })

            return JsonResponse(member_details, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    


