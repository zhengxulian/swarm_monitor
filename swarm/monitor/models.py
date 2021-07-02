from django.db import models


# Create your models here.
class NodeInfo(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=200, null=False)
    port = models.CharField(max_length=10, null=False)
    name = models.CharField(max_length=50, null=False)


class NodeStatus(models.Model):
    node_id = models.ForeignKey('NodeInfo', on_delete=models.CASCADE)
    version = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=100, null=False)
    connect = models.IntegerField(null=False, default=0)
    chequeSum = models.IntegerField(null=False, default=0)
    cashout = models.IntegerField(null=False, default=0)
    walletScan = models.TextField(null=True)
    chequeScan = models.TextField(null=True)
    uncashed = models.TextField(null=True)

