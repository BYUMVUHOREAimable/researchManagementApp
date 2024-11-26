from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from project.models import ResearchProject
from data.models import DataCollection

# Serializers
class ResearchProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchProject
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'created_by']

class DataCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataCollection
        fields = ['id', 'participant', 'project', 'data_submission_date', 'data']

# API Views
@api_view(['GET'])
def get_research_projects(request):
    """Get all research projects"""
    projects = ResearchProject.objects.all()
    serializer = ResearchProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_project_with_data(request, project_id):
    """Get a specific project with its data collections"""
    try:
        project = ResearchProject.objects.get(id=project_id)
        project_data = ResearchProjectSerializer(project).data
        
        data_collections = DataCollection.objects.filter(project=project)
        data_collections_data = DataCollectionSerializer(data_collections, many=True).data
        
        return Response({
            'project': project_data,
            'data_collections': data_collections_data
        })
    except ResearchProject.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)
