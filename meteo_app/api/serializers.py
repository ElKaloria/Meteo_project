from rest_framework import serializers


class CityHistorySerializer(serializers.Serializer):
    city = serializers.CharField()
    count = serializers.IntegerField()

    class Meta:
        fields = ['city', 'count']
        