from rest_framework import serializers
from django.contrib.auth.models import User

from Main.models import usr, Dealer, Driver

def encode(password):
    r = ""
    for char in password:
        r += str(ord(char)) + '\\'
    return r.encode()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password',)
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        
        new_u = usr.objects.create(user=user, bazooka=encode(validated_data['password']))
        new_u.save()
        
        return user
    
class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('__all__')
    
    def create(self, validated_data):
        user = User.objects.get(username=validated_data['username'])
        driver = Driver.objects.create(user=user, age=validated_data['age'], truck_no=validated_data['truck_no'], mobile=validated_data['mobile'], capacity=validated_data['capacity'], transporter_name=validated_data['transporter_name'], experience=validated_data['experience'], routes=validated_data['routes'])
        driver.save()
        return driver

class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ('__all__')
    
    def create(self, validated_data):
        user = User.objects.get(username=validated_data['username'])
        dealer = Dealer.objects.create(user=user, mobile=validated_data['mobile'], material_type=validated_data['material_type'], material_weight=validated_data['material_weight'], quantity=validated_data['quantity'], city=validated_data['city'], state=validated_data['state'])
        dealer.save()
        return dealer