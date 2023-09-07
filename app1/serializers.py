from rest_framework import serializers
from app1.models import *
from django.contrib.auth.hashers import make_password

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['matrimony_profile_for', 'name', 'mobile_number', 'gender','matrimony_id']
        

class BasicDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basic_Details
        fields = ['date_of_birth', 'religion', 'mother_tongue', 'email_id','password','member']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        print(password,"password before make_password")
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.password = make_password(password)
        instance.save()
        return instance


    

class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal_Details
        fields = ['marital_status','height','family_status','family_type','family_values','member']

        

class ProfessionalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional_Details
        fields = ['highest_education','employed_in','annual_income','work_location','state','occupation','member']

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['about_you','member']

class OTPVerificationSerializer(serializers.Serializer):
    member = serializers.IntegerField()
    otp = serializers.CharField(max_length=6)



class LoginUserSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Basic_Details
        fields = ['email_id','is_superuser','is_active']

class ImageSerializer(serializers.ModelSerializer):

    image = serializers.CharField()

    class Meta:
        model   = Image
        fields  = ['image','member']



class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferences
        fields = ['member','age_range_min','age_range_max','location','education','occupation','height','eye_color','skin_tone','body_type','hobbies']

    

class MembershipPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model  = MembershipPackage
        fields = ['plan_name','description','plan_price','time_period','id']



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver' 'content', 'timestamp']


class PremiumSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Premium
        fields  = ['member','amount','starting_date','ending_date','amount']



