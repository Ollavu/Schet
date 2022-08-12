from rest_framework import serializers
import top.models as mo
class ClosingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = mo.Closing
        fields = ['openid','date']
 
class ClosedRequest():
	"""docstring for ClosedRequests"""
	def __init__(self, name,obj,open_date,close_date):
		super(ClosedRequest, self).__init__()
		self.name = name
		self.obj = obj
		self.open_date = open_date
		self.close_date = close_date