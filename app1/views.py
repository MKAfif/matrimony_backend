from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import * 
from rest_framework.exceptions import ValidationError
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from django.shortcuts import get_object_or_404
from random import randint
import traceback
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib.auth import login
from . token import get_token
from django.contrib.auth.hashers import check_password
import cloudinary
import cloudinary.uploader
import cloudinary.api
import urllib.parse



class MemberCreateView(APIView):
    def post(self, request, format=None):
        data = request.data
        mobile_number = data.get('mobile_number')

        if Member.objects.filter(mobile_number=mobile_number).exists():
            raise ValidationError({'mobile_number': 'This mobile number already exists.'})

        serializer = MemberSerializer(data=data)
        if serializer.is_valid():
            member_instance = serializer.save()
            member_id = member_instance.id  
            response_data = {
                'member_id': member_id,
                'remaining_data': {
                    'matrimony_profile_for': member_instance.matrimony_profile_for,
                    'gender': member_instance.gender,
                    'name': member_instance.name,
                    'mobile_number': member_instance.mobile_number
                }
            }
          
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasicDetailsCreateView(APIView):

    def post(self, request, format=None):
        data     = request.data
        email_id = data.get('email_id')

        if Basic_Details.objects.filter(email_id = email_id).exists():
            raise ValidationError({'email_id':'This email already exists'})

        serializer = BasicDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonalDetailsCreateView(APIView):
    def post(self , request , format = None):
        data = request.data
        serializer = PersonalDetailsSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfessionalDetailsCreateView(APIView):
    def post (self,request,format = None):
        data = request.data
        serializer = ProfessionalDetailsSerializer(data = data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
     
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AboutDetailsCreateView(APIView):
    def post(self, request, format=None):
        data = request.data
        email_id = data.get('email')
        serializer = AboutSerializer(data=data)

        if serializer.is_valid():
            about_instance = serializer.save()
            member_id = about_instance.member_id

            # Generate and send OTP
            otp = str(randint(100000, 999999)) 
            print(otp) # Generate a random OTP
            cache.set(f'sent_otp_{member_id}', otp, timeout=None) 
            self.send_otp(member_id, email_id, otp)  # Send OTP to the registered email
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_otp(self, member_id, email_id, otp):
        user = get_object_or_404(Basic_Details, member_id=member_id)
        self.send_otp_email(email_id, otp)

    def send_otp_email(self, receiver_email, otp):
        sender_email = "plantorium1@gmail.com"
        password = "lhfkxofxdfyhflkq"
        
        subject = "OTP Verification"
        message = f"Your OTP for verification: {otp}"
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            print("OTP sent successfully")
        except Exception as e:
            print("Error sending OTP:", str(e))
            traceback.print_exc()



class OTPVerificationView(APIView):
    def post(self, request, format=None):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            member_id = serializer.validated_data['member']
            received_otp = serializer.validated_data['otp']


            sent_otp = cache.get(f'sent_otp_{member_id}')
             
            user = get_object_or_404(Basic_Details, member_id=member_id)
            
            
           
            if received_otp == sent_otp:
                user.is_verified = True
                user.save()
                return Response({'message': 'OTP verified and is_verified set to True'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class AdminLoginView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = Basic_Details.objects.get(email_id=email)
        except Basic_Details.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.password) and user.is_superuser:
            login(request, user)
            token = get_token(user)

            return JsonResponse({'message': 'Login successful','token' : token })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=400)



class ProfileVerificationView(APIView):
    def get(self, request):
        try:  
            basic_details  = Basic_Details.objects.filter(is_verified=True , is_active = False,is_superuser = False).order_by('-id')
            
            member_details = []
            for basic_detail in basic_details:
                member = Member.objects.get(id =basic_detail.member_id)
                member_details.append({
                    'name': member.name,
                    'id': basic_detail.id,
                    'email': basic_detail.email_id,
                    'date_of_birth': basic_detail.date_of_birth,            
                })

                print(member_details)

              
            return JsonResponse(member_details, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        


class AdminMemberVerification(APIView):

    def post(self,request,member_id):
        try:
            member = Basic_Details.objects.get(id = member_id)
            member.is_active = True
            member.save()
            return JsonResponse({'message':'Member Verified Successfully'})
    
        
        except:
            return JsonResponse({'error':'Member not found'},status=404)

    

class AdminMember(APIView):
    def get(self, request):
        try:  
            basic_details = Basic_Details.objects.filter(is_verified=True , is_active = True,is_superuser = False).order_by('-id')
            member_details = []
            for basic_detail in basic_details:
                member = Member.objects.get(id =basic_detail.member_id)
                member_details.append({
                    'name':member.name,
                    'id': basic_detail.id,
                    'email': basic_detail.email_id,
                    'date_of_birth': basic_detail.date_of_birth,            
                })

              
            return JsonResponse(member_details, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class MemberLogin(APIView):
    def post(self,request,*args,**kwargs):
        email    = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = Basic_Details.objects.get(email_id=email)
        except Basic_Details.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.password) and user.is_active:
            login(request, user)
            token = get_token(user)

            member_instance = user.member
            basic_details = member_instance.basic_details_profile.first()
            personal_details = member_instance.personal_details_profile.first()
            professional_details = member_instance.professional_details_profile.first()
            about = member_instance.about_profile

            image_instance = member_instance.image.order_by('-id').first()
            image_url = image_instance.image.url if image_instance else None

            # decoded_image_url = urllib.parse.unquote(image_url).lstrip('/') if image_url else None
            # decoded_image_url = decoded_image_url.replace("http:/", "http://")
            decoded_image_url = None
            if image_url:
                decoded_image_url = urllib.parse.unquote(image_url).lstrip('/')
                decoded_image_url = decoded_image_url.replace("http:/", "http://")

            member_data = {
                'member_id': member_instance.id,
                'matrimony_id': member_instance.matrimony_id,
                'matrimony_profile_for': member_instance.matrimony_profile_for,
                'gender': member_instance.gender,
                'name': member_instance.name,
                'mobile_number': member_instance.mobile_number,
                'image_url': decoded_image_url,
                

                # Basic details
                'religion': basic_details.religion if basic_details else None,
                'mother_tongue': basic_details.mother_tongue if basic_details else None,
                'date_of_birth': basic_details.date_of_birth if basic_details else None,

                # Personal details
                'marital_status': personal_details.marital_status if personal_details else None,
                'height': personal_details.height if personal_details else None,
                'family_status': personal_details.family_status if personal_details else None,
                'family_type': personal_details.family_type if personal_details else None,
                'family_values': personal_details.family_values if personal_details else None,

                # Professional details
                'highest_education': professional_details.highest_education if professional_details else None,
                'employed_in': professional_details.employed_in if professional_details else None,
                'annual_income': professional_details.annual_income if professional_details else None,
                'work_location': professional_details.work_location if professional_details else None,
                'state': professional_details.state if professional_details else None,
                'occupation': professional_details.occupation if professional_details else None,

                # About
                'about_you': about.about_you if about else None,
            }
          
        



            serializer = LoginUserSerializer(user)
            return JsonResponse({'message': 'Login successful','token' : token , 'userinfo':serializer.data, 'memberinfo':member_data })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'error': 'Invalid request method'}, status=400)
 


class ImageUpload(APIView):
    def post(self, request, *args, **kwargs):
        member_id = request.data.get('member')
        image_data = request.data.get('image') 
        
        if not member_id or not image_data:
            return Response({'error': 'member and image are required'}, status=status.HTTP_400_BAD_REQUEST)

        member = Member.objects.get(pk=member_id)
        
        
        uploaded_image = cloudinary.uploader.upload(image_data)


        image_data = {
            'member': member.id, 
            'image': uploaded_image['url']

        }
      
        serializer = ImageSerializer(data=image_data)
      
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class AllMembersView(APIView):

    def get(self, request):
        
        
        try:  
            member_id         = self.request.query_params.get('member_id')
            logged_in_member  = Member.objects.get(id=member_id)
            gender            = logged_in_member.gender
            logged_in_basic   = Basic_Details.objects.get(member_id = member_id)
            religion          = logged_in_basic.religion
            

            basic_details     = Basic_Details.objects.filter(is_active = True).order_by('-id')
            member_details    = []

            for basic_detail in basic_details:

                if basic_detail.member != logged_in_member:
                    if basic_detail.religion == religion:
                        if (gender == 'male' and basic_detail.member.gender == 'female') or (gender == 'female' and basic_detail.member.gender == 'male'):
                    
                            images = Image.objects.filter(member=basic_detail.member)
                            image_urls = [urllib.parse.unquote(image.image.url.lstrip('/')) for image in images]

                            modified_image_urls = [url.replace("http:/", "http://") for url in image_urls]
            
                        
                            member_details.append({
                                'id': basic_detail.member_id,
                                'email': basic_detail.email_id,
                                'date_of_birth': basic_detail.date_of_birth,
                                'image_urls': modified_image_urls,
                            })

          

            return JsonResponse({'members': member_details}, status=200)
        except Exception as e:
         
            return JsonResponse({'error': str(e)}, status=500)

class PreferenceCreateView(APIView):

    def post(self,request,format=None):
        data = request.data
        serializer = PreferenceSerializer(data = data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors , status= status.HTTP_400_BAD_REQUEST)


class MembershipPackageView(APIView):

    def get(self , request ,format = None):
        packages    = MembershipPackage.objects.all().order_by('id')
        serializer  = MembershipPackageSerializer(packages ,many = True)
        return Response(serializer.data ,status= status.HTTP_200_OK)



    def post(self,request,format = None):
        data = request.data
        serializer = MembershipPackageSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class IndividalMemberDetails(APIView):

    def get(self, request, member_id):
        member                  = get_object_or_404(Member, id=member_id)
        basic_details           = get_object_or_404(Basic_Details, member_id = member_id)
        preferences             = get_object_or_404(Preferences , member_id = member_id)
        professional_Details    = get_object_or_404(Professional_Details , member_id = member_id)
        personal_Details        = get_object_or_404(Personal_Details , member_id = member_id)
        about                   = get_object_or_404(About , member_id = member_id)
        image                   = get_object_or_404(Image,member_id = member_id)


        image_url = image.image.url if image else None

        decoded_image_url = urllib.parse.unquote(image_url).lstrip('/') if image_url else None
        decoded_image_url = decoded_image_url.replace("http:/", "http://")
            
        member_details = {
            'member_id'     : member_id,
            'id'            : member.matrimony_id,
            'name'          : member.name,
           'date_of_birth'  : basic_details.date_of_birth,
           'email_id'       : basic_details.email_id,
           'image_url'      : decoded_image_url,
           'age_range_min'  : preferences.age_range_min,
           'age_range_max'  : preferences.age_range_max,
           'location'       : preferences.location,
           'occupation'     : preferences.occupation,
           'education'      : preferences.education,
           'job'            : professional_Details.occupation,
           'marital_status' : personal_Details.marital_status,
           'about'          : about.about_you,


            
           
        }

        
        
        return JsonResponse(member_details)
    

class ShowInterestView(APIView):
    def post(self, request, **kwargs):
        data = request.data
        memberid = data.get('memberid')
        name     = data.get('name')
       
        
        if memberid is not None:
            member = get_object_or_404(Basic_Details, member_id=memberid)
            recepient_email = member.email_id
            self.send_interest(recepient_email, name)
            return Response({'message': 'Interest shown successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)


    def send_interest(self, recepient_email, interested_person_name):
        sender_email = "plantorium1@gmail.com"
        password = "lhfkxofxdfyhflkq"
        
        subject = "Someone shown interest"
        message = f"🌟 Exciting News! {interested_person_name} has shown interest in your profile. 🌟"
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recepient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recepient_email, msg.as_string())
            server.quit()
            print("intrest sent successfullyyy")
        except Exception as e:
            print("Error sending intrest:", str(e))
            traceback.print_exc()
