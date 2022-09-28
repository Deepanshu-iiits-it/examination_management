from rest_framework import serializers

from examination_management.core.models import Country, State, City, Address


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('country',)


class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ('state',)


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('city',)


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        exclude = ('is_active', 'is_deleted', 'created', 'modified',)


class AddressDetailSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    def get_city(self, address):
        return address.city.city

    def get_state(self, address):
        return address.state.state

    def get_country(self, address):
        return address.country.country

    class Meta:
        model = Address
        exclude = ('is_active', 'is_deleted', 'created', 'modified',)