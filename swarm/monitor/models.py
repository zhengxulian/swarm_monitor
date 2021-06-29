from django.db import models


# Create your models here.
class NodeInfo(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=200, null=False)
    port = models.CharField(max_length=100, null=False, unique=True)
    name = models.CharField(max_length=50, null=False)
    status = models.CharField(max_length=100, null=False)
    connect = models.IntegerField(null=False, default=0)
    chequeSum = models.IntegerField(null=False, default=0)
    cashout = models.IntegerField(null=False, default=0)
    walletScan = models.CharField(max_length=100, null=False)
    chequeScan = models.CharField(max_length=100, null=False)

