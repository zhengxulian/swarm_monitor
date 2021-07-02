"""swarm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import swarm.monitor.views

urlpatterns = {
    path('admin/', admin.site.urls),
    path('monitor/index', swarm.monitor.views.index),
    path('monitor/add_nodes', swarm.monitor.views.add_nodes),
    path('monitor/refresh', swarm.monitor.views.refresh),
    path('monitor/get_node_status', swarm.monitor.views.get_node_status),
    path('monitor/delete_node', swarm.monitor.views.delete_node),
}
