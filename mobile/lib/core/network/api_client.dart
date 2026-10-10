import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:uuid/uuid.dart';

class ApiClient {
  final Dio dio;
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();
  
  ApiClient() : dio = Dio(BaseOptions(baseUrl: 'http://localhost:8000/api/v1')) {
    _setupInterceptors();
  }

  void _setupInterceptors() {
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          // 1. App Version & Request ID
          options.headers['X-App-Version'] = '1.0.0';
          options.headers['X-Platform'] = 'android';
          options.headers['X-Request-ID'] = const Uuid().v4();

          // 2. Auth Token
          final token = await _secureStorage.read(key: 'access_token');
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }

          return handler.next(options);
        },
        onError: (DioException e, handler) async {
          // Single-flight token refresh logic per Architecture Docs
          if (e.response?.statusCode == 401) {
            final refreshToken = await _secureStorage.read(key: 'refresh_token');
            if (refreshToken != null) {
              try {
                // Attempt refresh
                final refreshResponse = await Dio().post(
                  'http://localhost:8000/api/v1/auth/refresh',
                  data: {'refresh_token': refreshToken}
                );
                
                final newAccessToken = refreshResponse.data['access_token'];
                await _secureStorage.write(key: 'access_token', value: newAccessToken);
                
                // Retry original request
                e.requestOptions.headers['Authorization'] = 'Bearer $newAccessToken';
                final retryResponse = await dio.fetch(e.requestOptions);
                return handler.resolve(retryResponse);
              } catch (refreshErr) {
                // Refresh failed, force logout
                await _secureStorage.deleteAll();
                // Navigate to login (handled by riverpod state)
              }
            }
          }
          return handler.next(e);
        },
      ),
    );
  }
}
