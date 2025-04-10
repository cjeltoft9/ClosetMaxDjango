from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser, Clothes, Closet
from .serializers import CustomUserSerializer, ClothesSerializer, ClosetSerializer
from django.middleware.csrf import get_token
import json
import logging

# Logger setup
logger = logging.getLogger(__name__)

# CSRF token retrieval
@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrf_token": csrf_token})

# Create User view (using the updated CustomUser model and serializer)
@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        try:
            # Try to parse the request body as JSON
            data = json.loads(request.body)
        except json.JSONDecodeError:
            # If JSON is invalid, return a 400 error
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)

        # Extract fields from the parsed data
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')

        # Log the incoming data for debugging purposes
        logger.debug(f"Received data: {data}")

        # Ensure the required fields are present
        if not username or not email or not password:
            return JsonResponse({'message': 'Username, email, and password are required.'}, status=400)

        # Ensure email is unique
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email is already taken'}, status=400)

        # Use the CustomUser serializer to create a new user
        user_data = {
            'username': username,
            'email': email,
            'phone': phone,
            'password': password
        }
        serializer = CustomUserSerializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()
            return JsonResponse({'message': 'User created successfully', 'user_id': user.id}, status=201)
        else:
            # Return the serializer errors for debugging
            return JsonResponse({'message': 'Error creating user', 'errors': serializer.errors}, status=400)

# Login User view
@api_view(['POST'])
def login_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if email and password are provided
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required.'}, status=400)

        # Attempt to get the user by email
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User with this email does not exist.'}, status=404)

        # Check if the provided password matches the stored hashed password
        if not user.check_password(password):
            return JsonResponse({'error': 'Incorrect password.'}, status=401)

        return JsonResponse({'message': 'Login successful!', 'user_id': user.id}, status=200)

    except Exception as e:
        logger.error(f"Error occurred during login: {e}")
        return JsonResponse({'error': str(e)}, status=500)

# Add Clothing with Image view
class AddClothingWithImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    

    def post(self, request):
        # Extract data from request
        closet_id = request.data.get('closet_id')

        material = request.data.get('material')
        size = request.data.get('size')
        brand = request.data.get('brand')
        season = request.data.get('season')
        clothing_type = request.data.get('clothing_type')
        favorite = request.data.get('favorite')
        image = request.FILES.get('image')
        user_id = request.data.get('user_id')

        # Validate required fields
        if not user_id or not image:
            return JsonResponse({"error": "User ID and image are required"}, status=400)

        # Look up the user
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=400)

        # Prepare clothing data
        clothing_data = {
        'user_id': user_id,
        'closet_id': closet_id or None,
        'material': material or None,
        'size': size or None,
        'brand': brand or None,
        'season': season or None,
        'clothing_type': clothing_type or None,
        'favorite': favorite or None,
        'image': image,
    }


        # Save the clothing object using the serializer
        serializer = ClothesSerializer(data=clothing_data)
        print("Incoming clothing_data:", clothing_data)

        if serializer.is_valid():
            clothing = serializer.save()
            return Response(ClothesSerializer(clothing, context={'request': request}).data, status=201)
        else:
            return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_closets(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({"error": "user_id is required"}, status=400)
    
    closets = Closet.objects.filter(user__id=user_id)
    serializer = ClosetSerializer(closets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_clothes(request):
    user_id = request.GET.get('user_id')
    closet_id = request.GET.get('closet_id')  # Optional

    if not user_id:
        return JsonResponse({"error": "user_id is required"}, status=400)

    clothes = Clothes.objects.filter(user__id=user_id)

    if closet_id and closet_id != "-1":
        clothes = clothes.filter(closet__id=closet_id)

    serializer = ClothesSerializer(clothes, many=True, context={"request": request})
    return Response(serializer.data)
