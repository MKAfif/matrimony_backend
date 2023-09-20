from django.shortcuts import render
from app1.models import *
from app1.serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.db.models import Q
import urllib.parse
from django.db.models import Sum
from decimal import Decimal



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
        current_amount = data.get('amount')

        print(current_amount)

        current_amount = Decimal(current_amount)

        existing_subscription = Premium.objects.filter(
            member=member_id
        ).first()

        if existing_subscription:
       
            if plan_name == 'Platinum':
                existing_subscription.is_platinum = True
            elif plan_name == 'Gold':
                existing_subscription.is_gold = True
            elif plan_name == 'Diamond':
                existing_subscription.is_diamond = True

            existing_subscription.amount += current_amount
            existing_subscription.save()

            return Response({'message': 'Membership successfully updated.'}, status=status.HTTP_200_OK)

      
        if plan_name == 'Platinum':
            data['is_platinum'] = True
        elif plan_name == 'Gold':
            data['is_gold'] = True
        elif plan_name == 'Diamond':
            data['is_diamond'] = True


        data['amount'] = current_amount

        serializer = PremiumSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
             
            ).order_by('-id')

            member_details = []
          
            for premium_user in premium_users:
                member        = Member.objects.get(id = premium_user.member_id)
                basic_details = Basic_Details.objects.get(member_id = premium_user.member_id)
                member_details.append({
                    'name' : member.name,
                    'id'   : premium_user.member_id,
                    'email': basic_details.email,
                   
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
                            'email': basic_detail.email,
                            'name': basic_detail.member.name,
                            'image_urls': modified_image_urls,
                        })

            return JsonResponse({'members': member_details}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



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


class PreferenceGetView(APIView):
    
    def get(self, request, memberId):
        try:
            memberpreferences = Preferences.objects.filter(member_id=memberId)
            serializer = PreferenceSerializer(memberpreferences, many=True)
            return Response(serializer.data)
        except Preferences.DoesNotExist:
            return Response({"detail": "Preferences do not exist for this member."}, status=status.HTTP_404_NOT_FOUND)
        

    def put(self, request, memberId):

        try:
            memberpreferences = Preferences.objects.filter(member_id=memberId)
            
            if not memberpreferences.exists():
                return Response({"detail": "Preferences do not exist for this member."}, status=status.HTTP_404_NOT_FOUND)

         
            serializer = PreferenceSerializer(memberpreferences[0], data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class Dashboard(APIView):

    def get(self, request):
        try:
            premium_members = []

            for premium in Premium.objects.all():
                member = Member.objects.get(id=premium.member_id)
                premium_members.append({
                    'name': member.name,
                    'amount': premium.amount,
                    'ending_date': premium.ending_date,
                    'is_platinum': premium.is_platinum,
                    'is_gold': premium.is_gold,
                    'is_diamond': premium.is_diamond,
                    'starting_date': premium.starting_date
                })

            return JsonResponse(premium_members, status=200, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class Revenue(APIView):

    def get(self, request):
        try:
           
            total_amount = Premium.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

            response_data = {
                'total': total_amount
            }

            return JsonResponse(response_data, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class Totalmember(APIView):

    def get(self , request):

        try:

            total_members = Member.objects.count()

            response_data = {
                'total' : total_members
            }

            return JsonResponse(response_data, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        



class AdminReject(APIView):

    def delete(self, request, member_id):

        try:
            personal_Details     = Personal_Details.objects.get(member_id = member_id)
            professional_Details = Professional_Details.objects.get(member_id = member_id)
            about                = About.objects.get(member_id = member_id)
            member               = Member.objects.get(id=member_id)


            about.delete()
            professional_Details.delete()
            personal_Details.delete()
            member.delete()


            return Response(status=status.HTTP_204_NO_CONTENT)
        except About.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)