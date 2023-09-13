from django.shortcuts import render
from app1.models import *
from app1.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# from pusher import pusher_client
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.db.models import Q
import urllib.parse



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
         
        plan_name = data.get('plan_name')
        member_id = data.get('member')
        print(member_id ,"memberid")

        existing_subscription = Premium.objects.filter(
            member=member_id,
            is_platinum=(plan_name == 'Platinum'),
            is_gold=(plan_name == 'Gold'),
            is_diamond=(plan_name == 'Diamond')
        ).first()

        if existing_subscription:
            return Response({'message': 'You have already upgraded to this package. Choose another package.'}, status=status.HTTP_400_BAD_REQUEST)
      
        if plan_name == 'Platinum':
            data['is_platinum'] = True
        elif plan_name == 'Gold':
            data['is_gold'] = True
        elif plan_name == 'Diamond':
            data['is_diamond'] = True

        serializer = PremiumSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckMembership(APIView):
    def get(self, request):
    
        member_id = self.request.query_params.get('member_id')
        plan_name = self.request.query_params.get('plan_name')

       
        existing_subscription = Premium.objects.filter(
            member=member_id,
            is_platinum=(plan_name == 'Platinum'),
            is_gold=(plan_name == 'Gold'),
            is_diamond=(plan_name == 'Diamond')

        ).exists()

        return Response({'alreadyTaken': existing_subscription})

        
class PremiumMember(APIView):
    def get(self, request):
        try:

            premium_users = Premium.objects.filter(
                Q(is_diamond=True) | Q(is_gold=True) | Q(is_platinum=True),
                # is_verified=True,
                # is_active=True,
                # is_superuser=False
            ).order_by('-id')

            member_details = []
          
            for premium_user in premium_users:
                member        = Member.objects.get(id = premium_user.member_id)
                basic_details = Basic_Details.objects.get(member_id = premium_user.member_id)
                member_details.append({
                    'name' : member.name,
                    'id'   : premium_user.member_id,
                    'email': basic_details.email_id,
                    # 'date_of_birth': user.date_of_birth,
                    # 'is_diamond': user.is_diamond,
                    # 'is_gold': user.is_gold,
                    # 'is_platinum': user.is_platinum
                })
            
            return JsonResponse(member_details, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    

class ChattingProfiles(APIView):

    def get(self, request):

        try:
            member_id = self.request.query_params.get('member_id')
            logged_in_member = Member.objects.get(id=member_id)
            gender = logged_in_member.gender
            name = logged_in_member.name
            logged_in_basic = Basic_Details.objects.get(member_id=member_id)
            religion = logged_in_basic.religion

            basic_details = Basic_Details.objects.filter(is_active=True).exclude(member=logged_in_member).order_by('-id')
            member_details = []

            for basic_detail in basic_details:
                if basic_detail.religion == religion:
                    if (gender == 'male' and basic_detail.member.gender == 'female') or (
                            gender == 'female' and basic_detail.member.gender == 'male'):

                        # Fetch images for the current filtered user
                        images = Image.objects.filter(member=basic_detail.member)
                        image_urls = [urllib.parse.unquote(image.image.url.lstrip('/')) for image in images]

                        modified_image_urls = [url.replace("http:/", "http://") for url in image_urls]

                        member_details.append({
                            'id': basic_detail.member_id,
                            'email': basic_detail.email_id,
                            'name': basic_detail.member.name,
                            'image_urls': modified_image_urls,
                        })

            return JsonResponse({'members': member_details}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


        

# class GetMessage(APIView):

#     def get(self, request, recepient_id):
#         try:

#             sender_id = request.query_params.get('sender_id')

#             messages = Message.objects.filter(
#                 (Q(sender_id=sender_id) & Q(receiver_id=recepient_id)) |
#                 (Q(sender_id=recepient_id) & Q(receiver_id=sender_id))
#             ).order_by('timestamp')

#             if not messages.exists():
#                 return JsonResponse({"error": "No messages found"}, status=404)

#             message_data = []
#             for message in messages:
#                 message_info = {
#                     "sender_id": message.sender_id,
#                     "receiver_id": message.receiver_id,
#                     "content": message.content,
#                     "timestamp": message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
#                 }
#                 message_data.append(message_info)

#             return JsonResponse({"recipient_data": message_data}, status=200)

#         except Message.DoesNotExist:
#             return JsonResponse({"error": "Messages not found"}, status=404)


class GetMessage(APIView):

    def get(self, request, recepient_id):
        try:
            sender_id = request.query_params.get('sender_id')

            messages = Message.objects.filter(
                (Q(sender_id=sender_id) & Q(receiver_id=recepient_id)) |
                (Q(sender_id=recepient_id) & Q(receiver_id=sender_id))
            ).order_by('timestamp')

            if not messages.exists():
                return JsonResponse({"error": "No messages found"}, status=404)

            message_data = []
            for message in messages:
                sender_image_url = Image.objects.get(member_id=message.sender_id).image.url
                decoded_image_url = urllib.parse.unquote(sender_image_url).lstrip('/')
                decoded_image_url = decoded_image_url.replace("http:/", "http://")

                message_info = {
                    "sender_id": message.sender_id,
                    "receiver_id": message.receiver_id,
                    "content": message.content,
                    "timestamp": message.timestamp,
                    "sender_image": decoded_image_url,
                }
                message_data.append(message_info)

            return JsonResponse({"recipient_data": message_data}, status=200)

        except (Message.DoesNotExist, Image.DoesNotExist):
            return JsonResponse({"error": "Messages or sender's image not found"}, status=404)